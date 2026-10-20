# CTB-004 — independent automated CAD QA

2026-10-20. Issue #9, branch `codex/ctb-004-anchor-disks`.
Source PR: #12; reviewed geometry/evidence head `4c52d0fb04c6f7a7fd849c76bb3d7eb2cd85917a`.
Reviewer: a separate Codex QA agent, distinct from the implementing agent.
**Result: PASS for the documented nominal local design studies; engineering selection and
physical/manufacturing approval remain pending.** This is not human G1 approval.

## Scope and independence

Read the issue, root AGENTS, CTB-000 v0.2 parameters/interfaces/open issues and explanatory
documents, project status and the three upstream selection decisions. The active references
are SOFT_CURVE, B_THROUGH_ADHESIVE at Z35/90/200/390, and A_COMPACT_CLOSED with Y_FIRST.
Reviewed IF-03/04/05/06/08/12/13 and the prospective IF-07 skin interfaces; no historical
V-leg, tilted hub or implicit Ø60 center aperture supplies geometry authority.

The independent runner is `parts/P04/tests/independent_occ_review.py`. It does **not** import
the P04 or upstream implementation models. It reconstructs material from actual exported
SVG polygon loops, independently reads DXF cut polylines, and extrudes the resulting profiles
with CadQuery/OpenCASCADE. The primary model uses Manifold, so the solid kernel differs.
The current P03 A cheek/Y and selected P02 spacer exports supply the actual 19-body base.
Layer/tag checks distinguish CUT geometry from NOT_CUT_DIMENSIONS annotations.

Exact boundary-prism sweeps and extrusion along the motion axis test the entire specified
translations. These are not frame samples and do not prove every possible rigid-body route.
Witnesses and skins are explicitly separate reservations, not released P05/P07 parts.

## Independently executed suites

| Suite | Unique cases | Result |
|---|---:|---|
| P04 anchor disks | 71 | PASS |
| P03 connector regression | 51 | PASS |
| P02 spacers regression | 52 | PASS |
| P01 cheek regression | 61 | PASS |
| CTB-000 source contract | 25 | PASS |
| CTB-000 import/integrity | 15 | PASS |
| **Total** | **275** | **275 passed; zero final failures or skips** |

The P04 suite was independently run against regenerated final exports. The unchanged
upstream suites were independently executed earlier in this task. A separately captured
before/after SHA-256 inventory confirms **174/174 protected CTB-000/P01/P02/P03 files
unchanged**. The QA agent changed no upstream geometry, source, tests or approved dimension.

The following alternate-kernel predicates are supporting evidence, **not extra unique unit
tests added to 275**:

| Per alternative A/B/C | Predicates / bodies | Result |
|---|---:|---|
| Actual local model | 21 valid solids; 210 final pairs | zero overlap |
| Prospective bottom skin, lower disk, upper disk lowering | 19 + 20 + 21 = 60 prior-body checks | zero overlap |
| Six matching web reservations against 21 real bodies and each other | 141 pairs | zero overlap |
| Topology-specific conditional reservation route | 168 swept/prior-body checks | zero overlap |
| Actual GLB | 21 watertight positive-volume nodes | matches OCC geometry |

Across A/B/C this is 630 final actual-model pairs, 180 skin/disk sweep pairs, 423 final
reservation pairs and 504 conditional-route sweep pairs. The upper-disk stage occurs in
two alternative route demonstrations; it is not a newly invented unique test.

## Geometry and export findings

- Both disks receive all six actual finite-thickness tongue footprints at the three 120°
  leg rotations. Six additional web interfaces occur at 60° increments. Lower and upper
  disk geometry is deliberately different.
- Actual P01 tongue RZ material area is **911.530734 mm²** over Z450..488. Its R1 top noses
  narrow from r45..69 below Z487 to r46..68 at Z488. The full 24 mm radial width is present
  throughout both disk slabs. The exact active source, including four spacer mortises and
  one Y mortise per cheek, remains intact.
