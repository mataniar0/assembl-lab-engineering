# CTB-012 engineering decisions (DESIGN_ONLY)

Priority P1 — structural joint interface issue. Executors: ChatGPT can inspect source, make parametric concept geometry, local planar QA, document impacts; Codex only for minimal independent CAD-kernel solid validation and limited fit study; physical qualified operator for real kerf/bend/glue.

1. Preserve frozen tabletop outer diameter350mm and total thickness50mm; skin original base radius171mm and rim outer radius175mm. Tabs protrude only into existing rim wall thickness in local slots; no added thickness.
2. Avoid extending rim teeth above z500 or below z450: doing so would alter the table envelope. Reverse joint polarity: radial tongues on 6mm disks, matching open notches in 4mm rim long edges. This is a geometrical finger-style register, not a self-locking anti-pullout joint.
3. Six paired upper/lower notch stations per half-rim, mirrored by exact angular skin stations using neutral radius173mm and phase 15/195deg from CTB-010 conceptual assembly. Alignment registration must be independently verified against the actual 3D source frame; NOT independently proved.
4. Initial R1 rim keeps all 63 original 0.8mm x34mm kerf slots per half and leaves only 2mm land from notch floor to neighboring kerf slot. Propose R2 reinforcement: shorten 18 kerf windows near notches per half, preserve their pitch/Y positions, get 6mm nominal local land. R2 may fold differently; no bend safety claim.
5. Base 6mm P07B tongue holes unchanged, zero kerf compensation, source P07R segment end length and seam unchanged. Avoid altering existing P01–P06.
6. Do not update CTB-011 nesting until model-independent CAD QA and nominal insertion review; original 342mm-disc envelope is no longer representative where tabs extend to349.6mm diameter.

Interfaces: IF-10 directly changed, IF-11 splice remains OPEN, IF-07/08/12 load transfer/retention unqualified. Revalidate P07T/P07B vs P05/P04 and shell after proposed joint contact; not a G2b carryover.

Variant statuses: SKIN_TAB = study candidate; RIM_NOTCHED = reference, 2mm land risk; RIM_REINFORCED = geometrically improved study, bending UNVERIFIED. No production approval.
