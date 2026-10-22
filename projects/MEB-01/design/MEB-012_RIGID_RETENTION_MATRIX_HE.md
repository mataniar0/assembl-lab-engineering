# MEB-012 — rigid relative X/Y/Z retention matrix (research only)

**2026-10-22 · P1 · ChatGPT direct · DESIGN_ONLY · no independent QA**. References MEB-011 T1 and Issue #70. The material/geometry of the original V8.2.2 and H1-IF2 source remain unchanged.

### Method
Group moving solids into: (1) front rail; (2) back rail; (3) rib1; (4) rib2; (5) roof with integral ears; (6) left rotating end cheek + socket **assumed joined**; (7) right cheek + socket **assumed joined**. Rigid translation of each group independently relative to the remaining lid in 6 axial directions (±X ±Y ±Z) using 0.25mm sampled increments up to8mm: **42 test paths**. This is *not* full 6-DOF testing or a real load/connection test.

- Each rail and each rib meets a nominal other-part volume within 0.25–0.5mm in each straight direction.
- Roof+ears meets nominal volume in each direction, but X± first blockers are not until **2.75mm axial slip**; engagement under load remains uncertain.
- The left end/socket pair can shift X− and right end/socket pair X+ at least8mm **relative to the rest of the moving lid alone**. That result is not full-product escape: adding **stationary body, fixed pivot and outside veneer** blocks their X± travel at approx **0.55mm** in 4 tested cases.
- A mechanical stop requires the wooden boss/head, veneer and socket to be adequately attached/strong. A modeled stop alone proves neither strength nor physically possible insertion.
- **Important:** An earlier nominal direct surface contact graph identified five lid connected-contact clusters; intentional clearances 0.2–0.4mm explain this, so absence of direct contact does NOT prove unattached parts. Equally, multiple rigid collision constraints do NOT prove load transfer or enough joint retention under real operation.

**G2a/G2b BLOCKED**, G3/G4 NOT_RUN. True continuous rotation with real kerfed 4mm skin, adhesive/veneer retention, 2.1mm lip strength, shoulder wood fatigue, 24-part insertion, measured net inside≥310 and physically approved outer profile remain open.

### Files
Conversation ZIP `MEB012_LOCK_STUDY_DESIGN_ONLY.zip` SHA256 `da3339e206d3cd3f385b2c706b4776c472efeb313d964b087cfa404450253dbb` (5 files): scripts for relative motion and stationary body stops, JSON data, Hebrew summary. Requires the complete T1 source ZIP `MEB011_T1_DESIGN_ONLY.zip`, SHA256 `4ce6a132bdb7a8fea9a98739a2b1d8d65c5644e11bbad10b92944a9ddd08d335`, available to user in conversation **not** committed to GitHub.

### LEAN next
**MEB-013, P1, ChatGPT first**: define/verify positive joint/axial assembly interfaces, update *affected* CAD only. Codex if a demonstrably hard multi-part 3D assembly kernel is needed; don't start G4 or claim manufacturing authorization without qualified physical evidence and independent QA.