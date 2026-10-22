# CTB-015 focused B1 — independent evidence review

**Reviewer:** `/root/ctb010_file_qa`, separate from the implementer.
**Branch/base:** `codex/ctb-015-b1` /
`3ca8e38cc084e82f237b427903249282ebe4d1e2`, CTB-015 source PR60.
**Disposition:** **CONFIRM REVISE / CURRENT_VERTICAL_ROUTE_NO_GO / STOP_AFTER_B1**.
The final nominal seam correction passes the stated tolerance; the inherited
vertical insertion still fails. This is acceptance of bounded failure evidence,
not design approval, a full six-degree-of-freedom impossibility claim or physical
release. No design-approval score is assigned.

## Independent checks actually performed

I read `NEXT_CODEX_B1.md`, the new verifier and recorded evidence. I then used
separate read-only code without importing `verify_b1.py`: minidom parsed original
SVG contours, ezdxf1.4.4 independently imported the two corrected DXFs, and
Shapely2.1.2 evaluated complete flat profiles under the prescribed wrap. I also
re-imported the diagnostic STEP with CadQuery2.7.0 / cadquery-ocp7.8.1.1.post1,
checked source correspondence, and calculated four local intersections only.

| Independent review action | Result |
|---|---|
| Two standard corrected DXF imports | PASS;64 closed loops each, exact numeric SVG agreement |
| DXF audit | 0 errors;1 LAYER-table-head-handle correction notice per document, in memory only |
| Recorded source-file SHA256 inventory | All11 match; no source diff against the base |
| Kerfs and notch lands |63 unchanged holes per half,18 shortened,6mm notch-floor-to-kerf minimum |
| Sharp puzzle dimensions | Neck one-sided limit≈12mm, head14mm, tip6mm; no fillet/strength qualification |
| Local complete final seams |2 re-imported OCC pair checks:0mm³ each |
| Actual R2 route at Z+2mm |2 independent OCC pair checks:≈64mm³ each, therefore FAIL |
| Diagnostic STEP |8 valid solids, correct four-object composition per seam |

The source DXF interoperability failure from CTB-014 is no longer present in
these two corrected files. The two metadata audit notices remain real advisories;
they are not ignored or represented as perfectly clean source metadata. I
verified that audit did not write or alter either source file.

## Mapping, completeness and counterexample

Native coordinates are h=sheet x and s=sheet y, with radius171..175mm,
Z=450+h and theta=phase+(s−0.2)/173, phases15/195 degrees. Shift the other complete
flat profile by `−π·173` to compare each seam in a common angular frame modulo2π.
For both seams I independently confirmed the complete mutual flat intersection
is covered by h0..50,s−10..3. There are no kerf apertures inside those clipped
local joint domains; the rest of the profiles was not silently filled.

Independent complete-flat-profile final overlap gives
**5.682734548951175e−7mm³** after the exact cylindrical area multiplier
`(175²−171²)/(2·173)=4`. This is below the **1e−4mm³** acceptance threshold and is
consistent with the source's approximately7.1e−8mm length-rounding residual.
The two re-imported final BRep intersections are0mm³. This is a tolerance-bounded
nominal result, not a measured physical gap, kerf allowance or snap-fit proof.

I checked the diagnostic fixed/moving BReps against the source domains:
their volumes equal4×native material area within1e−5mm³, and samples along
every boundary edge unwrap onto the correct native boundary within2e−6mm.
This checks the actual cylindrical/helical head edges rather than substituting
a rectangular or chordal profile. The implementer's pcurve construction and
ruled radial-face method are consistent with that exact source map.

The recorded B2 path is R1 first, then R2 lowered from Z+70 to0. The moving R2
piece is the **female at phase15** and the **male at phase195**. After independently
identifying the STEP bodies from phase, height bounds, source shape and volume:

| Seam phase | Final after undoing the +2mm pose | R2 at actual intermediate Z+2mm |
|---:|---:|---:|
|15°|0mm³|**63.99999867359965mm³**|
|195°|0mm³|**63.9999986737739mm³**|

Independent planar pose calculations give approximately63.999998011mm³ each, agreeing
within1e−4mm³. Each positive common has **two disconnected lobes**. The diagnostic
STEP therefore correctly has2 fixed+2 moved+4 common-lobe solids, **8**, not6.
These are local diagnostic solids, not eight additional wooden BOM components.

A real interior-pose collision suffices to reject that prescribed continuous
vertical route; a full swept-shell rerun is unnecessary to demonstrate the
counterexample. No alternate radial, elastic, preclosure or general6DOF route
was supplied or proven. Thus final-state PASS cannot be promoted to assembly GO.

## Accounting, limits and handoff

Primary evidence reconciles **17 unique formal cases:15 PASS,2 FAIL**, with two
negative controls. My targeted source and four local-pair rechecks do not add
extra passing cases to17. I did **not** rerun the17-case verifier, its negative
controls, four skin-band Booleans, complete shell, old global/full-table tests,
B2 or nesting. The four existing skin-band results and their complete constant-
section reconstruction were reviewed as bounded final-fit evidence, not as
insertion-path approval.

The declared history distinguishes one successful development construction
prototype, one formal17-case run and one artifact-only finalization after a
checker falsely expected6 STEP solids instead of8. That is **one checker repair,
zero source repairs**, with no failed CAD construction claimed. I independently
confirmed the eight-solid interpretation; no additional evidence defect was
found. Source geometry and all11 recorded source hashes remain unchanged.
The archived `CTB014-evidence-reference.json` also independently matches the
pinned prior-evidence SHA256
`3fc8ac39c9f045b1ebeb342a5c4b8085a47ba11b20af052d9a260cf9f1461058`;
the verifier can use that exact snapshot without requiring an old branch's Git
object in a fresh checkout. This provenance-only change requires no CAD replay.

Review command: existing ctb-001 Python running the read-only temporary audit
`/tmp/ctb015-independent-b1.py`; its result is in
`/tmp/ctb015-independent-results.json`. Repository reproduction and detailed
primary case records remain in `verify_b1.py` and `evidence.json`.

**Return to ChatGPT lead and STOP B1.** Revise/prove the closing motion or obtain
a reviewed design change if vertical lowering must be retained. Do not silently
change the corrected outlines, add guessed kerf/clearance or begin CTB-016
nesting. Keep LAYER-handle metadata cleanup separate from mechanical geometry.
IF-10/11 assembly feasibility remains unclosed; physical fit/bending/grain/kerf,
glue/fixtures/access and strength/load/stability remain unproved.
**DESIGN_ONLY / NO_CUTTING_APPROVAL / G3_NOT_RUN / G4_BLOCKED.** No self-merge.
