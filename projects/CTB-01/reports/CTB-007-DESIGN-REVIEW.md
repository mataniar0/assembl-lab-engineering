# CTB-007 — two skins and three experimental kerf-rim alternatives

Issue24, branch `codex/ctb-007-skins-rim`, source `6db45fa7ba0d9a81ff9bbc6d1a432133ab955214`.
**DESIGN_ONLY / AWAITING_LEAD_SELECTION**, G1 geometry and bounded G2a nominal tabletop paths.
Recommend A as the least change continued geometry/coupon-planning concept. This is not
an instruction or authorization to cut coupons or a claim of physically bendable plywood.

## Authorities and unchanged architecture

Read rootAGENTS, engineering skill/playbook/gates/quality policy, CTB000v0.2 authoritative
JSON/spec/decisions/BOM/blockers, currentSTATUS and CTB001–006 decisions/handoffs. Active
pre-ring 27: SOFT_CURVE with B_THROUGH_ADHESIVE35/90/200/390, A_COMPACT_CLOSED/Y_FIRST,
P04A_RIM_OPEN/NO_HOLE, P05A_RELIEVED_BOND. All 439 CTB000/P01–P06 files are byte-preserved.
P06 C is only a research choice, not an approved usable ring or cheek modification.
**CTB006R Issue23, IF09/B05 remain OPEN**; P06 and its unapproved cheeks are absent here.

Frozen externalØ350/H500/top50, nominal skins6/rim4 and portrait H800×W440 are unchanged.
P07B450..456, core456..494=38, P07T494..500; P04L456..462/U480..486 preserve18mm free gap.
The actual six P01 tongues pass through six R0.2 apertures in P07B; slots align to current
P03 candidate positions, nominalr44.8..69.2 andt-centres±10.5,width6.2. P07T is connected
NO_HOLE. Tongues end488,6mm below top underside494; no collision or historicalØ60 hole.
Relevant IF03/07/08/10/11/12 primary; IF04/05 consumed unchanged; IF09 reservation only.

## Three alternatives, exact finite parts

| Variant | Rim / skin construction | Counts | Specified feasible rigid route | Retained blocked trials |
|---|---|---|---|---|
| A TWO_BUTT_BOND |2 butt segments; closed0.8×34 slots at8mm adjacent pitch;8mm edge rails; R171 skins |27+2skins+2rim=31 |vertical or radial rim entry before top; rim may also lower after top |late bottom, rib after closed wall, closedtop lock access |
| B THREE_STEPPED_BOND |3 step-seam segments; offsets−4/+4/−4 atheight18/32; staggered slots;6.5mm edge rails; R171 skins |32 |radial sector entry, then top |vertical rim closure with or without top |
| C FOUR_EDGE_COMB |4 butt segments; alternating open-edge kerfs; new P07-local edge-comb skins and matching end notches |33 |rim down before top, then top into notches |radial rim and top-before-rim |

Only the named rigid, already mathematically curved configurations are proven accessible.
No finite-element bend, springback, forming force, glue cure or fixture sequence is claimed.
B's final position is collision-free but vertical approach is blocked; the successful radial
route is different and is explicitly swept. C's correct order matters even with a clean fit.

Common rim innerR171/outerR175, full height50. Mathematical neutral radius173 gives
P=1086.991058mm. Segment nominal arc lengths A543.495529/B362.330353/C271.747765.
Per-seam longitudinal gap0.4 gives total gaps0.8/1.2/1.6; coverage1086.191058/1085.791058/
1085.391058mm respectively, pending actual neutral-axis/kerf calibration. The one-piece
strip exceeds800 in either useful portrait orientation; each finite developed piece fits
W440×H800 with10mm provisional margin. Flat axisX=height50/Y=arc length: no scale changes
or invented900mm stock. A/B/C maximum bounding lengths≈543.096/369.930/271.348mm.
These are single-part screens, not approved sheet nesting.

All actual cut material is connected, valid and free of retained islands; inner loops are
waste. A/B long slots are closed through-cuts, C alternating cuts are open notches. Nominal basegrid
pitch8 with0.8 geometric openings leaves7.2mm midheight webs; B/C nominal same-row pitch16; C omits grid slots near edge-comb regions.
A8/B6.5 rails preserve both6mm skin edge zones. C interrupts those zones intentionally;
kerfs are excluded around the six edge-comb notch regions by8mm, and seam regions by12mm.
The first pattern's B seam margin was corrected by shifting kerf centres to20..L−20.
Sharp slot ends are experimental stress concentrations; screen values are not strength.

