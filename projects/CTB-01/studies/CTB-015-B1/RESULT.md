# CTB-015 B1 — REVISE: final fit passes, existing closing route fails

**REVISE / CURRENT_VERTICAL_ROUTE_NO_GO / STOP_AFTER_B1 / DESIGN_ONLY.**
No source changes, measured kerf/fit allowance, nesting, CTB-016, B2 or merge.

Inputs: CTB-015 PR60 head `3ca8e38cc084e82f237b427903249282ebe4d1e2`, stacked
over CTB-013/012 proposals. Branch `codex/ctb-015-b1`. Instructions are the
source branch's `NEXT_CODEX_B1.md`. IF-10/11 only; nominal R173, radial171..175,
Z450..500, phases15/195 and theta=phase+(s−0.2)/173. Source hashes and archived
CTB-014 evidence commit/hash are in evidence.json. No accepted source is edited.
The exact prior JSON is archived as CTB014-evidence-reference.json for clean
branch-only reproducibility; its29 old cases are not new executions here.

## What the correction fixes

| Focused case group | Cases | Result |
|---|---:|---|
| Corrected SVG and actual standard DXF imports | 4 | PASS;64 contours/master, identical numeric coordinates |
| Neck/head/notch/kerf geometry | 2 | PASS for source geometry only |
| Complete shell material vs bottom/top skin Z bands | 4 | PASS |
| Both complete curved final seam domains | 2 | PASS within numerical threshold |
| Existing R2 lowering route, one interior collision pose at each seam | 2 | **FAIL** |
| Old short-length seam and filled-notch negative controls | 2 | PASS; expected collisions detected |
| Source preservation and actual route provenance | 1 | PASS |
| **Unique cases** | **17** | **15 PASS /2 FAIL** |

Both new DXFs load in ezdxf1.4.4, with no geometry repair/recovery. Audit reports
zero errors but fixes **one invalid LAYER-table handle in memory per file**
(code110). These are2 metadata advisories; the original files are not written
or represented as pristine zero-fix audits. The prior AcDbPolyline import error
is resolved for these **two corrected masters**, not every old CTB-012/013 DXF.

Each half retains63 kerf apertures,18 shortened, exactly matching its previous
reinforced holes. Notch-floor to kerf land remains6mm. Neck one-sided section at
s−1.800001 is12.000000909mm (limit12), head14mm at s−4, tip6mm at s−7.8. Native
polygon corners/notch transitions are sharp, no specified neck fillet; these
measurements are **not strength, stress or bending qualification**.

## Actual curved CAD and final-state results

CadQuery2.7.0 / OpenCASCADE7.8.1.1 build cylindrical BRep faces with original
source edges as UV curves. Angled head edges map to helices; radial ruled faces
join inner/outer cylinders. Each closed joint solid is valid and its volume
agrees with4×native-profile area within1e-5mm³. This replaces CTB-014's smaller
inscribed collision subsets with **complete local seam domains**.

Domain h0..50/s−10..3 covers all possible mutual material overlap at each seam;
both rim parts are included. These are actual curved joint solids, not a planar
projection or inferred mesh result, and not an unnecessarily rebuilt whole table.

- **Phase15 final seam OCC common:0mm³.**
- **Phase195 final seam OCC common:0mm³.**
- Exact flat-domain integration leaves5.682734549e-7mm³ per seam from the
  7.1034e-8mm serialization difference between rounded length543.495529 and
  π×173. This is below source rounding1e-6mm and the numerical volume threshold
  1e-4mm³. It is not positive physical clearance or kerf compensation.
- All4 shell/skin final-Z-band tests pass; detailed tiny numerical volumes are
  recorded. The tests include complete material that can intersect each skin,
  preserving the actual tabs and original lower-skin holes.
- The old short-length negative control again gives about2.78109mm³ in this
  curved implementation, proving it detects the removed CTB-014 blocker. This
  single targeted control is not a historical suite replay.

## Actual assembly-route blocker

The accepted B2 evidence specifies **R1 first, then R2 lowered from Z+70 to0**,
lower skin/core already present, top afterwards. CTB-015 supplies no replacement
closure route. We test that actual inherited motion, not an arbitrary offset:

- At R2 offset **(0,0,+2)mm**, phase15 seam overlap is
  **63.99999867402044mm³**.
- At the same offset, phase195 seam overlap is
  **63.9999986740188mm³**.

At phase15 R2 is the female end; at phase195 it is the male end. Fixed R1 and
moving R2 are assigned accordingly. Independent developed-coordinate integration
agrees with both curved Boolean volumes. A positive collision at one interior
pose proves this entire continuous route fails; dense pose sampling or a full
swept shell cannot turn it into a pass. No alternate6DOF/elastic/pre-closure
path has been proved, and no universal rigid-assembly impossibility is claimed.

`route-collisions-DESIGN_ONLY.step` contains **8 valid re-imported diagnostic
solids**:2 fixed local parts,2 moved local parts and4 disconnected common lobes
(two lobes per seam). It is not an8-part wooden assembly or a production file.

**Smallest next action:** revise/specify and prove a closing motion/sequence
before CTB-016. If the existing vertical route must be retained, the re-entrant
head/receiver material intersected by that swept motion needs a reviewed source
CR (an entry/relief change can alter puzzle retention). Do not add guessed kerf
or silently resize the joint. No static-interference correction is justified by
the sub-tolerance rounding residual. Correct DXF table-handle metadata separately.
No alternative or corrected source is produced in this B1.

## Failures, repairs, reproduction and pause

The17 formal cases ran once. One successful local CAD-construction prototype
preceded them. A final artifact-count checker then expected6 solids; the two
disconnected common lobes per seam make the correct total8. **1 checker repair,
0 source/CAD repairs.** Targeted STEP re-import/result finalization completed
without replaying any Boolean/case suite. Both real route failures remain.
Two automatic audit metadata fixes occurred only inside parser memory, as above.

Reproduce all focused cases with the existing ctb-001 environment:

```sh
XDG_CACHE_HOME=/tmp/ctb-cache MPLCONFIGDIR=/tmp/ctb-mpl \
 /workspace/.venvs/ctb-001/bin/python projects/CTB-01/studies/CTB-015-B1/verify_b1.py
```

Separate review is in INDEPENDENT_QA.md. Stop after B1 for ChatGPT lead review.
No old global regressions, whole-table rebuild, B2, nesting, CTB-016, physical
kerf/material/bending/glue/strength/load/stability tests or merge. G3/G4 and
physical cutting remain unapproved; source clearance is deliberately uncalibrated.
