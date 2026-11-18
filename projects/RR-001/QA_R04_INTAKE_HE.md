# RR-001 — R04 CAD intake validation
**Status** `DESIGN_ONLY / NO_CUT / NO_OCCUPANT_USE / INDEPENDENT_QA_PENDING`.
This file records **same-author** Python/CadQuery and read-back tests, not an external independent review and not a production approval.

## Observed defect
Reopened the actual R03 STEP (97 solids, BOM alignment verified). Exact CAD nearest-shape distances between backrest disc and old pads:
- `BACK_LOWER_PAD_{L,R}`: **1.96525 mm** separation each.
- `BACK_UPPER_PAD_{L,R}`: **1.63478 mm** separation each.
- Even the closest frame body was 1.63mm away; hence nominal back disk was suspended without a modeled contact/retention interface.

## R04 correction
Replaced each of the four old conceptual pads with **three** nominal 6mm YZ-profile laminates aligned to the inclined rear disc plane, 12 new pad laminates total. This supersedes an intermediate 20mm-thick monolithic wedge that was rejected for lack of single-sheet 6mm cuttability.

The rear support is still *not a captured connection*: nominal contact cannot hold the disc against outward movement.

## Readback checks
| Scope | Results |
|---|---|
| STEP solids valid | **105/105** |
| GLB rendered nodes | **107**, units meters |
| Prior unchanged bodies | **93** same nominal bounding boxes/volumes |
| 12 laminated shims to nominal back disc | **12/12** zero distance to rear plane |
| Each laminated shim to supporting rail | **12/12** zero distance |
| Positive-volume overlap from shims to disc | 0 >0.01mm³ |
| Full CAD positive-volume overlap | 0 / **5,460** evaluated pairs; 45 candidate AABB pairs needing Boolean solid intersection |
| GLB extents | **446×760×794.808 mm** |
| Source generator checks | 171/171 nominal cases, including 85 one-part profiles; not a full nesting |
| Independent professional QA | **NOT_RUN** |

## New fabrication-fit blocker
18 pre-existing non-disc bodies fail the simple **axis-aligned single 6mm sheet thickness** inventory: 10 side-frame diaphragm blocks, 4 x 2mm seat cradle pads, 2 solid back cradle rails and 2 back side brackets. Their real materials, lamination/subpart decomposition and joinery are not established. They cannot be treated as finished cut profiles for nominal birch 6mm.

## Unresolved physics / use
- No measured seat/back wood discs (diameters are not authoritative).
- Neither disc has verified positive retention, including R04 back.
- No verified rocker-to-leg load path, R03 runner cross-tie pullout lock, glue fatigue, complete 3D swept assembly path.
- No applied human load, ergonomic/structural design assessment, full floor clearance/stop geometry, center-of-gravity analysis with occupant or stability tests.
- No material/kerf calibration or physical prototype; G3/G4 blocked.

## Revision history
1. R03 back-pads-to-back-disc gap found (geometry defect).
2. R04 first wedge: nominal contact candidate, but 20mm thick solid incompatible with implied 6mm sheet.
3. R04 second wedge: **3×6mm** layer layout per pad, 12 separate laminated parts, nominal geometric checks passed.
4. Positive retention and physical joinery **remain OPEN**.

**Gate truth:** G0 PROVISIONAL; G1 PARTIAL (geometry only); G2 BLOCKED; G3 NOT_RUN; G4 BLOCKED. Technical assessment by qualified independent reviewer is required before any physical load-bearing use or manufacturing.
