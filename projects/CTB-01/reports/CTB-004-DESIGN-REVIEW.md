# CTB-004 / CSH-3P design review — pending lead selection

2026-10-20. Issue #9. **DESIGN_ONLY**. Working branch `codex/ctb-004-anchor-disks`.
Base `f49e3b3be73b7d474302823cc9072148319c8f67` after PR #8; selected SOFT_CURVE,
B_THROUGH_ADHESIVE and A_COMPACT_CLOSED/Y_FIRST. No approved dimensions changed.
All174 upstream CTB-000/P01/P02/P03 source/output files are byte-preserved.

## Geometry and layer budget

Two distinct Ø190×6 candidate disks: P04L456..462 and P04U480..486. The table envelope
remains Ø350, Z450..500, thickness50. Prospective skins450..456/494..500 leave core38.
**Free disk face gap18; lower-face pitch24; upper-disk-to-top-skin gap8.**
Actual tongues end488: only2mm projection above U,6mm clearance below the top skin.
Calling pitch24 a free rib/spacer height would shift U to486..492, leaving only2mm
of tongue engagement in a6mm plate; that proposal is rejected dimensionally.

Six tongues are extracted from the current P03 A cheek, including all existing four B and
one Y mortises, and extruded6mm tangentially at t=±10.5, angles0/120/240. Actual R1 noses
narrow from r45..69 below Z487 to r46..68 at488. Complete r-z paths and XY sections at
450/456/462/480/486/487/487.5/488 are in `parts/P04/assembly/six-tongues.json`.
Both disks have **six closed tongue holes**, 24.4×6.2 nominal, R0.2 corners. Separate
six web interfaces at60° intervals are not substituted for tongue holes. Finite thickness
and actual three-leg rotations are modeled, never inferred from a historical image.
Nominal straight-edge t clearance0.1mm/side, radial0.2mm/side; actual minimum contour
clearance0.099518mm at rounded slot corners. Stock and kerf remain unmeasured/null.

## Three alternatives

| Alternative | Separate P04L / P04U web geometry | Matching38mm counterpart reservation | Feasible order after Y-first base + bottom-skin envelope |
|---|---|---|---|
| A_RIM_OPEN | six rim-open cuts Lr80.8..edge / Ur82.8..edge, width6.4 | six OPEN profiles r81..169, Z456..494, with upper inner-edge relief r81..83,Z479.8..486.2 | L → U → six OPEN radially inward100mm |
| B_CLOSED_RAIL | six closed rail cuts Lr81.3..88.7 / Ur81.8..88.2, width6.4 | six connected RAIL profiles: full-height r82..88 rail +r95.4..169 body +bridge r81..95.4,Z466..472 | L → six RAIL vertically down64mm → U |
| C_MIXED_ACCESS | OPEN0/120/240, RAIL60/180/300; upper provisionalØ24 aperture only | three OPEN +three RAIL, count remains six | L → three RAIL → U → three OPEN |

Every web witness is actual connected, finite6mm material with matching relieved geometry.
An uncut r81..169×38 web collides with the disks; it is an explicit negative control.
Witnesses are **not finished P05**, not actual BOM parts and not integrated production CAD.
CTB-005 must select/refine/version a compatible profile; see `parts/P04/CTB-005-HANDOFF.md`.

| Candidate | Lower/upper material area mm² | Lower/upper cut loops | Min tongue-to-outer boundary mm L/U | Closed-web outer land mm L/U |
|---|---:|---:|---:|---:|
| A | 26899.470 /26976.270 | 7 /7 | 12.394 /14.285 | open notch; no closed outer bridge |
| B | 27159.805 /27198.205 | 13 /13 | 24.510 /24.510 | 6.241 /6.741 |
| C | 27029.638 /26634.871 | 10 /11 | 12.394 /14.285 | 6.241 /6.741 at three closed cuts |

All six tongue holes retain14.8mm minimum between-hole land; minimum tongue-to-web land
A/C12.394 lower/14.285 upper, B12.864/13.336. The6mm geometric land threshold used in tests
is a screening assumption, **not validated plywood strength**. X envelopes are A189.890mm, C189.945mm and B190mm; notches reduce the occupied
extent below nominal circle diameter190. Exported dimensions distinguish these values.
Circular discretization360 chords yields maximum sagitta0.003617mm; coordinates export
at six decimals. These are numerical representations, not machining tolerances.

## B13 center opening assessment