A butt gaps have no positive splice lock; boundary bonding is unverified. B nominal two
horizontal steps share7.6mm each (8−0.4), ideal developed bearing60.8mm²/joint at4mm
thickness, with **zero nominal vertical clearance**. Real fit and retention remain untested;
a radially withdrawing segment is not a certified self-retaining whole rim. C uses butt
seams plus skin-edge registration; six skin tabsr169..175/t±4 are clipped to commonR175
so no corner exceedsØ350. Rim angular notches use0.2 nominal clearance andheight0..6.2/
43.8..50. C changes the proposed skin's radial construction, explicitly documented as
CR-CTB007-C-01; it does not modify any approved upstream P01/P04/P05. C has a tested3deg static angular
misregistration collision when seated, but the top can lift out. No variant completes skin Z retention.

## Mathematical material versus physical kerf development

Flat orthogonal profiles are sliced at every true height transition; each material interval
maps to a shared360-facet annulus and is extruded through that height. GLBs retain every
actual kerf/notch and seam, finite4mm material, and exactly31/32/33 actual bodies. They are
not full unperforated cylinders passed off as kerfed solids. The ideal axis173 gives mapped
volume4×flat area; faceting differs≈5.08×10⁻⁵ relative. MaxR175 facet sagitta0.006664mm.
This mathematical mapping does not account for neutral-axis migration, wood strain or
kerf opening/closure. `KERF_COUPON_PENDING`, measured stock/kerf/neutral axis all null.
Full50mm coupons, grain, strength, bendability, fixture, adhesive and finish tests NOT_RUN.

Smooth wood-like finish remains a hypothesis. All through-slots/seam gaps are real and
visible before finishing; filler/sanding is decorative, never a load-bearing bridge. No
unmodeled outer veneer or extra thickness is added. Finish must preserve externalØ350 or
trigger a reviewed change; appearance, shrinkage and durability need physical assessment.

## Contacts and proposed load paths

AtZ456 P04L/P07B share26899.470mm² nominal face area. P04U ends486,8mm below top skin:
there is no direct U→top face contact. Six original P05A have real face intervals82..168
atbothZ456/494:516mm²/rib/skin,3096 total per skin. These are boundary geometry, not measured
bonds or adequate shear transfer. No glue film is silently counted as a solid or capacity.

Rim-to-skin nominal boundary areas (faceted coincidence tolerance1e−7mm): A6441.722 each,
B6439.350 each, Cbottom5916.306/top5897.328mm². C loses boundary at its intentional edge
kerfs/notches. This quantifies contact availability; it supplies no permissible stress.

Original ribouterr169 still leaves **1.973374878mm minimum AIR** toR171 at t±3, not a glue
joint. Selected design explicitly transfers hypothesized loads through P05↔skins and
skin-edge↔rim; it does not require or claim a direct rib/rim joint. Optional near-rim P05tip-v2
would end≈170.77365 for0.2mm curved clearance and still need a real joint. That is a
NOT_IMPLEMENTED coordination option in proposals, no upstream extension/seventh rib.
IF07/08 structural bonds/disk restraint and P05 outward retention remain OPEN.

## Assembly and top-lock dependency

Actual lower19 are consumed unchanged from selected Y_FIRST. Lower actual P07B from520
before L/U disks; lower L, then U; insert all six original P05A radially100 with open rim.
Evaluate sixØ4 probe corridors from520 to488.5 before closing P07T: they are clear access
reservations, not actual P08 installation or tool/hand/force proof. No P08 solid is supplied.
Then use Avertical/radial, Bradial, or Cvertical rim entry, and lower top540→494. Full
valid route lengths/checks A12/294, B13/325, C14/357. C top-first and B vertical routes
remain genuinely BLOCKED. A rim-after-top trial has2 stages/59 comparisons but does not
recover lock access. All six closed-top corridors BLOCK. The late-bottom and closed-wall
rib controls also block. External holding, physical bending and a real lock remain OPEN.

## Decision and downstream limits

A preserves the simplest skins and fewest seams/pieces. B offers step registration with
an assembly-direction cost. C offers skin-edge angular registration at cost of more pieces,
interrupted contact and explicit radial-construction change. Recommend continued A study,
**AWAITING_LEAD_SELECTION**, not manufacturing. Full tableG2b awaits P06R and real P08;
B01–B13/officialIF states remain preserved. G3/G4 and cutting NOT_APPROVED.
