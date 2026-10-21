# CTB-006R C2 — local B1 GO, anti-return OPEN

Issue [#23](https://github.com/mataniar0/assembl-lab-engineering/issues/23), 2026-10-21.
Branch `codex/ctb-006r-c2-keyway-b1`, base `98f0132423bb33adc19b14a3188a662d36e50e1a`.
**LOCAL_G1_GEOMETRY_PLAUSIBLE / ANTI_T_RETURN_OPEN / DESIGN_ONLY / CR_REQUIRED.**

Only **one positive-t C2 key, one actual P01 C-mortise proposal and one local ring
terminal** were tested, with the nearest actual S3 and selected P03 Y as obstacles.
Existing parametric CAD/fillet functions are reused; no six-cheek assembly was built.
This is computational local feasibility, not independent QA, a G1 approval, a
self-locking joint, or whole-ring/whole-table validation.

Scope fixed by ChatGPT Phase A: P1, IF-09/B05 primary, IF-01/02/14 affected;
one C2 hypothesis, no fallback. Original selected sources remain unchanged.
The terminal widening 26.5→35 mm, stepped aperture and dual-head key are a
**P06-local PROPOSED / NOT_APPROVED CR**; the existing P01 ring mortise remains
`CR-CTB006-C-01 NOT_APPROVED`. Future coordinated P01 changes with P08 require review.

Geometry follows the updated Issue: r0=112.017645918429 mm; loading center r0−3.8,
parking center r0+2.6; radial key thickness6; bottom head Z235..241.8,
neck241.8..248.2, top head248.2..255; ring242..248. Actual source fillets: keyR0.4,
portalR0.2, terminalR0.5. Exact profiles and stage offsets are in `evidence.json`.

| Local case | Actual evidence |
|---|---|
| Three insertion movements | Lower +40→0 in Z; then +r6.4; then +t5.0. **Each complete swept solid has 0 mm³ overlap** with the ring, cheek, S3 and Y. Final key and ring-to-cheek/S3/Y pairs also have 0 overlap. |
| Direct ±Z40 | Ring obstruction **133.200000107 mm³** in either direction. |
| Direct −r6.4 / +r6.4 / +t5 | Ring obstruction **18.592824748 / 223.246472238 / 158.444976079 mm³**, respectively. |
| Reverse −t5 — OPEN | Complete swept volume is clear; anti-return is unsolved. Reverse −t5→−r6.4→+Z40 is clear throughout. |
| Shorter release — OPEN | After −t5, **+Z40 is already clear at the parked radial center**; radial return is unnecessary for this release route. |
| Cheek spreading | **5.2 mm free gap at parking**, versus 0.2 at loading. A 4 mm outward cheek sweep is clear even with key held. At6 mm the held key obstructs by64.858293750 mm³; removing it gives0. The key is held only for this diagnostic, not assumed anchored. |
| Actual material / stock screen | Minimum loading-head projection clearance is **0.198289 mm**; parked filleted-neck clearance≈0.200000 mm. The loading value is0.001711 mm below nominal0.2, within the source0.002 mm arc-chord discretization tolerance; no measured fit is claimed. Minimum portal-to-terminal outer boundary≈6.00000008 mm; radial end lands6.0/7.2, portal outer-t land9.7, head outer-t land6.0. Existing section-derived cheek exterior land≈12.218968 mm. Key and one-terminal-updated ring envelope fit H800×W440 with10 mm screening margins; **not nesting or production approval**. |
| Real filleted shoulders | Available flat planar overlap **19.8 mm² per head**, not the unfilleted22.2 estimate. At nominal position there is a0.2 mm Z air gap: this is potential geometric seating after gap closure, **not actual nominal contact or load capacity**. |

**16/16 unique local path/pose cases matched their stated expectations**, including
the deliberately open release paths; seven profile/stock predicates passed and
three ring-to-existing-part pairs were clear. No failed CAD attempt or geometry
repair. Three evidence builds (one removed a redundant upstream contour copy;
one added explicit contour-clearance measurements) and one read-only replay
repeat the same cases, not new tests.
All556 protected upstream tracked paths have an empty diff against base; source
SHA-256 values are recorded. No old regression suites ran.

Reproduce from repository root in the existing P06 pinned environment:

```sh
XDG_CACHE_HOME=/tmp/ctb-cache MPLCONFIGDIR=/tmp/ctb-mpl \
  /workspace/.venvs/ctb-006/bin/python projects/CTB-01/parts/P06/c2-keyway-b1/probe.py
```

Use `--write` only to regenerate JSON; dependencies are in [P06 requirements](../src/requirements.txt).
Only `probe.py`, `evidence.json` and this report are delivered. No images, DXF,
manufacturing files, six-side scaling or full regression. Rotations/combined
6DOF release, tolerances/kerf, fixtures, strength and physical trials are NOT_RUN.

**ChatGPT review needed:** resolve tangential anti-return and the 5.2 mm parked
cheek free travel before choosing further CAD work or a unified P01/P08 CR.
`INDEPENDENT_QA_PENDING`; second-kernel proof remains deferred under the Issue
because no affirmative full-retention/G2b claim is made. IF-09/B05 stay OPEN;
G2b/G3/G4, cutting and manufacture remain NOT_APPROVED. Stop after B1; no merge.

## Independent lead QA addendum — 2026-10-21

**Reviewed by ChatGPT, separate read-only code/data inspection:** **94/100 for the narrow local feasibility evidence only**, attached to [PR #43](https://github.com/mataniar0/assembl-lab-engineering/pull/43). All **16/16 stored path/pose cases** have matching expected outcomes, and **7/7 profile predicates** are true; source/diff and the 3 unaffected original-ring interface screens were inspected. The implementer's source-integrity seals were not independently rerun in a separate working tree, and **no second CAD kernel was executed** by this reviewer.

**No functional lock approval:** `−t5` permits the simple `+Z40` shortcut and the full reverse disassembly; even a HELD key allows 4mm outward cheek travel (parked free5.2mm). The 19.8mm²/head shoulder is separated by nominal0.2mm air and has no proven physical bearing. All actual P01/P06 changes remain `PROPOSED/NOT_APPROVED`, `IF-09/B05` OPEN, `G2b/G3/G4` NOT_APPROVED. Merge is for keeping evidence, not acceptance of a new lock.
