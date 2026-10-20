# CTB-005 / six actual P05 ribs — DESIGN_ONLY, awaiting lead selection

2026-10-20. Issue #13; branch `codex/ctb-005-radial-webs`, approved source base
`6292a0e22c9aacade5aa7c7995332494aa8de005`. Scope: G1 alternatives and bounded G2a
local CAD evidence. SOFT_CURVE, B_THROUGH_ADHESIVE, A_COMPACT_CLOSED/Y_FIRST and
P04 **A_RIM_OPEN / NO_HOLE** are selected upstream. All259 CTB-000/P01–P04 files
remain byte-preserved. No concept/CR is selected by this implementation.

## Three actual connected plywood concepts

Each alternative supplies exactly six identical one-piece6mm nominal P05 ribs at60° axes.
All span Z456..494,38mm, within50mm tabletop envelope450..500. A boundsr81..169; B/C
r82..169: explicit1mm inner setback inside the provisional r81..169 envelope. Profile
DXF/SVG/PNG, actual finite solids and model-derived sections replace the old P04 witnesses;
they are still DESIGN_ONLY, not machine-ready production files. Face grain parallelr is
a stated hypothesis, not a plywood strength result. Corner radii and fit are uncalibrated.

| Concept | Real outline / joint | Original selected P04 | Separate retention proposal |
|---|---|---|---|
| A_RELIEVED_BOND | R1 outer88×38; rounded R0.8 inner upper relief to r83.2,Z479.6..486.4 | Final27body and radial insertion PASS; outward withdrawal FREE | Glue/skin restraint remains unverified; no P04 revision |
| B_DOUBLE_RAIL | full-height rail82..88 +body96..169 +10mm bridge82..98,Z465..475; R0.8 fillets | **BLOCKED**, upper disk interference28.8mm³/rib,172.8 total | CR-CTB005-B-01: closed L/U slots; staged rail installation and conditional translation capture |
| C_LOWER_CAPTURE_STEP | lowerrail82..88,Z456..466; body96..169; broadhead82..169,Z465..479.6; narrower upperhead83.2..169; R0.4 fillets | Final27body and radial insertion PASS; outward withdrawal FREE | CR-CTB005-C-01: lowerclosedslots only; originalU backstop opposes lifting via actual step |

A's relief deliberately differs from the old rectangular witness: rounded ends need extra
0.2mm radial and0.2mm vertical allowance for the radius, preserving clear real paths.
No original P04 witness is overwritten. Full-height uncut38mm rectangle collides and is
retained as a genuine negative control. A has envelope budgets upper7.6mm/lower23.6; afterR1outercorners the actual
inner-edge spans are **6.6mm/22.6mm**, with backbone85.8 at the relief; R0.8 mitigates an ideal sharp reentrant corner, not a verified
fatigue/stress rating. B rail6/bridge10 and C rail6/lowerhead14.6 meet6mm **geometric screen**.
C's tiny stop is separately exposed and is not treated as a6mm-certified bearing face.

| Quantity | A | B | C |
|---|---:|---:|---:|
| Face area mm² |3328.443|3081.445|3216.579|
| Nominal solid volume/rib mm³ |19970.655|18488.669|19299.477|
| Geometric bottom-skin boundary area mm² |516.0|454.8|464.4|
| Geometric top-skin boundary area mm² |516.0|454.8|510.0|
| Lower disk candidate broadside area, both faces mm² |166.914|71.445|71.859|
| Upper disk candidate broadside area, both faces mm² |141.013|72.0|140.953|

Broadside areas are the actual RZ material intersected with each disk Zslab and finite
slot-side chord, times2. They are **potential coating/clearance-interface reservations**;
the0.2mm/side air gap means no solid-to-solid bond at nominal placement. Modelled glue
area is0 because no adhesive solid/joint is supplied; physical bond properties/coverage are
UNKNOWN. Boundary length×6 at skin faces is geometric contact only, not tested glued area.

## P04-v2 change proposals and restraint claims

B restores six mouths to a continuousR95 perimeter, adds closed R0.2 web slots L81.3..88.7
andU81.8..88.2,W6.4. It retains all six tongue holes, NO_HOLE, disk positions andØ190×6.
Geometric exterior land is6.248/6.748mm for L/U. P05 rail radial allowance L0.7/U0.2mm
per end; outerbody starts96,1mm clear of circle95. Bridge465..475 fits the18mm face gap,
with3mm below/5mm above to the disks. B's unchanged-original27body overlap makes baseline
retention trials invalid; they are explicitly NOT_EVALUATED rather than reported as a lock.

C proposes only lower closed slots81.8..88.2,W6.4,R0.2, exterior land6.748mm; upperA is
unchanged. The stepped upperhead lets U lower past material above480, but lifting the rib
brings its wide lower step against U's underside. Actual exported flatstop r82.4..82.8 at
Z479.6 is **0.4×6=2.4mm²**, with0.4mm initial vertical gap. This is a stress concentration
and a poor basis for an untested load claim. Quoting the raw1.2mm sketch step or0.8mm
backstop overlap as a full bearing face would overstate actual filleted geometry.

