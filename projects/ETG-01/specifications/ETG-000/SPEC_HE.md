# ETG-000 v0.3 — H1 glued-pivot G0 ICD / PRE_NESTING_DESIGN_ONLY

**Issue:** #18 · **Owner decisions:** D09 H1 hinge, D11 permanent adhesive (replaces P12 mechanical clip), D12 four rounded corners · **branch evidence:** Draft PR #71 · **stage:** G0_DRAFT / DESIGN_ONLY (NO production release).

## Frozen external requirements / open dimensions
Body 260×160×150mm nominal; birch 6mm nominal; H800×W440mm portrait laser sheet X0..440, Y0..800; four rounded laminated corners; integrated recessed wood H1, opening 0–120°. Actual sheet caliper and kerf, adhesive shear/peel and wear, rounded/recess appearance, complete assembly G3 and independent QA remain OPEN.

## Source authority
C11 newly reconstructed editable CAD source is delivered in the user's ChatGPT ZIP `ETG_01_C11_PRE_NESTING_DESIGN_ONLY.zip` SHA256 `ee6b1068eca3bb9ba65d0655a20138478a98609e7e16968d4bd4a5dacbfe60e1`, **not stored in GitHub**. Original V7.6 FCIPH source remains unavailable and cannot be treated as validating H1. This G0 file is a configuration record, not independently reviewed CAD.

## Active provisional BOM / IF status
`PARTS.csv` contains 13 historical family IDs (P12 mechanical clip and P13 optional tray are quantity zero). C11 present **102 flat nominal 6mm cut parts:** 5 walls/base P01–P05; P06 48 front corner laminates, 36 rear corner laminates, four rear fixed ears and two keepers (P06 90 total); P07 roof 1, P08 glue webs 2, rotating cheeks P09/P10 1 each; P11 pins 2. No separate P12 retainer, no optional P13 cradle in current CAD.
`interfaces.csv`: 28 traceable IDs, **24 OPEN + 4 SUPERSEDED** (IF13, IF14, IF27, IF28 cap interfaces retired). IF11/12 now require adhesive pin↔rotating cheek while IF25/26 require **free rotation** through P06 fixed bearing. IF01–08 represent glued structural contacts, not verified strength.

## What is evidenced and NOT evidenced
C9 12/12 geometric self checks, C10 6/6 flat sheet checks, C11 four rounded corner 6/6 checks; final C11 20/20 verified geometry/export assertions; 102 separate SVG & 102 DXF vectors reimported and source STEP reimported as 102 solids. Finite 0–120° 3D rigid-motion samples only; nominal insertion paths of both wooden pins checked. No assurance that glue stays outside bearings or holds the shaft under load. No real G2b fit with actual etrog/optional cradle. Two rear roof corner cutouts remain open. Physical G3 NOT_RUN; manufacturing nesting G4 NOT_AUTHORIZED; independent QA PENDING.

**Boundary:** Arrived at entrance to trial nesting; sheets/positions/count NOT computed. Any future design-only exploratory nesting must be labeled DESIGN_ONLY, no kerf compensation or released cutting files. Formal G4 requires independent QA and actual G3 material/adhesive/fit trials.