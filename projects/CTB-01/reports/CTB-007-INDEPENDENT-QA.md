# CTB-007 — independent focused CAD QA

Reviewer `/root/ctb007_qa`, separate from implementer `/root`; work2026-10-20–21, sealed2026-10-21.
Issue24, existing branch `codex/ctb-007-skins-rim`, baseline
`6db45fa7ba0d9a81ff9bbc6d1a432133ab955214`.
**PASS for bounded G1 DESIGN_ONLY studies and specified G2a nominal rigid paths.**
**96/100; unresolved in-scope CRITICAL0 / MAJOR0.**
No selection, P01/P05/P06 CR, positive retention, merge or cutting approval follows.

## Authority, scope and independence

Read Issue24, AGENTS, engineering skill/playbook/gates/QA policy, authoritative CTB000
parameters/interfaces/specification/decisions/BOM/open records, and CTB001–006 lead decisions
and handoffs. P06 C is only a further-study choice; CTB006R Issue23 is OPEN. Active P07
models correctly use the selected pre-ring27 with original jointed SOFT_CURVE cheeks,
B_THROUGH_ADHESIVE spacers35/90/200/390, A_COMPACT_CLOSED/Y_FIRST, P04A/NO_HOLE and P05A.
No P06-mortised cheek is promoted; no ring or P08/fixture/adhesive solid enters the BOM.

Captured **439 protected CTB000/P01–P06 hashes before work**, independently compared each
byte with Git base, and repeat that check in the reviewer runner. Frozen H500, topØ350×50,
6mm skins,4mm rim and portraitH800×W440 are preserved. C edge-comb skin construction is
an explicit P07-local alternative/CR, not a silent upstream modification. IF03/07/08/10/
11/12 are the affected scope; IF04/05 consumed unchanged, IF09/B05 remain OPEN.

`tests/independent_occ_review.py` imports no component implementation model. It parses actual
regenerated SVG/DXF, transforms portrait rim axes(height,s) back to(s,height), reconstructs
27 original solids in OpenCASCADE, independently derives every horizontal material band,
and constructs finite bent facets/slabs in a second CAD kernel. It does not substitute a
solid cylinder for kerfed material. The primary model uses Manifold.

Independent cell partition uses actual A top-cut contour for the common faceted inner
boundary, scaled175/171 for the outer boundary. Every profile's periodic seam complement,
connected cut topology, actual cut scale, annular material volume and GLB node geometry are
checked. Vertical sweeps are unioned in the developed plane **before** mapping (Z translation
commutes with that map); radial sweeps use translated XY boundary prisms, unioned per band.
This differs from the implementation while checking the same finite mathematical material.
No wood-deformation accuracy or neutral-axis calibration is inferred.

## Unique executed cases

| Scope | Unique cases | Result | Evidence |
|---|---:|---|---|
| New P07 Tier1 |46|46 PASS|independent final core execution |
| Focused integration |7|7 PASS|independent final core execution |
| G0 static data smoke |25|25 PASS|clean implementer log inspected |
| Import/integrity smoke |15|15 PASS|clean implementer log inspected |
| **Selected total** |**93**|**93 PASS**|repeats do not increase unique counts |

Independent final53 ran in isolated CTB007 Python3.12.14 and includes strengthened actual
web/seam-margin checks.347 unaffected older component cases are NOT_RUN:297 P01–P05 and
50 P06.40 baseline/import checks were selected as bounded smoke. No broad previous-suite,
physical test, hosted CAD CI or nightly PASS is invented. Only playbook-validation.yml
exists, without scheduled CAD triggers; infrastructure Issue20 remains OPEN and
NIGHTLY_REGRESSION_NOT_CONFIGURED.

## Initial failures and corrections retained

- Primary generation1 failed while rendering empty LineString/nan bounds; empty sections
  are skipped. It was not accepted as clean generation merely because partial files existed.
- Primary Tier1 first45/46: one C clipped-tab edge1.745e-12mm rounded to duplicate6dp
  vertices. Topology-preserving1e-9 simplification removes that numerical redundant edge;
  final exported contours remain clipped toR175, connected and non-self-crossing.
- Initial exact-boundary contact undercount was corrected to bounded1e-7 coincidence;
  independent edge-endpoint/midpoint distance measurements check the reported areas.
- Experimental kerf centres moved to20..L−20 to satisfy actual12mm B seam keepout. No
  measured material/kerf property is claimed. All final cut profiles preserve geometry screens.
- Display-only exploded rim515..565 was clipped by the former550 display crop; crop/axes
  now extend585, and the full50mm rim was independently inspected. No CAD part was changed.
- Reviewer first preflight parser incorrectly required a CUT group from historical P03
  exports. Historical-root fallback was restored only for old exports; new P07 still requires
  explicit CUT. Initial traceback retained; final independent upper235 comparisons pass.
- Reviewer first full OCC run failed constructing a radial sweep wire:22 generated union
  holes had areas1.01e-28..8.08e-28mm² and edges3.55e-15..4.02e-14mm. Only generated
  radial-sweep holes below1e-14mm² are removed with area deltas recorded. **No actual SVG,
  DXF, flat profile or final bent part is filtered.** First traceback and quantified
  diagnostics retained; A/B kernel audit passed; the corrected C-only kernel retest also passed. The final source/export seal verifies the combined evidence.

