# CTB-002 validation / DESIGN_ONLY

Source base: main849d40c45ddad721dc2aafec8241b45d9cf56a62. All CTB000 and P01 files
remain unchanged; versioned candidate holes are under P02 only. SOFT_CURVE selection
is retained. Source schema and pinned requirements are in P02/src. Full reproducible
commands are in P02/tests/README.md; no services are needed.

## Execution record

| Execution | Cases | Pass | Fail | Evidence |
|---|---:|---:|---:|---|
| Initial P02 cycle |48|46|2|CTB-002-tests-cycle1.log|
| Repair retest |48|48|0|CTB-002-tests-cycle2.log|
| Expanded final suite |52|52|0|CTB-002-tests-final.log|
| Clean venv tests before export repair (existing GLB) |52|52|0|CTB-002-clean-tests-before-export-repair.log|
| Clean venv after dependency repair / regenerated artifacts |52|52|0|CTB-002-clean-tests.log|
| Upstream P01 |61|61|0|CTB-002-upstream-P01.log|
| CTB000 source |25|25|0|CTB-002-baseline.log|
| Baseline import/integrity |15|15|0|CTB-002-import.log|

Final primary suites: **153/153 passed,0 failures,0 skipped**. P02 source was generated
and tested after fresh installation of pinned requirements in an isolated venv (no
system site packages), with generation log CTB-002-clean-generation.log. Five primary
P02 suite executions:48 initial,48 repair,52 expanded,52 fresh-venv tests on existing
artifacts before export repair,52 after successful clean regeneration; two initial test
failures followed by zero test failures. The initial clean exporter failed separately
(see item6); only the final exit0 regeneration establishes reproducibility. Ring panel
positions were corrected before that final regeneration.

Independent automated reviewer also ran the153 cases and independently reconstructed
B SVG solids in OpenCASCADE:6 valid solids,15 final intersections,15 continuous-sweep
intersections allclear,3 interfering negative controls detected,4 land checks passed.
These nested geometric assertions are reported separately, not added to the153-case
suite total. Portable reconstruction script and results JSON are preserved. Independent
report is CTB-002-INDEPENDENT-QA.md; this is not engineering-lead G1 approval.
Final results distinguish a passing test that confirms an intentionally BLOCKED A
concept from a claim that A meets design acceptance. It does not. Negative controls
pass only when a deliberately broken geometry is detected. No physical checks executed.

## Failures, repairs and retests (no hidden omissions)

1. Initial C lower P02B exterior land5.312927 mm was below the declared6 mm hypothesis.
   Reduced asymmetric radial offset10→8.5, preserving the unchanged P01 exterior,
   all spacer counts and ordinary-part geometry. New land6.661427 mm, between-hole web
   6.6 mm; full static/swept checks repeated successfully. This is a PROVISIONAL C-only
   design correction, not an approved parameter or chosen B change.
2. Upstream inventory assertion incorrectly expected>50 files. Actual Git/source inventory
   is47 (15 baseline +32 P01); now compares exactly47 and the complete path set, then
   compares every file byte against pre-task Git commit, as well as SHA256. No file was
   missing and no upstream geometry was changed.
3. Independent visual review found the P02B axes overlapped the cheek panel in the initial
   concept sheet. Corrected subplot positions for all three concepts, regenerated and
   visually reviewed; added axes-intersection/content-hash regression. P02B is now visible.
4. Independent review found rightmost ring-study3D axis labels clipped. Shrunk/moved that
   panel and reduced label padding; render reinspection recorded in independent QA.
5. Independent reviewer initially invoked default Python, which lacked Shapely. Corrected
   to documented venv; no implementation edit or tested artifact was affected. No tests
   executed in that failed invocation. Core setup now has a standalone pinned venv recipe.

6. Fresh-venv GLB export failed with ModuleNotFoundError scipy in Trimesh face→vertex
   color conversion. Existing GLB tests had passed but did not establish clean generation.
   Preserved `CTB-002-clean-generation-FAILED.log` (exit1); added pinned SciPy1.17.1 to
   core requirements. Reinstalled, reran the WHOLE exporter with shell `set -euo pipefail`,
   confirmed exit0, then52/52 tests on its fresh artifacts. `CTB-002-clean-generation.log`
   contains that successful run. Independent reviewer also reran on these new exports.
   No verification was bypassed. The failed run's unnormalized SVGs were replaced by the
   successful generator's normalized outputs; final whitespace check passes.

