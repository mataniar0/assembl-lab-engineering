# CTB-002 independent QA — 2026-10-19

**PASS FOR DESIGN REVIEW ONLY.** The selected B_THROUGH_ADHESIVE proposal has no
unreported CAD defect found within the tested nominal one-leg scope. Its local
continuous insertion proof passes. A_KEYED_HEAD remains explicitly BLOCKED; C is a
nominal CAD alternative after repair. This report grants no engineering-lead G1,
whole-system G2, physical fit/strength, production, cutting or merge approval.

A separate reviewer agent performed this audit, independently executed the suites,
identified defects for the implementation agent to repair, and reconstructed exported
geometry using a different solid kernel. The reviewer did not modify implementation
or choose the working concept. The OpenCASCADE review script was authored separately,
then preserved by the implementation agent without importing the P02 model.

## Inputs, scope and executions

Read Issue #5, root AGENTS.md, CTB-000 SPEC_HE/DECISIONS and authoritative parameters,
interfaces/open issues, P01-SEL-001, P01 design/model/SOFT_CURVE profile/dimensions and
CTB-001 interface matrix. Audited P02 source/schema/generator/tests, exported profiles,
BOM, collision/path/ring/stock data, assembly instructions, design/interface/validation
reports and updated STATUS. Visually inspected all three repaired concept sheets,
assembled/exploded leg, five-step insertion strip and final 2D/3D ring study.

Independently executed from the repository root:

```sh
/workspace/.venvs/ctb-002/bin/python projects/CTB-01/parts/P02/tests/test_spacers.py
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/parts/P01/tests/test_geometry.py
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/specifications/CTB-000/validate_contract.py
/workspace/.venvs/ctb-001/bin/python tools/check_ctb_baseline.py
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/parts/P02/tests/independent_occ_review.py
```

Writable caches were set with `MPLCONFIGDIR=/tmp/ctb002-qa-mpl` and
`XDG_CACHE_HOME=/tmp/ctb002-qa-cache`. The first command used the newly installed,
isolated P02 venv. The existing P01 environment supplied optional CadQuery/OpenCASCADE.
The primary agent's fresh installation/generation is separately logged; this reviewer
did not perform that installation.

| Independently executed suite | Cases | Result |
|---|---:|---|
| P02 final geometry, exports, paths and negative controls | 52 | 52 PASS, 0 fail, 0 skip |
| Original P01 regression | 61 | 61 PASS, 0 fail, 0 skip |
| CTB-000 original validator | 25 | 25 PASS |
| Baseline import/integrity | 15 | 15 PASS |
| **Unique suite total** | **153** | **153 PASS** |

Final independent P02 run after successful clean regeneration took 4.633 s; P01 took 0.846 s. The optional solid-kernel
assertions below are additional nested geometric evidence, not extra suite cases
added to the 153 count. Primary development failures and repair/retest logs remain
in [CTB-002-VALIDATION.md](CTB-002-VALIDATION.md).

## Independent exported-geometry proof

[Portable independent script](../parts/P02/tests/independent_occ_review.py) reads
actual B SVG polygon loops and JSON placements, with no modelling-source imports.
CadQuery 2.7 / OpenCASCADE 7.8.1 reconstructs two mortised cheek solids plus four
horizontal spacers. All six solids are valid. It independently confirms:

- All 15 final material intersections are zero within the stated 1e-6 mm³ threshold.
- All 15 moving-sweep/previous-part intersections across five insertion steps are zero.
  Spacer sweeps are exact polygon/line unions constructed from boundary-edge
  quadrilaterals, rather than the implementation's constrained-triangle hull method.
  The moving second cheek is its real mortised section over the full t7.5..53.5 sweep.
- Tabs fit the complete mortise corner geometry through both 6 mm cheek slabs;
  this is solid material evidence, not matching bounding boxes or sampled positions.
- Minimum hole-to-exterior lands from exported contours are S1 8.00037421,
  S2 11.91583983, S3 13.58219911 and S4 18.30000000 mm. All exceed the declared
  6 mm geometric hypothesis; that hypothesis is not a structural minimum approval.

Independent deliberate defects produce positive collisions: reverse insertion
561.600000 mm³, mortises shifted 4 mm radially 136.479674 mm³, and a 6.8 mm spacer
against a nominal 6 mm cheek 57.557326 mm³. These prove the independent predicate
rejects material interference. The last case changes only spacer thickness; the
primary sensitivity table changes both cheek and spacer thickness and therefore
correctly reports a different maximum, 103.156288 mm³.

[Recorded kernel results](CTB-002-OCC-independent-results.json) preserve these values.
A separate GLB inspection found six watertight positive-volume parts. Each exported
mesh volume agrees with its reconstructed solid within 0.03 mm³; bounds correctly
convert GLTF metres to mm, including z0..488 and cheek t intervals -13.5..-7.5 /
7.5..13.5. Float32 mesh rounding is distinct from the solid-kernel threshold.

## Findings, corrections and retests