- Reviewer C contact assertion initially undercounted: the all-or-nothing1e-7 endpoint
  test dropped12 partially truncated inner facets per skin. Actual export normal offsets
  reach5.434226e-7mm at6dp precision. Independent projected collinear partial-overlap,
  with1e-6mm coordinate uncertainty, recovers127.337361mm²; bottom5916.305521/top5897.327959
  agree with primary within6.49e-5mm². **The area-agreement threshold remains0.005mm².**
  No actual contact region or component geometry changed; exact12-edge diagnostics and
  failed trace are retained. Only C's kernel audit was rerun after that measurement repair;
  A/B valid kernel records remain and allfinal export hashes are rebound/rechecked.

These are distinct failures/corrections, not additional passing test cases. Expected B
vertical/C late-rim collisions, free skin lift and all missing physical evidence remain
BLOCKED/OPEN/NOT_RUN, rather than being relabelled PASS.

## Geometry and physical gate limits

Actual exported kerf widths0.8mm are geometric hypothesis values, not measured machine kerf.
A has63 closed34mm cuts/segment; B41 staggered19mm cuts/segment; C25/23/25/23 alternating
43.5mm edge cuts plus2/4/2/4 skin-comb notches. Each cut pattern is one connected polygon;
all intended holes are waste, no retained islands. Actual midheight webs≥7.2mm and seam
margins≥12mm are screened; sharp ends, grain, strain and fatigue remain unverified.
8mm is a nominal grid, with intentional omissions near C combs; same-row16 is nominal.

All skins and portrait-transposed bands fit H800×W440 with provisional10mm margins.
That is single-part envelope fit after placement, not production nesting. NO_HOLE top
is continuous. Bottom has six individual holes matched to the actual six original tongues.
R171 skins apply to A/B; C's six integral perimeter tabs are explicitly clipped toR175.
Layers450..456/456..494/494..500 total50. Tongues end488, leaving6mm to top underside.
P05 rib-to-skin lands are516mm² each/3096 per skin; lower disk contact≈26899.470mm²;
upper disk has8mm AIR to top. Original1.973375mm rib-to-rim AIR remains unfilled.

All interfaces are nominal boundary geometry. No actual glue film, stress limit, real
physical kerf bend, neutral axis, grain, coupon, filler, finish durability, fixture/cure,
load, fatigue or stability evidence exists. Skin uplift remains FREE. B step joints have
zero nominal vertical clearance and require the radial route; C skin registration is not
6DOF capture. Probe access is a hypothetical Ø4 corridor ending488.5, not actual P08,
tool/hand access or a lock insertion proof. Closing the top blocks those six corridors.
CTB006R, B01–B13, official IF states, whole-product G2b, G3/G4 and cutting remain held.


## Final independent finite material and routes

| Study | Real bodies | Focused new-material pairs | Full vertical order | Full radial order | Top-before-rim trial |
|---|---:|---:|---|---|---|
| A |31|114 /0 overlap|12 stages/294 checks PASS|12/294 PASS|2 rim stages/59 checks PASS|
| B |32|145 /0 overlap|13/325 BLOCKED|13/325 PASS|3/90 BLOCKED|
| C |33|177 /0 overlap|14/357 PASS|14/357 BLOCKED|4/122 BLOCKED|

**436 independently checked pairs involving new material, all zero positive OCC overlap.**
Untouched upstream-only351 pairs were not needlessly repeated in each concept:439 bytes
were verified, all27 solids were independently reconstructed, and every original GLB node
was matched. Primary full final matrices contain465/496/528 pairs. Matrix comparisons and
alternative route repeats are not additional unittest cases.

Each full order includes actual P07B before L/U disks, six radial P05 insertions before
wall closure, then the particular rim route and top. C top-before-rim and B vertical
step-seam closure remain blocked despite clean final positions. A can lower its rim after
closing top, but that does not recover P08 access. All six hypothetical probe corridors
are clear with the top open and blocked by the solid top. Late bottom installation and
bottom-without-slots controls independently collide. Top upward withdrawal remains FREE
for all3; no positive skin retention or certified ring/lock is invented.

Actual mapped material includes every geometric kerf/notch. Periodically wrapped flat
profiles have no positive splice overlap; B's step contact is zero-clearance geometry,
not qualified bearing/fit. Independent flat screens verify all actual widths, lengths,
connectedness,≥7.2mm midheight webs and≥12mm true seam lands. The ideal173-axis volume
4×flat area differs from faceted volumes by≈5.08e-5 relative, the stated geometric
approximation rather than material-deformation accuracy.

All31/32/33 positive watertight GLB nodes match finite OCC reference geometry. Maximum
metre-to-mm bound difference **0.000012398mm**, maximum relative volume difference
**2.960e-6**.33 actual SVG/DXF/GLB raw hashes and15 normalized cut-geometry digests match
final files; final route statuses were independently asserted rather than only printed.
`assembly/independent-final-seal.json` binds source inputs and all recorded checks.

