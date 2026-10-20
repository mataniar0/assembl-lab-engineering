# ETG-000 v0.1 — מסמך בקרת ממשקים (ICD)

**Stage:** `G0_DRAFT / DESIGN_ONLY` · **Issue:** #18 · **Units:** mm and degrees.
מקורות התהליך: `AGENTS.md`, `engineering-process/PLAYBOOK_HE.md`, `GATES.md`, `QUALITY_STANDARD.md` ו-`.agents/skills/assembl-lab-product-engineering/SKILL.md`.

## 1. Source of truth and provenance
- `parameters.json` — values with FROZEN/PROVISIONAL/DERIVED/OPEN and provenance.
- `PARTS.csv` — *provisional* product BOM and stable IDs. Counts not verified from current parametric source.
- `interfaces.csv` — IF-01..IF-24; all OPEN for fresh G0/G1 review, despite historical audit PASS.
- `OPEN_ISSUES.csv` — blockers and closure evidence.
- `LEGACY_REGISTER.md` — V7.2, V7.6 reconciliation and exclusion of Megillah V8.3.9.
- `../../DECISIONS.md`, `../../STATUS.md`, `../../BRIEF.md` — product records.

## 2. Frames and envelope
Global outer body origin = front-left-bottom; +X length front-to-right, +Y depth toward rear, +Z up. Body expectation 260×160×150. Rearward FCIPH extension ~178.4 total depth is a historic approximation, **not the body depth**.
Cutting-sheet convention explicitly **portrait**: X across width 440, Y along height 800. Legacy V7.6 cutting bounds must be re-oriented/rechecked before G4. Do not inherit CTB-01 specifics.

## 3. Structural path
Body panels P01–P05 via laminated keyed corners P06; lid P07–P10 via integrated FCIPH, pinned/anchored through P11–P12; optional P13 fits free cavity. A historical slice count of 96 (64 plain + 30 keyed + 2 special) is provisional, subject to BOM vs geometry check.

## 4. FCIPH preliminary contract
V7.2: ear Ø32, pocket Ø32.8 => **radial 0.40**; pin Ø14, hole Ø14.6 => **radial 0.30**. Relief `RELIEF_0P4MM` is a **shallow recess depth 0.40**, never a through-cut. Movement audit target 0–120°, all moving solids plus clear assembly/insertion paths. Real fit and durability **OPEN**, including laser depth/recess fabrication feasibility. V7.6 self-described audit: 108 PASS, 6 repairs, does not count as newly performed independent QA.

## 5. Acceptance for G0
1. All part references and IF endpoints appear in BOM.
2. Constants, computed values, assumptions and measurements are distinct and source-traceable.
3. Rear hinge envelope, old nesting orientation, optional cradle and missing native CAD recorded as unresolved.
4. Repository QA rechecks JSON/CSV consistency and negative control examples; independent reviewer verifies content.
5. G0 approval is **baseline for component design only**, never permission for cutting, assembly, sale or production release.

## 6. Restriction
Keep any archived cutting files quarantined as `legacy/` with hashes and labels until native regeneration, export checks, G2 3D sweep and G3 measured testing. No unverified files are bundled in this PR.
