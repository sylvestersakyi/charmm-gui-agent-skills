---
name: charmm-gui-solution-builder
description: Use computer use to prepare proteins, protein complexes, or protein–ligand complexes in CHARMM-GUI Solution Builder, track batches with at most two active jobs, and verify downloaded packages. Requires user-selected scientific settings and matching ligand inputs when applicable.
---

# CHARMM-GUI Solution Builder

Operate the current CHARMM-GUI UI through the agent's supported computer-use tools. Use visible labels and fresh page observations, not stored screen coordinates or hidden request endpoints. A signed-in browser and local upload/download access are required. Reading this skill does not install those capabilities.

## Intake

Obtain a system name, input PDB path, intended assembly/model/chains, and output directory for every case. Review missing coordinates, alternate conformations, chain termini, disulfides, and retained waters/ions/cofactors. Do not silently delete heterogens, mutate residues, rebuild loops, or change biological assembly.

Collect the scientific choices together before submitting: box shape and dimensions or padding rule, salt identity/concentration, protein/ligand force fields and water model, temperature, output engine(s), and applicable protonation/terminal patches. Offer the visible defaults for confirmation instead of treating a personal workflow's settings as universal. A target pH is not a guarantee of a correct protonation assignment; obtain explicit prepared states or an agreed preparation method. Do not confuse ordinary Solution Builder preparation with constant-pH simulation.

For ligand-containing structures, read [ligand handling](references/ligands.md) before upload. For every case read [batch and output handling](references/batch.md). Respect the active tool's authorization rules for transmission of the chosen files to CHARMM-GUI.

Stage copies in a new case directory with `scripts/files.py stage`; preserve source bytes. Use letters, digits, and underscores in upload basenames; the live site rejected a hyphen on 2026-11-13. The helper normalizes filenames only. Record source-to-upload mapping and SHA-256 values. It does not repair PDB contents or prove ligand correspondence.

## Browser workflow

1. Open https://www.charmm-gui.org/?doc=input/solution. Recover an existing login using the supported browser flow when authorized. If the user must complete a challenge, preserve the page and request that step.
2. Choose **Protein Solution System**, upload the staged PDB, and proceed to **Select Model/Chain**. Confirm the selected model and chains against intake, including every intended complex partner.
3. Review PDB Reader manipulation controls. Apply only agreed terminal/protonation patches and structural choices. For ligands, use the linked ligand procedure. Record warnings and the assigned job ID/link immediately; verify tab identity before every subsequent submission.
4. Generate the CHARMM PDB. Wait for actual completion and inspect warnings and generated structure identity. Missing atoms, unsupported components, or severe warnings block that case until resolved. Do not treat a Next button alone as proof of success.
5. Set the agreed waterbox shape and dimensions/padding. Never borrow another system's box. Record actual dimensions. Set salt species, concentration, placement method, and neutralization controls according to the agreed settings; calculate solvent composition and verify the result before solvation.
6. Advance through **Solvate Molecule** and **Setup Periodic Boundary Condition** only after the preceding operation completes. Verify solvator/PBC outputs and periodic box information. Retain automatic PME grid generation when agreed and available.
7. On input generation, verify force field, water model where exposed, engine selection, temperature, ensemble, and any optional mass/ion corrections. Do not silently enable optional controls or substitute an unavailable engine.
8. Generate inputs, wait for the final page, and verify the expected files and download control. Download once; if the browser reports a blocked download, inspect the local download directory before retrying.
9. Follow the batch reference to pair, inspect, and extract the archive. For OpenMM expect `step3_pbcsetup.pdb`, `openmm/step4_equilibration.inp`, and `openmm/step5_production.inp`, allowing a documented current layout only after inspection. Inspect selected engine outputs explicitly if using another engine.

## Completion

Report each system's selected chains, actual settings, job identity, warnings, archive and extracted output paths, and verification result. Distinguish generated inputs from a completed MD simulation. Report overlap only if two distinct jobs were actually observed processing simultaneously.

The live UI may change. If a scientific choice no longer maps clearly to the agreed setup, pause that case and explain the discrepancy. Consult the [official ligand tutorial](https://www.charmm-gui.org/?doc=demo&id=protein_ligand&lesson=1) and [FAQ](https://www.charmm-gui.org/?doc=faq) as needed.