1. **C lower-cheek land failure:** the initial 10 mm asymmetric offset left only
   5.312927 mm exterior land, below the declared 6 mm hypothesis. The implementation
   changed only C P02B offset to 8.5 mm. Reviewed final minimum 6.661427 mm, lower
   between-hole web 6.6 mm, and successful nominal solid/path retests. Ordinary C
   spacers remain identical; both offset holes remain on each identical cheek.
2. **Overlapping concept panels:** independent visual review found P02B hidden by
   the cheek panel. The implementation repaired subplot placement for all three
   sheets and added layout/content regression evidence. Reinspection confirms both
   spacer types and the full mortise-study cheek are visible without panel overlap.
3. **Ring-study presentation:** initial 3D tick/unit labels were clipped. Final
   manually separated panels show readable 2D sections, bypass reservation and 3D
   reservation/plate positions with explicit conditional status. Reinspection passed.
4. **Test inventory expectation:** the initial primary test expected more than 50
   upstream files although the correct inventory is 47. The repaired test verifies
   the exact 15 baseline + 32 original P01 files and their pre-task Git bytes. This
   was a harness error, not a missing part or an upstream edit.
5. **Status wording:** historic baseline wording could be read as denying the new
   local collision evidence. The implementation qualified that paragraph as baseline
   history and preserved the distinction between unchanged baseline inputs and the
   candidate-only relocation. Final STATUS is consistent with the design report.
6. **Reviewer invocation correction:** an early default-Python geometry probe failed
   because Shapely was absent there. The documented venv resolved it; no geometry
   or artifact had to change. No tests executed during that failed probe.
7. **Clean-export dependency failure:** the primary agent found that the initial
   isolated-venv generator ended with `ModuleNotFoundError: scipy` while Trimesh
   converted GLB face colors to vertex colors. Tests on the previously existing GLB
   had passed, so that run did not prove successful clean generation. The failed
   exporter log and pre-repair tests remain preserved. SciPy 1.17.1 is now pinned
   as a core dependency. Reviewed the successful replacement generation log and
   installed version; after its confirmed exit 0, independently reran all 52 P02
   cases, the portable OCC reconstruction and fresh GLB/solid volume comparison.
   All passed. The earlier artifacts are no longer the basis for reproducibility.

The initial C/harness failures, subsequent repair tests, expanded suite, failed clean
export and repaired clean-repeatability execution are disclosed in validation logs. This reviewer reran the
repaired/final tests; it did not execute the primary agent's initial failing suite.
No observed defect remains hidden by a passing-only summary.

## Acceptance boundary and unresolved engineering

- Exactly four spacers per leg remain: reinforced lower P02B at z35 and three
  geometrically identical P02 at z90/200/390. Versioned candidate BOM is P02×9,
  P02B×3 and P01×6, with no loose locking part or purchased hardware hidden in it.
  P02B is wider in body/engagement; no strength increase or load rating is proven.
- CTB-000 and all original P01 files remain byte-for-byte equal to pre-task commit
  `849d40c45ddad721dc2aafec8241b45d9cf56a62`. New mortises exist only in versioned
  P02 candidate copies. Selected external SOFT_CURVE, tongue and foot remain intact.
  All 14 IF IDs and 13 B records are preserved; no legacy V model is active.
- DXF/SVG contour equality, closed/simple loops, actual PNG geometry/scale,
  per-part portrait H800×W440 envelopes with provisional 10 mm margins, source
  regeneration, nominal 15 mm inner gap / 27 mm outside section and negative
  controls pass. Sheet fit is not actual nesting or fabrication-margin approval.
- The original z245 spacer overlaps the conservative ring reservation by
  3993.37749 mm³. Candidate relocation to z200 leaves 22 mm plate / 21.8 mm mortise
  Z clearance. Outside bypass t18.5..24.5 gives 5 mm to the nominal cheek. These
  are quantified local options; ring geometry, return/engagement and whole-ring
  route remain unknown. CTB-006 must approve coordination; B05 / IF-09 remain open.
  No permanent hole lies in z225..265 and the fourth spacer is never replaced by a ring.
- A's low land is 1.716869 mm, heads project to a 35 mm envelope, and the coordinated
  slide/reverse-slide keeper remains unproven. Its clear static position is not an
  insertion or retention PASS. A is correctly BLOCKED, not silently accepted.
- B and C shoulders resist inward cheek approach; neither positively retains outward
  separation before an unvalidated adhesive/capture procedure. The nominal B path
  requires fixtures supporting each part. Stock, kerf, beam/edge quality, small ideal
  radii, grain/plywood layup, adhesive and clamp/cure procedures require real validation.
  Hypothetical 5.6 mm stock leaves unintended shoulder gaps; thicker stock collides.
- Upper spacer/mortise has Z separation from the existing Y reservation and tongue,
  but this does not solve Y r94 versus cheek r90. B01/B02/B03/B04/B05/B07/B10/B11
  remain unresolved as applicable; all other baseline blockers remain preserved.
  Full-tripod/table integration, top retention, strength, stability and physical
  cutting remain outside this PASS boundary.

The deliverables are suitable to open a PR for human design review. They are not
approved for physical cutting, G1 signoff, manufacturing, downstream integration or merge.