- L456..462 and U480..486 give **18 mm free face gap**, 24 mm lower-face pitch, 8 mm to
  top-skin underside Z494, and 2 mm tongue projection above U. The full envelope remains
  Z450..500, 50 mm total; the actual local model is not a finished tabletop.
- Six closed tongue holes per disk retain 14.8 mm minimum tongue-to-tongue land. A's
  tongue-to-exterior minimum is 12.393779/14.285190 mm for L/U. B's closed web holes retain
  6.241223/6.740747 mm exterior land. These are geometric dimensions, not strength limits.
- Nominal straight tangential tongue allowance is 0.1 mm per side. Independently computed
  minimum Euclidean clearance, including rounded slot corners, is **0.099518 mm**.
  Actual stock thickness, laser kerf and physical fit are unmeasured.
- SVG and DXF cut profiles agree with **zero symmetric-difference area** at their exported
  six-decimal coordinates. A has 7/7 loops, B 13/13, C 10/11 for lower/upper. All material is
  connected, all cut contours closed, and each part fits H800×W440 with provisional 10 mm
  single-part margins. This is not nesting approval.
- The nominal circle radius is 95 mm. A's notched X width is 189.890304 mm; B's is 190 mm;
  C's asymmetric X width is 189.945152 mm. Nominal diameter and remaining envelope are
  distinct dimensions.
- The three GLBs contain exactly 21 real parts each, with no hidden web, skin, wall, lock
  or fastener nodes. Applied scene transforms and metre-to-mm conversion agree with OCC;
  maximum bounding-coordinate difference is 0.0000124 mm and relative volume differences
  are below 5×10⁻⁶. The largest absolute volume difference is 0.334603 mm³.
- Reviewed the plan/section drawings and actual/exploded assembly renderings. Sections
  distinguish the web plane t=0 from the tongue plane t=10.5. Skin/witness views are
  labelled reservations. The implementation agent corrected the earlier bottom-skin
  hatching overlay to show actual sectioned tongue openings.

## Assembly and genuine negative controls

With the previously demonstrated Y_FIRST base, the bottom-skin envelope can be lowered
before the disks. L then U can be lowered continuously from above all six actual tongues.
The alternate kernel independently confirms the following conditional counterpart orders:

| Alternative | Collision-free nominal route |
|---|---|
| A | L → U → six OPEN reservations translated radially inward |
| B | L → six RAIL reservations lowered vertically → U |
| C | L → three RAIL reservations lowered vertically → U → three OPEN reservations radially inward |

The independent witness sweep uses 90 mm radial / 70 mm vertical travel, while the primary
study uses 100 / 64 mm; both cover free starts outside the relevant obstructions. Each
reservation is a single connected 6 mm solid with 38 mm overall height. OPEN's upper inner
relief and RAIL's inner rail/outer body/bridge are actual modeled material, not imagined
clearance through an uncut rectangular rib.

Intentional bad cases are correctly rejected. Representative independently reconstructed
intersection volumes are:

| Deliberate defect / order | A | B | C |
|---|---:|---:|---:|
| Disk rotated 10° against real cheeks, maximum mm³ | 864 | 864 | 864 |
| One real tongue hole filled, mm³ | 864 | 864 | 864 |
| 6.8 mm cheek against nominal slot, mm³ | 86.4 | 86.4 | 86.4 |
| One web interface moved 5°, mm³ | 468 | 216 | 468 |
| Uncut 38 mm OPEN web against upper disk, mm³ | 64.8 | n/a | 64.8 |
| Uncut 38 mm RAIL web against lower disk, mm³ | n/a | 236.9401 | 236.9401 |
| Upper disk lowered after OPEN web, mm³ | 84.24 | n/a | 84.24 |
| RAIL web lowered after upper disk, mm³ | n/a | 272.9401 | 272.9401 |

