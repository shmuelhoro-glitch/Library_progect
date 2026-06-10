# פרויקט ניהול ספרייה


## ניהול ספרייה באמצעות קריאות HTTP וניהול הנתונים  ב (data-base) MYSQL
משתמש בfast-api 
#
**ספרים**

המערכת מאפשרת להכניס ספרים חדשים לספרייה, לעדכן פרטים, קבלת רשימת הספרים ואפשרות לראות ספר לפי הid :
כמו כן יש אפשרות לעדכן האם הספר מושאל כרגע או לא 
#
**חברים**

כמו כן המערכת מאפשרת גם את ניהול החברים בספריה הוספה, עדכון פרטים, הפעלה והשבתה
#
ניתן גם לקבל את רשימת החברים המלאה או חבר מסוים לפי הid שלו
#
**דוחות**

ניתן לקבל דוח כללי על המצב הנוכחי 

אפשר לקבל דוח ספרים לפי ז'אנר 

וגם ניתן לבדוק מי החבר הכי פעיל !
#
## הקוד ליצירת ה docker : 
```docker run --name mysql-w8 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=library_db -p 3306:3306 -d mysql:8```
#

## הקוד ליצירת הdatabase
#### לפתיחת הקובץ דרך שורת הפקודה : 
```docker exec -it mysql-w8 mysql -uroot -proot```

#### בוחרים בדאטה-בייס המבוקש:
```USE library_db;```

#### יצירת הטבלה "books"  באופן ידני:
```CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(50) NOT NULL, author VARCHAR(50) NOT NULL, genre ENUM( 'Fiction', 'Non-Fiction', 'Science', 'History', 'Other' ) NOT NULL , is_available BOOLEAN DEFAULT TRUE, borrowed_by_member_id INT DEFAULT NULL);```



#### יצירת הטבלה "members"  באופן ידני:
```CREATE TABLE IF NOT EXISTS members (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NOT NULL, email VARCHAR(50) UNIQUE NOT NULL, is_active BOOLEAN DEFAULT TRUE, total_borrows INT NOT NULL);```



## הוראות הרצה
אחרי שמריצים את השורות של בניית הקונטיינר יש שתי אופציות להריץ את התוכנית
או לכתוב בשורת הפקודה ```uvicorn main:app --reload``` -> ואז לשלוח קריאות תקינות בהתאם לטבלת הקריאות (או פתיחת הסוואגר ```localhost:8000/docs```)




## מבנה התיקיות הוא

    library-api/
        │
        │
        ├── main.py
        ├── database/
        │ ├── db_connection.py
        │ ├── book_db.py
        │ └── member_db.py
        ├── routes/
        │ ├── book_routes.py
        │ ├── member_routes.py
        │ └── report_routes.py
        ├── logs/
        │ └── app.log
        │
        ├── README.md
        ├── requirements.txt
        └── .gitignore

    
#

## מבנה הטבלאות


### טבלת `books` — שדות

| שדה | הסבר |
| ----- | ----: |
| `id` | מפתח ראשי |
| `title` | כותרת הספר, עמודה לא ריקה, מקסימום 50 תווים |
| `author` | שם המחבר, עמודה לא ריקה, מקסימום 50 תווים |
| `genre` | **ערכי `genre` מותרים:**  Fiction | Non-Fiction | Science | History | Other — מומש כעמודת ENUM במסד הנתונים, כל ערך אחר מחזיר שגיאה, עמודה לא ריקה |
| `is_available` | האם הספר זמין להשאלה — FALSE מסמן הושאל עמודה לא ריקה |
| `borrowed_by_member_id` | מזהה החבר שמחזיק את הספר — NULL אם זמין |

### טבלת `members` — שדות

| שדה | הסבר |
| ----- | ----: |
| `id` | מפתח ראשי |
| `name` | שם החבר, עמודה לא ריקה, מקסימום 50 תווים |
| `email` | כתובת מייל — ייחודית, עמודה לא ריקה |
| `is_active` | האם החבר פעיל — FALSE לא יכול להשאיל עמודה לא ריקה |
| `total_borrows` | מונה סה"כ השאלות — עולה ב-1 בכל השאלה עמודה לא ריקה |

## מודול פייטון database

### `db_connection.py` — פונקציות

| פונקציה | תפקיד |
| ----- | ----: |
| `get_connection` | יוצר חיבור ל-MySQL — כל מחלקת DB משתמשת בה |
| `create_tables` | יוצר את טבלאות `books` ו-`members` אם לא קיימות — רץ בעליית השרת, בתחילת פונק main |

### מחלקות OOP — `BookDB`

אחראי על כל פעולות SQL מול טבלת `books`.

