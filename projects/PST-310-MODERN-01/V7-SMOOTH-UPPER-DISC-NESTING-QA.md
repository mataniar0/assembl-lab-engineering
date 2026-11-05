# PST-310 Modern V7 — smooth upper disk and re-nested flat laser parts

**Date: 2026-11-05 · CAD/NESTING COMPLETE — DESIGN_ONLY (glue-only upper plate not structurally qualified).**

## Owner proposal / design change
Owner observed 12 visible through-slots in the top Ø310 plate in the V6 nesting and asked to remove them and rely on lower-disc joinery. V7 accepts this aesthetic change and goes further, making the full Ø310 upper disk **an unperforated circle**: **no radial slots and no peripheral rim scallops**. Exactly the same outer diameter, total stand height **550mm**, top structural box height **60mm**, 3 modern laminated birch legs, and single-piece lower triangular brace.

## Actual cut source geometry changes vs V6
1. **Top disk** `TOP_DISC_D310_SMOOTH_6MM`: birch6 Ø310, original CAD BREP circle, now **0 internal cut loops**, **0 edge notches** (was12 internal through-slots and12 rim edge notches).
2. **Six radial web pieces** `CORE_RIB_01..06_6MM`: removed 2 upper projecting tabs per rib (12 total), trimmed to underside Z544; **lower tabs and rib shape remain otherwise compatible with the V6 bottom disc**.
3. **Six flexible 4mm rim sectors** `RIM_01..06_BIRCH4_LOWER_ONLY`: removed 2 upper tabs per sector (12 total), body height48mm Z496..544 and **two bottom tabs retained per sector**. 39 kerf rows / 58 single-line slits each, **348 lines total**. Same neutral midline radius R153 and developed sector length **160.221225mm**, 6× total **961.327352mm** as user-approved V6 circumference.
4. **Exact geometry unchanged in nine components**: Ø310 bottom disc, six birch6 laminated leg cheeks, one-piece lower triangular brace, and flat slotted internal center brace. A separate V6→V7 Shapely symmetric-difference audit confirms unchanged source polygons across all nine.
5. **Top-to-web/rim retention becomes glued face-to-face**. Each radial core web and each curved rim strip makes nominal top-face planar contact at Z544, total 12 glue-contact faces totaling about **7117.756mm²**. This number is **not an adhesive bond strength calculation**, particularly for pull-off/peel or wet-potted use.

## Actual CAD checks
- **22/22** OCC solid bodies valid, **22 STEP solids** reimported valid, **22 GLB meshes** reimported.
- All **231 static assembly body pairs**: 158 culled with 3D bounding boxes, **73 actual OCC intersection checks**, zero collisions >0.01mm³.
- Candidate **18-stage assembly**, 311 sampled insertion offsets, **494 OCC Boolean intersections**, zero collisions in sampled rigid configurations. This does not establish continuous 6DOF reachability, joint strength, real plywood/kerf fit or the physical bending behavior.
- Disk upper BREP face circle radius R155; serialized upper cut file has no through-holes or edge slots.

## Recomputed four-board nesting
- **16 birch6 instances** over **3 sheets (440×800mm)**, **6 birch4 rim sectors** on **1 sheet**, still four sheets total.
- Minimum inter-part separations measured: 6mm S01 2.699597mm; 6mm S02 2.699808mm; 6mm S03 9.070358mm; 4mm S01 6.0mm. Stock margin ≥5mm on each sheet. Requested minimum 1mm.
- **22 separate SVG / DXF pairs** and **4 sheet-level SVG/DXF pairs**, checked by an independent XML+ezdxf reopening and coordinate/layer comparison. **59 closed vector contours** + **348 single-line kerf strokes**, exact parts-per-sheet once, no board boundary CUT entities, and full sheet/part geometry parity to ≤0.00006mm.
- The small internal connector still nests in the open scrap hole of the continuous triangle on S03: cut this component and openings **before freeing the outer triangle**.

## Physical release HOLD — new failure mode introduced by the user's requested design change
The upper cover now depends on adhesive and is **NOT mechanically locked** by tabs. The approved V6 nominal circumference, user's bend/load/stability acceptance and V6 geometry reviews do **not** automatically validate glue pull-off or peel resistance of this V7 cover.
- Do not lift or transport the pot stand by gripping the top Ø310 cover until the glue joint is physically tested.
- Verify real 6mm / 4mm ply thickness and machine kerf, dry assembly, moisture barrier and load from the intended pot with wet soil/water. Glue substrate cure/clamping, creep, humidity and shear/peel resistance remain unverified.
- Do not mix V6 cut files of the **top disk, six core ribs or six 4mm sectors** with V7 files. The other nine cut parts remain geometrically identical.
- Status is **DESIGN_ONLY** despite successful CAD/nesting checks. No certified load rating and no full-production cutting approval.

## ChatGPT deliverables not committed here
The following local conversation artifacts were generated and archive CRC tested:
- `PST_310_V7_SMOOTH_TOP_NESTING_SVG_DXF_DESIGN_ONLY.zip`: full 22 individual SVG/DXF part sets, 4 sheet-level SVG/DXF, CAD/assembly/vector QA, BOM and previews.
- `PST_310_V7_CHANGED_PARTS_ONLY_SVG_DXF.zip`: 13 modified parts (top,6 ribs,6 sectors), plus README.
- `PST_310_V7_SMOOTH_TOP_FULL_CAD_NESTING_DESIGN_ONLY.zip`: STEP assembly/top, full GLB, independent parts STEP, Python source, QA/previews and all cutting files.

**This GitHub PR commits this engineering QA/report only.** The STEP/GLB, source scripts, SVG/DXF and ZIP binaries are generated in ChatGPT's runtime and are not present on this GitHub branch. Do not merge this draft as if it were a release of production source geometry.
