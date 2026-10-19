# CTB-01 status — CTB-002 design review

**BASELINE_FOR_COMPONENT_DESIGN_NOT_PRODUCTION** — CTB-000 v0.2 merged in PR #2.
**CTB-001 / P01: SOFT_CURVE SELECTED_FOR_DOWNSTREAM_COMPONENT_DESIGN — DESIGN_ONLY.**
Three parametric cheek candidates delivered under Issue #3; the engineering lead selected
SOFT_CURVE for downstream coordinated design, per `parts/P01/P01-SELECTION.md`.
This is not complete G1 joinery approval, nor permission for physical manufacture/nesting.
See [design review](reports/CTB-001-DESIGN-REVIEW.md),
[interface matrix](reports/CTB-001-INTERFACE-MATRIX.md) and
[validation record](reports/CTB-001-VALIDATION.md).
Final automated checks: 61 P01 + 25 source + 15 import = 101 passed, zero final failures.
Initial failures and repairs are retained in the validation record; independent automated
QA is recorded separately and does not replace engineering-lead approval.

## CTB-002 — DESIGN_REVIEW_PENDING / DESIGN_ONLY

Issue #5: three spacer joint studies and a versioned SOFT_CURVE mortise proposal.
Recommended B_THROUGH_ADHESIVE has one reinforced P02B at35 and three identical P02
at90/200/390. Candidate BOM P02×9 +P02B×3 +P01×6. Original P01 files/exterior unchanged.
Local rigid CAD final/swept checks pass for B; this does not prove adhesive, material,
physical fit, retention or whole-table assembly. A explicitly BLOCKED; C alternative
requires review. PC-CTB002-01 proposes245→200 only in candidate data, pending CTB006
ring coordination. Ring remains OPEN; no ring-specific holes. All B01–B13 preserved.
See [CTB002 comparison](reports/CTB-002-DESIGN-REVIEW.md),
[interface matrix](reports/CTB-002-INTERFACE-MATRIX.md) and
[validation/failures](reports/CTB-002-VALIDATION.md).
Final automated suites52 P02 +61 P01 +25 baseline +15 import =153 passed;
independent CAD-kernel QA is recorded in CTB002-INDEPENDENT-QA.
No final G1 joinery or physical cutting approval. No automatic merge.

## Authoritative baseline

All 15 original files are in `specifications/CTB-000/`, byte-for-byte unchanged.
Use `CTB-000_parameters.json` and `CTB-000_interfaces.json`; diagrams are schematic.
Preserved interfaces: IF-01 through IF-14; no interface is upgraded to validated.

Ø350 mm tabletop, 500 mm overall height, 50 mm top thickness; three legs at
0°/120°/240°, each with two parallel 6 mm birch cheeks, 15 mm inner gap, four
spacers per leg. CSH-3Y hub, CSH-3P anchor disks, VTP-R KERF-4 FLEX 4 mm birch rim.
Cutting stock: **800 mm height × 440 mm width**, portrait; X≤440/Y≤800.
Compatibility array is `[height,width] = [800,440]`.

## Unresolved issues (preserved, not closed by import)

| ID | Severity | Topic | Owner | Closure condition |
|---|---|---|---|---|
| B01 | BLOCKER | TOP LOCK | CTB-004 / CTB-008 | No structural assembly release |
| B02 | BLOCKER | ASSEMBLY ORDER | CTB-003 / CTB-004 / CTB-009 | Demonstrate a collision-free sequential assembly |
| B03 | BLOCKER | LEG GEOMETRY | CTB-001 | Produce single source of truth for six identical cheeks |
| B04 | HIGH | Y ARM ENVELOPE | CTB-001 / CTB-003 | Resolve 4mm overhang and mechanical joint reach |
| B05 | HIGH | RING INTERFACE | CTB-002 / CTB-006 | Specify one engagement design and no clash |
| B06 | HIGH | HUB-RIB INTERFACE | CTB-004 / CTB-005 | Demonstrate 3D intersections and assembly |
| B07 | HIGH | STABILITY | CTB-001 / CTB-009 | Set design loads and test stability |
| B08 | HIGH | KERF WALL | CTB-007 | Build 50mm coupons and test bend/joint/glue/filler |
| B09 | MEDIUM | RIM GEOMETRY | CTB-007 | Design and calibrate 2+ segments |
| B10 | HIGH | FIT | CTB-001..007 | Measure actual stock; fit coupon tests |
| B11 | HIGH | MATERIAL/LOAD | CTB-009 / physical trial | Do not present load rating |
| B12 | MEDIUM | SINGLE SOURCE | CTB-000 | Strictly quarantine superseded CAD |
| B13 | MEDIUM | CENTER HOLE | CTB-004 | Verify actual DXF and define opening only if functional |

The complete descriptions remain in the authoritative open-issues CSV. In particular,
B01 upper retention, B02 assembly order and B03 final leg geometry block assembly release.
Legacy V-leg LEG_A/LEG_B and tilted/multilayer CSH CAD remain quarantined as historical
references; no obsolete CAD is present in active sources or imported by this task.
The four historical ZIPs named in MANIFEST.json were not supplied; their hashes and
mechanical contents have not been independently verified in this task.

## CTB-000 baseline validation history and source discrepancies

See `reports/CTB-000-DELIVERY.md`, the complete test logs and source SHA-256 inventory.
Source validator: 25/25 PASS. Additional import consistency checks: 15/15 PASS.
Original CTB-000 frozen and provisional data remain unchanged. CTB-002 separately proposes
spacer245→200 only in versioned candidate data, pending CTB006 coordination. Local
one-leg nominal CAD collision/insertion proof is documented above; full-table3D integration,
physical fit/bending, load/stability and actual nesting remain unverified.

The supplied SVG/PNG retain a v0.1 title inside a v0.2 package and a schematic forked
side silhouette. These are source presentation discrepancies, not authoritative leg CAD.
They are preserved for review; do not use their silhouette to start CTB-001.
The only 900×440 mentions document the superseded sheet, not active settings.

## Next gate

Engineering lead selected SOFT_CURVE; CTB-002 now proposes coordinated candidate P01
mortises and four spacers. Lead review of B joinery, provisional200 height and CTB006
ring agreement is pending. Original P01 and frozen system parameters remain unchanged.
See `parts/P01/P01-SELECTION.md` and CTB002 reports.
Y reach, ring/spacer coordination, fit, locking, assembly, stability and all B01–B13
records remain open. Complete G1 joinery, integration and production are not approved.
Production remains blocked through independent assembly QA and physical tests.
