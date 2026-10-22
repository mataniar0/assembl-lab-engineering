# CTB-015 next focused Codex B1 — necessary stop point
**Priority P1; executor:** Codex (independent `ezdxf` + CAD-kernel) after ChatGPT planar correction. Do not merge or expand to full-table regression.
Inputs:
- `projects/CTB-01/studies/CTB-015-CHATGPT/P07R1_LENGTH_CORRECTED_DESIGN_ONLY.{svg,dxf}`
- `projects/CTB-01/studies/CTB-015-CHATGPT/P07R2_LENGTH_CORRECTED_DESIGN_ONLY.{svg,dxf}`
- CTB-012 tabbed P07T/P07B SVGs and CTB-014 B1 evidence, original material-axis mapping.
Steps:
1. Validate new DXF standard parsing through ezdxf, independent coordinate compare with corresponding SVG.
2. Validate polygon topology and minimum lands at joint, including neck/head curvature and notch transitions.
3. Use OCC nominal cylindrical wrap R173 to calculate BOTH final curved seam overlap volumes and rim-to-skin final 3D interferences. Source has deliberately zero kerf compensation and no physical clearance allowances.
4. Test actual assembly insertion path if final state is collision-free; report GO/REVISE/NO-GO. If overlaps persist, provide smallest geometry correction recommendation (not a silent source edit) and stop.
5. State tests/failures/corrections and independent review. No nesting, no production cutting authorization, no old global reruns.

Completion criterion: If not proven no collision and feasible insertion, STOP; no CTB-016 nesting.
