# CTB-009 B1 — LOCAL_CAD_GEOMETRY_GO_ONLY

Issue [#34](https://github.com/mataniar0/assembl-lab-engineering/issues/34), 2026-10-21.
Branch `codex/ctb-009-bonded-local-b1`; base `a4f3cf09224736ec24c247e18967b5c2e5b438ee`.
**DESIGN_ONLY / BOND_CAPACITY_UNKNOWN / G2b_NOT_PASSED / INDEPENDENT_QA_PENDING.**

One actual L1 positive-t P01 candidate and one P06 terminal without a keeper
aperture were extruded directly from the PR#46 SVG polygons using existing
P06/P02 CAD functions. The nearest real S3 and selected P03 Y were obstacles.
No keys, adhesive layer, six-cheek assembly or complete32-body model was created.
Scope: changed IF-09/B05, preserving IF-01/02/14; upper bonded IF-12 and
IF-06/07/08 are not proven by this check.

| Unique local3D case | Observed overlap |
|---|---|
| Original unmodified cheek / old C terminal negative | **936.000000 mm³**, detected as expected. |
| Candidate initial t offset+40 / final0 | **0 mm³** versus ring, S3 and Y in both poses. |
| Exact complete Y_FIRST cheek translation +40→0 | **0 mm³** versus all three obstacles. Continuous swept solid, not sampled poses. |
| Candidate final / old apertured C terminal | **0 mm³**. |
| Filled-hole material / complete cheek sweep | **0 mm³**; hole filling adds no collision on this specified route. |
| New ring terminal / S3 and Y | **0 mm³**. Ring vertical gaps: S3=39mm, Y=159mm. |
| Deliberately oversized6.8mm ring negative | **62.399999070 mm³**, detected as expected. |

**8/8 unique3D cases matched expectations**, plus five source/profile prerequisites.
Radial and axial edge gaps are0.2mm each; the actual rounded polygon minimum
clearance is **0.199036710mm** (polygonal fillet approximation, not measured fit).
Minimum wood from new mortise to outer silhouette is **10.963951423mm**; to the
nearest old mortise **38.652866247mm**, using actual segment-to-segment distances.
Local hole filling restores43.484857783mm² of planar material. Facing projection
is156mm² per horizontal face, with positive0.2mm axial air gaps: **zero nominal
face contact, no effective bonded-area or capacity proof**.

Original P01 outer/five mortise loops and P06 outer/central-hole loops are exactly
preserved in the loaded candidate vertices. Protected tracked sources have an
empty diff against base;43 input/source SHA-256 values are in `evidence.json`.
No failed CAD case or source geometry repair. One local crop precision refinement
aligned the8.2×10⁻⁸mm parametric/export rounding difference; two evidence builds
and one read-only replay cover the same eight cases.

**Inherited source defect, not repaired:** both PR#46 SVGs have nonnumeric
`viewBox` labels and numeric viewport text in `title`. Their mechanical polygon
coordinates are valid and were used directly; the `scale(1,-1)` group is a display
flip. The local CAD GO does **not** validate SVG viewing/export metadata. ChatGPT
should correct packaging separately while preserving the actual mechanical loops.

Reproduce from repository root with the existing P06 pinned environment:

```sh
XDG_CACHE_HOME=/tmp/ctb-cache MPLCONFIGDIR=/tmp/ctb-mpl \
  /workspace/.venvs/ctb-006/bin/python projects/CTB-01/parts/P06/adhesive-study/local-b1/probe.py
```

Use `--write` to regenerate JSON; dependencies: [P06 requirements](../../src/requirements.txt).
Only `probe.py`, `evidence.json` and this report are delivered. No upstream edits,
new cut files, gallery or historical regression suites. Stop for ChatGPT independent
review before authorization of six-cheek/32-body integration and secondary CAD QA.
Bonding/fixture/cure access, upper load path, physical fit/kerf/strength/stability,
G2b/G3/G4 and cutting/production remain OPEN/NOT_APPROVED. No self-merge.