L lowered after U also collides: overlap exceeds 159,000 mm³ for every alternative.
The bottom-skin envelope lowered after L likewise collides. An incorrect **24 mm free
gap** is rejected dimensionally: U would move to Z486..492, leaving only 2 mm of tongue
engagement in a 6 mm disk. A zero-collision result alone cannot make that budget valid.
These are expected negative-control detections, not unresolved failures of the proposed
nominal routes.

## Failures and corrections during review

1. Runtime discovery found system Python without Shapely and the CTB-003 venv without
   CadQuery. Selected the existing CTB-001 venv containing both. No verification bypass,
   credential change or product-geometry change was needed.
2. The reviewer's first OCC harness incorrectly required the entire tongue RZ profile to
   equal a sharp-corner 24×38 rectangle. The actual source has rounded top corners, giving
   a 0.469266 mm² difference. Corrected the harness to preserve and measure the actual
   exported source, while still requiring the complete radial range and full engagement
   at both disk levels. No model or upstream source was changed to satisfy this check.
3. Inspected the primary initial test log: 71 cases ran with 22 failures. Its corrected log
   and the independent final 71-case run pass. Repairs address bounded six-decimal export
   comparison, near-zero NO_HOLE area residue, faint raster lines and nominal diameter
   versus the actual notched X envelope. The detailed implementation repair record belongs
   in CTB-004-VALIDATION.md; these do not establish a physical material test.

After the reviewer correction, both the initial full core audit and the enriched final
OCC/GLB/misplaced-interface audit passed for A/B/C. No unresolved nominal collision defect
was found in the 21-real-body model or its explicitly conditional reservation studies.

## Holds and review recommendation

A/B retain no center hole; C's upper Ø24 is an explicit provisional inspection comparison,
not an inherited aperture. The 0/24/36 mm assessments do not establish a need for a service
opening. Recommending A/NO_HOLE is reasonable for engineering review, but this QA does
not select it or formally close B13.

CTB-005 must finish and approve actual six-web geometry, joint relief, fillets, load path,
grain, glue and fixtures. The open notches provide no positive radial capture; the rail
bridge/land geometry has no demonstrated structural rating. CTB-007 must coordinate actual
skins/wall and keep access open during assembly. The modeled Ø4 tool approach stops above
the tongues; it is a reservation, not a specified functioning retainer. Only 2 mm projection
remains above U; B01/IF-12 positive locking belongs to CTB-008 and remains open. Complete
table assembly, ring, strength, stability, measured thickness/kerf and physical validation
remain unverified. Zero nominal overlap supplies no adhesive strength or outward retention.

**Recommend independent engineering-lead review of this reproducible DESIGN_ONLY study.**
No merge, positive lock approval, completed-table G2, G3 physical approval, production
nesting or authorization to cut physically is provided.

## QA score and gate disposition

Applied the ASSEMBL LAB engineering skill, playbook, gates, QA policy and QA template from
`origin/main` at `441d18b8fc9c2ad1a169fffc5556c12b5d2ce519`, which advanced through the
separate ENG-001 process PR while this component branch retained its original baseline.
This assessment updates reporting only; the audited geometry and test results are unchanged.
Policy source: `engineering-process/QUALITY_STANDARD.md` at that main commit.

The score applies to the **G1 DESIGN_ONLY disk alternatives and the precisely demonstrated
21-real-body local CAD routes**, including conditional counterpart reservations. It does
not score a finished P05, complete table, positive lock or physical product.

