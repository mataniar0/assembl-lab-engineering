# MEB-023 — Co-planar recessed hinge CAD and nesting | DESIGN_ONLY
**2026-10-26 · P1 · ChatGPT direct · LEAN TASK PLANNING v1.1. Issue #95.**

Owner correction to MEB-022: moving LID_END and stationary BODY_END are both nominal 6mm at exactly the same X span. BODY_END gets an open, full-depth circular relief at the hinge lobe, and its fixed outer side stack has no axial air gaps. The OUTER_FASCIA remains fixed and wraps over the closed lid top.

**Stack L:** OUTER_FASCIA X-2..2, fixed hidden backing X2..6, BODY_END X6..12, moving LID_END X6..12. **Stack R:** BODY_END and LID_END X324..330, backing X330..334, OUTER_FASCIA X334..338. Facing fixed layers touch exactly in CAD; they depend on good adhesives mechanically. No body pivot bore. Full-depth BODY_END notch Y75 Z75 radius11.2mm; moving boss nominal radius10.5mm yields minimum0.6996mm in-plane clearance across441 sample poses0..110deg. Previous uncut body end has about58.146mm2 2D overlap at0deg, which verifies the notch is essential.

Updated roof glue wings to X6..14 / X322..330, saddle X12..18 / X318..324, rail half laps and flat plywood shoulder pins shifted. Nominal external length340mm (owner review required; previous354mm), nominal usable inner X312mm (minimum310). Crown fixed fascia reveal remains2.5mm, owner aesthetic review still required.

**Computational evidence:**24/24 CadQuery solids, STEP roundtrips 24 each at0/110deg, GLB 24 watertight parts each, CadQuery BRep collision check at0,30,55,80,110deg zero penetrating pairs, 441/441 2.5D sampled rotation angles clear, targeted same-author recess QA27/27 and separately implemented same-author DXF/stock QA87/87 PASS, with unnotched-body negative control correctly failing. All checks rerun after extracting ZIP in fresh directory. No qualified independent QA. No proof of real material strengths, slot bending or smoothness between angular samples.

**Nesting:** one 440W×800H nominal6mm sheet (19 parts,24.82% net area), one same stock nominal4mm (5 parts,18.02% area), exact-contour min spacing4mm, 188 theoretical zero-width kerf centerlines. All source-derived SVG/DXF cut shapes, STEP,GLB, PNG CAD renders/diagrams included with the user-conversation source package.

**Archive name and custody:** MEB023_RECESSED_COPLANAR_LID_END_CAD_NEST_DESIGN_ONLY.zip SHA256 344dad1b9b22726beba0fb5f85577e11c0bf1a0dd2ad14f1acd1963296c388fc,153 entries (~5.23MB), available as user conversation download, **NOT committed to repository**. This branch provides traceability; full source code review requires the archive.

**CRITICAL DESIGN REMAINING:** moving LID_END touches the fixed backing axially at X6 or X330 in ideal CAD (no interlayer air gap); the 2.5D circular clearance is **not** physical axial running clearance. Need a positive axial clearance/tolerance solution, face strength, assembly sequence and pin restraint. 4mm birch kerfed bend and bond strength, measured plywood/Kerf, independent QA, G3/G4 all NOT_RUN / NOT_APPROVED. No merge or release for laser cutting.
