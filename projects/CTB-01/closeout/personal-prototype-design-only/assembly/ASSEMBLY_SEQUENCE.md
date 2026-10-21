# Conceptual assembly — DESIGN_ONLY

Coordinates: right-handed XYZ mm, floor Z0; legs L1/L2/L3 at 0/120/240 degrees. Local t positive CCW. Sheet labels are exact body IDs; map each ID through BOM/instances.csv. No parts are rotated in sheet plans.

Initial ring pre-position +31 CAD translations are inherited from B2, NOT rerun. Offsets are relative to final assembly position, in global XYZ. This is not a validated physical glue/cure/fixture procedure.

| Step | Body / sheet label | Start offset XYZ mm → final (0,0,0) |
|---:|---|---|
| 0 | P06_BONDED | Pre-position Z242..248; temporary support/access UNPROVED |
| 1 | P03 | [0, 0, 113] |
| 2 | L1_P01_1 | [0.0, -40.0, 0] |
| 3 | L1_S1 | [-0.0, 40.0, 0] |
| 4 | L1_S2 | [-0.0, 40.0, 0] |
| 5 | L1_S3 | [-0.0, 40.0, 0] |
| 6 | L1_S4 | [-0.0, 40.0, 0] |
| 7 | L1_P01_2 | [-0.0, 40.0, 0] |
| 8 | L2_P01_1 | [34.64101615137755, 19.999999999999993, 0] |
| 9 | L2_S1 | [-34.64101615137755, -19.999999999999993, 0] |
| 10 | L2_S2 | [-34.64101615137755, -19.999999999999993, 0] |
| 11 | L2_S3 | [-34.64101615137755, -19.999999999999993, 0] |
| 12 | L2_S4 | [-34.64101615137755, -19.999999999999993, 0] |
| 13 | L2_P01_2 | [-34.64101615137755, -19.999999999999993, 0] |
| 14 | L3_P01_1 | [-34.641016151377535, 20.000000000000018, 0] |
| 15 | L3_S1 | [34.641016151377535, -20.000000000000018, 0] |
| 16 | L3_S2 | [34.641016151377535, -20.000000000000018, 0] |
| 17 | L3_S3 | [34.641016151377535, -20.000000000000018, 0] |
| 18 | L3_S4 | [34.641016151377535, -20.000000000000018, 0] |
| 19 | L3_P01_2 | [34.641016151377535, -20.000000000000018, 0] |
| 20 | P07B | [0, 0, 70] |
| 21 | P04L | [0, 0, 64] |
| 22 | P04U | [0, 0, 40] |
| 23 | P05_1 | [100.0, 0.0, 0] |
| 24 | P05_2 | [50.000000000000014, 86.60254037844386, 0] |
| 25 | P05_3 | [-49.99999999999998, 86.60254037844388, 0] |
| 26 | P05_4 | [-100.0, 1.2246467991473532e-14, 0] |
| 27 | P05_5 | [-50.00000000000004, -86.60254037844383, 0] |
| 28 | P05_6 | [50.000000000000014, -86.60254037844386, 0] |
| 29 | P07R1 | [0, 0, 70] |
| 30 | P07R2 | [0, 0, 70] |
| 31 | P07T | [0, 0, 46] |

P01_1 centers t=-10.5 and P01_2 t=+10.5, 6mm thick, gap15mm. S1=reinforced P02B Z35, S2 Z90, S3 Z200, S4 Z390. All P01 use one identical master. Place ring, then Y_FIRST, cheek/spacers per leg, bottom skin BEFORE disks, six radial ribs BEFORE rim, solid top last. P07R1/2 are identical flat profiles but distinct assembly phases15/195 degrees; use verified B2 scene for spatial orientation. No P08 keys.

P04U↔P05 ~0.2mm AIR; P04U→top 8mm AIR; ribs↔rim ~1.97287mm AIR. No adhesive bridge, continuous structural load path or strength proven. Rim is ideal pre-bent geometry only; bend length/neutral axis uncalibrated. Glue application/cure/access/fixtures, actual fit/kerf, loads/stability NOT_RUN. G3_NOT_PERFORMED_OWNER_DEFERRED; G4_BLOCKED.
