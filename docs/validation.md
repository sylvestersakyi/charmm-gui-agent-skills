# Validation status

Observed with Codex computer use in Chrome on 2026-11-13. Three public Solution Builder examples completed through verified OpenMM downloads. Drude is included as a documented workflow, **not live-tested in this release**. No production MD was run.

## Live results

| Example | Result | Verification |
| --- | --- | --- |
| 1UBQ, ubiquitin | Completed | Correct job root, embedded source PDB byte-identical, 122 archive members, expected OpenMM files |
| 2PTC, trypsin–BPTI | Completed | Both protein chains retained, source PDB byte-identical, 130 archive members, expected OpenMM files |
| 3PTB, trypsin–benzamidine | Completed with parameter warning | Source PDB and supplied SDF byte-identical, 138 archive members, expected OpenMM files |

All three archives were read, checked for safe paths/member types, and extracted into separate new directories. Generated inputs retained 303.15 K, NVT equilibration and NPT production settings. The recorded cubic box lengths were 64, 86 and 71 Å respectively. Full private job IDs, archive hashes, input mappings and output locations remain in a local ledger, outside this repository.

The ligand example used neutral CCD BEN and reported CGenFF parameter penalty **60**, charge penalty **2.837**. The nine heavy atoms matched the ligand graph, with 0.0 Å maximum displacement at the PDB Reader stage after accounting for the C → C7 name mapping. Subsequent system preparation includes positioning/minimization. These checks do not validate ligand parameters, physiological protonation or production simulation stability.

## Batch and recovery observations

A batch of three cases used at most two active jobs. Two distinct jobs were observed processing concurrently; the third started after the first completed. Final archives were paired by job root and embedded source files, not generic download names.

The site rejected hyphens in an uploaded filename. A staged underscore-only name was accepted with the original bytes preserved. The helper now produces underscore names.

A browser download navigation error was recovered by returning to the same completed job and registering a download event listener before clicking the download control. No replacement job was submitted. Browser-control interruptions were also recovered using current page state. Expired jobs, lost ledgers and uncertain submissions without a captured ID were not live-tested.

## Local checks and limits

| Check | Result |
| --- | --- |
| Both skill frontmatter validators | Pass |
| Seven helper unit tests | Pass |
| Byte-preserving staging and normalized-name collisions | Pass |
| Missing supplied input file | Rejected before creating destination |
| Existing staging/extraction destinations | Rejected without overwriting |
| Wrong-job, incomplete, corrupt, oversized, traversal, link and duplicate-member archives | Rejected |
| Clean-checkout installation to isolated skill directories | Pass: local Git clone, isolated copies, references and helper invocation; existing names refused |
| Missing ligand requirement when no SDF is supplied at all | Instruction review only; no live negative GUI submission |
| Ambiguous additive PSF/PDB pairing | Required identity/provenance checks documented; not behaviorally tested |
| Drude conversion | Not run; needs an equilibrated additive fixture |
| Other engines, browsers and agents | Not tested |

Tests establish the helper's file handling, not autonomous chemistry validation. The agent must still review ligand correspondence and Drude input lineage. Compatibility is limited to the observed examples and UI; this is not a universal ligand-support claim.

## Reproduce local checks

Run `python3 -m unittest discover -s tests -v` from a checkout. Copy each complete skill folder into a new isolated skills directory, confirm the referenced Markdown and helper files exist, and run each helper's `--help`. Installation must refuse or preserve existing skill names. Actual discovery in a fresh Codex chat depends on that installation's skills configuration.

Installation evidence: a fresh local Git clone passed all seven tests. Both skill folders were copied into a temporary isolated skills directory; linked local references resolved, both helpers ran, and repeat copy attempts refused existing destinations. Personal installed skills were preserved. Fresh-chat discovery was not tested.
