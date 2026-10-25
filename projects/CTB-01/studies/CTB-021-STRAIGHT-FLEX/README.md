# CTB-021 — rim-only straight-seam trial, physical fit HOLD

Only P07R1 & P07R2 birch 4mm parts are changed. CTB-017 P07T/P07B 6mm skins, legs, anchors, all other parts were NOT edited.

The two neck/puzzle ends are deleted and replaced with straight ends at y=0.2 and y=543.695529. Outer width50mm. All six notches at centers 45,135,225,315,405,495mm on BOTH edges remain EXACTLY in original positions, 12mm opening width and6mm notch depth. SVG/DXF has 135 rows of open alternating A/B kerfs from y4.2 to540.2 every 4mm, shortening lines rather than skipping rows in the six notch bands. Each rim has 202 open line cuts. Nest: 4mm 440×800, only two rim parts; no sheet perimeter in cutter geometry.

**WARNING:** User has physically reported CTB-019 rim overlap. Removing the 8mm puzzle protrusions from source contour does NOT change its flat body length (543.495529mm each, total nominal midline C=1086.991058mm at R173); therefore it does NOT by itself solve circumference mismatch. Skin base circle R171 has circumference1074.424688mm; rim theoretical outside R175 ->1099.557429mm. No physical overlap measurement O exists. Keep status DESIGN_ONLY, NOT READY FOR FULL CUT.

Corrective procedure: dry fit the two rim strips to existing skin tabs, engage each notch if possible, and mark both seams. If all tabs fit and overlap O uniform, estimate candidate corrected half length 543.495529−O/2 and rephase notches to measured effective radius. Mere end-only trimming cannot fix misaligned tabs. Separate tested internal splice can be added after alignment; do not glue until verified. No 6mm part should change.

Geometric QA: both updated parts have exact old notch edges, closed new straight contour, 135 rows/202 lines, 3 SVG↔DXF vector matching targets; local zip archive separately validated with independent ezdxf. Physical bend, load, seam strength, insertion sweep and measured perimeter NOT_RUN.
