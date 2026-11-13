# Batch state, recovery, and output verification

## Before submitting

Create a private run directory and a persistent JSON ledger, outside public Git content. Each case records: unique system name; workflow; original and staged file paths/checksums; ligand mapping or equilibration provenance; selected scientific settings; job ID/link; browser tab association; stage/status; timestamps; warnings; archive checksum/path; extraction path and verification evidence. Write changes after each transition, not only at completion. Never store credentials or cookies.

Use statuses such as `queued`, `preflight_blocked`, `submitted`, `processing`, `generated`, `downloaded`, `verified`, `failed`, and `needs_user`. Record the last confirmed stage separately. A blocked page may still have an active server job.

## Two-slot queue

Maintain at most two active jobs across Solution Builder and Drude Prepper together. Inspect known existing user jobs before starting; do not disrupt them. If capacity is uncertain, resolve it before submitting. Count submitted, processing, and unknown-state jobs as occupying slots until confirmed finished or failed. A browser tab is not a slot and a blocked case does not automatically free capacity.

Preflight each queued case before upload. Record the first assigned job ID before starting another. At each advance verify the visible job ID matches the ledger; session state may change across tabs. Poll by observing page progress with bounded waits. Never click Calculate/Next repeatedly while processing. As a job reaches confirmed generated inputs or terminal failure, admit the next eligible case. Download/verification can proceed while another confirmed job is processing.

Skip preflight-blocked cases, record the reason, and continue eligible cases. Do not repeatedly retry an unsupported ligand or failed structure. Record parameter-quality warnings and penalties and continue requested preparation when generation is otherwise valid. Explain the need for scientific review in the final report; a penalty alone is not a reason to stop a workflow demo. Pause only when a warning prevents faithful preparation or requires an unresolved scientific choice, or when the user requested stricter gating. Do not claim concurrent processing without seeing both distinct jobs processing at overlapping times.

## Resume after interruption

Load the ledger first. Open the recorded job/retriever link through the UI and compare job identity, uploaded inputs, settings, stage, and warnings. Never create a replacement merely because a tab closed. If a click may have submitted but no ID was captured, inspect the site's job history and ask if ambiguity remains; count the uncertain submission against capacity. Resume only the next uncompleted step supported by current evidence. A vanished/expired job requires explicit resolution before resubmission.

## Downloads and extraction

Record final completion before downloading. Save downloads to the case's private area or identify them in the browser's download directory. When supported, register the browser download event listener before clicking the download control, then wait for its saved path. A navigation error alone does not establish whether a download succeeded. Keep the original archive intact. A generic filename or timestamp is insufficient to pair a package to a case.

Inspect the archive root/metadata for the recorded job ID and compare the embedded original inputs or documented structural identity against the ledger. Record how this match was established. Confirm gzip/tar readability and expected engine files. Compare selected chains/components and box where possible. Do not execute downloaded scripts during verification.

The local `scripts/files.py archive` helper verifies a `charmm-gui-JOBID` root, safe member types/paths, and the selected OpenMM file profile. It does not prove molecular identity. Other root layouts or engines require explicit manual inspection and a recorded equivalent check, not bypassing identity verification.

Extract only to a new destination after inspection. Reject path traversal, absolute paths, links, device entries, duplicate members, and unreasonable sizes. Preserve the package's internal folder structure. Never overwrite an existing case or relocate the user's additive system. On extraction failure clean up only newly created staging content and report the case; leave source/archive/existing results unchanged.

Final report: all case statuses, settings, job identity, warnings, verified outputs, unresolved issues, and whether overlap was directly observed. Keep private job URLs out of public demonstrations and repository commits.