With disks fixed atZ, exact outward20mm/inward5mm/up6.4mm/down6.4mm sweeps are blocked:

| Conditional proposal | Outward max collision mm³ | Upward max mm³ | Downward max mm³ |
|---|---:|---:|---:|
| B, both disksv2 |244.140|57.270|128.148|
| C, lowerv2/originalupper |244.140|28.589|138.369|

These demonstrate obstruction of the **named translations**, not6DOF locking, tested
bearing or restraint of the disks themselves. CTB-008 disk/tongueZ retention and fixtures
remain required. No extra fasteners, locking wedges or hidden seventh rib are modeled.
Neither proposal is approved; see `parts/P05/proposals/*/CHANGE-PROPOSAL.md`. Subsequent
adoption requires explicit lead review, downstream retests and versioned promotion.

## Whole earlier path and real27-body local assembly

Selected P03 Y_FIRST is re-executed:18 moving stages/171 exact prior-body sweep checks,
plus the actual19body model. Then prospective bottom skin is lowered BEFORE disks. The
skin is clearly an envelope, never an actual BOM part. Lower disk then upper disk, then
six radial inward100mm P05 moves works with original P04 for A and C. This yields27 real
parts (selected21 +six P05),351 final pairs and207 continuous skin/disk/rib comparisons.
B's original route is BLOCKED and its GLB is explicitly named BLOCKED; no required-path
failure is disguised as a successful baseline fit.

Both conditional proposals use envelope→L→six ribs down64mm→U, with27 real bodies,
351 final pairs and207 continuous comparisons at zero nominal overlap. B replaces both
disks only inside its proposal model; C only lower. Five GLBs distinguish baseline from
CR_REQUIRED proposal models. The BOM adds exactly P05×6; proposed disk substitutions are
not counted as extra hardware. All six instances inverse-rotate to the identical master.

Forbidden tested routes include lowerafterupper, latebottomskin, radialinsertion after a
closed wall, too-thick6.8mm ribs,5° rotated ribs, an uncut38mm web, and lifting after top
closure. A's upperdisk inserted after its existing rib head also collides; B/C deliberately
use narrower through-head staging, so upperafterrib is a valid route for their proposals.
Exact extrusions and Minkowski swept polygons check the entire motion, not frame samples.
A CAD route does not prove access for fingers, fixtures, glue placement/cure or forces.

## Skin/rim load path and future upper locks

Actual outerr169 with finite t±3 leaves min1.973375mm to curved rimR171 (2mm at t0).
That gap is AIR. Proposed load path skin→rib→disk interfaces→tongues→base requires real
bond/shear/bearing design at every link. Spaced skins/six radial planes could distribute
vertical/lateral/torsional load, but no stiffness, design loads, adhesive or stability
calculation/test has been performed. Kerfed wall continuity cannot be assumed structural.

CTB-007 handoff compares flat boundary bonds versus a versioned tab/skin-slot pair, and
preserved airgap versus a versioned near-rim extension/support. Changes must be explicit;
no modified skin, new support ring or physical glue bridge is silently in the27body BOM.
See `parts/P05/CTB-007-008-HANDOFF.md` for exact dimensions, alternatives and blocked claims.

Six assumedØ4 tool envelopes can approach tongue centers from520 to488.5 with all27 parts,
top open, but a closed top skin blocks access. Tonguesend488, only2mm aboveUtop486,6mm
below top skin494. Tools are reservations, not real retainer/hand/fixture designs. B01/IF-12
remains OPEN; solid top offers no assumed locking access and NO_HOLE remains unchanged.

## Numerical representation and recommendation

A uses quad8 rounded rectangles: R1 maximum chord sagitta0.004815mm, R0.8 relief0.003852mm.
B/C explicit fillet arcs use0.002mm chord tolerance. Export coordinates round to6decimals;
model-vs-export Hausdorff bound1e-6mm and area bound derive from that rounding. Manifold
collision epsilon1e-6mm³ and GLB relativevolume1e-5 are numerical, not machining accuracy.
Cut paths are separate from NOT_CUT_DIMENSIONS/grain annotation, physical SVGmm1:1 and
PNG96dpi. Singlepart margins10mm fit H800×W440; no full sheet nesting is claimed.

Recommend **A_RELIEVED_BOND as the compatible downstream study**, with radial restraint and
structural skin bonding expressly OPEN. If mechanical capture is required at this stage,
prefer reviewing B's stronger-sized bridge concept over C's tiny step stop, while accepting
that both need P04 CRs and fixed-disk retention. This is advice for lead selection, not a
selection or authorization. G2b whole table, G3 physical and G4 production remain unapproved.
