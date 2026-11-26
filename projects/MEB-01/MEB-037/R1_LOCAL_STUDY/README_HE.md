# MEB-037-R1 B — ארכיון מועמד CAD (25.11.2026)

**DESIGN_ONLY / PARTIAL_ARCHIVE / INDEPENDENT_QA_PENDING**. גרסת התכנון העדכנית לעיון, לאחר אישור כיוון בעל המוצר ב-Issue #125. לא גרסת ייצור.

## תיעוד וראיות
- [דוח ביצוע מקומי](LOCAL_REVIEW_RESULTS.md) ו-[סיכום תוצאות](QA_SUMMARY.json).
- [מצאי מלא של חבילת המקור, SHA-256 ומצב העברה](ARTIFACT_MANIFEST.json).
- [דוח מועמד מקורי מלא](candidate_R2_result.json), [בדיקת R6 וירטואלית](R6_virtual_QA.json), [בקרות תקלה](negative_controls_QA.json), [סיווג 26 מגעים](contact_review.csv).
- קוד שחזור מודל CAD נומינלי: source_profiles_compact.json, review.py, build_candidate_review.py. שלושת הקבצים ודוחות הבדיקה המפורטים נשמרו ונבדקו מול מזהי Git blob של חבילת המקור.
- 7/28 פריטי החבילה המקורית נשמרו בהתאמת בתים. מקור CadQuery 2.8.0, numpy, shapely; לא בוצעה הרצה חדשה מתוך המאגר. קובצי STEP, שלושה GLB, שלושה PNG, ZIP ויתר קובצי הראיות טרם הועלו. אין להציג דגמי MEB-037 ההיסטוריים כאילו היו R1 B.
- מקור ה-ZIP: MEB037_R1_B_CAD_review.zip; SHA256 379c4db838ab13fe8893afe22abf81fb4bd02bd99a95f186e0e2ef96c45bea4d.

## סטטוס תכנון
20 חלקים, 190 זוגות, אפס חדירות חיוביות בסף הבדיקה, עשרה אזורי לשוניות ללא חדירה. תוצאות נומינליות בלבד; R6, מגע וסבולות פיזיות וביקורת בלתי תלויה עדיין פתוחים. G3 NOT_RUN, G4 BLOCKED. אין שחרור לייצור.

PR #128 נשאר טיוטה; הגרסאות ההיסטוריות נשמרות.
