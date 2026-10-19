# Local base assembly — A working candidate / DESIGN_ONLY

All19 bodies are represented: P03×1,6 identical candidate P01,9 P02 and3 P02B of selected
B geometry. XYZ right-handed, localr outward/t CCW/z up, mm. P03 is horizontal at407..413.
No discs/tabletop/ring/top-lock or invisible retainer exists in this model. Fixtures
support each body; their physical geometry/access and forces are not certified here.

## Y-first route that passed

0. Fixture the single Y at centerZ410 with arms0/120/240. No prior part obstructs its
   initial placement; no installation through a previously built table is claimed.
1. For legL1 (0°), move its first cheek from localt−40 offset to its final center−10.5
   (approach+t). The exact Y aperture passes over its matching side tab.
2. Insert S1/P02B atZ35, S2/P02 at90, S3/P02 at200, S4/P02 at390 along−t, each starting
   40 mm from final. Negative tabs enter the fixed first cheek; hold each in its fixture.
3. Move the second IDENTICAL cheek from+40 offset to center+10.5 along−t, engaging all
   four spacer tabs and the other Y side tab simultaneously.
4. Repeat the same six moves at120° forL2, then240° forL3, with ALL previous bodies kept
   in every collision check. Do not mirror holes or quietly use a different handed cheek.

18 moving stages generate171 moving-sweep/prior-solid checks. Every full translational
sweep is tested, not sparse poses. Cheek tangential sweeps extrude actual mortised r-z
material across the full46 mm interval. Spacer sweeps are planar Minkowski sums of real
contours and40 mm segments, extruded6 in z. Rotation is applied to the whole swept solid.
Each nominal final pair (171 pairs among19) is independently checked. Epsilon1e-6 mm³
is numerical tolerance on flattened geometry, not machine fit precision.

The stage image shows actual XY projections, start/end and arrows; projection overlap
alone is not evidence of3D collision. Actual paths and every pair's volume are in
assembly-proofs.json and per-variant mechanical-dimensions. Transparent assembled/exploded
views and GLB show actual mortised solids. GLTF units METRES; JSON/source mm; highest
cheek z0.488 m =488 mm. Exploded offsets are illustrative, not alternative proven paths.

## Prebuilt modules and central insertion — tested and blocked as applicable

For each joint, three complete6-body modules were tested starting60 mm radially out,
40 mm tangentially offset or80 mm vertically up, translating to final. Each route has
126 sweep/prior-part comparisons across the3 module stages. Internal relative geometry
of each rigid module stays unchanged. A/B closed side holes obstruct all3 tested routes.
C's edge-open channel permits radial approach; its other two tested directions obstruct.

Also test placing a central Y into all THREE fixed modules simultaneously: vertical
80 mm-down approach and global-X60 mm approach, each against all18 fixed bodies. All
three candidates block in those specified approaches. These are explicit obstruction
witnesses for the stated paths, not a proof that every conceivable rigid rotation/path
is impossible. If an early stage blocks, later reported checks are counterfactual
obstructions and are not claimed as an executed feasible sequence.

A/B side tabs give nominal r/z geometric engagement/bearing after intentional clearances;
they do not provide positive outward cheek retention or certify adhesive/clamp/cure.
C is radially removable and has no reverse-slide retainer. The chosen Y-first route
therefore demonstrates local nominal assembly only, not full mechanical locking, G2,
physical fit, loaded stability or manufacturing readiness.
