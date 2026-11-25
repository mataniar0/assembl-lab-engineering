# ST-001 R20 — Digital interface and assembly screening
Status: PARTIAL / DESIGN_ONLY / NO_CUT / NO_OCCUPANT_USE.
Source: PR #127, f6d732ecf589eda71853d0c3f54d7ae65bcdbed2. Issue #126. Owner approves permanent bonded product requirements only.

## Diagnostic cycle 1: failure classification
Reopened QA.json, QA.csv, LAYERS.csv, INTERFACES.csv and BOM.csv. All 24 existing failed approach cases were reclassified: 8 E01-only, 12 A01/A02-only, 4 A01/A02 plus A03. No F01 blocker appears. Removing F01 proxies changes none of the 24 existing failures. The 8 existing passing approach cases retain their scope; no new continuous motion or solid-kernel calculation was run. Failure results apply to the final-state configurations tested, not every possible assembly sequence.

## Display correction cycle 1
Created separate display-only GLB exports with 88 original body layer nodes and meshes; 16 off-body F01 proxy nodes and their unused geometry removed. Both outputs independently read back and compared against their source exports: 88/88 corresponding position and index buffers byte-identical and node translations identical per file. No physical joint geometry, source FreeCAD document, dimensions or controlled BOM changed. The no-F01 proposal remains a display variant, not a finalized bonded design.

## Open requirements
24 approach failures remain; full digital sequence not validated. Nominal contact does not establish load-bearing fixation, and removal of the display proxies does not establish joint retention. All 56 non-lock interface design statuses remain BLOCKED pending appropriate professional review. No structural verification, physical test, or OCCT rerun performed. No fabrication files, no merge, no production release. G2b/G3/G4 BLOCKED.