Independent rim/skin boundary areas, mm²:

| Study | Bottom | Top |
|---|---:|---:|
| A |6441.721656|6441.721656|
| B |6439.349744|6439.349744|
| C |5916.305521|5897.327959|

All agree with primary areas within0.000065mm². C requires projected partial-collinear
measurement because of the12 truncated facets per skin; recovered area is numerical
measurement repair, not added material/bond. The1e-6mm export-coordinate uncertainty
neither bridges0.2mm intentional gaps nor relaxes the0.005mm² area agreement assertion.

Final sections, actual/exploded views and path tables inspected. Full50mm exploded rims
remain visible. Dashed R171/R175 cylinder outlines at450/500 and the separate JSON are
explicitly **ANALYTIC_CLOSED_CYLINDRICAL_RESERVATION_NOT_MATERIAL_NOT_BOM**. They do not
replace perforated finite solids or add a hidden body. P06 reservation/Issue23, P08 absence
and physical-bend NOT_RUN are clearly labelled. Path-table images remain dense but legible.

## Score and release decision

| Dimension | Maximum | Awarded | Basis / limitation |
|---|---:|---:|---|
| Contract/traceability |20|20|439 unchanged files, selected original27, explicit C skin CR/P06R hold |
| Geometry/CAD/export integrity |25|25|actual15 cut profiles, finite mapped material/OCC,33 export hashes and real-body GLB parity |
| Interfaces/assembly |20|19|all named rigid routes/blocked trials and contact/access evidence; actual fixtures/P08 absent |
| Reproducibility/controls |20|18|53 independently repeated cases, clean93 log inspected, second kernel; optional CQ runtime reused and numerical harness repairs disclosed |
| Documentation/visuals/handoff |15|14|clear physical/gate boundaries and full-height visuals; dense sequence tables |
| **Total** |**100**|**96**|bounded DESIGN_ONLY only |

**QA≥90: YES; in-scope CRITICAL0/MAJOR0.** Recommend lead review of the bounded design
study. A is available as a least-change further-study candidate; this review does not
select it, approve C's CR, approve any P06 cheek change, close IF09/B05 or merge.
P06R Issue23, actual P08, fullG2b and G3/G4 remain OPEN/NOT_APPROVED. No physical
kerf coupon, measured stock, adhesive/bearing/load/finish or structural/stability claim.
No authorization to cut or use physical materials.

## Reproduction and retained evidence

Core reviewer runtime: isolatedCTB007 Python3.12.14 with pinned requirements; alternate
CadQuery2.7.0/OCP7.8.1.1 runtime from existingCTB001. Requirements-qa.txt documents the
optional second kernel. Independent runner imports no implementation model.

```sh
/workspace/.venvs/ctb-007/bin/python -m unittest discover -s projects/CTB-01/parts/P07/tests -p 'test_*.py' -v
XDG_CACHE_HOME=/tmp/ctb007-qa-cache /workspace/.venvs/ctb-001/bin/python \
  projects/CTB-01/parts/P07/tests/independent_occ_review.py \
  --output /tmp/ctb007-independent-full.json
# Independent exported-design web/slot/seam screens alone:
XDG_CACHE_HOME=/tmp/ctb007-qa-cache /workspace/.venvs/ctb-001/bin/python \
  projects/CTB-01/parts/P07/tests/independent_occ_review.py --flat-screens-only \
  --output /tmp/ctb007-independent-flat.json
```

The recorded repair run used `--variants C` with the previous successful A/B output to
rerun only the affected measurement/kernel audit. It did not rerun untouched components
or manufacture a full clean rerun claim. Final sealed JSON includes all three valid audits,
full source/export hashes and expected status assertions.

Final pre-commit hygiene: staging detected CRLF in `BOM-v1.csv` as trailing whitespace.
The implementer normalized it to LF. Independent reconstruction of CRLF exactly
reproduces the previously sealed SHA256; all 15 CSV rows and values are identical,
and all three variant quantities still match their export metadata. The other 11
source hashes and all 33 raw export hashes are unchanged. Only the BOM source hash
was rebound in the final seal. No geometry changed and no OCC rerun was needed;
the 96/100 verdict is unchanged. Initial diagnostic and independent confirmation are
retained in `initial-precommit-whitespace.log` and `independent-BOM-LF-hygiene.log`.

Evidence: `assembly/independent-occ-review.json`, `independent-final-seal.json`;
`tests/logs/independent-focused-tests.log`, `independent-upstream-preflight.json/.log`,
`independent-protected-before.json`, `independent-parser-initial-error.log`,
`independent-occ-initial-NullObject.log`, `independent-sweep-diagnostics.json`,
`independent-occ-review.log` (A/B success and original C measurement error),
`independent-C-contact-initial-error.log`, `independent-partial-contact-diagnostics.json`,
`independent-occ-C-retest.log`, `independent-flat-screens.json`, `independent-final-seal.log`,
`independent-BOM-LF-hygiene.log`.
Primary initial failure/correction and clean93 logs remain separately retained.
