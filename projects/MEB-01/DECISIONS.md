# MEB-01 Decision log
| Decision | Status | Rationale |
|---|---|---|
| MEB-D-001: V8.2.2 is the referenced legacy source | APPROVED_FOR_INTAKE | New work starts from most recent archived DXF and reports, not V8.1 or rendered concept |
| MEB-D-002: Preserve original DXF and audit evidence unchanged | APPROVED_FOR_INTAKE | Provenance and reversibility |
| MEB-D-003: New geometric files have status DESIGN_ONLY unless approved at subsequent gates | APPROVED | Playbook / gates |
| MEB-D-004: Target stock HEIGHT800 × WIDTH440mm | APPROVED_REQUIREMENT | Product owner explicit chat decision2026-10-20; legacy nesting not approved |
| MEB-D-005: Required opening110deg | APPROVED_REQUIREMENT | Product owner explicit chat decision2026-10-20; actual motion NOT_RUN |
| MEB-D-006: Chosen construction/physical adhesive and bend process | OPEN | Actual fit and strength evidence absent |

No other old dimension is frozen by this document. Important changes to aesthetics, functionality, material, and risk need owner decision.

MEB-D-007: frame and coordinate-parameter reference in `proposals/G0-reference/` is PROPOSED for lead review only. Owner decisions D004/D005 freeze requirements, not performance or geometry. Future changes require a reviewed CR; these decisions do not authorize cutting.

## Owner decision — MEB-D-008 (2026-10-20): minimum usable inside length

**APPROVED_REQUIREMENT:** **שומרים על אורך פנימי שימושי של לפחות 310 מ״מ לאורך ציר X** עבור מגילת אסתר. זו דרישת חלל נטו, לאחר פריטי קצה, ציר, מחזיקים וכל בליטה לחלל; אינה נמדדת רק בין שני מישורים נומינליים ללא אביזרים. הדיוק והמיקום הסופיים יוגדרו בחוזה G0, והבטחת שימושיות פיזית תיבדק ב־G3. זה אינו אישור לחלל ברוחב/גובה 65 מ״מ שטרם נבדק בפועל.

**DESIGN CONSEQUENCES:**
- חלופת חוץ 322 מ״מ תוך שמירת מכלולי הציר הקיימים (פנים נומינלי 288 מ״מ) **REJECTED_BY_REQUIREMENT**.
- חלופת חוץ 322 מ״מ / פנים 310 מ״מ נשארת **RESEARCH_ONLY** ותחייב תכנון מחדש של הקצוות והציר.
- חלופת חוץ 346 מ״מ / פנים נומינלי 312 מ״מ ב־H1 v0.3 היא **WORKING_CANDIDATE**, לא אורך חיצוני מאושר סופית. יש לאמת נפח נטו כולל בליטות, הוצאת מגילה, חוזק הציר ומעטפת חוץ.
- אין לשנות את דרישות ה־800×440 מ״מ ואת פתיחת 110°.

**OPEN:** אורך חוץ סופי, מרווח טיפול מעבר לממד מגילה מדוד, עובי חומר/kerf ומכניקה; אין לאשר G1/G2/G3/G4 על בסיס קביעה זו בלבד.
