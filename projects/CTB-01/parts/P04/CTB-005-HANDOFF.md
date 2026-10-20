# CTB-005 input contract v1 — proposed interfaces, DESIGN_ONLY

Pending engineering-lead selection. Six webs, never an extra hidden spacer or seventh rib.
Actual final P05 CAD is CTB-005 scope; files `witness-*.{svg,dxf,png}` are finite-thickness
interface witnesses only, not P05 release. Actual21-body model excludes all six witnesses.
Use global XYZ; each web has local r outward, t tangent, z upward, angles0/60/120/180/240/300.
Nominal plywood6 along t. All proposed fits unmeasured; B10/IF-08 remain open.

Shared web envelope r81..169, Z456..494, height38. Disks R95, L456..462, U480..486;
free face gap18, pitch24, remaining8 to top-skin underside494. Web outer ends r169 leave
2mm nominal to skin radius171; no attachment to skin/wall is designed. Core envelope alone
is not a finished tabletop. No geometry may cross skins without a new coordinated proposal.

| Candidate | Angles | Exact disk cuts / matching witness | Required order after base and bottom-skin envelope |
|---|---|---|---|
| A | all six OPEN | L r80.8..96.5, U r82.8..96.5, t±3.2. Witness r81..169,Z456..494 minus r81..83,Z479.8..486.2 | L → U → six OPEN radially inward100mm; before wall/top closure |
| B | all six RAIL | L closed r81.3..88.7, U r81.8..88.2, t±3.2. Witness union: full-height rail r82..88, full-height body r95.4..169, bridge r81..95.4,Z466..472 | L → six RAIL vertically down64mm → U; top remains open |
| C | OPEN0/120/240; RAIL60/180/300 | respective A/B interfaces; upper centerØ24 provisional inspection study, lower none | L → three RAIL down64mm → U → three OPEN inward100mm |

Machine-readable RZ/XY loops and exact start/end vectors are in `variants/*/*-dimensions.json`,
`connections-and-paths.json` and `assembly/proofs.json`. Witnesses are connected profiles,
not a floating tab and not an imagined uncut38mm rectangle. The uncut rectangle collides.
Lower/upper cuts intentionally differ. OPEN upper relief leaves 0.2mm radial gap and 0.2mm
vertical relief at upper-disk faces; lower fits0.2mm radially. RAIL end gaps L0.7/U0.2mm,
outerbody-to-circle0.4mm, bridge-to-Ltop4/bridge-to-Ubottom8mm. All web t gaps0.2mm/side.
At clearance the nominal contact area is zero; effective bearing, glue bond and preload are
unverified. Disk-layer overlap along height is6mm, not a tested adhesive engagement rating.

A recommended only for simple accessible assembly; open notches provide no positive radial
capture. B has topological radial capture but narrow6mm rail/bridge stress concentrations
and requires fixtures/staged insertion. C adds two web families and a nonessential provisional
hole; recommend no center hole absent demonstrated function. Ø24/Ø36 studies derive from
an assumed20mm probe with2/8mm radial allowance, not a measured tool or approved opening.
No Ø60 center opening is inherited from imagery.

B01/IF-12 positive tongue lock is **CTB-008**, not supplied by these sliding disks.
B06/IF-06 final web topology, fillets, glue/mounting, grain, tolerance stack and fixture access
remain CTB-005 dependencies; B02 whole assembly, B10 material/kerf and B11 loads stay open.
The rail witness's6mm bridge and OPEN relief need structural review and physical coupons.
CTB-007 must coordinate bottom-skin-before-disks and leave rim/top open for web/lock access.
No current P05/P07 upstream file has been changed; any selected counterpart revision must
be versioned and independently rechecked. No production/physical cutting authorization.
