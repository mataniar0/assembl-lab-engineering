# CTB-013 preliminary implementer geometry review — DESIGN_ONLY

- Two 4mm rim files, P07R1 and P07R2; each 64 closed outline/hole contours (outer + 63 retained kerf slots). DXF contains 64 closed LWPOLYLINE entities and SVG contains 64 polygons per strip. Sheet bounds in native x/y = x0..50 and y-7.8..543.295529, compatible with 440x800mm sheet *individually*.
- 76 exterior contour vertices per strip after addition of nominal single male neck/puzzle head on one end and female recess on the other; strict crossing checks of distinct nonadjacent boundary edges returned **zero proper crossings** in both outlines.
- Reciprocal profiles geometrically align by nominal end-coordinate translation, but that does **not** establish positive assembly clearance or possible physical insertion. No measured kerf compensation, no grain/flex testing, no rounded-neck fatigue check, no 3D assembly path check.
- Previous CTB-012 strengthened kerf layout remains 63 slots; no new openings near seam end.
- Design-stage initial geometric failures observed: **0**; source geometry repair loops: **0**; deliberately invalid sample controls NOT_RUN; independent CAD-kernel review PENDING; physical review NOT_RUN.

### Explicit blockers

- Nominal reciprocal seam profile has zero planar clearance; actual physical interlocking would require calibrated allowance and a verified side-insertion path. This is a design concept, **not cut-ready**.
- Original kerf-bend neutral arc developed length and end closure cannot yet be asserted as exact under real bend and material thickness.
- Minimum material land and hinge-neck local stress need solid modeling and tests; edge rounding remains to be specified.
- IF-11 seam, IF-10 rim/skins, IF-07/08/12 retention and physical material/strength gates remain unresolved, with G3 NOT_RUN and G4 BLOCKED.
