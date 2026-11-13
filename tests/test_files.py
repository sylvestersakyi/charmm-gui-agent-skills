import importlib.util
import io
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/charmm-gui-solution-builder/scripts/files.py'
spec = importlib.util.spec_from_file_location('files', SCRIPT)
files = importlib.util.module_from_spec(spec)
spec.loader.exec_module(files)


class FileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def archive(self, extras=(), missing=False):
        path = self.root / 'test.tgz'
        with tarfile.open(path, 'w:gz') as tar:
            for p in files.PROFILES['solution-openmm'][:-1 if missing else None]:
                info = tarfile.TarInfo('charmm-gui-123/' + p)
                info.size = 3
                tar.addfile(info, io.BytesIO(b'abc'))
            for name, kind in extras:
                info = tarfile.TarInfo(name)
                info.type = kind
                if kind == tarfile.SYMTYPE:
                    info.linkname = '/tmp/escape'
                tar.addfile(info, io.BytesIO())
        return path

    def test_stage_preserves_bytes_and_resolves_name_collisions(self):
        a = self.root / 'A test.pdb'
        b = self.root / 'A-test.pdb'
        a.write_bytes(b'ATOM  original\n')
        b.write_bytes(b'ATOM  distinct\n')
        dest = self.root / 'stage'
        manifest = files.stage([a, b], dest)
        self.assertEqual(len(set(x['staged_name'] for x in manifest)), 2)
        for src, row in zip([a, b], manifest):
            self.assertEqual(src.read_bytes(), (dest / row['staged_name']).read_bytes())
            self.assertRegex(row['staged_name'], r'^[a-z0-9_]+\.pdb$')

    def test_stage_refuses_collision_and_missing_input(self):
        a = self.root / 'a.pdb'
        a.write_text('ATOM\n')
        dest = self.root / 'stage'
        files.stage([a], dest)
        with self.assertRaises(ValueError):
            files.stage([a], dest)
        with self.assertRaises(FileNotFoundError):
            files.stage([self.root / 'missing.sdf'], self.root / 'missing')
        self.assertFalse((self.root / 'missing').exists())

    def test_valid_archive_extracts_without_overwriting(self):
        path = self.archive()
        dest = self.root / 'result'
        result = files.extract_tar(path, dest, '123', 'solution-openmm')
        self.assertEqual(result['members'], 3)
        self.assertEqual((dest / 'charmm-gui-123/step3_pbcsetup.pdb').read_bytes(), b'abc')
        with self.assertRaises(ValueError):
            files.extract_tar(path, dest, '123', 'solution-openmm')

    def test_wrong_job_and_incomplete_package(self):
        with self.assertRaises(ValueError):
            files.inspect_tar(self.archive(), '999', 'solution-openmm')
        with self.assertRaises(ValueError):
            files.inspect_tar(self.archive(missing=True), '123', 'solution-openmm')

    def test_rejects_traversal_links_absolute_and_duplicates(self):
        for name, kind in [('charmm-gui-123/../../escape', tarfile.REGTYPE),
                           ('/tmp/escape', tarfile.REGTYPE),
                           ('charmm-gui-123/link', tarfile.SYMTYPE),
                           ('charmm-gui-123/step3_pbcsetup.pdb', tarfile.REGTYPE)]:
            with self.subTest(name=name):
                path = self.archive([(name, kind)])
                with self.assertRaises(ValueError):
                    files.extract_tar(path, self.root / 'bad', '123', 'solution-openmm')
                self.assertFalse((self.root / 'bad').exists())

    def test_limits_and_corrupt_archive(self):
        with self.assertRaises(ValueError):
            files.inspect_tar(self.archive(), '123', 'solution-openmm', max_bytes=2)
        broken = self.root / 'broken.tgz'
        broken.write_bytes(b'not a tar')
        with self.assertRaises(tarfile.TarError):
            files.inspect_tar(broken, '123', 'solution-openmm')

    def test_self_contained_helper_copies_match(self):
        self.assertEqual(SCRIPT.read_bytes(), (ROOT / 'skills/charmm-gui-drude-prepper/scripts/files.py').read_bytes())


if __name__ == '__main__':
    unittest.main()
