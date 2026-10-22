# CTB-014 — B1: NO-GO for the current nominal geometry

**STOP_AFTER_B1 / DESIGN_ONLY / LEAD_REVIEW_PENDING.** No source geometry was
changed. No kerf, material, strength or elastic snap-fit allowance is assumed.
No nesting, B2, production exports or merge.

## Exact inputs and bounded claim

CTB-012 PR56 `3326b49fc49eaa63c6ef2a904a7d3cb69fec2ebd`, stacked CTB-013 PR57
`72595e4cd7164efa44b4ebda8bf48bf7b2c51c11`; both are **OPEN proposals**, not
approved geometry. Branch `codex/ctb-014-puzzle-b1` is based on that CTB-013 head.
24 original study files are SHA256 pinned in evidence.json; original P01–P07,
specifications and assembly sources are unchanged.

P1, IF-10 rim/skins and IF-11 seams. IF-07/08/12 structural/retention dependencies
remain open. The smallest remaining question is whether these precise source
profiles can occupy the prescribed final frame and admit a rigid insertion.
The local engineering skill and LEAN policy apply; ChatGPT reviews after B1.

OpenCASCADE (`cadquery-ocp 7.8.1.1.post1`, CadQuery2.7.0) uses the **source-defined
nominal** mapping: native rim x=h, y=s; Z=450+h, radial material171..175,
theta=phase+(s−0.2)/173; phase15/195deg. This is an ideal mathematical wrap,
not an assertion about physical bend dimensions or material thickness.

## Results

| Check | Cases | Result |
|---|---:|---|
| Actual SVG profiles / raw DXF coordinate agreement | 8 | PASS |
| Standard ezdxf import of original DXF | 8 | **FAIL**: missing `AcDbPolyline` subclass |
| Clean temporary CTB-012 regeneration, numeric geometry | 1 | PASS;12 temporary vectors match |
| Notch-floor to kerf-slot lands | 4 | PASS as nominal geometry only |
| P07R1/R2 material vs P07B/P07T at final Z bands | 4 | PASS; maximum overlap2.468e-9mm³ |
| Two final puzzle seams | 2 | **FAIL**: positive 3D material overlap |
| Filled-notch and separated-witness controls | 2 | PASS, expected outcomes detected |
| **Total unique cases** | **29** | **19 PASS /10 FAIL** |

The8 DXF failures share one export-format cause. Their original raw coordinate
tags match the8 valid SVGs, so nominal CAD diagnosis remains possible **using
the SVGs**, without repairing or certifying the DXFs. No invalid DXF is called
PASS. The two geometric failures share a seam-registration cause.

The prescribed half-circumference is **π×173=543.495529071mm**, whereas each
body from s0.2 to543.295529 is **543.095529mm**: **0.400000071mm shortfall per
seam**. The headed reciprocal profile overlaps after the actual phase rotation;
coincidence under flat body-length translation does not prove circular fit.

At each seam, two independently defined rectangular material subsets are
strictly contained in the respective original source profiles. Exact circular
annular-sector BReps give a common volume of **0.071992mm³ per seam** at
**Z468.3..468.4mm**. This is a robust **lower bound**, not a whole-rim Boolean
volume. The source-subset bounds and global3D intersection bounding boxes are
recorded in evidence.json; the actual curved witness bodies and intersection
are in `collision-witnesses-DESIGN_ONLY.step` (two joints, three witness solids
per joint; **not** a6-part wood assembly or cutting model).
The tiny rectangle inset is a conservative proof-subset selection, not a
clearance/kerf allowance or a change to either original profile.

Separately, source-profile intersection area is0.6952728321mm² per seam; the
nominal cylindrical map integrates that to2.781091329mm³ per seam (Jacobian
integrated over radial171..175 is4). This analytic total is **not represented
as an independently computed full-shell Boolean result**.

The4 skin tests include all shell material in Z450..456 and494..500, with
actual skin tabs/holes; the puzzle head lies outside those bands. They prove
bounded final-band non-overlap, **not** whole-shell or insertion approval.
CTB-012 nominal tangential allowance is0.25mm per side before coordinate
rounding; physical fit is unmeasured. Minimum notch-to-kerf land: reference2mm,
reinforced/puzzle6mm. Each puzzle half retains63 slots,18 shortened. The puzzle
neck is nominal12mm at its one-sided limiting section, head14mm at s−4 and
tip6mm at s−7.8; the source has sharp polygon corners, no qualified fillet or
neck/bend strength evidence.

## Assembly decision, failures and handoff

**BLOCKED_AT_FINAL_STATE:** no collision-free rigid path can end in the proved
overlapping prescribed state. Therefore a full shell sweep/closure path is
**NOT_RUN**, rather than passed or approximated by pose sampling. Top/bottom
insertion-path approval, elastic snapping/deformation and alternative final
registrations are not established. No new alternative was designed.

Three verifier attempts: first aborted on a real DXF import defect before CAD;
second exposed one checker-only byte-text false failure (`39` vs`39.0`) in
regenerated DXF; third completed the bounded CAD diagnosis. One extra source-only
temporary diagnostic rebuild confirmed numeric equality. **0 source repairs,
1 checker repair**, plus1 diagnostic raw-tag-reader adaptation that preserves
all original DXF failures. Repeated cases/aborts are not added to29.

One subsequent repository-format check flagged OCCT's generated STEP line-end
blanks. One artifact-only formatting repair removed those blanks; all STEP
non-whitespace tokens and quoted strings are identical, and re-import preserves
all6 valid solids and their volumes. This is separate from the29 design cases,
does not modify original sources and causes no full-suite/sweep replay.

Reproduce from this branch, no source writes:

```sh
XDG_CACHE_HOME=/tmp/ctb-cache MPLCONFIGDIR=/tmp/ctb-mpl \
 /workspace/.venvs/ctb-001/bin/python projects/CTB-01/studies/CTB-014-B1/verify_b1.py
```

Independent review is recorded separately in INDEPENDENT_QA.md. Lead must
resolve the nominal circumference/seam registration and DXF validity in future
versioned sources before requesting another B1. **No source corrections are
implemented here.** No historical full-table/B2 suite ran. Physical kerf,
fit, grain/flex, glue, neck stress, load and stability NOT_RUN; G3/G4 remain
unapproved. Stop for ChatGPT review; no self-merge or physical cutting approval.
