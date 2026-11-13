# CHARMM-GUI agent skills

Computer-use instructions for an agent to guide molecular systems through CHARMM-GUI, track a batch, and verify downloaded preparation packages.

**Tested with Codex:** three public Solution Builder examples completed through verified OpenMM downloads. **Drude Prepper is documented but not live-tested in this release.** See [validation status](docs/validation.md). This is an independent project, not an official CHARMM-GUI or OpenAI product.

## Workflows

| Skill | Intended workflow | Required inputs |
| --- | --- | --- |
| `charmm-gui-solution-builder` | Protein or protein–protein complex solvation | PDB, intended assembly/chains, preparation settings |
| Same skill, ligand reference | Protein–ligand complex solvation | Complex PDB, corresponding ligand SDF(s), explicit ligand identity/protonation and preparation settings |
| `charmm-gui-drude-prepper` | Additive system to classical Drude preparation | Matching additive PSF and equilibrated PDB, box information, equilibration and imaging provenance |

These are skills an agent reads, not a standalone browser bot or background service. They require an active agent session with computer use, file upload/download access, and sufficient runtime. The agent asks for missing scientific choices, advances eligible jobs, records warnings, and downloads verified outputs. Authentication challenges and unresolved chemistry can still require you.

A maximum of two jobs may be active at once across the batch. This is this package's cap, not a verified statement of the service's universal limit. Existing active jobs also consume capacity. A generated package is not evidence of a stable production simulation or accurate binding predictions.

## Install for Codex

Requirements: Codex with a working computer-use/browser integration, a CHARMM-GUI account, filesystem access, Python 3.10+ for the optional local helper, and a signed-in browser. A skill cannot install or grant browser permissions itself. Other agents can read the Markdown but are not validated here.

Clone the repository and inspect its contents:

```sh
git clone https://github.com/sylvestersakyi/charmm-gui-agent-skills.git
```

Then ask Codex:

> Install the two skills from this checkout's `skills/` directory into my Codex skills directory. Preserve any existing versions and stop if either name already exists. Do not upload files or submit jobs during installation.

For a standard local setup, copy each complete skill directory into `~/.codex/skills/` (or the skills directory under your configured `CODEX_HOME`). Start a new chat and confirm that both skill names are available. Do not overwrite a personal version without reviewing its differences.

Alternatively, tell an agent:

> Read https://github.com/sylvestersakyi/charmm-gui-agent-skills and the complete relevant skill, including its linked references. Check your computer-use and filesystem capabilities before attempting the workflow. Ask me for missing inputs and scientific choices.

Merely reading a GitHub URL does not permanently install a skill.

## Example requests

> Use $charmm-gui-solution-builder for the PDBs in my selected input directory. Ask me for assembly/chains, box, salt, force field, temperature, protonation choices, and output engine. Once those are settled, process up to two jobs at once, keep a ledger, and download verified packages to a new output directory.

> Use $charmm-gui-solution-builder for this complex PDB and the accompanying ligand SDF. Verify the residue-to-SDF mapping and use staged copies for filename changes. Ask before changing molecular identities or protonation states.

> Use $charmm-gui-drude-prepper for these matching additive PSF and equilibrated PDB files. Verify atom ordering, box information, and my equilibration/imaging record. Generate and download the OpenMM package.

The user must authorize transmission of their selected structures to CHARMM-GUI under the agent's active tool policy. Never put credentials in a prompt or job ledger.

## Local helper

Each skill includes the same self-contained `scripts/files.py`. Run it with `--help` for staging and archive inspection/extraction. It never opens a browser or submits a job. Staging changes only filenames; ligand chemistry and residue mappings still require review. Archive inspection cannot by itself prove input identity or scientific correctness.

Private run directories contain a ledger, staged input manifest, original downloads, extracted packages, and verification notes. Keep these outside a public checkout or under ignored `runs/`.

## Examples, evidence, and contributions

See [public examples](examples/README.md), [acceptance checks](docs/validation.md), and [sources and attribution](docs/sources.md). When reporting an issue, include the workflow stage and a redacted error, not credentials, private job URLs, or research files. Website changes may require updating the instructions. Test changes against the live UI before extending compatibility claims.

## License

Original instructions and helper code are offered under the [MIT License](LICENSE). CHARMM-GUI, force fields, third-party software, and external example datasets retain their own terms. This repository does not redistribute CHARMM-GUI or its generated force-field packages.
