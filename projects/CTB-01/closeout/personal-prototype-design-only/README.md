# CTB-010 — experimental personal prototype digital package

**DESIGN_ONLY / PERSONAL_PROTOTYPE / FIT_STRENGTH_UNVERIFIED. G3_NOT_PERFORMED_OWNER_DEFERRED / G4_BLOCKED.**
Stage3/4 only, branch codex/ctb-010-final-digital-closeout; baseline 9caa69445d3f9816bdf23a934d8824b86e1ad913.
Geometry evidence inherited from merged PR49 and secondary PR53 (lead QA96/100),
not rerun. Separate final file review: QA/INDEPENDENT_QA.md. ChatGPT lead review
and final digital-closeout decision remain pending.
Personal noncommercial one-off; no safe-use/load rating or cutting authorization.

32 wood instances, 12 assembly roles, 11 unique cut masters. P01 master repeated6;
P07R_MASTER repeated2 maps to distinct P07R1/P07R2 assembly bodies. P04L/U remain
different contours. P08 keys0. CAD_sources/authoritative holds byte-identical
native input SVGs; native-profiles.json records exact numeric contour vertices.
SVG/ and DXF/ contain each unique master once; nesting/ contains numbered sheets
and labels matching BOM/instances.csv. Only CUT_OUTER and CUT_INNER are cut data;
ANNOTATION_NOT_CUT and REFERENCE_SHEET_NOT_CUT are display-only. No engraving.

Units mm, 1:1, portrait bed WIDTH440 × HEIGHT800. Nominal material groups6/4mm
are separate. Planning margin10mm and part gap5mm are provisional, unmeasured
allowances, NOT calibrated cutting tolerances. No common-line cutting or use
of aperture waste. Packing uses conservative bounding envelopes; no optimum
sheet-count claim. Rotation0 only, no mirror; source sheet axes preserved.
Grain/flex axis and actual stock thickness UNMEASURED, physical orientation
must be checked separately; this is no approved grain/bending recipe.

Machine kerf UNKNOWN, compensation0 (uncompensated experimental contours).
Rim retains actual63 closed 0.8mm nominal kerf openings per segment, pitch8mm;
173mm neutral-axis hypothesis and developed length are unvalidated physically.
No cut compensation, sanding allowance or stretch correction was invented.
No physical fit/bend, glue/cure/fixture/access, strength/load/stability test ran.

See manifest/CUT_PARTS_MANIFEST.json for all placements, native source digests,
stock metrics, layers and gates; BOM/ for quantities; assembly/ for numbered
ring+31 movement documentation and a byte-identical verified GLB preview;
QA/ for separate-parser DXF/SVG checks and archived geometry evidence.

Reproduce exports (from the repository baseline, no CAD kernel runs):
```sh
XDG_CACHE_HOME=/tmp/ctb-cache /workspace/.venvs/ctb-001/bin/python projects/CTB-01/closeout/personal-prototype-design-only/CAD_sources/build_package.py
XDG_CACHE_HOME=/tmp/ctb-cache /workspace/.venvs/ctb-001/bin/python projects/CTB-01/closeout/personal-prototype-design-only/QA/verify_package.py
```
Seal only after QA PASS using build_package.py --seal. The sibling ZIP includes
CAD_sources, DXF, SVG, nesting, BOM, assembly, QA, manifest and this README;
manifest/SHA256SUMS.json seals every file except itself. The sibling .sha256
file seals the ZIP (no circular self-hash). ZIP entry timestamps are fixed.
No G2b self-approval, no self-merge; stop for ChatGPT lead review.
