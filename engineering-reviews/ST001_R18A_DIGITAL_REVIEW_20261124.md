# ST-001 R18-A — digital review

Issue #122 | PARTIAL / DESIGN_ONLY / NO_CUT / NO_OCCUPANT_USE

R17 handoff and R16 GLB reopened. One local mesh correction cycle: 16 wall meshes represented as 32 separate nominal 4 mm layers, 8 diaphragms reduced to nominal 4 mm, four additional diaphragm display placeholders interpolated, cap layers normalized to 4 mm. This is a visual mesh transformation, not a complete parametric solid CAD source or verified joint geometry.

GLB readback: 88/88 mesh-width screens pass (0.01 mm numerical tolerance, convex-hull minimum width); 88/88 meshes watertight. 52/60 components, 88/104 layers represented; 16 F01 layers undefined. Height 400 mm; horizontal bounds approx. 421.83 x 421.83 mm. 32 wall layers and 4 lower cap layers have lower bound Z=0. Nominal 50x50 leg cross section not reverified. No X, top plate, or seat.

All 16 adjacent upper/lower rail-to-leg group pairs remain separated according to convex projection screens. No complete collision audit, assembly path, lock retention, or structural verification performed. Existing visual finger geometry is not verified mating geometry. No STEP or production profiles/nesting.

G0 PARTIAL; G1 PARTIAL; G2a BLOCKED; G2b NOT_RUN; G3 NOT_RUN; G4 BLOCKED. Independent QA NOT_RUN. R18-A acceptance NOT MET. Local digital review package (not uploaded to repo): assembled/exploded GLB, preview, CSV layer/interface screens, results JSON, visual transformation script and README. No manufacturing release.
