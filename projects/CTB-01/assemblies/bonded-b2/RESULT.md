# CTB-009 B2 — G2b_CAD_CANDIDATE_GO_ONLY

Issue [#34](https://github.com/mataniar0/assembl-lab-engineering/issues/34), 2026-10-21.
Branch `codex/ctb-009-bonded-whole-assembly-b2`; base `daa8879badb921ca3ca3c6d7c848ada90ffae7e7`.
**DESIGN_ONLY / INDEPENDENT_QA_PENDING / SECONDARY_KERNEL_PENDING.**
**BOND_CAPACITY_NOT_RUN / G3_NOT_PERFORMED_OWNER_DEFERRED / G4_BLOCKED.**

P0 scope: instantiate the approved study candidate once, check all32 simultaneous
wood bodies and the complete ordered rigid-material route, with changed-interface
CAD checks and explicit inherited P07A provenance. IF-09/01/02/14 are affected by
the six identical ring mortises; IF-04/05/06/07/08/12 and upper load paths remain
geometrically documented, with bonding/functional qualification OPEN.

**Exactly32 distinct, connected, positive-volume wood solids**: P01×6, P02×9,
P02B×3, P03×1, P04×2, P05×6, P06×1, P07 skins×2, rim strips×2. Six P01 geometries
replace their existing instances;25 original P07A objects are reused unchanged.
Zero P08 keys, adhesives, fasteners or fixture solids. The32-node GLB round-trip
has32 watertight meshes; CAD unitsmm, glTFmetres. The rim remains the original
mathematical pre-bent, perforated material, not a physical bending simulation.

| Evidence category | Unique checks / result |
|---|---|
| Simultaneous final geometry | **496 fresh pairs**, maximum overlap7×10⁻⁹mm³, below10⁻⁶mm³ epsilon. |
| Whole insertion sequence | **31 moving stages** after initially positioning P06. **274 new swept pair checks**, plus **222 explicitly inherited P07A pair checks**, covering all496 predecessor relationships. No failed stage. |
| Negative controls | **12 fresh cases**: six missing-ring-mortise cheeks overlap≈936mm³ each; six6.8mm-ring stock trials overlap≈62.4mm³ each. All detected. |
| Source/body invariants | Five provenance/profile and eight BOM/exterior predicates pass. All32 solids remain one connected component each. Protected project tracked diff is empty. |

Thus **782 distinct new geometric pair/control checks** were evaluated
(496+274+12); the222 inherited cases are **not** counted as newly executed.
No historical P07A93-case or unrelated component regression suite was rerun.

Order: P06 held atZ242..248 → P03 down → each leg's first cheek, four spacers,
second cheek in Y_FIRST → actual P07B → P04L → P04U → six radial P05 insertions
→ two rigid mathematical P07R insertions → solid P07T. The31 named steps,
offsets, freshly tested partners and inherited partners are in `evidence.json`.
An assertion verifies complete predecessor coverage with no omitted/double-counted
partner. Ring support, glue application/access, cure and fixtures are **not proved**.

Upper-stage sweeps are recomputed against all six replaced cheeks and the new
ring. Their unchanged other partners inherit `P07/assembly/proofs.json`, selector
`A.routes.bottom_disks_ribs_rim_top`, byte-identical to original merged commit
`8f57abc75113ad2f4d37455dfd1905e951cde98a`. All451 upstream/seal source hashes match;
the proof and specific source hashes are included. B1 was not replayed for the
viewBox-only fix; current numeric metadata and actual polygon coordinates load.

All six joint section-envelope clearances are **0.199036612..0.199036767mm**, versus
nominal0.2mm (source fillet/chord and SVG precision). Minimum affected wood ligament
is10.963951423mm to the original exterior and38.652866247mm to prior mortises.
These are geometric measurements, not kerf, glue-gap or strength qualifications.
Original upper tongues still endZ488; tabletopØ350/H500/top50, gap15, cheeks6mm,
four spacers per leg, P07T NO_HOLE and original source profiles remain unchanged.

**Geometric load-path limits:** P04U is8mm below P07T. Each U↔P05 interface has
at least≈0.2mm whole-band geometric separation, as does the measured L↔P05 band;
there is no zero-gap U-to-rib contact or direct U-to-top bridge. Intended load
transfer requires qualified bonding across these actual interfaces. Rib-to-skin
flat coincidences are516mm² per rib per skin; L-to-bottom coincidence26899.470377mm².
Actual faceted rib/rim section distances atZ457.5 are≈1.972870mm of AIR, not glue.
No projected/coincident area is asserted to be an effective bonded area or capacity.

**Failures/fixes:** first attempt stopped before finite assembly because a new
source check compared lexical numeric SVG text. Original/candidate coordinates
were numerically identical; fixed the checker once. Zero design/source geometry
repairs. Two full candidate builds and two read-only replays cover the same cases;
the second build added per-rib distance reporting. History is retained in JSON.

Reproduce using the existing P07 pinned environment:

```sh
XDG_CACHE_HOME=/tmp/ctb-cache MPLCONFIGDIR=/tmp/ctb-mpl \
  /workspace/.venvs/ctb-007/bin/python projects/CTB-01/assemblies/bonded-b2/integrate.py
```

`--write` regenerates evidence and the one GLB; normal replay also verifies the
archived model hash. Deliverables: `integrate.py`, `evidence.json`, this report and
`assembly-DESIGN_ONLY.glb`. No production exports, nesting, gallery or new alternative.

**Review gate:** this is a CAD candidate GO, **not G2b PASS**. ChatGPT must independently
review actual model/evidence. Before any G2b PASS, separately reconstruct the changed
cheeks/ring in an alternate CAD kernel and confirm final32-body coexistence plus
critical changed swept paths; retain pinned provenance for unchanged routes. That
secondary execution is NOT_RUN, and no independent score is claimed here. Bond,
fixture/cure/access and structural qualification remain OPEN. G3 is owner-deferred,
not PASS or N/A; G4 stays blocked. No self-merge or physical cutting/use approval.