Each disk/variant explicitly assesses three options; there is **no Ø60 aperture**.

| Mode | Diameter mm | Material removed mm² | Min aperture-to-tongue land mm | Function/access status |
|---|---:|---:|---:|---|
| NO_HOLE | 0 | 0 | 45.437 from center point | Recommended baseline; no demonstrated need for a central opening |
| ACCESS_HOLE_PROVISIONAL | 24 | 452.366 | 33.438 | Assumed20mm inspection/probe envelope +2mm radial allowance; no measured tool |
| FUNCTIONAL_PORT_PROPOSAL | 36 | 1017.824 | 27.438 | Assumed20mm service probe +8mm handling allowance; hypothetical function, no requirement established |

All remain one connected disk; per-variant aperture-to-web/perimeter lands are quantified
in each `P04*-dimensions.json`. Neither assumed port grants external access after P07T
closes the top. C's upperØ24 is a comparison candidate only; lower stays solid at center.
B13 remains officially OPEN; **recommend A with NO_HOLE**, pending lead decision.
A central opening does not supply six tongue locks or justify a hole in the top skin.

## Assembly, access and actual component counts

The actual21 bodies are6 P01 +9 P02 +3 P02B +1 P03 +1 P04L +1 P04U. GLBs contain only
these21; bottom/top skin, wall, six web witnesses and tools are separately labelled studies.
Upstream Y_FIRST18 moving stages/171 continuous prior-body checks are preserved.
Continuous exact vertical swept solids verify prospective bottom skin→L→U against19,
20 and21 prior bodies respectively (60 checks/variant). No sampled frames stand in for a
continuous proof. Each complete conditional witness route has168 additional swept/prior
checks (includes upper placement); its final matching interfaces have141 checks.
The two routes are alternative demonstrations, so do not add the repeated U stage as a
new unique test. Final21-body local models have210 pair checks/variant.

The following specified routes are **BLOCKED**, not feasible assembly claims:
- Upper disk first, then lower disk from above (L crosses U).
- Bottom-skin envelope lowered after either disk (its remaining solid crosses the disk).
- U lowered after an OPEN witness (the web head above486.2 catches the disk).
- RAIL witness lowered after U (the connecting bridge crosses upper-disk material).
- OPEN witnesses inserted radially after a closed wall envelopeR171..175.

These reject the tested translations, not every imaginable rotational assembly strategy.
Keep the wall/top open through web installation and CTB-008 lock work. Six hypotheticalØ4
vertical tool envelopes can approach tongue centers fromZ520 to488.5 after disks and
matching witnesses; they collide with a subsequently closed top skin. This only reserves
space for an assumed tool, not access for a specified retainer, force, fixture or real hand.
Sliding tongue slots provide **no demonstrated positive top lock**. B01/IF-12 remain blocked.

## Recommendation and load-path limitations

Recommend **A_RIM_OPEN, NO_HOLE** for engineering-lead consideration: one web family,
accessible radial staging and no narrow closed outer bridge. No selection is made in this PR.
A's open notches offer no positive radial web capture; skins/joinery/glue/fixtures must
supply an engineered load path. B captures rails topologically but demands assembly-first
staging,6mm rail/bridge stress review and actual fitting. C adds two counterpart families
and an unproven access opening; it offers no demonstrated structural advantage.

Clearance interfaces have zero nominal interference and no adhesive bond solid: do not
interpret six6mm-high overlaps as tested bearing, adhesive area or strength. Lower disk
can contact the prospective bottom skin atZ456, webs reach both skins, but their actual
attachments are not designed. CTB-005/007/008/009 must resolve B06/IF-08 load transfer,
positive retention, adhesive, grain/fillets, material, fixtures and whole-table order.
Ring/stability/physical thickness and kerf are still open. No completed50mm tabletop,
G2/G3 approval, load rating, nesting, physical cutting or manufacturing release is claimed.

## Review artifacts

For each A/B/C: separate P04L/U DXF/SVG/PNG and dimension/provenance JSON, real horizontal
and vertical section drawings, actual/exploded21-body render, close core/witness/layer
reservation render, GLB, mating/path evidence and labelled counterpart witness exports.
All DXF cut loops live on CUT_* layers; dimensions/text on NOT_CUT_DIMENSIONS. SVG uses
physicalmm dimensions and explicit XY→screen inversion; PNG is1:1 at96dpi. Single-part
H800×W440 with provisional10mm margins passes; no actual sheet nesting is delivered.
