# [PRODUCT-ID]-000 — Interface Control Document (ICD)

**Version:** [v0.1] · **Status:** `BASELINE_FOR_COMPONENT_DESIGN / DESIGN_ONLY`

## 1. Source of truth
- Source project brief: [...]
- Frozen decision record: `DECISIONS.md`
- Parameters machine-readable: `parameters.json`
- Interface list: `interfaces.json` / `interfaces.csv`
- Open issues: `OPEN_ISSUES.csv`
- Active/obsolete CAD version registry: [...]

## 2. Reference frames & units
**Units:** [mm, deg] · **Global xyz origin:** [...] · **Axes and orientation:** [...] · **Local part bases:** [...] · **Sheet coordinates:** X across WIDTH, Y along HEIGHT, unless this project declares otherwise.

## 3. Parameter register
| Parameter ID | Value | Unit | Status | Who approved | Source |
|---|---:|---|---|---|---|
| [EXT_HEIGHT] | [ ] | mm | FROZEN / OPEN | [ ] | [ ] |
| [PLYWOOD_T] | [ ] | mm | PROVISIONAL | [ ] | [ ] |
| [SHEET_H] | [ ] | mm | OPEN | [ ] | [ ] |
| [SHEET_W] | [ ] | mm | OPEN | [ ] | [ ] |

FROZEN values cannot change without Change Request. DERIVED values specify formulas. PROVISIONAL values are assumptions; OPEN values lack a defensible measurement or decision.

## 4. Part family/BOM
| Part ID | Name | Qty | Material | Attaches to | Owner task | Status |
|---|---|---:|---|---|---|---|
| [P01] | [...] | [...] | [...] | [...] | [PROJECT-001] | DESIGN_ONLY |

## 5. Interface register
| IF ID | Components | Required geometry/fit | Source parameters | Proof needed | Status |
|---|---|---|---|---|---|
| IF-01 | P01–P02 | [...] | [...] | [...] | OPEN |

Interface statuses: `OPEN`, `PROVISIONAL`, `CAD_VALIDATED`, `PHYSICAL_VALIDATED` and `RELEASED`. Include **method, geometry and evidence** for every status promotion.

## 6. Build and release constraints
- Order-of-assembly hypotheses: [...]
- Material thickness actually measured? [NO]
- Kerf actually measured? [NO]
- Physical load/stability tests? [NOT_RUN]
- Single-part bounding fit versus actual production nesting: [...]
- Critical blockers and assigned resolution tasks: [...]

## 7. G0 acceptance checklist
- [ ] Frozen/derived/provisional values distinguished.
- [ ] Every referenced part is in BOM.
- [ ] Every connection has an IF ID.
- [ ] Sheet HEIGHT/WIDTH unambiguously ordered.
- [ ] CAD baseline geometry/revision and legacy quarantine explicit.
- [ ] Consistency tests pass and independent review recorded.
- [ ] Owner-relevant decisions recorded.
- [ ] Unresolved blockers carried to G1.
