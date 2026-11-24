# MEB-037 execution record

2026-11-24 · Python 3.12.14 · CadQuery 2.7.0 · OCP 7.8.1.1.post1. See ../requirements.txt for the numerical and rendering dependencies used to reproduce the output.

| Attempt | Observed outcome | Repair or verification |
|---|---|---|
| First assembly reconstruction | 20 solids, 190 pair computations, seven intersections. Floor/end L/R 144 mm³ each, pin R/end R 3.86 mm³, skin/pins 36.19 and 39.89 mm³, skin/ends 120.95 mm³ each. | Compared four floor orientations, matched the right pin to the left using the source reflection and compared both skin orientations. |
| Geometry repair and retest | Five intersections resolved. Two skin/end intersections approximately 6.93 mm³ each remained. | Confirmed in an empty output directory with 20 solids, 190 pair computations and seven body/lid angular samples. The two intersections are exactly located in MEB037_REFERENCE_QA.json. |
| First interface audit | Fixture failed with AttributeError while checking polygon pairs. | Used sheet values and reran all ten negative controls successfully. Verified that lowering the actual skin by 5 mm triggers the lid/body detector. |
| First and second visualization runs | Matplotlib rejected singular color keywords and then an empty edge-color array with shading. | Used face colors and default edges. All three views rendered. |
| Final export and paths | STEP 20/20 valid solids with maximum volume difference 2.33×10⁻⁸ mm³. Three GLBs each had 20/20 named part nodes. Six isolated insertion sweeps returned zero positive intersections. | Rendered PNGs from the GLBs and checked the 110° image. Verified an unobstructed 316 × 69 × 64.8 mm box inside the nominal body. |

One geometry correction cycle. Two rendering fixes and one interface-audit fixture fix are counted separately. The pre-fix import warning about an unwritable ezdxf cache was non-fatal. Build commands are in ../README_HE.md.

The reconstruction includes 190 unique static pair cases, seven discrete motion states, six isolated insertion cases, ten negative controls, four export checks, one internal prism check, three R6 pattern evaluations and six orientation trials. Angular samples and isolated translations give the stated scoped results. Continuous motion, full assembly order, combined tab joinery, new nesting, and physical tests remain open under the acceptance matrix. Independent review remains pending.