| מתודה | מי קורא לה | מה היא עושה |
| ----- | ----- | ----- |
| `create_book(data)` | `POST /books` | INSERT לטבלת books — `is_available=True`, `borrowed_by=NULL` |
| `get_all_books()` | `GET /books` | מחזירה רשימת כל הספרים |
| `get_book_by_id(id)` | `GET /books/{id}` | מחזירה ספר אחד על פי ID או None |
| `update_book(id, data)` | `PUT /books/{id}` | מעדכן שדות שנשלחו |
| `set_available(id, val, member_id)` | `PUT /books/{id}/return/{member_id} PUT /books/{id}/borrow/{member_id}` | מעדכן `is_available` ו-`borrowed_by_member_id` |
| `count_total_books()` | `GET /reports/summary` | סופר את סך כל הספרים במסד הנתונים |
| `count_available_books()` | `GET /reports/summary` | סופר ספרים עם `is_available=True` |
| `count_borrowed_books()` | `GET /reports/summary` | סופר ספרים עם `is_available=False` |
| `count_by_genre(genre)` | `GET /reports/books-by-genre` | סופר ספרים לפי ז'אנר |
| `count_active_borrows_by_member(member_id)` | `PUT /books/{id}/borrow/{member_id}` | סופר כמה ספרים החבר מחזיק כרגע (לאכיפת חוק 7\) — ספירת books עם borrowed\_by\_member\_id השווה ל-member\_id |

## 

## חוקי מערכת

| חוק | נושא | הכלל |
| ----: | ----: | ----: |
| 1 | יצירת ספר | המשתמש שולח title/author/genre — המערכת מוסיפה `is_available=True`, `borrowed_by=NULL` |
| 2 | genre | חייב להיות Fiction / Non-Fiction / Science / History / Other — כל ערך אחר מחזיר שגיאה יש לוודא הן בהוספה (POST) והן בעדכון (PATCH) |
| 3 | יצירת חבר | המשתמש שולח name/email — המערכת מוסיפה `is_active=True`, `total_borrows=0` |
| 4 | email | חייב להיות ייחודי — אם קיים כבר מחזיר שגיאה |
| 5 | חבר לא פעיל | אם `is_active=False` — אי אפשר להשאיל ספר |
| 6 | ספר לא זמין | אי אפשר להשאיל ספר שכבר מושאל (`is_available=False`) |
| 7 | מקסימום ספרים | חבר לא יכול להחזיק יותר מ-3 ספרים בו-זמנית |
| 8 | החזרת ספר | ניתן להחזיר ספר רק אם הוא מושאל לאותו חבר שמחזיר אותו |

## Logging

פורמט חובה:  
time | level | message

חובה לכתוב לוג:

- לוג בתחילת כל REST   
- לוג לפני עדכונים מול SQL  
- לוג במקרה של שגיאה  
- לוג בסיום כל REST 



## רשימת endpoints

### Books

| Method | Endpoint | תיאור |
| :---- | :---- | :---- |
| `POST` | `/books` | יצירת ספר |
| `GET` | `/books` | כל הספרים |
| `GET` | `/books/{id}` | ספר לפי ID |
| `PATCH` | `/books/{id}` | עדכון ספר |
| `PATCH` | `/books/{id}/borrow/{member_id}` | השאלת ספר לחבר |
| `PATCH` | `/books/{id}/return/{member_id}` | החזרת ספר מחבר |

### Members

| Method | Endpoint | תיאור |
| :---- | :---- | ----: |
| `POST` | `/members` | יצירת חבר |
| `GET` | `/members` | כל החברים |
| `GET` | `/members/{id}` | חבר לפי ID |
| `PATCH` | `/members/{id}` | עדכון חבר |
| `PATCH` | `/members/{id}/deactivate` | השבתת חבר |
| `PATCH` | `/members/{id}/activate` | הפעלת חבר |

### Reports

| Method | Endpoint | תיאור |
| :---- | :---- | ----- |
| `GET` | `/reports/summary` | דוח כללי |
| `GET` | `/reports/books-by-genre` | ספרים לפי ז'אנר |
| `GET` | `/reports/top-member` | החבר הכי פעיל |

##

## זרימת הנתונים

לקוח מבצע קריאה לשרת -> הקריאה מגיעה לראוטר שמעביר למודול המתאים -> אם הקריאה היא יצירה או עדכון ולידציה ראשונה על הקלט מתבצעת באמצעות pydantic -> קריאות קבלת נתונים ללא סינון מועברות ישר לפונקציה המתאימה שקוראת מהדאטה ומחזירה את הדרוש, ואם זה קריאה שצריכה לקבל מסנן או כל דבר אחר שדורש וולידציה אז הפונקציה מהקריאה תעביר לוולידציה שתבקש ממודול הדאטה את הנתונים ותחזיר ללקוח





