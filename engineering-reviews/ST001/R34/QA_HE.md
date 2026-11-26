# ST-001 R34 — עקיבות מקור CAD ואימות ממשקים

**BLOCKED · DESIGN_ONLY / NO_CUT / NO_OCCUPANT_USE**
26.11.2026 · P0 · [משימה #130](https://github.com/mataniar0/assembl-lab-engineering/issues/130) · [דוח JSON](QA.json)

לא נמצא מקור B-rep מקורי של R30 בקבצים ובענפי המאגר שנבדקו. הקובץ הטבעי הזמין מ־R18 נפתח בהצלחה ב־FreeCAD. הוא מכיל 104 שכבות, או 88 בלי מצייני מקום, מול 72 רשתות המדווחות ב־R30. בנוסף, משפחת המסילות העליונות מסומנת B01 ב־R18 ו־B21 בדרישות R30. לכן ההתאמה הישירה של קובץ R18 ל־R30 קיבלה `FAIL`. השאלה אם יש מקור R30 נפרד מחוץ לקבצים הזמינים נשארה פתוחה.

## מלאי מקורות

| מקור | עקיבות ותוצאה |
|---|---|
| R30 GLB | SHA‑256 מדווח `fd30d431a07994b09f5b8aab76ad4b78136e7d2ba90b85e35abfbd7e51e03d5f`. דוח R33 מציין התאמה לדוחות המקומיים. קובצי R30–R33 לא נמצאו בסביבת הבדיקה הנוכחית. |
| R30 CAD | חיפוש בשמות קבצים, בקובצי סקירה ובהיסטוריית הענפים לא העלה מקור טבעי קיים או רשומת מקור–ייצוא המשייכת אותו ל־GLB. |
| R18-A-FIX | קובץ FCStd טבעי ומקור Python פרמטרי נפרד ב־commit `f6d732ecf589eda71853d0c3f54d7ae65bcdbed2`. SHA‑256 של ה־FCStd הוא `2693fd695f0ee91bf0fbc8b17c9fca725b6e93019bc80025feb2f7fc3364b8a9`. מזהי שאר קובצי הראיה ב־JSON. [מקור ותוצרים ב־PR #127](../R18A_FIX/README_HE.md) |
| R21 | דוח התצוגה מציין 80 רשתות פעילות. [דוח R21](https://github.com/mataniar0/assembl-lab-engineering/blob/b8bfe123f2a77c628f2730af3a9a1c08ed2e6843/engineering-reviews/ST001/R21_VISUAL/QA.json) |
| R33 | דוח פומבי מדווח על 72/72 רשתות תקינות, 2,556 זוגות, 28,756 השוואות ואפס חפיפות מעל סף הדגימה. התוצאה מוגבלת לחתכים שנדגמו. מניין 16 הממשקים נשאר מדווח. [תוצאת R33](https://github.com/mataniar0/assembl-lab-engineering/issues/129#issuecomment-7184936852) |

## מטריצת התאמה

| מדד | R30 לפי הראיות הזמינות | R18 שנפתח ונבדק | מצב |
|---|---|---|---|
| ספירת שכבות או רשתות | 72 מדווחות | 104 גופי שכבות, מתוכם 16 מצייני מקום | FAIL בהתאמה ישירה |
| EB ו־A01/A02 | משפחות מוזכרות | ארבע רשומות EB בקטלוג. 16 שכבות בכל אחת ממשפחות A01 ו־A02 | PARTIAL; מיפוי לשכבות R30 חסר |
| מסילות עליונות | B21 | B01; ארבע שכבות | FAIL בהתאמת המזהים |
| C01 | משפחה נדרשת | 16 שכבות | PARTIAL; חסרים מספר השכבות ומיפוי החברים ב־R30 |
| ממשקי מסילה | 16 מדווחים | 16 רשומות היסטוריות של מגע פאות קצה | PARTIAL; התאמה בין המזהים פתוחה |
| מעטפת מנורמלת | מידות וטרנספורמציית נרמול חסרות | מעטפת גוף R18 בצירי XYZ היא 422.055067×422.055067×400.000000 מ״מ בלי מצייני מקום | BLOCKED |

## מצב פרטני של 16 הממשקים

דוח R33 מציין את המספר הכולל. המזהים המקוריים והשיוך לחלקים חסרים, לכן המספרים כאן הם שורות מעקב בלבד. 16 מזהי R18, לרבות סטטוס המגע הנומינלי וסטטוס התכן ההיסטוריים, נשמרו ב־JSON לצורך השוואה כאשר יתקבל מיפוי.

| שורת מעקב | ייצוג R30 ברמת ממשק | אימות B-rep |
|---|---|---|
| 01 | BLOCKED | BLOCKED / NOT_RUN |
| 02 | BLOCKED | BLOCKED / NOT_RUN |
| 03 | BLOCKED | BLOCKED / NOT_RUN |
| 04 | BLOCKED | BLOCKED / NOT_RUN |
| 05 | BLOCKED | BLOCKED / NOT_RUN |
| 06 | BLOCKED | BLOCKED / NOT_RUN |
| 07 | BLOCKED | BLOCKED / NOT_RUN |
| 08 | BLOCKED | BLOCKED / NOT_RUN |
| 09 | BLOCKED | BLOCKED / NOT_RUN |
| 10 | BLOCKED | BLOCKED / NOT_RUN |
| 11 | BLOCKED | BLOCKED / NOT_RUN |
| 12 | BLOCKED | BLOCKED / NOT_RUN |
| 13 | BLOCKED | BLOCKED / NOT_RUN |
| 14 | BLOCKED | BLOCKED / NOT_RUN |
| 15 | BLOCKED | BLOCKED / NOT_RUN |
| 16 | BLOCKED | BLOCKED / NOT_RUN |

## בדיקת הקובץ ההיסטורי

ב־FreeCAD 1.0.0, ‏OCCT 7.8.1 ו־Python 3.13.5 נפתח ה־FCStd לקריאה. נספרו 104 מופעי `Part::Feature` ששמותיהם תואמים בדיוק ל־`LAYERS.csv`. בכל אחד נמצא מוצק יחיד, תקין לפי `Shape.isValid()`, סגור ובעל נפח חיובי. פער הנפח הגדול ביותר מול הקטלוג ההיסטורי היה כ־4.81×10⁻⁷ ממ״ק. המעטפת היא איחוד התיבות התוחמות של 88 הגופים שאינם מצייני מקום.

לשחזור, פותחים ב־FreeCAD את [קובץ ה־FCStd המקובע לגרסה](https://github.com/mataniar0/assembl-lab-engineering/blob/f6d732ecf589eda71853d0c3f54d7ae65bcdbed2/engineering-reviews/ST001/R18A_FIX/evidence/R18A_FIX_REVIEW.FCStd) ומריצים במסוף Python שלו:

```python
objects = [o for o in App.ActiveDocument.Objects if o.TypeId == "Part::Feature"]
valid = [o.Label for o in objects if len(o.Shape.Solids) == 1
         and o.Shape.isClosed() and o.Shape.isValid() and o.Shape.Volume > 0]
print(len(objects), len(valid))
```

104 מקרי טופולוגיה היסטוריים עברו, בדיקת זהות אחת עברה, ונמדדה מעטפת אחת. נקראו 16 רשומות ממשק היסטוריות. בדיקות חפיפה בין מוצקים, מסלולים ובדיקות גאומטריה חדשות ל־R30 נשארו `NOT_RUN`. בדיקות GLB של R33 נשמרו כראיה מדווחת ומספר ההרצות החוזרות שלהן הוא אפס. מספר מחזורי התיקון בגאומטריה ובתיעוד הוא אפס.

## מסירה

R34‑01 עד R34‑04 בוצעו חלקית. ביקורת העקיבות מול R33 הושלמה בתחום הקיים. שערי G0–G2 חסומים. G3/G4 מחוץ להיקף וחסומים. לביקורת ChatGPT נדרשים קובץ ה־CAD המקורי של R30 או מקור פרמטרי מקובע לגרסה, רשומת ייצוא המקשרת אותו ל־SHA-256 של ה־GLB, וראיות הכוללות את מזהי כל 16 הממשקים, שיוך החלקים, טרנספורמציית הנרמול וספי הבדיקה.
