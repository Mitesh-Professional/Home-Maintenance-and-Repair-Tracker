import eel
import sqlite3 as sql
import bcrypt
import os


class DB:
    conn = sql.connect("home_maintenance_and_repair_tracker.db")
    cur = conn.cursor()
    user_info = ""

    def __init__(self):
        create_table_sql = '''
                CREATE TABLE IF NOT EXISTS login (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                gender TEXT NOT NULL,
                status BOOLEAN NOT NULL DEFAULT FALSE,
                birthdate TEXT NOT NULL);'''
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

    def hash_password(self, password):
        self.password = password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    def verify_password(self, user_pass, stored_pass):
        self.user_pass = user_pass
        self.stored_pass = stored_pass
        return bcrypt.checkpw(user_pass.encode('utf-8'), stored_pass.encode('utf-8'))


eel.init('Web')
db_conn = DB()


@eel.expose
def button_signup(user_name, user_email, user_pass, user_birthdate, gender):
    email = user_name
    sql_query = '''SELECT * FROM login WHERE email = (?)'''
    if db_conn.sql_data_check(sql_query, (email,)):
        return False
    else:
        insert_sql = '''
        INSERT INTO login (username, email, password,gender,birthdate)
        VALUES (?, ?, ?, ?, ?);
        '''
        password = db_conn.hash_password(user_pass)
        data = (user_name, user_email, password, gender, user_birthdate)
        db_conn.insert_data(insert_sql, data)
        return True


@eel.expose
def button_login(user_email, user_pass):
    sql = '''SELECT * FROM login WHERE email = ? OR password = ?'''

    hashed_password = bcrypt.hashpw(user_pass.encode('utf-8'), bcrypt.gensalt())

    data = (user_email, hashed_password)

    user_info = db_conn.sql_data_check(sql, data)

    if db_conn.sql_data_check(sql, data):
        if user_email == user_info[0][2] and db_conn.verify_password(user_pass, user_info[0][3]):
            db_conn.user_info = {'UserName': user_info[0][1], 'Email': user_info[0][2], 'Status': user_info[0][5]}
            return {'UserName': user_info[0][1], 'Email': user_info[0][2], 'User_Verification': True}
        elif not db_conn.verify_password(user_pass, user_info[0][3]):
            return {'User_Verification': False, 'Info': 'Your Password is incorrect.'}
    else:
        print(db_conn.user_info)
        return {'User_Verification': False, 'Info': 'Your email ID or password is incorrect.'}


@eel.expose
def user_profile_info():
    return db_conn.user_info


# select_sql = 'SELECT * FROM login;'
# db_conn.search_file(select_sql)
#
# print(db_conn.user_info)
eel.start('src/components/login_page.html', size=(1366, 743))
