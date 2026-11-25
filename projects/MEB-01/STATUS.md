# MEB-01 — current development status (25 Nov 2026)

**Latest candidate:** MEB-037-R1 B · **DESIGN_ONLY / PARTIAL_ARCHIVE / INDEPENDENT_QA_PENDING**  
**Task:** [#125](https://github.com/mataniar0/assembl-lab-engineering/issues/125) · [Draft PR #128](https://github.com/mataniar0/assembl-lab-engineering/pull/128)  
**Release:** NOT_APPROVED. Original manufacturing/reference files remain historical; no production replacement.

| Deliverable | State |
|---|---|
| CAD candidate | 20-part nominal assembly, 3 changed / 17 retained |
| Static comparison | 190 pair results; zero positive-volume collisions above 0.0001 mm³ |
| Joint regions | 10/10 no positive-volume intersection, not physical fit approval |
| Motion and sequence | Nominal 0–110° rigid-body screen and 26 path checks; limits documented |
| R6 | Virtual review only; actual material bending NOT_RUN |
| Independent QA | PENDING |
| Source archive | Three source files match the local bundle Git blob hashes; parameter extract provided |
| Binary deliverables | Original STEP, GLBs, PNGs and ZIP remain outside repository; no binary transfer confirmed |
| Final layout and production | BLOCKED |

**Current entry point:** [MEB-037-R1 B archive](MEB-037/R1_LOCAL_STUDY/README_HE.md), [local QA report](MEB-037/R1_LOCAL_STUDY/LOCAL_REVIEW_RESULTS.md), [artifact manifest](MEB-037/R1_LOCAL_STUDY/ARTIFACT_MANIFEST.json).

The following older status is retained for provenance; it is not the current MEB-037 assessment.

---

# MEB-01 status
**Source:** V8.2.2 at ebeefe308efaf80329e16e42a84d51557878fd58
**Task:** Issue16 / Draft PR17 · **Stage:** G0 REVIEW_REQUIRED (full approval BLOCKED) · **Production:** NOT_APPROVED

| Workstream | State | Evidence / next action |
|---|---|---|
| Source provenance | VERIFIED20/20 pinned blobs | reports/MEB-000-geometry.json; independent raw QA |
| Original DXF inspection | PARSED17/17, unitsmm | 14part definitions,2sheets,1coupon |
| MEB-000 contract | v0.2 REVIEW_REQUIRED |3owner-approved requirements, other geometry provisional |
| Coordinate-reference reconstruction |14DXF/SVG pairs, DESIGN_ONLY | Single measured-vertex model; not a high-level generative kernel |
| Owner target stock | FROZEN HEIGHT800×WIDTH440mm | Explicit chat decision2026-10-20 |
| Required opening | FROZEN110deg | Requirement only; continuous3D motion NOT_RUN |
| Existing6mm sheet versus target | FAIL,822×348mm | MEB-B01; new packing needed before G4 |
| Existing4mm sheet bbox versus target | PASS bounds only | No margins/kerf/manufacturing approval |
| Independent QA | COMPLETE for bounded reference evidence,94/100 | Separate raw reader63cases plus14SVG checks; full G0 approval withheld |
| Parametric design kernel | NOT_IMPLEMENTED | G1 separately authorized after G0 review |
| Measured thickness/kerf/bend/bond | NOT_RUN | G3 |
| Full solid assembly/motion | NOT_RUN | G2 |
| Manufacture/commercial release | NOT_APPROVED | G4/G5 |

**Historical56indices:**49scoped2D/intakePASS,7NOT_RUN, not56newPASS.
**New risk:** MEB-B12,~0.09975mm exterior web at3lid-skin slots.
**Open issues:** MEB-B01..MEB-B12. Requirements for B01/B02 resolved by owner;
remaining packing/motion evidence is still open. B09 datum/finished envelope needs
lead review. All11interface statuses remain OPEN;2D evidence does not promote gates.

**Next authorized action:** engineering lead reviews Draft PR17, proposed datum,
reference-evidence boundaries and B12. Propose scoped component tasks afterwards;
no automatic G1 start, merge, cutting or production approval.
