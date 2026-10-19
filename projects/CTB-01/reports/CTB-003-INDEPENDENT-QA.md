# CTB-003 independent QA — 2026-10-19

**PASS FOR DESIGN REVIEW ONLY.** No unresolved nominal CAD, export or demonstrated
local assembly-path defect was found in the final study. A_COMPACT_CLOSED remains a
proposed working candidate for human review. This report grants no G1 design selection,
positive outward retention, whole-table G2, physical fit/load/stability, manufacturing,
cutting or merge approval. Eight prebuilt-module approaches and all six simultaneous
central-Y approaches are correctly reported as BLOCKED rather than hidden by final fit.

A separate reviewer agent read the requirements, audited the implementation and actual
exports, reported presentation defects, independently executed the required suites and
reconstructed all three concepts with a different solid kernel. The reviewer did not
modify implementation geometry, choose a candidate or close an official B/IF issue.

## References and preserved inputs

Read Issue #7, AGENTS.md, STATUS, CTB-000 v0.2 SPEC_HE/DECISIONS and authoritative
parameters/interfaces/open issues; P01-SEL-001, selected SOFT_CURVE source/exports;
CTB002-SEL-001, B_THROUGH_ADHESIVE model, versioned mortised cheek, four spacer stations,
assembly proof and interface matrix. Reviewed P03 controlling JSON/schema, model,
generator, tests, all three exported concepts, 19-part GLB, assembly order, change
proposals and final design/interface/validation reports.

Independently compared all **118 protected upstream files** with their Git bytes at
`ecee5f0633a6d7c122087ba75c92eddad4cb0932`: 15 CTB-000, 32 P01 and 71 P02. All match
both pre-task Git and the new SHA-256 inventory. Original frozen parameters, selected
SOFT_CURVE exterior and B spacer/mortise outputs remain unchanged. New cheek candidates
exist only under P03. All 14 IF and 13 B records remain preserved.

## Independently executed suites and reproducibility

| Suite | Cases | Result |
|---|---:|---|
| P03 connector geometry, exports, paths and negative controls | 51 | 51 PASS |
| Unchanged P02 spacer regression | 52 | 52 PASS |
| Unchanged P01 cheek regression | 61 | 61 PASS |
| CTB-000 original contract validator | 25 | 25 PASS |
| Baseline import/integrity | 15 | 15 PASS |
| **Unique suite total** | **204** | **204 PASS; 0 fail, 0 skip** |

The reviewer ran P01/contract/import with `/workspace/.venvs/ctb-001/bin/python`, P02
and an initial P03 run with `ctb-002/bin/python`, then independently reran the final
51 P03 cases in the newly installed `ctb-003` environment after presentation repairs.
Final P03 execution took 8.898 s; see
[final independent suite log](CTB-003-independent-51-final.log). Commands and dependency
pins are in [tests/README](../parts/P03/tests/README.md). Writable review caches used
`XDG_CACHE_HOME=/tmp/ctb003-qa-cache` and `MPLCONFIGDIR=/tmp/ctb003-qa-mpl`.

Reviewed the primary agent's isolated-venv installation, successful generator exit 0,
clean 51-case test log and all four regression logs. This supports repeatable generation
in the actual instance; the reviewer did not perform that fresh installation, and no
restored/new cloud-instance validation is claimed. Additional nested geometric checks
below are separate evidence and do not inflate the 204-case count.

## Independent exported-material and continuous-path reconstruction

[Portable independent OCC reviewer](../parts/P03/tests/independent_occ_review.py) reads
actual SVG polygon loops and JSON station placements. It imports no P01/P02/P03
modelling code. CadQuery **2.7.0 / OCP 7.8.1.1** independently extrudes the mortised
cheeks and selected B spacer contours, rotates complete solids by 0/120/240 degrees,
and reconstructs one Y plus six identical candidate cheeks and twelve spacers.

For **each** of A, B and C:

- All 19 reconstructed material solids are valid. All 171 final pair intersections
  are zero within the declared 1e-6 mm³ numerical threshold.
- All 18 Y-first moving stages pass all 171 comparisons against every previously
  installed part, including the other completed legs. The initial state contains Y;
  the first cheek, four spacers and second identical cheek follow for each leg.
- Sweeps cover the complete translations, rather than sampled poses. Cheek movement
  uses its actual mortised r-z material across the full tangential slab. Spacer and
  in-plane module sweeps use endpoint polygons plus boundary-edge quadrilaterals,
  including hole boundaries. This differs from the implementation's constrained-
  triangle convex-hull construction. Orthogonal motion expands the extrusion itself.
- Each prebuilt-module direction performs 126 comparisons: all six moving module
  parts against Y and all previously completed modules. Blocked earlier stages make
  later stages counterfactual witnesses, as the implementation explicitly records.

| Maximum prebuilt-module material intersection, mm³ | Radial 60 mm | Tangential 40 mm | Vertical 80 mm |
|---|---:|---:|---:|
| A_COMPACT_CLOSED | 575.329398 | 2986.489372 | 3636.897292 |
| B_DUAL_CLOSED | 718.658747 | 2601.049372 | 3275.182389 |
| C_OPEN_REMOVABLE | **0 — PASS** | 1033.009372 | 3816.867292 |

The entire central Y was also independently swept against all **18** fixed cheek/
spacer bodies simultaneously. Vertical/global-X maxima are A 5978.632335/1389.600000,
B 6563.749862/1231.200000 and C 6938.020146/712.800000 mm³. All six specified paths
are blocked. These observations concern the stated rigid translations; they are not
a universal proof about every possible rotation or multi-axis path.