One functional repair batch fixed initial C/harness failures and layout; a presentation
follow-up fixed ring labels; a dependency repair fixed fresh-export reproducibility. Four added regression/verification cases expand48→52.
All original failed-case logs are preserved, not replaced by a passing-only summary.

A remains explicitly BLOCKED: lowland1.716869<6, head projection beyond cheek envelope
(35 vs27) and no proven reverse-slide restraint/coordinated insertion. Its nominal static
placement has no intersections; that cannot establish safe/feasible locked assembly.
A and C/B nominal fit/land screens have different statuses; do not combine them.

Thickness-sensitivity interference and the original245 ring-reservation overlap are
intentional counterexamples with exact nonzero values, not silently accepted geometry.
Selected nominal B, after declared changes, has no unreported CAD defect in its tested scope.

## Proof boundaries and actual geometry

Manifold3D3.3.2 constructs real solid material from exact exported-model planar contours,
including mortise holes. B has6 bodies; all15 final pairwise intersections and15 continuous
moving-vs-prior sweep checks are zero within1e-6 mm³. Sweeps cover each40 mm translation
continuously via polygon/line Minkowski sums, and the second cheek over t7.5..53.5. The
representation uses P01's≤0.02 mm chord contour and P02's≤0.005 mm ideal fillet chords;
numerical epsilon is not a physical tolerance. Stock6, slots6.4, shoulder contact and
radial allowances are declared assumptions. No force/friction/deformation/glue simulation.

Negative controls include zero thickness, zero residual web, forced two-part overlap,
shifted mortises,6.8 mm stock, reverse insertion and a missing C spare-hole pattern.
They prevent zero-test/matching-bbox/position-only passes. DXF loops vs SVG vs dimensions,
PNG actual pixels/scale, GLB positive watertight volume and source upstream integrity are
checked independently of rendering. Body reinforcement is geometry-only.

Ring diagrams/matrices use a conservative spatial reservation, not invented finalized
ring CAD. Relocation200 has22 mm plate /21.8 mm slot Z gap; bypass245 needs external
CTB006 coordination. Both retain four spacers. Full-ring route and engagement unresolved.
Y separation is a nominal envelope check; original r94/r90 mismatch remains open.

## Deliverable inventory

- P02/src: design.json/schema, model.py, generate.py, pinned requirements.
- Each of3 variants: P02/P02B and P01-SOFT_CURVE-mortise-study-v1 DXF,SVG,PNG,
  dimension JSON; concept-layout SVG/PNG, mechanical-dimensions and layout-evidence.
- P02/assembly: one-leg GLB, assembled/exploded, insertion and ring images, insertion
  instructions, collision/path matrix, ring matrix, hypothetical stock sensitivity,
  upstream hashes.
- P02/tests:52-case suite and runner README; independent OCC reconstruction script.
- P02 README, versioned BOM (P02×9 +P02B×3, candidate P01×6), ignore local bytecode.
- CTB002 design review/interface/validation/independent QA reports and actual logs/results.
- Updated STATUS. No modified CTB000, P01 source, selected exterior, upper tongue or foot.

Final mechanical G1/whole-system G2, stock/kerf fit, adhesives, structural strength,
loads/stability, machine margin/grain/edge finishing and physical cutting remain unapproved.

## Final packaging checks

Original47 upstream files match the pre-task Git commit byte-for-byte. All generated
SVGs parse; generated review SVG whitespace is normalized. Repository diff whitespace
check passes. Alternative A remains intentionally BLOCKED and is not a released design.
No reported failure remains unexplained. Required engineering decisions remain pending
in the interface matrix and review; no physical cutting approval or auto-merge.

Reusable cloud draft fields install_script/start_skill now install the pinned P02
requirements and record the153-case workflow; no services required. Saving the draft
does not execute or publish it. Review/save/publish in environment settings to activate
future-task configuration. Current-instance/fresh-venv validation is verified; restoration
in another cloud task has not been tested.

Independent execution logs are retained as CTB-002-independent-{p02,p01,contract,baseline,occ}.log;
CTB-002-OCC-independent-results.json records final exported-SVG/OCC reconstruction.
