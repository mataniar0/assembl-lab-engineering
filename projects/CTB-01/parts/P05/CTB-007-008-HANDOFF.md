# CTB-005 → CTB-007 / CTB-008 interface handoff v1 — DESIGN_ONLY

All IF-06, IF-07, IF-08, IF-12 and B01/B02/B06/B10/B11 dependencies retain their official
state. No actual skin, rim, top lock, adhesive, fixture or strength is supplied by P05 CAD.
Selected disks A_RIM_OPEN / NO_HOLE are untouched. A actual P05 uses both original disks;
B requires both P04-v2 proposals; C's retention requires only the lower P04-v2 proposal.
See proposals/B,C/CHANGE-PROPOSAL.md. Neither CR is selected or approved by this handoff.

Shared: six identical6mm ribs per concept at0/60/120/180/240/300, Z456..494 (38), outerr169.
A innerr81; B/C railinnerr82 (explicit1mm setback inside the provisional r81..169 envelope).
DisksL456..462/U480..486; freegap18, pitch24; uppergap8 toskin494; tonguesend488, only2mm
aboveU. All proposals keep50mm outer top budget450..500 and NO_HOLE. Physical G3/G4 NOT_RUN.

## Skin connection alternatives for CTB-007

**OPTION-1 / flat boundary bond:** retain current38mm rib height. Actual straight contact
intervals atZ456/494 and their interval-length×6 boundary areas are in P05-dimensions.json.
They are candidate glue lands, not measured adhesive joints. A's nominal surface area is
516mm²/skin; B/C differ due split/rounded ends. Nominal material has no finite overlap with
skins and no glue solid; actual bonded area is unknown (not a tested capacity). Specify
plywood edge preparation, adhesive gap/toughness, cure, clamping/fixtures, grain and coupons.
Skins must actually transfer shear/torsion, otherwise disk/web contacts do not establish a
complete structural load path. Radial insertion and CTB-008 work precede closing the top.

**OPTION-2 / versioned tab-and-slot skin pair:** CTB-007 could propose integral P05 tabs into
matched P07B/T slots (no extra rib/hardware count), with explicit P05-v2/skin-v2 geometry.
For example1mm tab projection at each face would require rib envelope455..495 instead of
current456..494; this is a future coordinated interface change, not current accepted CAD.
It can stay within external450..500 while changing the38mm rib budget and insertion path.
Blindly adding such tabs would collide with the current uncut skin envelope. Rebuild all
paths/skin cuts and review physical fit before adopting. No tabs or skin edits are made here.

## Rim/inner support alternatives for CTB-007

**OPTION-1 / preserve air gap:** keep ribouterr169 and riminsideR171. Nominal radial gap2mm;
finite tangentialhalfwidth3 gives min curved gap171−sqrt(169²+3²)=1.973375mm. This is AIR,
not glue. Let designed skin joints carry web loads and let the kerfed wall connect to skin
edges only; wall bending/edge support must be proven independently (B08/B09). No extra rail
or hidden seventh rib is implied by this option.

**OPTION-2 / versioned near-rim tip:** propose a future P05 outer extension to
r=sqrt((171−0.2)²−3²)=170.77365mm, leaving≥0.2mm nominal curved clearance at both t=±3 edges.
This needs a P05-v2/rim contract and actual gap/kerf/adhesive/bend tests, not a2mm glue bridge.
A shaped support strip/ring would alternatively add real BOM parts; none is silently included
in the current27-body model. CTB-007 must name/count any support parts before claiming fit.
Keep all radial rib installation before wall closure; closedwall blocks the actual sweep.

## Retention / load path / locking

A's reversible radial route is free outward: no positive radial restraint. Its finite upper
relief has R0.8, inner r83.2 and Z479.6..486.4; cap envelope7.6 (actual inner-edge span6.6 afterR1), lower envelope23.6 (edge22.6),
and backbone85.8 are geometric,
not certified stress limits. Proposed glue zones along both disk sidewalls have0.2mm/side
air gap; their broadside areas are reservations, never demonstrated bonded/loaded area.
B's full-height6mm rail and10mm bridge use closed P04-v2 slots in both disks. C's6mm lower
rail is caught in proposed lower slots and its upper step meets the ORIGINAL upper disk's
inner backstop: actual flatstop r82.4..82.8 at479.6 is only0.4×6=2.4mm² geometric face.
That small stop is a stress concern; no load rating. Specified out/in/up/down translations
block only with disks fixed atZ; no6DOF capture or positive locking of the disks themselves.

Loads could travel skin→rib→two disk sidewalls/rail/step→tongues→selected Y/base, with lateral
and torsional transfer through spaced skins and six radial planes. Every glue/wood-bearing
link requires design and test; vertical boundary contact alone cannot carry tension/shear.
Do not infer stiffness from zero CAD overlap. Do not assume kerfed wall structural continuity.

Six hypotheticalØ4 tool cylinders reach tongue centers fromZ520 down to488.5 with all27
parts present, top open. Closed top skin blocks them. This does not specify a retainer, hand,
toolforce or cure fixture. CTB-008 must design real anti-pull-out locks for tongues ending488,
prove access before top closure and coordinate disk Z restraint. No access through a solid
top is assumed; no center hole or positive top lock is added. Future lock obstruction and
late-wall/top assembly are explicit negative controls in each connections-and-paths.json.
