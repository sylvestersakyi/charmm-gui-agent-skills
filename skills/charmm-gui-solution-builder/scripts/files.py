#!/usr/bin/env python3
"""Local, byte-preserving staging and conservative CHARMM-GUI tar inspection."""
import argparse
import hashlib
import json
import re
import shutil
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

PROFILES = {
    'solution-openmm': ['step3_pbcsetup.pdb', 'openmm/step4_equilibration.inp',
                        'openmm/step5_production.inp'],
    'drude-openmm': ['step2_drude.psf', 'step2_drude.pdb', 'openmm/openmm_run.py',
                     'openmm/step3_charmm2omm.pdb', 'openmm/step3_charmm2omm.psf',
                     'openmm/step4_equilibration.inp', 'openmm/step5_production.inp'],
}


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def stage(paths, destination):
    destination = Path(destination).absolute()
    sources = [Path(p).resolve(strict=True) for p in paths]
    if not sources or any(not p.is_file() for p in sources):
        raise ValueError('Supply one or more existing regular input files')
    if any(p.suffix.lower() not in {'.pdb', '.psf', '.sdf'} for p in sources):
        raise ValueError('Only PDB, PSF, and SDF inputs are supported')
    if destination.exists() or destination.is_symlink():
        raise ValueError('Staging destination already exists; nothing overwritten')
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix='.stage-', dir=destination.parent))
    try:
        manifest = []
        for i, src in enumerate(sources, 1):
            stem = re.sub(r'[^a-z0-9]+', '_', src.stem.lower()).strip('_')[:30] or 'input'
            name = f'{i:02d}_{stem}{src.suffix.lower()}'
            original_hash = sha256(src)
            shutil.copyfile(src, temp / name)
            if sha256(temp / name) != original_hash or sha256(src) != original_hash:
                raise ValueError('Input changed while staging')
            manifest.append({'source': str(src), 'staged_name': name, 'sha256': original_hash})
        (temp / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        # mkdir reserves the target and refuses collisions, including concurrent ones.
        destination.mkdir()
        try:
            for p in temp.iterdir():
                p.rename(destination / p.name)
        except BaseException:
            shutil.rmtree(destination)
            raise
        return manifest
    finally:
        shutil.rmtree(temp)


def inspect_tar(archive, job_id, profile, max_bytes=2_000_000_000):
    if not re.fullmatch(r'[0-9]+', str(job_id)):
        raise ValueError('Job ID must contain digits only')
    expected_root = 'charmm-gui-' + str(job_id)
    seen, regular, total = set(), set(), 0
    with tarfile.open(archive, 'r:gz') as tar:
        members = []
        for member in tar:
            if len(members) >= 100000:
                raise ValueError('Archive has too many members')
            path = PurePosixPath(member.name)
            if (path.is_absolute() or '..' in path.parts or '\\' in member.name
                    or not path.parts or path.parts[0] != expected_root):
                raise ValueError('Unsafe path or archive/job identity mismatch')
            normalized = str(path)
            if normalized in seen:
                raise ValueError('Duplicate archive member')
            seen.add(normalized)
            if not (member.isfile() or member.isdir()):
                raise ValueError('Archive links and special files are not allowed')
            total += member.size
            if member.size < 0 or total > max_bytes:
                raise ValueError('Archive exceeds uncompressed size limit')
            if member.isfile():
                regular.add(normalized)
                # Read all payloads to detect truncation, not only the headers.
                stream = tar.extractfile(member)
                read = 0
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    read += len(chunk)
                if read != member.size:
                    raise ValueError('Truncated archive member')
            members.append(member)
        required = {expected_root + '/' + p for p in PROFILES[profile]}
        if not required <= regular:
            raise ValueError('Missing expected files: ' + ', '.join(sorted(required - regular)))
        if any(m.size == 0 and str(PurePosixPath(m.name)) in required for m in members):
            raise ValueError('An expected output file is empty')
    return {'root': expected_root, 'members': len(members), 'uncompressed_bytes': total,
            'profile': profile, 'archive_sha256': sha256(archive),
            'molecular_identity': 'Requires separate comparison to the case ledger'}


def extract_tar(archive, destination, job_id, profile, max_bytes=2_000_000_000):
    destination = Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError('Extraction destination already exists; nothing overwritten')
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix='.extract-', dir=destination.parent))
    try:
        # Snapshot the source before validating, so extraction uses the inspected bytes.
        snapshot = temp / 'archive.tgz'
        shutil.copyfile(archive, snapshot)
        result = inspect_tar(snapshot, job_id, profile, max_bytes)
        payload = temp / 'payload'
        payload.mkdir()
        with tarfile.open(snapshot, 'r:gz') as tar:
            for member in tar:
                target = payload.joinpath(*PurePosixPath(member.name).parts)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with target.open('xb') as out, tar.extractfile(member) as source:
                        shutil.copyfileobj(source, out)
        destination.mkdir()
        try:
            for item in payload.iterdir():
                item.rename(destination / item.name)
        except BaseException:
            shutil.rmtree(destination)
            raise
        result['destination'] = str(destination)
        return result
    finally:
        shutil.rmtree(temp)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('stage', help='Copy inputs under safe names into a new directory')
    p.add_argument('--destination', required=True)
    p.add_argument('files', nargs='+')
    p = sub.add_parser('archive', help='Inspect a downloaded gzip tar; optionally extract')
    p.add_argument('archive')
    p.add_argument('--job-id', required=True)
    p.add_argument('--profile', choices=PROFILES, required=True)
    p.add_argument('--destination', help='New directory; omit to inspect only')
    p.add_argument('--max-bytes', type=int, default=2_000_000_000)
    args = parser.parse_args()
    try:
        if args.command == 'stage':
            result = stage(args.files, args.destination)
        elif args.destination:
            result = extract_tar(args.archive, args.destination, args.job_id, args.profile, args.max_bytes)
        else:
            result = inspect_tar(args.archive, args.job_id, args.profile, args.max_bytes)
    except (OSError, ValueError, tarfile.TarError, EOFError) as error:
        parser.exit(1, f'ERROR: {error}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
