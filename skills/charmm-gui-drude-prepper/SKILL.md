---
name: charmm-gui-drude-prepper
description: Use computer use to convert matching additive PSF and equilibrated coordinates into CHARMM-GUI Drude Prepper solution packages, with verified periodic box information, batch tracking, and downloaded-output checks. Does not perform the prerequisite equilibration simulation.
---

# CHARMM-GUI Drude Prepper

Use the agent's supported computer-use interface with a signed-in CHARMM-GUI browser session. Inspect current labels and page state. This skill prepares inputs; it does not run prerequisite additive equilibration or prove production-simulation stability.

## Required inputs and scientific checks

For each system obtain:

- A matching additive PSF and equilibrated PDB from the same preparation lineage, with original paths and checksums.
- Equilibration provenance: source preparation, protocol/duration, completion evidence, and identity of the exported frame. A particular filename or marker file is not required, and a filename containing “equilibrated” is not evidence.
- Coordinate imaging evidence that molecules are whole and correctly represented under the periodic box. Do not fix imaging or reorder atoms silently.
- Periodic box information from that frame. For the supported rectangular route, parse `CRYST1`, check positive finite lengths and 90-degree angles, and use those exact lengths. Do not reuse the initial crystal cell or pre-equilibration box. Other cell shapes require a separately verified route.
- Destination directory, requested temperature and output engines, and confirmation that this is a solution system.

Check PSF/PDB atom count and ordered identities (segment/chain mapping, residue IDs/names, atom names). Matching counts alone do not prove correspondence. Resolve naming conversions explicitly; never make mismatches disappear by blindly renumbering. Reject non-finite/missing coordinates. A ligand supported by additive CGenFF is not automatically supported by the Drude force field: verify component support and stop the affected case if parameters are missing.

The [official FAQ](https://www.charmm-gui.org/?doc=faq) recommends equilibrating the additive system before conversion. See also the [Drude Prepper methods paper](https://doi.org/10.1002/jcc.26795). Do not label freshly solvated coordinates as equilibrated.

Read [batch and output handling](references/batch.md). Stage byte-preserving copies with `scripts/files.py stage`. Follow the active tool policy for uploads.

## Browser workflow

1. Open https://www.charmm-gui.org/?doc=input/drude. Recover sign-in through the supported browser flow when authorized; hand off unavailable authentication challenges.
2. Upload the checked PSF and paired coordinate file. Select their actual formats, usually CHARMM PSF and PDB. Do not assume a VMD-generated PSF has CHARMM format.
3. Enable PBC, select Rectangular, and enter the exact equilibrated frame's X/Y/Z lengths. Recheck input pairing and box before proceeding to **Select Model/Chain**.
4. Record the job ID/link as soon as assigned. Wait for Drude Reader completion; confirm Drude structure files and inspect warnings, component recognition, and computed output. Missing parameters, failed minimization, or severe structural errors block the case.
5. Choose **Solution**, the agreed engine(s), and temperature. Continue to **Generate Drude Inputs**. Processing can be lengthy; advancing output is not a reason to resubmit.
6. Verify the final generation message and file listing. Download the archive, pair it to the job and inputs, then inspect and extract according to the batch reference.
7. For OpenMM, verify `step2_drude.psf`, `step2_drude.pdb`, `openmm/openmm_run.py`, `openmm/step3_charmm2omm.pdb`, `openmm/step3_charmm2omm.psf`, `openmm/step4_equilibration.inp`, and `openmm/step5_production.inp`. Any layout change requires explicit inspection, not assuming success from the archive name.

## Completion

Report input pairing and equilibration provenance, box, engine, temperature, job identity, warnings, verified archive path, and output directory. Keep the original additive system untouched; write Drude outputs to a new directory. State unresolved warnings even if generation finished. Do not claim that downloaded input files have been simulated successfully.
