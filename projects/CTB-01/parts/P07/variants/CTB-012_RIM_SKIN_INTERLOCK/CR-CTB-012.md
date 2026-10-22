# CR-CTB-012 — revise IF-10 rim-to-skin connection

**Status:** PROPOSED / DESIGN_ONLY — engineering-lead and product-owner review pending.

Problem: CTB-010 P07 rim-to-skin was glue-only, with no tongue/slot mechanical register. The previously delivered G2b geometry and CTB-011 nesting contain no mechanical rim-to-skin finger joints.

Proposal: retain 350mm outer diameter and 50mm slab height; add 12 edge fingers to each 6mm circular skin (0.0..3.8mm radial added relative to R171 base), and 6 upper and 6 lower edge recesses on EACH of the two 4mm rim strips. Reinforced study modifies 18 of 63 bending cuts PER STRIP near recesses, increasing the minimum nominal bridge to 6mm.

Scope: P07T, P07B, P07R1, P07R2 **versioned copies only**, IF-10. New features change real part contours and invalidate existing sheet nesting; re-run interface studies before nesting and G3 tests. No old master overwritten.

Known risks: modified kerf-flex, unmeasured plywood thickness/kerf, joint peel/pullout, rim seam/splice IF-11, P05 rib load path IF-07, upper hub/skin IF-08, tongue retention IF-12. The concept does not mechanically lock against upward removal; adhesive or added retainer remains necessary.

Decision requested at G1/G2: confirm whether the visible intermittent tab ends (nominal 0.2mm recessed from outside face) meet the intended wood surface appearance, confirm 3D kinematics and sleeve bend shape, then perform G3 calibrated coupon tests with qualified supervision before any manufacturing release.
