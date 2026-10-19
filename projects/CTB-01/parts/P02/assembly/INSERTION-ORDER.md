# B working concept — one-leg assembly / DESIGN_ONLY

Axes: r outward, t tangential, z upward. Spacer plates in r-t, nominal6 mm in z.
Cheeks are the same r-z profile with the same four mortises, extruded6 mm in t.
Final centers±10.5; inner faces±7.5; outside±13.5. No mirrored or separately drilled cheek.

1. Fixture the first mortised cheek at center t=-10.5. Support it and every spacer;
   the bare assembly has no approved self-support or glue strength.
2. Insert P02B S1 atz35, then P02 S2 atz90, S3 atz200, S4 atz390, independently
   along **−t**. Each starts40 mm from its final t placement; the negative tab enters
   the fixed cheek from its inner side. Stop at the shoulder. Hold each in its fixture.
3. Place the second identical cheek40 mm above its final t position (center50.5)
   and translate it along−t to center10.5. All four positive tabs enter simultaneously.
4. The proposed assembly would require a separately validated adhesive application,
   clamping, cure and inspection procedure. No actual glue/physical work is performed.

`collision-and-insertion.json` records all15 final pairwise material intersections
and15 moving-sweep/fixed-part checks across the five steps. Both sets have zero
positive-volume intersections at the nominal study dimensions. Contact is permitted.

The sweep is continuous, not a sparse animation: each horizontal plate contour is
Minkowski-summed with a40 mm t segment via constrained triangles, then extruded in z.
The moving cheek is its actual mortised r-z material extruded over t7.5..53.5.
Every swept solid is intersected with all parts already installed, using Manifold3D
CSG. Threshold1e-6 mm³ applies to this flattened model, not machine accuracy.
Independent QA reconstructs SVG paths using OpenCASCADE and a different boundary-edge
sweep construction. See tests/independent_occ_review.py and its recorded results.

Intentional clearances: slot per-side radial/z allowance0.2 mm in this CAD hypothesis;
shoulder contact at t±7.5 sets nominal gap15. Mortise height6.4 is not a measured fit.
Shoulders provide inward bearing; the B tabs alone **do not positively retain cheeks
against outward separation**. Glue/capture/load capacity remains unverified. Local
translational access says nothing about Y, ring, disc, top lock or full-table assembly.

`one-leg-DESIGN_ONLY.glb` contains six watertight nominal mesh parts, GLTF in METRES;
source/JSON are mm (model z0.488 m =488 mm). Transparent previews show actual holes,
not a substituted uncut cheek. Exploded positions are illustrative; continuous paths
and their endpoints are authoritative in the JSON. No production/cutting release.
