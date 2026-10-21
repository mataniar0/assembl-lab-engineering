# CTB-010 — stage3/4 delivery for lead review

Branch `codex/ctb-010-final-digital-closeout`; baseline merged PR53
`9caa69445d3f9816bdf23a934d8824b86e1ad913`. Refs Issues50/51/52 (parallel
CTB-010 handoffs; shared execution, not three separate studies).

**DESIGN_ONLY / PERSONAL_PROTOTYPE / FIT_STRENGTH_UNVERIFIED.**

| Digital stage | Result / boundary |
|---|---|
| 1 — secondary CAD | INHERITED_CONFIRMED from merged PR53; no kernel rerun |
| 2 — G2b evidence | Accepted evidence reused; formal final closeout for ChatGPT, no self-approval |
| 3 — source vectors/nesting | PASS for uncompensated experimental design files |
| 4 — file/package QA | Computational PASS; independent file-review report in QA/INDEPENDENT_QA.md; lead decision pending |

32 wooden bodies, 12 assembly roles, 11 actual cut masters; one unchanged
P01 master×6 and one identical rim master×2. P04L and P04U remain different.
38 final vector files: 11 master DXF +11 master SVG +8 per-sheet DXF +8 per-sheet
SVG. Stock: **7 nominal6mm sheets +1 nominal4mm sheet**, portrait WIDTH440×HEIGHT800.
Unrotated conservative envelopes, 10mm provisional edge margins/5mm part gaps.
No optimization or calibrated grain/kerf/physical-fit claim. Per-sheet material
and envelope utilization and every numbered placement are in manifest and CSV.

Files and folders:

- `CAD_sources/`: reproducible exporter, pinned dependencies, exact native
  contour JSON, twelve byte-identical authoritative source SVGs, baseline
  parameter and interface snapshots. Existing original CAD remains untouched.
- `DXF/`, `SVG/`: 11 unique 1:1mm masters, explicit CUT_OUTER/CUT_INNER and
  display-only annotations; no engraving or invented kerf compensation.
- `nesting/`: eight stock plans in both formats and sheet utilization CSV.
- `BOM/`: quantity-by-role CSV and 32 body-to-sheet mapping CSV; P08 keys0.
- `assembly/`: numbered ring pre-position +31 inherited translations,
  orientation notes and byte-identical accepted GLB, no model regeneration.
- `QA/`: separate-parser verifier, full named evidence, execution history,
  archived B2/secondary proofs, computational and independent review reports.
- `manifest/`: complete source/cut/stock/placement manifest and SHA256 inventory.
- `README.md`, `DECISIONS.md`, this report; one sibling downloadable ZIP and
  ZIP SHA256 sidecar. ZIP entries are re-opened and compared to the sealed tree.

New computational scope: **94 unique file-QA cases, all PASS**, including five
real corrupt-file controls (duplicate cut, missing kerf slot, SVG scale,
out-of-bed placement, missing BOM placement). All38 output vector files and
32 placements were re-imported. Expected negative rejections are passes of
controls, not unexplained output failures. No invalid cutting files,
geometry repairs or failed file-verifier attempts occurred. Re-executions
after adding native JSON/seal coverage and final review-status wording are
recorded separately in QA/execution-history.json, never added to94.

One later repository-format check failed: Git treated default CSV CRLF line
endings as trailing whitespace. One formatting repair normalized all3 CSV
tables to LF and fixed the exporter's line terminator. Three focused CSV
checks prove exact parsed-row equality and reconstruction of each originally
checked CRLF SHA256. See QA/packaging-evidence.json; file-evidence digests were
refreshed only for those verified3 CSV files with an explicit proof link.
No vector/layout/source values changed and no full suite/kernel was rerun.

Independent reviewer `/root/ctb010_file_qa` uses separate read-only source/vector,
BOM and archive checks; its repeated logical cases do not increase the94 count.
See its report for actual check coverage and score. ChatGPT lead approval remains
pending. No new B1, B2 or OpenCASCADE execution: **0**; inherited 782 primary,
222 inherited and 569 secondary pair/control records are not new test counts.
Historical checker fixes remain in the copied original evidence, distinct from
this zero-failure export task.

Reproduction and sealing commands are in README. The scripts require only
ezdxf1.4.4 and shapely2.1.2; no CAD-kernel dependency or geometry regression call.
Review commits/PR with these files; implementation agent does not self-merge.

Open physical limitations: measured stock/grain/flex/kerf, bend calibration,
fit, glue/fixtures/cure/access, strength/load/stability **NOT_RUN**. P04U↔rib
~0.2mm AIR, U→top8mm AIR, rib↔rim~1.97287mm AIR and ring↔cheek~0.199mm are
preserved; no adhesive bridge or continuous structural capacity is asserted.
IF-09/12 bonding and IF-06/07/08 structural transfer, IF-10/11 physical bending
and IF-14 stability remain unqualified. **G3_NOT_PERFORMED_OWNER_DEFERRED /
G4_BLOCKED.** Personal noncommercial scope, no physical cut/use authorization.
