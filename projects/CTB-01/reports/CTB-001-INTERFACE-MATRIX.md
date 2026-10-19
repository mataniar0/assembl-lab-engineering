# CTB-001 interface/dependency matrix — before modelling

Issue #3 explicitly authorizes P01 concepts only. CTB-000 v0.2 is unchanged.
All outputs DESIGN_ONLY; no G1 selection or dependent component design is authorized.

| IF | Inputs / dependencies | P01 evidence in this task | Status / blockers |
|---|---|---|---|
| IF-01 | Frozen: 6 mm cheeks, 15 mm gap, 4 spacers/leg. Provisional z35/90/245/390; CTB-002 | Six instances, nominal spacing; 16 mm high uncut spacer reservation bands, minimum 24 mm body section screening | PROVISIONAL / B03 B05 B10; no mortises or spacer design |
| IF-02 | Candidate Y z410, r94 vs cheek r90; arm width14.6 and hole20.4×6.2; CTB-003 | Preserve upper r35..90 envelope; show Y reservation and 4 mm overhang; two remedies below | BLOCKED / B04 B10; no final Y cutout |
| IF-03 | Candidate tongue r45..69 z450..488; bottom skin z450..456, nominal slot r44.8..69.2 width6.2; CTB-007 | Dimension tongue and nominal section overlap; compute 0.2 mm radial/0.1 mm tangential per-side nominal allowances only | PROVISIONAL / B03 B10; material/kerf unmeasured |
| IF-04 | Lower disc z456..462 Ø190 candidate; CTB-004 | Tongue spans disc plane; radial extent inside r95 envelope | PROVISIONAL; disc slot topology, fit and insertion unknown; B01 B02 B10 |
| IF-05 | Upper disc z480..486 Ø190 candidate; tongue ends488, top skin begins494 | Tongue spans disc plane; 2 mm above disc and 6 mm below top skin | PROVISIONAL; positive retention and access remain undefined; B01 B02 B10 |
| IF-09 | Ring z/geometry/engagement OPEN; CTB-006, CTB-002 | Uncut study band z225..265, overlapping spacer z245 reservation explicitly shown | BLOCKED / B05; no joint, cut or dependent ring design |
| IF-14 | Provisional foot center r240; ground z0, unknown load cases | Flat landing; six projected contacts and support polygon screening; no load capacity | PENDING_PHYSICAL / B07 B11; floor compliance and tipping unknown |

## B04 remedies for review (neither applied)

1. Extend the upper cheek envelope from r90 to at least r98 near z410, preserving
   4 mm nominal end land beyond the r94 Y arm. Adds material but affects silhouette,
   engagement and adjacent spacer. Requires CTB-003 coordination, updated provisional
   interface and CAD/physical checks; 4 mm is a study land, not an approved minimum.
2. Shorten/rework the Y arm to r86 or less inside the existing r90 cheek envelope,
   reserving the same study end land. Preserves P01 silhouette but reduces engagement
   length and may affect tab placement/load path. Requires CTB-003 redesign and review.

A nominal 14.6 mm arm inside a 15 mm gap does not prove a joint. No remedy is silently
applied and IF-02 remains BLOCKED. The 20.4×6.2 reference mortise is drawn as an
annotation-only reservation at r58..78.4/z406.9..413.1; its radial center is a P01 study
assumption, not a confirmed Y-tab position. No cut geometry is created there.

## Locking and assembly reservations

B01 / IF-12 remains OPEN: tongue ends at z488; z486..494 around it is a reservation
for CTB-004/008 retention/access study, not a certified lock or collision-free volume.
B02 / IF-13 remains unresolved: no sequence for prebuilt twin legs through both discs
and Y is proven. Three-leg preview intentionally omits those components; absence
of collisions among bare cheeks cannot establish assembly feasibility.

B03 remains open until a candidate is selected, reviewed, approved and coordinated.
B05 spacer/ring overlap requires CTB-002/006 agreement before any holes are cut.
B07 support radius and load cases remain unknown; the r240 center triangle inradius
is only120 mm, inside tabletop radius175. B10 requires measured plywood and kerf
coupons. No approved parameter, original IF status or open-issue record is modified.
