import eel
import sqlite3 as sql

conn = sql.connect("todo_app.db")
cur = conn.cursor()
create_table_sql = '''
    CREATE TABLE IF NOT EXISTS login (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        birthdate TEXT NOT NULL,
        gender TEXT NOT NULL
    );
    '''
cur.execute(create_table_sql)

eel.init('Web')


@eel.expose
def button_login(user_name, user_pass, user_birthdate, gender):
    insert_sql = '''
    INSERT INTO login (email, password, birthdate, gender)
    VALUES (?, ?, ?, ?);
    '''
    data = (user_name, user_pass, user_birthdate, gender)
    cur.execute(insert_sql, data)
    conn.commit()


select_sql = 'SELECT * FROM login;'
cur.execute(select_sql)
rows = cur.fetchall()
for row in rows:
    print(row)

eel.start('index.html', size=(1366, 743))