| Area | Maximum | Awarded | Independent rationale |
|---|---:|---:|---|
| Contract and traceability | 20 | 20 | Frozen inputs and selected authority verified; 174 upstream files unchanged; provisional dimensions, IF dependencies and source provenance explicit. |
| CAD geometry and export integrity | 25 | 25 | Actual SVG/DXF loops and finite solids independently reconstructed; connected material, hole topology, dimensions, stock envelopes and all 63 GLB instances checked. |
| Interfaces and assembly evidence | 20 | 19 | Continuous real-body and matching-reservation routes pass with effective negative controls; remaining access evidence is limited to an assumed tool envelope rather than a specified retainer or fixture. That limitation remains an explicit downstream hold. |
| Reproducibility, negative controls and regressions | 20 | 18 | All 275 unique cases independently rerun and alternate-kernel script reproduced; fresh core-generation logs reviewed. The alternate-kernel review reused an existing version-recorded QA venv rather than independently rebuilding that optional environment from scratch. |
| Documentation, visuals and handoff | 15 | 14 | Separate lower/upper layouts, exact interfaces, blocked orders, failures and CTB-005 handoff are clear; some generated captions remain compact and would benefit from optional readability polish. |
| **Total** | **100** | **96** | **Meets the ≥90 design-review threshold.** |

Scores express evidence coverage within the stated scope; deductions do not convert a
disclosed future dependency into a fabricated CAD failure.

| Severity / scope | Finding | Disposition |
|---|---|---|
| In-scope CRITICAL | **0 unresolved**: no impossible required nominal route, invalid contour, frozen-value incompatibility or unsupported production claim found. | No critical blocker to engineering-lead review of this study. |
| In-scope MAJOR | **0 unresolved**: no missing required regression, loss of reproducibility or known inaccurate final dimensional render found. | Previously observed harness/export-presentation defects were corrected and retested. |
| In-scope MINOR | **1 optional readability item**: some automatically generated captions pack many dimensions into a line. | Optional caption refinement; exact SVG/DXF and dimension JSON remain available. No geometry correction required. |
| Later-gate dependencies | B01/IF-12 retention, B02 whole-table order, B06/IF-06/08 finished web/load path, B10 measured fit and B11 physical loads remain unverified; B13 selection remains open. | Preserve these holds for the exact downstream claims they block; no issue is formally closed by the score. |

**Score ≥90: YES. In-scope critical blockers zero: YES.**
Independent QA recommendation: **APPROVE_DESIGN_ONLY for engineering-lead consideration**.
The engineering lead still owns the actual selection/PR approval decision; this reviewer
does not merge or authorize manufacturing.

| Gate | Evidence status |
|---|---|
| G1 component decision | Independent CAD QA PASS; engineering-lead selection/approval **PENDING**. |
| G2a local subassembly | Named nominal 21-body routes demonstrated; six prospective web solids remain labelled conditional reservations. No complete-table claim. |
| G2b whole system | **NOT_RUN / BLOCKED** for the complete product: finished P05, ring, skins/wall, positive lock and coordinated integration are absent. |
| G3 physical prototype | **NOT_RUN**: no actual plywood measurement, kerf coupon, adhesive/cure test, physical assembly, load, stability or independent physical assessment. |
| G4 manufacturing release | **NOT_RUN**: no G3 approval, calibrated production files, reviewed production nesting or release authorization. |

The 96/100 score and nominal CAD evidence do not establish measured fit, structural
strength, stability, physical safety or production readiness.

## Reproduce the alternate-kernel audit

The executed runtime has CadQuery 2.7.0 / OCP 7.8.1.1, Shapely 2.1.2, ezdxf 1.4.4 and
trimesh 4.11.2. See `parts/P04/tests/README.md` for installing optional QA dependencies.

```sh
XDG_CACHE_HOME=/tmp/ctb004-qa-cache /workspace/.venvs/ctb-001/bin/python \
  projects/CTB-01/parts/P04/tests/independent_occ_review.py \
  --output /tmp/ctb004-independent-occ-final-results.json
```

The script finds the checkout from its ancestors and accepts an output path; it does not
depend on P04 source imports or a fixed repository location. Independently executed suite
logs and machine-readable OCC evidence are retained alongside the validation record.
