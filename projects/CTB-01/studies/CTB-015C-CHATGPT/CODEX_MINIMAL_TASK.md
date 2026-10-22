# B1-only next Codex task: CTB-015C alternative two-seam rim closure

**P1; CHATGPT FIRST executed:** source geometry retained, route concepts A/B and DXF metadata fix authored and preliminary raw DXF token QA complete.

Inputs: `projects/CTB-01/studies/CTB-015-B1/RESULT.md`, `verify_b1.py`, `evidence.json`, corrected rim vector masters `CTB-015-CHATGPT`, and metadata-only DXFs `CTB-015C-CHATGPT`. CTB-012 P07T/P07B unchanged.

Deliver a bounded GO/REVISE/NO-GO decision on a **complete closure/assembly route**, not just zero overlap at the final static pose:
1. Independently load and audit both candidate updated DXFs with standard ezdxf, ensure geometry matches unchanged corresponding CTB-015 SVGs; report unresolved warnings precisely.
2. Evaluate if candidate B's **horizontal, symmetric, rigid movement of BOTH half-rim arcs** can continuously close BOTH opposite male/female seams, with lower skin/core represented. Use the existing PR61 OCC joint-solids and only necessary scene/motion checks. Include actual motion parameterization and credible continuous clearance/sweep verification. If no rigid 6DOF path demonstrated, do not label GO.
3. For candidate A state explicitly whether it depends on unknown material bending/deformation and why ideal rigid existing solids cannot qualify it, rather than simulate unmeasured material behavior.
4. Record first collision/blocked point where applicable; exact suite count, errors and fixes. Independent separate check of scope.
5. STOP AFTER B1. No sources changed, no full-table regression, no production release, no nesting, no self merge.

If B is not demonstrated and A remains deformation dependent, return REVISE/NO-GO so ChatGPT can explore versioned joinery/sequence revisions before CTB-016.
