# CTB-014 B1 — independent evidence review

**Reviewer:** `/root/ctb010_file_qa`, separate from the implementer.
**Branch/base:** `codex/ctb-014-puzzle-b1` /
`72595e4cd7164efa44b4ebda8bf48bf7b2c51c11` (CTB-013 PR57, stacked on CTB-012
PR56; both proposed sources remain unmerged/under review).
**Disposition:** **CONFIRM NO-GO_CURRENT_NOMINAL_GEOMETRY / STOP_AFTER_B1**.
This accepts the bounded failure evidence, not the design or a physical release.
No design-approval score is assigned to a demonstrably blocked nominal endpoint.

## Independent verification actually performed

I reviewed the source-defined frame in the CTB-012 README: native rim x=height,
y=developed length, radial interval171..175mm, Z=450+h and
theta=phase+(s−0.2)/173, phases15/195 degrees. This is a nominal ideal-cylinder
map; no calibrated kerf, elastic bending or material-fit assumption is justified.
At each seam, shifting the other flat profile by `−π·173` gives the same angular
location modulo2π under that prescribed map.

I used a separate read-only program, without importing `verify_b1.py`, to parse
original SVGs with minidom, inspect plain DXF tag pairs and reconstruct the two
local collision witnesses. Unlike the implementer's planar arc-wire extrusion,
my OpenCASCADE witnesses subtract an inner full cylinder from an outer cylinder
sector, then rotate to the appropriate source phase. Environment: CadQuery2.7.0,
cadquery-ocp7.8.1.1.post1, ezdxf1.4.4, Shapely2.1.2; existing ctb-001 Python.

| Independent review action | Number / result |
|---|---|
| Source-file digests against recorded originals | 24 match |
| Actual standard DXF re-imports | 8 fail with missing `AcDbPolyline`, as reported |
| Original raw DXF/SVG numeric-contour comparisons | 8 match; no repair/recovery performed |
| Original-profile containment of the male/female witness subsets | 2 seam pairs proved |
| Independent local OCC Boolean common | 2 positive-volume intersections |
| Diagnostic STEP re-import | 6 valid subset/common solids; volumes and intersection bounds match |
| Original parts/specification/assembly diff against the base | Empty |

For both seams I verified that the source material contains the complete
rectangles h18.3..18.4, s−4.83999..−3.34001 (male) and
h18.3..18.4, s−3.51999..−2.20001 (wrapped female), including their boundaries.
Their mapped material therefore proves a lower bound on real nominal overlap;
they are not guessed shell envelopes or oversized collision probes.

Independent Boolean common volumes:

- Phase15: **0.07199200000001255mm³**.
- Phase195: **0.07199199999999242mm³**.

The corresponding analytic subset is0.07199199999999847mm³, agreeing far below
the study's1e-4mm³ threshold. The cylindrical map gives exactly4×flat material
area because `(175²−171²)/(2·173)=4`. Separately, my whole flat joint intersection
is0.6952728321449737mm², giving the reported **2.781091328579895mm³** ideal-wrap
overlap. That latter value is analytic, **not** a whole-shell OCC Boolean result.

Half-circumference is543.4955290710342mm; source body length is543.095529mm,
leaving a **0.40000007103424196mm registration shortfall per seam**. The failure
is thus material in the specified final frame, not just a drawing coincidence.
No collision-free rigid assembly path can terminate at that overlapping state.
This does not prove impossibility after a changed registration/design or with
unmodelled material deformation; those possibilities are outside this B1.

## Review boundaries and test accounting

The primary record's29 unique cases reconcile exactly: **19 PASS,10 FAIL**,
comprising8 actual importer failures and2 nominal seam collisions. My targeted
rechecks do not become extra passing primary cases, and I did **not** rerun the
29-case suite, CTB-012 generator, B2, old regressions, whole-shell construction,
insertion sweeps or nesting.

I reviewed the four recorded complete skin-Z-band intersections and their
constant-section reconstruction method; I did not rerun those four Booleans.
Their approximately2.47e-9mm³ results establish only nominal final-band fit at
P07B/P07T, not insertion paths. Existing kernel negative controls were reviewed
in the source/evidence and are not represented as independently rerun controls.

Neck wording must remain geometric: the sharp polygon has a **one-sided12mm
limit** at the inward endpoints19..31 at s=−1.8; the exact shoulder section at
that level spans16mm. Head14mm at s=−4 and tip6mm at s=−7.8 agree with the source.
There is no specified fillet or strength result. The recorded2mm reference
versus6mm reinforced notch-to-kerf lands and63 slots/18 locally shortened slots
are geometric evidence, not qualification of neck strength or bending stiffness.

Three implementer attempts are disclosed: the initial genuine DXF import abort,
the regenerated-DXF numeric-text comparison false failure, and the completed
diagnostic run. One checker repair and one raw-tag diagnostic adaptation are
distinct from **zero source-CAD repairs**. Recovering numeric tags does not turn
the eight DXF interoperability failures into passes. I found no additional
critical error in the bounded NO-GO reasoning.

The read-only local audit command used
`/workspace/.venvs/ctb-001/bin/python /tmp/ctb014-independent-b1.py`; the two
collision Booleans and STEP re-import were bounded reviewer checks only.
Source hashes and the STEP hash were checked against `evidence.json`.

**Handoff:** stop at B1 and return the two independent blockers to ChatGPT lead:
source DXF interoperability and positive nominal seam material overlap. Do not
silently fix source dimensions, seam registration, kerf or vector files, and do
not start B2/nesting/full-shell development. IF-10/11 feasibility remains blocked;
IF-07/08/12 and physical fit/bending/glue/fixture/load/stability remain open.
**DESIGN_ONLY / NO_CUTTING_APPROVAL / G3_NOT_RUN / G4_BLOCKED.** No self-merge.

## Packaging-only follow-up

The repository whitespace check subsequently flagged OCCT's generated STEP
line-end blanks. The recorded one repository-format failure/one artifact-format
repair is separate from the29 design cases and does not repair the blocked
design. I reviewed the deterministic generated-artifact trim and its recorded
unchanged-token/quoted-string proof, independently verified the current STEP
digest and absence of end-of-line blanks, and re-imported that STEP again.
All6 solids are valid and their six volumes are **exactly equal** to my prior
pre-trim re-import values. All24 original source hashes and29-case19PASS/10FAIL
accounting remain unchanged. No full-suite, seam Boolean, insertion sweep or
source-vector rerun/edit was needed. The truthful **NO-GO / STOP_AFTER_B1**
recommendation remains unchanged.
