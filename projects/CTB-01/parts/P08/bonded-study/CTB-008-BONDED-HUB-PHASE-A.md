# CTB-008 — Phase A / permanent bonded upper hub, zero new P08 parts (DESIGN_ONLY)

**Date:** 2026-10-21 · **Issue:** [#33](https://github.com/mataniar0/assembl-lab-engineering/issues/33) · **Priority:** P1 · **Executor:** ChatGPT alone for source geometry/requirements; Codex only if changed 3D geometry actually arises.
**Working assumption requested by owner:** the permanent **P06 mid-ring** bond is assumed to pass strength qualification **for progressing project planning**. This is NOT an actual passed test, and DOES NOT establish strength or permission for a **different P08/top hub** adhesive interface. Owner previously accepted permanently bonded **P06**, not yet expressly approved permanent bonding of the upper P04 hub. P08 remains a candidate/owner-decision item.

## Chosen single lower-complexity concept — `P08_BONDED_DUAL_DISK_V1`

Replace failed mechanically free P08 slide keys (PR #40) and the unanchored floating P08B plate (Issue #33) with **direct structural bonds from each of six P01 upper tongues to BOTH existing P04L and P04U slotted disks**, plus qualified links from the disk/rib network to P07B/P07T skins. No additional wooden P08 parts; do not cut thin 1.4mm slot roofs, extend tongue tips or add central top access holes.

**Key distinction:** this is *not* a self-retaining positive mechanical lock. It is a proposed **permanent adhesive load-path architecture**. IF-12/B01 acceptance language would need explicit owner-reviewed functional change request from "positive mechanical keeper" to "qualified permanent bonded fixation" before this concept could satisfy the requirement. If owner requires tool-free disassembly or an independent mechanical lock, this candidate is NOT a substitute.

### Source-based geometry facts

Frozen exterior: tabletop Ø350mm, top H500mm/50mm thick, six identical nominal6mm P01 cheeks at 3×120°, upper tongue r45..69, t centre±10.5, Z488 tip. P04L Ø190 nominal6mm Z456..462, P04U Ø190 nominal6mm Z480..486, lower skin P07B Z450..456, continuous **NO_HOLE** upper skin P07T Z494..500, six P05 radial webs r81..169 / Z456..494.

Source SVG blobs: `parts/P04/variants/A/P04U.svg` **3db35260806cb3830b4a6ac65e352edcf70eec39** and `P04L.svg` **c76099efb4daf86e17ac027cf976d69ee0eae0fc**. Each contains six real rounded tongue slots, bounds in leg-local coordinates r44.8..69.2 / t7.4..13.6 and symmetric negatives/rotations, with **0.2mm nominal radial clearance and0.1mm tangential clearance on either side**, six identical slot perimeters≈**60.8546mm** determined by independent traversal of 36-vertex SVG polygons. Existing P04 dimension JSON reports tongue penetration through all6mm of each slab; the P01 profile ends Z488 and spans both layers. Per nominal6mm slab, **6×60.8546×6≈2,190.77mm² total geometric cut-slot wall envelope**. Both slabs total≈**4,381.53mm² wall envelope** (not proven actually wetted, aligned, in wood-to-wood contact or mechanically effective). The upper tongue finishes **2mm above P04U top Z486**, and **6mm below P07T underside Z494**. **P04U to upper skin = 8mm empty vertical separation**; no automatic tip-to-top-skin retention.

The selected 31-body P07A model **already contains all six cheeks, two disks, six webs, two skins and two curved rim parts**. P08 adds ZERO physical CAD solids in this proposal. The nominal *bonded P06* would add ONE mid-ring, giving **32 nominal wooden bodies excluding adhesive/fixtures**. This is a hypothetical BOM and excludes any future load path reinforcement changes.

### Structural load-path graph — distinct links must be qualified
1. `P01→P04L` and `P01→P04U`: separate 12 six-mm through-wall adhesive interfaces (IF04/05). Must block P01 longitudinal/up/down slip; mere numerical 0.1/0.2mm air is not a bond. Ends r=45/69 include edge-to-face and exposed ply layers; prove compatible adhesive/measured bond-line and actual loads including shear, peel and sustained eccentric loads.
2. `P04L→P07B`: nominal coplanar disk-bottom-to-skin-top interface Z456, previously reported ~26,899mm² projected area; without an appropriate bonded structural joint these pieces are not secured. Check actual coverage and support/fixture.
3. `P04U→P05→P07T/P07B`: the upper disk has **NO direct top-skin contact (Z486→494 gap8)**. Its connection must be proved via actual P05-to-disk notches / rib engagement and/or another reviewed upper-disk-to-structure feature. Selected P05 A's disk-to-web notches are OPEN and have unverified 0.2mm clearance; rib-to-skin projected top/bottom land ~516mm² PER rib per skin only, not strength/bond rating. **Do not credit incidental P05 collision in PR#40 as glue or positive axial disk stop**.
4. `P07R→skins` bent rim is an independent unqualified physical joint; P05-to-rim ≈1.97–2mm AIR is NOT glue. Tabletop strength/tipping/finished stock remain outside this Phase A.

This is a **topologically connected potential bonded graph only if ALL claimed connections exist and are independently qualified**. Proving P01→disks alone cannot validate disk→skins uplift or whole tabletop action. Acceptable assembly timing is proposed `Y_FIRST→P07B→P04L→P04U→P05→rim→P07T` (same original selected P07A geometry/motion order; bonding operations and cure-fixture accessibility NOT PROVED). No new P08 insertion motion exists.

### Lean reuse and required checks

**Existing geometry reuse:** No active P01 upper tongue, P04 disk, P05, P07 or P08 solid changes; prior P07A 31-body valid finite assembly paths are **geometrically unchanged** for this candidate alone. Do NOT pay Codex to replay the same static collision calculations merely because joints are now annotated "glued". However, the **future P06_C_BONDED_TABS CR alters P01 at Z≈245** and needs versioned unified cheek revalidation under CTB-009, and treating adhesive as physical material/process is outside previous rigid CAD paths.

**Minimal design acceptance checklist (not yet passing):**
- [ ] Owner approves a **non-disassemblable upper hub** and revised IF12/B01 function (not just P06 glue).
- [ ] Qualified P01↔P04L and P01↔P04U actual bond areas, tolerances, plywood fiber orientation, material specifications and shear/peel/fatigue envelope.
- [ ] Qualified P04L↔P07B and P04U↔P05↔skins **actual** structural restraint against disk +Z / separation; distinguish top skin from upper disk.
- [ ] Actual safe full table force transfer, stability and upper skin/rim joints; do not infer from geometric perimeter.
- [ ] Compatible versioned `P01` with proposed P06 ring mortise (all six IDENTICAL) and any necessary upper hub modifications; if P08 remains unmodified, this is a single mid-z cheek source CR only.
- [ ] Physical material/adhesive and fitting evidence at G3 and manufacturing release G4 before use, none of which are covered by owner's *planning assumption*.

**Recommendation:** advance `P08_BONDED_DUAL_DISK_V1` as **phase-A concept** and obtain owner's decision on whether the *upper* joint may also be permanent. Then ChatGPT can refine the interface/structural QA specification; **no Codex B1 justified yet** because no new solid geometry is being requested. Only schedule Codex one-site finite CAD if a versioned disk/cheek/connector geometry change is demonstrably required.

**Unclosed:** `IF-12/B01/B02 OPEN`, `IF-08/IF-06/IF-07` structural bonding OPEN, `P06 IF-09/B05 CONDITIONAL`, `G2b/G3/G4 NOT_APPROVED`, no cutting/production authorization. Historical failed mechanical P08 key remains archived in [PR #40](https://github.com/mataniar0/assembl-lab-engineering/pull/40).
