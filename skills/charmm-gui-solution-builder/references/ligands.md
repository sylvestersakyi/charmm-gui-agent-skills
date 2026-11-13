# Protein–ligand input handling

The complex PDB supplies the bound pose. A ligand SDF supplies molecular identity, connectivity, bond orders, stereochemistry, and the intended charge/protonation state. An idealized SDF conformation must not replace the deposited/bound pose.

## Establish correspondence before upload

For each distinct ligand chemistry, require an explicit mapping from PDB chain, residue number/insertion code, and residue name to an SDF record. Check heavy-atom elements/counts, atom mapping, connectivity, stereochemistry, and charge against the intended ligand. PDB atom names alone do not prove chemical identity. Multiple SDF records, identical residue names for different chemicals, missing ligand atoms, or uncertain tautomers require resolution. Record every retained cofactor, ion, and ligand instance separately.

Use a chemically aware parser when available for SDF inspection; record the tool and result. If chemical equivalence cannot be established, stop that case. Do not use a file-staging helper as a chemistry validator. Covalent ligands, metals requiring special parameters, and unsupported chemical groups need a separately verified preparation route.

## Stage conservatively

Make a new staged copy of each file with a short ASCII filename, preserving extensions and bytes. `scripts/files.py stage` does this with a source/checksum manifest and unique numbered names. It does not rename PDB atom/residue fields or SDF titles. If CHARMM-GUI requires an internal naming change, first identify the exact constraint in the current UI, obtain agreement for that change, and record a reversible mapping on a separate derived copy. Preserve atom order, residue numbering, coordinates, bond orders, and original files.

## Current-UI route

After model/chain selection, inspect the ligand-reading controls for each detected nonstandard residue. Check recognized CHARMM components against the intended chemistry. Where parameter generation is needed and supported, use the UI's CGenFF/SDF input route and attach the mapped SDF; confirm whether the control uses supplied or RCSB SDF data. Do not quietly substitute a database molecule for a custom ligand.

The [official general tutorial](https://www.charmm-gui.org/?doc=demo&id=protein_ligand&lesson=1) describes searching existing CHARMM parameters and generating ligand parameters when needed. The [custom ligand tutorial](https://www.charmm-gui.org/?doc=demo&id=protein_ligand&lesson=2) describes preparing custom topology/parameters with Ligand Reader & Modeler and supplying those files to Solution Builder. If the current page lacks a direct SDF route, use that documented UI route and retain its provenance, or mark the case blocked if prerequisites or authorization are unavailable. Do not invent a control or change the file extension to evade validation.

Review generated topology, ligand identity/pose, charge, and CGenFF warnings/penalties before solvation. Parameter generation success does not certify parameter quality; report issues requiring scientific assessment. A reported parameter penalty alone does not block otherwise valid requested preparation; retain it prominently in the ledger and final report, without claiming production readiness. Keep the input pose and compare atom mappings where output conventions differ. Continue with Solution Builder only after the intended ligand and selected protein chains are present.

## Observed SDF control (2026-11-13)

In PDB Reader manipulation, under **Reading Hetero Chain Residues**, select **Use CHARMM General Force Field to generate CHARMM top & par files**, then **the SDF file uploaded from** for the relevant residue and attach its mapped SDF. Verify the displayed filename and that the RCSB SDF radio option is no longer selected. Leave **Guess bond orders from connectivity** off for a valid supplied SDF. This route was observed for BEN; other ligands still require their own checks.
