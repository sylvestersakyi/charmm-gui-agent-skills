# Public validation examples

Examples are for workflow testing, not production-ready scientific recommendations. Retrieve originals into a private run directory, record source URL, retrieval date, and SHA-256, and retain unchanged originals. Review chains, heterogens, alternate conformations, termini, disulfides, and missing coordinates before submission.

| Case | Source | Purpose |
| --- | --- | --- |
| Ubiquitin, 1UBQ | https://www.rcsb.org/structure/1UBQ | Protein-only Solution Builder; first batch case |
| Trypsin–BPTI, 2PTC | https://www.rcsb.org/structure/2PTC | Protein–protein Solution Builder; retain both protein chains |
| Trypsin–benzamidine, 3PTB | https://www.rcsb.org/structure/3PTB | Protein–ligand Solution Builder; inspect BEN correspondence and calcium; third queued case |

PDB downloads: `https://files.rcsb.org/download/1UBQ.pdb`, `https://files.rcsb.org/download/2PTC.pdb`, and `https://files.rcsb.org/download/3PTB.pdb`. Retrieve the BEN SDF through RCSB's ligand download interface and record whether coordinates are idealized or deposited. An SDF's coordinates must not replace the bound pose in the complex.

For Drude validation, a separate, publicly shareable, equilibrated additive PSF/PDB pair and its preparation provenance are required. Neither an RCSB PDB nor freshly generated Solution Builder coordinates meet this requirement. The user excluded a Drude demonstration from this release. No live Drude acceptance result is claimed. Preparing a new MD trajectory is outside this package's scope.

Demonstration settings recorded before submission: CHARMM36m protein parameters; compatible CGenFF ligand route where applicable; TIP3P additive water; rectangular box with 10 Å boundary padding; 0.15 M KCl; 303.15 K; OpenMM output. These are example choices, not universal defaults. Record the actual box dimensions and any accepted differences from the current UI.

The 3PTB demo used the neutral RCSB BEN chemical component SDF (`https://files.rcsb.org/ligands/download/BEN_ideal.sdf`) only for chemical definition. Its nine heavy atoms matched the deposited ligand graph and retained the bound heavy-atom pose through PDB Reader (maximum displacement 0.0 Å after the documented atom-name mapping). CGenFF reported a parameter penalty of **60** and charge penalty **2.837**. These were reported; this is a file-handling demonstration, not a validation of ligand parameters or physiological protonation.
