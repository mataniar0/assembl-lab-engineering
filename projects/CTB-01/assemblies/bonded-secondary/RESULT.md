# CTB-009 — focused secondary CAD-kernel verification

Issue #34; P0; baseline `6ef432f16b12145bf8821aa540d6bf0e50264d4d` (merged PR #49).
Branch: `codex/ctb-009-secondary-kernel`. **DESIGN_ONLY.**

The lead's latest Issue scope is one secondary-engine verification, followed by
ChatGPT lead QA. No new design, geometry modification, whole historical test
replay, image gallery or manufacturing exports are authorized by this phase.
This implementation does not self-approve G2b or represent its own testing as
independent reviewer QA.

## Result

**SECONDARY_KERNEL_GEOMETRY_CONFIRMED / LEAD_REVIEW_PENDING.**
CadQuery 2.7.0 / OpenCASCADE `cadquery-ocp 7.8.1.1.post1` executed the following:

| Check | Unique cases | Result |
|---|---:|---|
| Final solid pairs | 496 | PASS; maximum overlap 0mm³ |
| Selected continuous swept pairs (8 movements) | 71 | PASS; maximum overlap 0mm³ |
| Representative negative controls | 2 | PASS; missing mortise 936mm³, 6.8mm ring 62.4mm³ |
| **Geometric pair/control total** | **569** | **PASS** |
| Additional 32-body parity and six joint-distance measurements | 32 + 6 | PASS; not added to the pair/control total |

Six joint clearances: 0.1990366123..0.1990367674mm. Maximum primary-manifest
bounds difference 2.091e-7mm, relative volume difference 1.281e-9. Existing GLB
parity passes for all 32 objects (maximum bounds difference 1.240e-5mm).
All 32 reconstructed BReps are valid, single-connected positive-volume solids.
33 input files are SHA-256 recorded. No original CAD or primary evidence changed.
Two execution attempts: one checker-only false failure, one completed verification;
one checker repair, **zero CAD repairs and zero unresolved geometric failures**
in this bounded scope. This is secondary-engine evidence, not a separate reviewer
approval or a fresh proof of every historical assembly motion.

## Inputs, method and scope

`verify_occ.py` reuses the existing P07 independent SVG reader and BRep helpers
(`parts/P07/tests/independent_occ_review.py`), without importing any primary
component `model.py` or running `bonded-b2/integrate.py`. It reconstructs actual
selected SVG material in OpenCASCADE, a different engine and Boolean algorithm
from B2's Manifold3D. Two mathematical pre-bent kerfed rim segments are rebuilt
from their finite exported material and each fused into **one** connected BRep;
66 intermediate cells per strip are not counted as wooden parts.

The 32-part candidate is unchanged: six unified bonded P01 cheeks, twelve
B_THROUGH_ADHESIVE spacers, A_COMPACT_CLOSED Y, two A disks, six A_RELIEVED_BOND
ribs, one keyless bonded C ring, two P07A skins and two rim segments. No P08,
adhesive, hardware or fixture solids. Every BRep is checked for validity,
connectivity and positive volume, and compared with both the primary manifest
and the existing GLB's actual transformed geometry.

Affected interfaces: IF-09 directly; IF-01/02 cheek insertions, IF-03 bottom
skin insertion and final IF-04/05/06/07/08/10/11/13 placement. IF-12 adhesive
retention capacity and IF-14 stability are not proved. Frozen geometry remains
Ø350/H500/top50, six 6mm cheeks with 15mm gaps at 0/120/240 degrees. The stock
definition remains portrait H800×W440; no new sheet/nesting claim is made.

The narrow swept selection comprises eight of the 31 existing motions:

- Y lowering 113mm against the new ring.
- All six changed cheeks translated tangentially 40mm, against every actual
  predecessor at their insertion time. Extrusion parallel to the translation
  gives the exact 46mm-deep swept material, preserving the profile's holes.
- Bottom skin lowering 70mm against the seven changed predecessor bodies.

The other 23 motions are **NOT_RUN** in this secondary study. Their archived
primary/inherited evidence remains in `../bonded-b2/evidence.json`. The old
782 primary and 222 inherited checks are not represented as newly executed.
Final pair checking covers all 496 combinations, with AABB separation before
OpenCASCADE Boolean intersection and unchanged 1e-6mm³ overlap acceptance.
The six joint distances are additional measurements, not extra final-pair cases.

## Reproduce and inspect

From repository root, using the existing secondary-kernel environment:

```sh
XDG_CACHE_HOME=/tmp/ctb-cache MPLCONFIGDIR=/tmp/ctb-mpl \
  /workspace/.venvs/ctb-001/bin/python \
  projects/CTB-01/assemblies/bonded-secondary/verify_occ.py
```

Exact engine/library versions, selected paths, source hashes, full named pair
matrix, body bounds/volumes, six distances, controls and execution history are
in `evidence.json`. The program writes failure evidence and raises on any failed
assertion; it never converts a failed Boolean into an empty intersection.

Initial checker failure: after reconstructing all 32 BReps, an overstrict
module-presence assertion rejected Manifold's optional transitive import by
the GLB/trimesh dependency stack. No Manifold Boolean or primary model was
executed. The checker now discloses that import and disables the module's
Manifold constructor with a raising tripwire. This is a verifier-only repair;
zero source CAD repairs. The initial attempt completed no pair tests.

## Release boundary and handoff

Submit these three files only: reproducible verifier, one evidence JSON, this
report. All original CAD, the B2 GLB and B2 evidence stay untouched. ChatGPT must
review the actual code and results before any formal G2b decision:
**INDEPENDENT_QA_PENDING / CHATGPT_LEAD_REVIEW_PENDING**.

Retain the original physical limitations: the ring is assumed held at
Z242..248 initially; fixture/cure/access are unproved. P04U↔P05 ~0.2mm AIR,
P04U→top 8mm AIR and ribs↔rim ~1.97287mm AIR are inherited geometric findings,
not fresh bond tests. No continuous structural load path or bond capacity is
claimed. Ideal pre-bent rim geometry is not a kerf-bending qualification.
**G3_NOT_PERFORMED_OWNER_DEFERRED / G4_BLOCKED**. Personal-use noncommercial
scope is preserved; this verification is not physical cutting/use approval.
No self-merge, no new production files, no automatic next development phase.
