# CTB-010 — computational final-file QA

**PASS / DESIGN_ONLY / CHATGPT_LEAD_REVIEW_PENDING**.
This is implementer-run file QA with separate parsers, not independent reviewer signoff.
Priority P1; user requested stage3 onward; B1/B2/OpenCASCADE reruns **0**.

94 unique named cases: 94 PASS,
0 FAIL, including 5 true corrupt-file controls.
Groups: source12; master DXF/SVG22; sheet DXF/SVG16; placement32;
BOM/provenance/sequence/frozen7; negative5. Repeated executions are not new cases.
Execution attempts and all initial failures/corrections belong in execution-history.json
and the delivery review; 3 verifier attempts currently recorded.

32 wood instances, 12 roles, 11 cut masters. Stock sheets: {6: 7, 4: 1}.
Portrait WIDTH440 × HEIGHT800, provisional edge margin10 and inter-part gap5mm.
Every final DXF/SVG is re-imported (ezdxf / minidom, no exporter import), with
units, closed/simple loops, no duplicates/orphan holes/common-line cuts, native
contour fidelity, 1:1 bounds, stock separation, actual outer-envelope spacing
and BOM/source mapping checked. Negative controls corrupt a real duplicate
cut, omit a rim slot, alter SVG scale, move cuts outside bed and remove a BOM
placement; all must be rejected. Detailed metrics and actual checked-file
digests are in file-evidence.json. Hash/ZIP sealing is a subsequent packaging check.

Inherited evidence: PR49 B2 and PR53 secondary CAD, with accepted source hashes.
One initial B2 checker repair and one secondary isolation-checker repair are
historical and are NOT new failures/runs here. Their recorded 782/222 and 569
pair/control cases are NOT added to the new file-QA count. GLB is byte-identical
to the validated candidate; no model rebuild or new renderer ran.

G2b final decision remains for ChatGPT. Material thickness/grain/flex axis/kerf,
physical fit/bending/glue/cure/fixture/access, load and stability NOT_RUN.
G3_NOT_PERFORMED_OWNER_DEFERRED; G4_BLOCKED. No physical cut/use approval,
no certification claim and no self-merge. Inspect README, manifest, BOM,
ASSEMBLY_SEQUENCE and the downloadable ZIP for the complete bounded handoff.

Post-QA repository-format check: Git flagged CSV CRLF endings. One format-only repair normalized3 tables to LF;3 targeted checks proved identical parsed rows and reconstructed original digests. See packaging-evidence.json. No failed file-suite cases or CAD/source repairs;94 unique cases unchanged, no full suite/kernel rerun.
