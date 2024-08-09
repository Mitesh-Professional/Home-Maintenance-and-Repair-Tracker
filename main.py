import eel
import sqlite3 as sql


class DB:
    conn = sql.connect("todo_app.db")
    cur = conn.cursor()

    def __init__(self):
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS login (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                birthdate TEXT NOT NULL,
                gender TEXT NOT NULL
            );
            '''
        self.cur.execute(create_table_sql)

    def search_file(self, query):
        self.query = query
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def condition_search(self, query, data):
        self.query = query
        self.data = data
        self.cur.execute(query, data)
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def insert_data(self, query, data):
        self.query = query
        self.data = data
        self.cur.execute(query, data)
        self.conn.commit()

    def sql_data_check(self, query, data):
        self.query = query
        self.data = data
        self.cur.execute(query, data)
        rows = self.cur.fetchall()
        return rows


eel.init('Web')
db_conn = DB()


@eel.expose
def button_signup(user_name, user_pass, user_birthdate, gender):
    email = user_name
    sql_query = '''SELECT * FROM login WHERE email = (?)'''
    if db_conn.sql_data_check(sql_query, (email,)):
        return False
    else:
        insert_sql = '''
        INSERT INTO login (email, password, birthdate, gender)
        VALUES (?, ?, ?, ?);
        '''
        data = (user_name, user_pass, user_birthdate, gender)
        db_conn.insert_data(insert_sql, data)
        return True

@eel.expose
def button_login(user_name, user_pass):
    sql = '''SELECT * FROM login WHERE email = ? AND password = ?'''
    data = (user_name, user_pass)
    db_conn.condition_search(sql, data)
    # print(data)


select_sql = 'SELECT * FROM login;'
db_conn.search_file(select_sql)



eel.start('src/components/login_page.html', size=(1366, 743))
