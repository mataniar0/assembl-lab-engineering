# CTB-008 B1 — NO_GO: slide-key self-ejection remains possible

Issue [#33](https://github.com/mataniar0/assembl-lab-engineering/issues/33), LEAN B1 only, 2026-10-21.
Branch `codex/ctb-008-upper-lock`; main baseline `98f0132423bb33adc19b14a3188a662d36e50e1a`.
**DESIGN_ONLY / CR_REQUIRED / INDEPENDENT_QA_PENDING. STOP before B2.**

One real 6 mm wooden slide-key geometry was tested with six identical proposed
P01 tongue overlays and the exact selected P07A 31-body geometry. Its two headed
ends obstruct a direct tangential pull after a 3 mm radial seating slide, but the
reverse radial slide is free. Each key can then leave its tongue and move clear
of the upper disk **with the real NO_HOLE top already closed**. This candidate
does not positively retain itself; a held key is not a valid locking assumption.
This finding concerns this candidate, not every possible wood lock.

P1; ChatGPT's Phase A selected the through-slot slide-key hypothesis. Scope was
IF-12/B01, affected IF-04/05 and assembly B02; actual P01/P04/P05/P07A reused.
CTB-006R/IF-09/B05 remain independently OPEN; no ring was added to this assembly.

**Single proposed CR, NOT_APPROVED: `CR-CTB008-B1-01`.** All six identical tongues
extend from Z488 to **493.8**, retain the 1 mm tip radius, and receive one rounded
R0.2 through-slot at local r50..64, Z486..492.4. Remaining side lands are 5 mm;
roof land is only **1.4 mm**, unqualified for strength. The key occupies
Z486.2..492.2, leaving 1.8 mm to top underside Z494; tongue-tip clearance is 0.2 mm.
Its exact flat contour, mirrored/rotated positions and motion coordinates are in
`evidence.json`. No P04/P05/P07 change is proposed. The original 2 mm exposed
head cannot contain this 6 mm through-key; the example extension to Z492 would
still leave **−0.4 mm** roof for this slot. Neither is a second CAD alternative.

| Focused check | Evidence / result |
|---|---|
| Protected originals | **556/556** files match main; 60 source hashes and both complete inventory seals recorded. Frozen Ø350/H500/top50 and H800×W440 stock remain unchanged. |
| One candidate / six interfaces | Valid connected profiles and positive-volume bodies; 31 original bodies, 6 cheek replacements, 6 added keys = **37** proposed bodies. |
| Final interfaces | All **366** finite-body pairs involving changed parts: maximum overlap **0 mm³**. Unchanged pairs were not replayed. |
| Key installation | All six routes clear: lower at outward q40 from bottom Z520, slide q40→0, then seat r+3. Exact continuous material sweeps, not pose-only tests. |
| Top closing / late access | Top closes with maximum numerical overlap **7×10⁻⁹ mm³**, below epsilon 10⁻⁶. Late vertical key feed intersects P07T by **882.985397747 mm³** per key. |
| Self-ejection — **FAIL** | Direct q+1 pull hits a cheek by **13.386349387 mm³**; nevertheless r−3 → q+40 → r+60 is clear for every key, including endpoints, with all other real parts and the top fixed. Keys become unseated and clear the disk footprint inside the cavity. No hand/tool/physical handling proof is claimed. |
| Tongue withdrawal negative | With its key artificially held, each actual tongue's ±1 mm axial sweep hits the key by about **28.8 mm³**. Missing key: disk-only overlap **0** in both directions. Conditional restraint does not survive free key escape. |
| Actual upper-disk movement | U's +1 mm sweep hits held keys by up to **87.968227998 mm³**. Once keys clear U, it instead hits existing **P05** by **6.569951616 mm³**; that obstruction is not a P08 lock. The first +0.1 mm is clear of non-key parts. Disk axial retention is **not resolved by this candidate**. |

**8 unique evidence checks verified; the self-retention design requirement FAILS.**
No geometry repair or further candidate was developed. Initial disk testing found
that keys withdrawn by q40 still overlie U (117.731386366 mm³ conditional contact).
One control refinement checked the additional r+60 clearance path, exposing the
separate P05 obstruction instead of crediting loose keys with disk retention.
Two evidence builds and one read-only replay cover the same eight checks, not
additional unique tests. No software failure occurred.

Reproduce using the existing pinned P07 environment, from repository root:

```sh
XDG_CACHE_HOME=/tmp/ctb-cache MPLCONFIGDIR=/tmp/ctb-mpl \
  /workspace/.venvs/ctb-007/bin/python projects/CTB-01/parts/P08/b1/feasibility.py
```

[Dependencies](../../P07/src/requirements.txt); `--write` regenerates `evidence.json`.
Only this report, `feasibility.py` and coordinate/proof `evidence.json` are delivered.
No upstream model/export was overwritten; no DXF/PNG/GLB or fallback was produced.
No unrelated regression suite ran. This is implementer evidence, not independent QA.
ChatGPT Phase C must independently review it; no positive capture solution or G2b
claim is made, so no alternate-kernel validation was commissioned for this NO_GO.

**Single lead decision needed:** whether to authorize a revised coordinated
P01/P08 capture topology that prevents this reversible unseating; do not advance
this candidate to B2. Material/kerf, physical access/fit, roof strength, bearing,
adhesive, load/stability, full G2b, G3/G4 and cutting/manufacture remain
**NOT_RUN / NOT_APPROVED**. IF-12/B01 and B02 remain OPEN. No self-merge.

## Independent engineering-lead QA addendum — 2026-10-21

**Result:** `B1_NEGATIVE_EVIDENCE_ACCEPTED / DESIGN_ONLY / CR_REQUIRED`, **94/100 for the limited NO-GO proof only**. Engineering-lead COMMENT review is attached to [PR #40](https://github.com/mataniar0/assembl-lab-engineering/pull/40).

The earlier `INDEPENDENT_QA_PENDING` describes the PR state on initial Codex delivery. The lead independently parsed and checked the stored data with **12/12 data-consistency assertions**, reviewed its geometry code and unchanged-source Git diff; **did not independently rerun a second CAD kernel or conduct physical checks**. All eight implementer checks validate recorded observations—not functioning locks. Six within-cavity reverse paths are geometrically free despite P07T closed, **not evidence of physical spontaneous release**. The amended conclusion rejects ONLY the proposed reversible slide-key and thin-roof P01 extension as unqualified; it does not reject every wooden retainer.

`CR-CTB008-B1-01 NOT_APPROVED; IF-12/B01/B02 OPEN`. Preserve the separate `CTB-006R/IF-09/B05` blocker and future six-cheek unified source requirement. Merging this data report does not approve manufacturing, cutting, functional retention, prototype, G2b, G3, or G4.