[Final/path reconstruction data](CTB-003-independent-occ-results.json) and
[central-Y results](CTB-003-independent-central-results.json) preserve the pairwise
values. Nominal material collision evidence does not model support/clamp access,
friction, glue, insertion forces, deformation, tolerances or any physical assembly.

## Interface, contour and mesh cross-checks

Independent actual DXF/SVG parsing confirms millimetres, closed unique valid loops,
matching material areas/contours, one connected Y with no islands, six identical cheek
patterns per concept, and per-part portrait H800×W440 fit with provisional 10 mm margins.
All four original B spacer holes survive unchanged in every candidate. A/B preserve
the selected exterior; C deliberately changes its inner edge and stays CR_REQUIRED_NOT_SELECTED.
Rounded six-decimal SVG coordinates introduce less than 0.000162 mm² symmetric-
difference area under a 120-degree rotation; this is serialization roundoff.

A/B maximum global XY radius is 85.769983 mm, independently below 86; local arm tip
85.5 leaves 4.5 mm to the cheek's local r90 reference. The old r94 overhang is therefore
resolved geometrically in the candidate, without changing the baseline. C is smaller.
These local-r and global-radius measurements are distinct. The illustrative end land
and 6 mm land screen are study hypotheses, not certified structural minima.

A's new closed hole has 15.8 mm minimum external land. B has 16.8/7.8 mm lands and
9.6 mm between holes. C has deliberately zero mouth-to-edge land, with a separate
19.8 mm remaining outer bridge. The actual new slot bottom 406.8 versus unchanged S4
hole top 393.2 gives **13.6 mm**, rather than the older reservation's 13.7 mm. Nominal
Y z407..413 versus S4 solid top393 gives 14 mm. Core14.6 in gap15 leaves 0.2 mm per side;
the 6 mm tab/cheek depth and 6.4 mm slot are nominal uncalibrated geometry.

The GLB contains exactly 19 watertight positive-volume nodes and no hidden lock or
full-table component. Applying its node transforms and metre-to-mm conversion agrees
with independent OCC volumes within 2.96e-6 relative error. A further direct audit
compared **all 7,602 mesh vertices** with independently constructed extruded SVG vertices
and station/rotation matrices: maximum positional difference **0.000029003 mm**,
consistent with float32 encoding. This does not establish manufacturing precision.
See [export data](CTB-003-independent-export-results.json) and
[vertex data](CTB-003-independent-vertices-results.json).

## Negative controls, review findings and retests

Independent deliberate defects reject a trivial always-clear predicate:

- A 6.8 mm Y against the nominal exported cheek collides by **38.355291 mm³**.
- Moving only the Y mortise 4 mm radially collides by **136.464686 mm³**.
- Severing the full upper cheek neck creates **two disconnected material components**.
- The blocked prebuilt and central-Y paths above remain genuine nonzero obstruction
  controls despite feasible final positions.

[Negative-control data](CTB-003-independent-negative-results.json) preserve these
results. The primary suite separately catches restored r94, lost arm web, wrong cheek
entry, shifted mortise, zero thickness and thick Y stock.

Reviewed repairs and retests:

1. The first sequence image was a text list with no visible motion. Reviewer feedback
   led to 18 actual start/end XY projections and arrows, grouped by leg rotation.
   Reinspection confirms readable directions and installed-part check counts.
2. C's long title clipped/approached the panel title. The implementation wrapped and
   reduced it; the final original-size image is readable and retains the CR hold.
3. The primary agent found that a full-width dashed Y-height rectangle could imply
   material across the cheek. It replaced the detail with the actual Y intersection
   at local t10.5. Reinspection of all three final layouts confirms only the real
   single/dual tab sections are shown inside the slots/open channel. Final 51-case
   independent rerun passes. These were presentation changes, not contour repairs.
4. The review mesh comparison initially used an arbitrary absolute 0.06 mm³ allowance.
   P03 differs by 0.090809 mm³ because float32 stores z407.000005..412.999988, giving
   thickness5.999982 rather than6. The reviewer corrected the review-only criterion
   to 5e-6 relative after checking coordinates, volumes and all vertices. No production
   geometry or solid-kernel collision threshold was changed.
5. Combining the independently passing review scripts into one portable file briefly
   shadowed a helper function with a dictionary. The reviewer repaired the wrapper
   variable name and completed the combined script with exit 0. This was a reviewer
   harness packaging failure; no implementation artifact or geometric result changed.

No unresolved nominal CAD defect remains from this review. Primary generation/test
cycles, blocked attempts and presentation repairs remain disclosed in
[CTB-003-VALIDATION](CTB-003-VALIDATION.md); this report does not replace that record.

## Engineering decisions and acceptance boundary

A's shortening, new hole and demonstrated Y-first route are suitable for lead review.
A/B provide nominal r/z engagement; neither positively retains outward cheek separation.
B's additional tab span is not evidence of stronger locking. C's radial route is
reversible and lacks a retainer; its exterior change requires the explicit CR decision.
No invisible component, adhesive assertion or friction assumption supplies that retention.

Y-to-bottom-skin/disc distances are envelope reservations only. Actual ring/discs/top
locks, fixtures, whole-product sequence and loaded behavior were not designed or
validated here. Plywood thickness, kerf, grain/layup, notch stress, adhesive/cure,
strength, floor contact and stability remain open. Official B01–B13/IF statuses remain
unchanged until the responsible human decision. B04 has nominal geometry evidence;
local three-leg assembly evidence does not grant full-table G2 or physical G3/G4.

**Suitable to submit a DESIGN_ONLY PR for independent human review. No physical cutting,
manufacturing release, human approval or merge is authorized by this QA result.**
