# RR-001 — Natural wood disc rocking chair (engineering intake)
**Status:** `G0_PROVISIONAL / G1_PARTIAL_DESIGN_ONLY / G2_BLOCKED / G3_NOT_RUN / G4_BLOCKED / NO_CUT / NO_OCCUPANT_USE`
**Work tracking:** [RR-001 engineering issue #117](https://github.com/mataniar0/assembl-lab-engineering/issues/117)
**R04 design artifact:** `RR001_R04_Engineering_Design_Study_DESIGN_ONLY.zip`, SHA256 `74866dae1a4306bdd574f19832e5d01fcfa18d4349496fcd320a2b5b5aaa16b7`; package currently in ChatGPT conversation, **not stored in this repository**.

## Design intent
User-selected rocking chair with **two natural unmachined live-edge wood discs**:
- seat disk placed horizontally;
- back disk slightly reclined;
- frame combines **EB (hollow engineered plywood beams/diaphragms)**, **FJ (nominal finger/tab joints)**, and laminated curved rockers;
- two direct transverse box-beam ties between the curved rockers, plus X braces and knee reinforcements.

Do not reinterpret pictures as dimensioned manufacturing plans. The physical wood discs are not measured or evaluated. This is **not** a usable chair.

## Engineering baseline
See [project G0 and interface overview](G0_INTERFACES_HE.md) and [R04 intake QA](QA_R04_INTAKE_HE.md).
Prior R03 local source had 97 STEP solids and 99 GLB display parts. Actual STEP audit of back pads detected 1.63–1.97mm gaps. R04 replaces four nonmating pads with 12 laminated 6mm geometric contact shims, creating 105 STEP solids and 107 GLB display meshes. Nominal zero collision is **not** proof of structural retention.

## Unresolved blockers
1. Physical dimensions, flatness, cracks and moisture of both natural discs.
2. Positive capture and wood-movement-aware attachment of seat and backrest (not just rear-plane contact).
3. Structural FJ/EB load paths, glue/lamination, runner cross-tie pullout and full assembly sequence.
4. Rocker tipping, center-of-mass, fatigue, floor clearance and appropriate rocking stops, assessed by qualified engineer.
5. 18 nominally non-single-6mm CAD bodies in historical model require actual stock/material decomposition.
6. Kerf, actual material thickness and safe machine area unmeasured; nesting, physical G3, production G4 **not performed**.
7. Independent QA pending.

### Next priority
`P0`: measured-disc G0 → select and engineer real seat/back retention → FJ pullout + full assembly swept paths → professional human-load/stability assessment → physical prototype tests. Source code/CAD are in the chat ZIP until uploaded explicitly.

The proposed construction-method reference is in [methods PR #116](https://github.com/mataniar0/assembl-lab-engineering/pull/116). Standard [Playbook](../../engineering-process/PLAYBOOK_HE.md) and [Gates](../../engineering-process/GATES.md) govern actual approval.
