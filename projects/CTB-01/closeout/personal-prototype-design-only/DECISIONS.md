# CTB-010 digital-package decisions — proposals for lead review

Priority P1, stages3/4 only. User explicitly authorized continuation after the
accepted secondary CAD proof; B1/B2/OpenCASCADE executions in this task: **0**.
Applicable skill: `.agents/skills/assembl-lab-product-engineering/SKILL.md`.
Lead ChatGPT reviews; Codex implements exports; a separate QA agent examines
actual files under the playbook's independent-review requirement.

- Preserve all original selected parts and the versioned bonded P01/P06
  candidate. New assets live only in this closeout directory. No CR or design
  geometry change is proposed; all interface dimensions remain unchanged.
- Distinguish 12 named assembly roles from 11 unique cutting shapes:
  P07R1/P07R2 have exactly identical native contours but different assembly
  phases; share one P07R_MASTER and retain both placement/body identifiers.
  Six P01 cheeks share one unchanged master; no P08 wooden parts.
- Export native cut polygons verbatim as straight-segment closed contours.
  Preserve source polygon discretization; do not refit curves, resize slots,
  add kerf compensation, extrapolate physical bend length or project a mesh.
- Use conservative non-overlapping bounding envelopes, first-fit bottom-left
  packing with rotation0 and no reflection. H800×W440 portrait, margin10/gap5mm
  are **planning allowances**, not measured fit/kerf tolerances. No use of
  aperture waste or common-line cuts. Seven nominal6mm sheets plus one4mm
  sheet are a feasible conservative proposal, not an optimum or purchase plan.
- Preserve source sheet axes. Grain/flex direction and real stock thickness
  are UNMEASURED; the digital plan cannot qualify physical orientation or bend.
- Use CUT_OUTER/CUT_INNER only for experimental cut vectors. All labels and
  stock edges are explicitly NOT_CUT; no engraving operation is prescribed.
- Copy the accepted GLB byte-for-byte as a preview; no new model generation.
  Retain separate primary/secondary evidence provenance and ring+31 motions.
- File QA, package sealing and independent review are new; historical CAD
  assertions and QA scores are inherited, never counted as new executions.
- Do not self-approve G2b, merge, authorize cutting or advance physical gates.
  G3_NOT_PERFORMED_OWNER_DEFERRED / G4_BLOCKED. The one-off personal-use scope
  needs no commercial certification packaging; it still has no measured
  material/glue/kerf/load/stability evidence.
