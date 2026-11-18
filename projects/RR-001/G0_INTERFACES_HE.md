# RR-001 G0 — dimensions and interface register (HE)
**Stage:** `PROVISIONAL_BASELINE_ONLY` — neither approved structure nor physical test.

## Dimensional authority
All values are **nominal R04 CAD**, not measured chair stock:
| Parameter | CAD value | Classification |
|---|---|---|
| Reference frame | X width; Y length along rocker; Z vertical; STEP mm / GLB m | modeling convention |
| Overall extents | 446 × 760 × 795.4 mm (X×Y×Z) | derived from STEP |
| Natural seat disc | Ø345 × 32 mm; Z429..461 | photo-based provisional |
| Natural back disc | Ø290 × 30 mm; 10° lean; center Y−208, Z650 | photo-based provisional |
| Rockers | 2×(6 laminae × nominal 6 mm), arc R1050, Y±380, profile height52 | provisional |
| Direct rocker cross-ties | 2 EB assemblies at Y±245, Z44..71 | R03 CAD geometry inherited |
| Transverse seat box beams | 2 at Y−110,+92, nominal Z391..427 | inherited |
| Machine work envelope | 900 mm HEIGHT × 450 mm WIDTH | owner-reported, not physically calibrated |
| Birch plywood | nominal 6mm; actual grain, kerf and bond strength | OPEN |
| Actual wood slices | measure diameters, min thickness, cracks, moisture, surface topography | OPEN |

## Interfaces and priorities
| IF | Priority | Connection | Scope evidence | Closure required |
|---|---|---|---|---|
| IF-01 | P0 | seat disc ↔ sub-seat support | four underside pads touch ideal seat | positive wood-compatible capture; real disc measurements |
| IF-02 | P0 | back disc ↔ rail-backed supports | R04 12 laminated wedges contact ideal disc plane | captured retention, no face-only assumption; physical disc shape |
| IF-03 | P0 | 6mm laminated wedges ↔ each other/rails | nominal face mating | shear/bond/positive fastening and fatigue verification |
| IF-04 | P0 | transverse rocker ties ↔ runner laminates | R03 8 FJ male/female CAD pairs | positive pullout lock in X; minimum lands; insertion proof |
| IF-05 | P0 | curved runner lamination stack ↔ runner lamination stack | 6 layers per runner | glue and cyclic loading verification |
| IF-06 | P0 | side truss ↔ runner | static CAD placement | structural anchorage/rigid load transfer |
| IF-07 | P0 | seat EB beams ↔ side cheeks | nominal FJ receiver geometry | anti-withdrawal and assembly access |
| IF-08 | P1 | low X braces ↔ box ties | butt contact in R02 | true joinery and load transfer |
| IF-09 | P1 | knee gussets ↔ runner/truss | conceptual surface contact | mechanical attachment |
| IF-10 | P0 | rockers ↔ floor during pitch | old ±15° nominal floor proxy | dynamic stability, person center-of-gravity, anti-tip/stop checks |
| IF-11 | P0 | rear cradle rails ↔ side panels | rail nominal placement only | load-carrying fasteners/joint |
| IF-12 | P0 | CAD bodies ↔ machine/stock | 85 profile nominal fit checks | real stock/sheet margins, kerf and 18 non-sheet-shaped legacy parts |
| IF-13 | P0 | assembled geometry ↔ assembly motion | no full swept proof | collision-free component insertion and access |
| IF-14 | P0 | occupied chair ↔ material and motion loads | no physical evidence | qualified professional structural/dynamic tests |

## Engineering decisions (G0 candidate, not freeze)
- Keep R03 rocker, chair frame, direct ties and seat configuration unmodified in R04.
- Backrest correction is a geometrical mating study only: replace 4 non-contact pads with 12 6mm laminated contact wedges.
- Do **not** treat a wood disc resting against a planar wedge as secure attachment. Neither disk has proven positive capture.
- Do **not** silently interpret 18 non-6mm single-body solids as single 6mm laser-cut parts; material or decomposition must be decided later.
- Structural, aesthetic, machine and material changes beyond this bounded study require versioning and proper owner/design decisions.

## Next gate
Professional assessment of load/stability concept plus true physical disk measurements are prerequisites to any release of load-bearing G1 joints or an occupied rocking chair. Read the [Gates](../../engineering-process/GATES.md) before claiming `G2`/`G3`/`G4`.
