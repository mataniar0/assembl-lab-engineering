# Engineering stage gates

Each gate is a **specific assertion with a bounded scope**. A passed earlier gate does not imply a later one.

| Gate | Purpose | Evidence required | Permissible release/status |
|---|---|---|---|
| G0 — Interface baseline | Lock agreed inputs and dependencies | BRIEF, preliminary BOM, units/axes, frozen/provisional parameters, interface IDs, open blockers, consistency checks | `BASELINE_FOR_COMPONENT_DESIGN` |
| G1 — Component design | Validate individual parts and local joinery candidates | Single-source parametric CAD, 1:1 exports, contour/topology checks, local fit *model*, alternatives, independent QA, unresolved contracts | `DESIGN_ONLY` candidate selected for downstream |
| G2a — Subassembly | Demonstrate local assembly feasibility | Real 3D material, parts counts, all local interfaces, continuous swept path or explicit blocked state, QA | `SUBASSEMBLY_CAD_VALIDATED` scoped by tested paths |
| G2b — Whole-system assembly | Demonstrate integrated geometry and sequence | Complete assembly model, cross-component regressions, full collision/insertion study, no unreported interface issue | `WHOLE_PRODUCT_CAD_VALIDATED` scoped to CAD |
| G3 — Physical prototype | Validate physical behaviour | Recorded material, measured fit/kerf, physical assembly, load and stability test plans/results appropriate to product, independent technical assessment where relevant | `PROTOTYPE_VERIFIED` limited to tested conditions |
| G4 — Manufacturing release | Authorize production drawings | Approved G3 plus manufacturing plan, reviewed nestings, compensations, part IDs, traceability, release authority | `PRODUCTION_RELEASED` |
| G5 — Commercial handoff | Publishing/fulfillment readiness | G4 or explicit non-sale concept disclaimer, approved images/descriptions, commercial requirements | `PUBLISH_READY` |

## Hard-stop rules
1. Missing/contradictory frozen requirement or unapproved change to approved geometry: **STOP**, create issue/Change Request.
2. Geometry-invalid cut contour, failed interface or insertion path needed for the stage, missing meaningful QA or undocumented dependency: **BLOCKED** for that claimed gate.
3. Unmeasured tolerances, glue performance, material or load limits cannot be promoted from nominal CAD to physical PASS.
4. A blocker may remain open when **merging a clearly labeled design study** if it does **not** invalidate the study's precise scoped claim. Such a merge does **not** close the blocker or raise the product's release gate.
5. A report should distinguish: `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`, and `NOT_APPLICABLE`. Don't label unavailable/unsafe tests as passes.
6. The implementer cannot self-merge. Lead merge approval requires ≥90/100 code/CAD QA where scoring applies, **zero in-scope critical blockers**, and traceable evidence. Separately, physical G3 and product G4 require actual competent testing and release evidence, not scores alone.

## Change control
Frozen parameters: only change via reviewed Change Request with downstream impact analysis and a version increment. Provisional design parameters may be updated in versioned proposal files, then promoted deliberately after a documented decision. Old versions stay identifiable.

## Escalation
Routine design-study selection and merges: engineering lead may decide under delegated authorization. Major aesthetic direction, footprint, functionality, materials, safety or important trade-offs: owner decision. Structural/load-related claims may need competent independent engineering evaluation. Never delegate safety certification to an automated CAD test alone.
