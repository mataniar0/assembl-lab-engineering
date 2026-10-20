# G0 reference reconstruction — unapproved DESIGN_ONLY proposal

Source commit: `ebeefe308efaf80329e16e42a84d51557878fd58` in assembl-lab-site.
The source files are read-only evidence. `measured_profiles.json` is an extracted,
coordinate-parametric **traced reference**, retaining every original contour vertex
and kerf LINE. `reconstruct_reference.py` generates 14 DXF/SVG pairs from that one
model. It is not a fully generative dimensional design kernel: varying thickness,
cavity or curvature does not yet recompute dependent joints. G1 must implement and
validate those relationships before design changes. No unapproved shape change is
hidden in the trace. Round-trip tests compare all 14 exported profiles with the
measured reference, including hole boundaries and kerf coordinates.

## Inferred assembly registration (proposal, not a datum stored in 2D DXF)

Units mm, angles degrees. Proposed right-handed XYZ: X along body length, Y from
front to rear, Z upward; origin at the nominal lower/front/left external body corner.
- FRONT: local(u,v) -> (u,0,v), extrusion Y=0..6.
- REAR: local(u,v) -> (u,71,v), extrusion Y=71..77.
- END_A: local(u,v) -> (0,u,v), extrusion X=0..6.
- END_B: local(u,v) -> (316,u,v), extrusion X=316..322.
- BOTTOM: local(u,v) -> (u,v,0), extrusion Z=0..6.

These placements imply body envelope322×77×71 and cavity
X=6..316,Y=6..71,Z=6..71 ->310×65×65. They are numerical registration proposals,
not a full solid assembly/collision test or measured finished-product dimensions.
Tabs/recesses are checked in their source planes. A complete finished outside
height/width including lid, rings and caps stays OPEN.

## Hinge and lid partial registration

In the END_A local(Y,Z) plane, translate BODY_RING by(-22,+59).
Bore center(14,19) becomes(Y=-8,Z=78). Its extended foot intersects actual end
material over16×12=192mm². This matches the legacy face-area number, not adhesive
capacity. End_B mirrored axial placement, cap/ear stack and clearance remain OPEN.

Lid-end arc spans local chord x19..96 (77mm), chord baseline y4, rise23.4347826087.
Derived circle radius43.3423913043, center(57.5,-15.9076086956), arc length94.7965436.
The rib shares the77mm chord but its own y=0 baseline. Skin unrolled width94.7965436.
Its three12mm tabs correspond to30/50/70% arc positions. Slot angular spans are
12.2mm **at the outer reference radius**, not a12.2mm rectangular tangential hole;
actual slot mid-radius arc length is11.594819mm. Their radial span is4.1mm.
Bent-tab containment and insertion are NOT_RUN; do not infer fit from these numbers.

The proposed center rib occupies longitudinal X=158..164 under skin solid band
X=154..168. Kerf cuts may end on band boundaries; none enters its interior.
Kerf margins12mm are measured from main skin X=6..316, not tab extrema X=0..322.
All three skin slots leave shortest exterior material~0.09974969mm. This is a new
G1 risk (MEB-B12); it is distinct from the5.780053mm inter-hole bridge.

## Sheet frames and unresolved gates

Legacy sheets use X=0..900(long),Y=0..440(short), as measured from extents and audit.
6mm material extents X14..836,Y20..368 ->822×348. This **existing layout** does not
fit800×440 in either90° orientation. This does not prove that a new packing is
impossible. The4mm sheet occupies322×94.7965436 at X10..332,Y10..104.7965436.
Owner confirmed target HEIGHT800 × WIDTH440mm and required opening110deg on2026-10-20. Target sheet frame proposal:X=0..440 across width,Y=0..800 along height; this is newly specified for MEB, not inherited. Margins, kerf, new nesting,110deg swept-motion verification and datum approval remain pending.

G0 reference-evidence work is reviewable; full G0 approval remains BLOCKED.
G1 components are not authorized by this document. G2/G3 NOT_RUN; G4 NOT_APPROVED.
