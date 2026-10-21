# CTB-010 — independent digital-file review

**Reviewer:** `/root/ctb010_file_qa`, separate from the export implementer.
**Branch:** `codex/ctb-010-final-digital-closeout`; baseline
`9caa69445d3f9816bdf23a934d8824b86e1ad913`.
**Scope:** stages3/4 experimental personal-prototype vectors, nesting and handoff.
**Decision:** `PASS / APPROVE_DESIGN_ONLY_FOR_LEAD_REVIEW`, **96/100**.
ChatGPT's lead decision and merge remain pending. No G2b self-approval.

## What I actually checked

I read the exporter and verifier, then used a separate read-only program without
importing either. Native SVG polygons were parsed with ElementTree and compared
with the native-profile JSON; final DXF was re-imported using ezdxf1.4.4 and final
SVG was separately parsed with ElementTree, including mm/viewBox/display-axis
transforms. Shapely2.1.2 checked valid material, closed boundaries, apertures,
actual contour differences and placement clearances.

| Independently re-evaluated logical cases | Count | Result |
|---|---:|---|
| Authoritative source copies / native profiles | 12 | PASS |
| Master vectors, DXF and SVG | 22 | PASS |
| Stock-sheet vectors, DXF and SVG | 16 | PASS |
| Body placements checked against both re-imports | 32 | PASS |
| **Read-only geometry/source rechecks** | **82** | **PASS** |
| Separate real corrupt-file controls | 5 | All rejected |

The five independently tested corruptions duplicated a cut contour, removed one
rim slot, changed SVG physical scale, moved cuts outside the bed and removed a
BOM placement. These re-evaluate existing cases; **do not add 82+5 to the
implementer's 94 unique-case total**. I did not rerun its whole verifier.

Observed results:

- All **38 final vector files** agree with the original selected source material
  to 1e-7mm boundary/bounds and 1e-5mm² material-area comparison tolerances.
  No crossed/common-line or duplicate boundaries, orphan apertures or invalid
  material polygons were found.
- Exactly32 wood bodies map to12 roles and11 unique masters. All6 P01 use one
  source; both rim instances share the identical master and retain distinct body
  IDs. P04L/U remain different shapes. P08 count0; P07T has no holes.
- The two flat rim strips retain **126 total apertures**,63 each, of nominal
  0.8×34mm. No mesh projection, curve refitting or kerf compensation was used.
- Eight portrait sheets, **7 nominal6mm +1 nominal4mm**, with no thickness mixing,
  rotations or reflections. Actual minimum outer-part gap **5mm** and stock-edge
  margin **10mm**; all cuts fit WIDTH440×HEIGHT800. This is feasible conservative
  packing, not an optimality or calibrated grain/flex claim.
- Numbered ring pre-position +31 translations match accepted B2 records.
  The GLB, inherited primary/secondary JSON and secondary source hashes match
  the repository originals. This is byte/provenance review, **not CAD execution**.
- Source polygons, original parts/specification files and accepted geometry
  remain unchanged. Native JSON and strengthened pre-seal checked-file hashes
  are covered by the final verifier. Its sealing code verifies QA digests before
  archiving, then reopens the ZIP and compares membership/bytes/CRC.

I independently reopened the preparatory ZIP after its first seal:72 entries,
71 per-file inventory digests, exact package-tree byte equality, unique/safe
entry paths, CRC and ZIP SHA256 sidecar all passed. This report is added after
that check and must be included by the final reseal; the final ZIP's non-circular
SHA256 belongs in its sibling `.zip.sha256`, not inside the ZIP itself.

The read-only review ran using `/workspace/.venvs/ctb-001/bin/python`; its
temporary audit script `/tmp/ctb010-independent-file-check.py` has SHA256
`070f9dd7c8fbcd2f85f4ea10b64b9623b26db966368647f8e17730b2cdaed43d`.
The archive check used Python `zipfile`/`hashlib` against every package member.
Repository-reproducible file QA and exact named cases are in
`QA/verify_package.py` and `QA/file-evidence.json`.

## Failure accounting and score

Independent checks: **zero unexpected failures, zero geometry corrections**.
Implementer evidence records94/94 unique cases, including5 negative controls;
its three passing file-verifier executions are repeat executions, not282 cases.
Coverage refinements/native JSON sealing and final report wording did not repair
failed source geometry. Historical B1/B2/secondary checker fixes are preserved
in inherited evidence and are not new execution failures here.

| Area | Awarded / maximum |
|---|---:|
| Contract and traceability | 20/20 |
| Geometry/export fidelity | 25/25 |
| Assembly/interfaces within file-review scope | 19/20 |
| Reproducibility/negative controls | 18/20 |
| Documentation/handoff | 14/15 |
| **Total** | **96/100** |

**Critical/major in-scope blockers:0.** No design revision requested.
Independent final archive resealing and ChatGPT lead approval remain separate
from the vector/file evidence. The current package does not qualify measured
stock/grain/flex/kerf, physical fit/bending, glue/cure/fixture/access, loads or
stability; **B1/B2/OpenCASCADE runs during this review:0**.

IF-09/12 bonding, IF-06/07/08 structural transfer, IF-10/11 physical bending and
IF-14 stability remain unqualified. Existing ~0.2mm upper-disk/rib AIR,
8mm upper-disk/top AIR and ~1.97287mm rib/rim AIR are not adhesive bridges or a
proven continuous load path. **G3_NOT_PERFORMED_OWNER_DEFERRED / G4_BLOCKED.**
This review authorizes no physical cutting/use, strength claim or self-merge.

## Focused packaging-format follow-up

The later repository formatting check (`git diff --cached --check`) flagged the
three CSV files' default CRLF endings. **One repository-format failure and one
formatting repair** are recorded separately in `QA/packaging-evidence.json`;
this is not a CAD/source or 94-case file-suite failure.

I independently compared each LF-normalized CSV with the pre-repair parsed rows
and SHA256 I had captured. All three retain exactly the same rows; restoring
CRLF reconstructs each original digest exactly, and updated QA digests match.
The exporter now explicitly writes LF. Fifty-six vector/native/source/placement
inputs, including all38 final vector files, remain byte-identical to the prior
sealed inventory. No new full-suite or CAD-kernel run was needed. Scoped review
remains **96/100**, zero geometry repairs and zero critical/major blockers;
archive integrity is rechecked after the final reseal.
