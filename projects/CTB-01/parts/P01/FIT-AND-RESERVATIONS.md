# P01 fit / slot worksheet — PROVISIONAL

No dependent slots are cut. Values below are baseline candidates, not measured fits.
`actual_stock_thickness_mm`, `measured_kerf_mm`, `desired_fit_allowance_mm` are all
**unknown**, to be measured using supervised material/machine coupons. No default
value is substituted for them.

| Reference | Nominal study | Evidence and prerequisite |
|---|---|---|
| Bottom-skin slot radial | [44.8,69.2] vs tongue [45,69]: 0.2 mm each side | Source candidate only; CTB-007 and coupons pending |
| Bottom-skin slot tangential | 6.2 vs nominal cheek6: 0.1 mm each side | Source candidate only; no approved clearance |
| Cheek gap / Y arm | 15 vs14.6: 0.2 mm each side | Nominal only; not proof of side-tab joint or Y fit |
| Y cheek mortise | 20.4×6.2 at study r58..78.4,z406.9..413.1 | Annotation only, CTB-003 must resolve r94/r90 mismatch |
| Disc slots / retention | Unknown geometry and fit | CTB-004/008 must define topology and locking |
| Spacer / ring slots | Unknown geometry and fit | CTB-002/006 agreement required; ring z245 study overlaps spacer |

At fixed cheek center offsets ±10.5, actual inner gap is `21 - measured_thickness`,
not automatically15. Actual overall section is `21 + measured_thickness`, not
necessarily27. If cut paths are followed on the beam centerline without CAM compensation,
a straight internal opening finishes approximately `drawn_width + measured_kerf`,
and an external tab `drawn_width - measured_kerf`. These are calibration formulas,
not prescribed fit values. CAM compensation would change that bookkeeping and must
not be applied twice. Coupon results and grain/material behavior govern final values.

All profile exports are uncompensated design contours. R1 tip, R2 shoulder/root,
R4 foot easings and geometric R6 facets are ideal planar radii represented with ≤0.02 mm
chord tolerance. They require machine/process review; they are not certified tool or
edge-safety radii. Sharp 6 mm thickness edges still need a separately defined finish.
