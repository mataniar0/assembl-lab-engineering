# CTB-01 status — CTB-000 v0.2 import

**BASELINE_FOR_COMPONENT_DESIGN_NOT_PRODUCTION** — G0 contract only, pending PR review.
CTB-001 has NOT started. No component geometry, nesting or manufacturing files were created.

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

## Validation and discrepancies

See `reports/CTB-000-DELIVERY.md`, the complete test logs and source SHA-256 inventory.
Source validator: 25/25 PASS. Additional import consistency checks: 15/15 PASS.
No frozen or provisional parameters were changed. No physical verification, load rating,
fit/bending test, stability test, 3D collision check or actual nesting is claimed.

The supplied SVG/PNG retain a v0.1 title inside a v0.2 package and a schematic forked
side silhouette. These are source presentation discrepancies, not authoritative leg CAD.
They are preserved for review; do not use their silhouette to start CTB-001.
The only 900×440 mentions document the superseded sheet, not active settings.

## Next gate

Project manager reviews this import PR; product owner retains design approval.
No automatic merge. Further component tasks require separate authorization. Production
remains blocked through component approval, integration, independent QA and physical tests.
