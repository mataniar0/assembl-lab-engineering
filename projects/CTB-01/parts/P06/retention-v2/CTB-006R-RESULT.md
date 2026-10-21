# CTB-006R B1 — NO-GO: unchanged-C early-capture preflight

**Issue:** [#23](https://github.com/mataniar0/assembl-lab-engineering/issues/23) · **2026-10-21**

**Branch:** `codex/ctb-006r-retention` · **Base:** `532f8889ef8ec318908a7f08dcae2d0e3e792e92`

**DESIGN_ONLY / BLOCKED / CR_REQUIRED. IF-09/B05 remain OPEN.**

The selected Candidate 1 fails its first prerequisite with the existing geometry:
pre-positioning a C keeper at its working position obstructs the subsequent
straight Y_FIRST cheek insertion. The final cheek also does not capture the key
against upward withdrawal. **Stop B1; no B2 or replacement CAD was developed.**
This rejects the unchanged-profile, fixed-early-key sequence tested here; it does
not establish that every redesigned assembly-captive mechanism is impossible.

Scope fixed before calculation: P1; ChatGPT already selected the conditional
assembly-captive hypothesis in Issue #23. Codex's remaining question was whether
the actual C key can precede the existing cheek translation and become trapped.
The owner's current instruction authorizes this B1 despite the Issue's earlier
CTB-008 scheduling trigger. Interfaces: IF-09 (ring), IF-01 (four spacers),
IF-02 (Y_FIRST), IF-14 (assembly). No interface approval is implied.

| Focused evidence check | Actual result |
|---|---|
| Original inputs protected | **553/553** upstream files byte-identical to base; 60 source-file SHA-256 hashes and both complete inventory seals in `evidence.json`. |
| Dimensions / nearby parts | Cheeks 6 mm, inner gap 15 mm; spacers Z35/90/200/390; ring Z242..248; keys Z235..256; Y Z407..413. Key-family gaps: S3 **32 mm**, Y **151 mm**. |
| Proposed final interfaces | All six cheeks use the existing **unapproved P06 C mortise overlay**. 154 ring/key-to-base and ring-family internal finite-solid pairs: maximum overlap **0 mm³**. This is not a fit claim for original P01. |
| Early-key insertion prerequisite | **FAIL on all six interfaces**. Start at local t offset ±40 mm and final position are clear; at offset ±10 mm a real finite cheek intersects its key by **299.915806077 mm³**. Complete translation-sweep intersection is **632.374099702 mm³** per interface. |
| Upward capture prerequisite | **FAIL on all six keys**: the entire +40 mm withdrawal sweep and its endpoint have **0 mm³** overlap with the other 25 local bodies. Positive Z motion is unrestrained on this route. |
| Fixed-key / missing-key spreading control | A finite 4 mm outward cheek pose hits its held key by **332.458293624 mm³**. Remove that key: overlap with remaining ring-family parts becomes **0 mm³**. This control isolates ring restraint; other joints are not substitutes for keeper retention. |

**Six unique evidence checks verified; two design prerequisites fail.** A successful
probe exit verifies these observations, **not** successful locking. Initial
single-interface exploration and six-interface recording agreed; no geometry/code
repair was required. A documentation hygiene check flagged two Markdown trailing-
space line breaks; they were removed and the check repeated. The stored evidence
was also replayed read-only. No positive
mutual key/cheek retention, larger bearing seat or 6DOF lock is proved. Simply
clearing an unchanged straight approach also clears its exact reverse while all
other bodies stay fixed; new retention/actuation cannot be assumed from a notch.

Reproduce from repository root with the existing P06 pinned environment:

```sh
XDG_CACHE_HOME=/tmp/ctb-cache MPLCONFIGDIR=/tmp/ctb-mpl \
  /workspace/.venvs/ctb-006/bin/python projects/CTB-01/parts/P06/retention-v2/feasibility.py
```

Dependencies: [existing requirements](../src/requirements.txt). Use `--write` only
to regenerate `evidence.json`. Deliverables are this report, `feasibility.py` and
`evidence.json`; no cut profiles, renders, alternate candidate or production BOM.
No upstream file, selected geometry, spacer or frozen dimension was changed.

**Review / open decisions:** `INDEPENDENT_QA_PENDING` — ChatGPT Phase C must review
the actual evidence before any further development. No separate alternate-kernel
confirmation was commissioned for this negative feasibility finding; no positive
retention or critical collision-free capture path is asserted. The current six-
cheek `CR-CTB006-C-01` remains NOT_APPROVED. Existing 7.8 mm²/key seat and recorded
12.218968 mm geometric outer cheek land were not redesigned or recertified.
Further keeper geometry/actuation or the documented fallback requires a new lead
decision. Full upper-assembly integration, new land/seat qualification, unrelated
regressions, physical fit/kerf, strength, bearing, load and stability: **NOT_RUN**.
No G2b/G3/G4, physical cutting or manufacture approval; no self-merge.
