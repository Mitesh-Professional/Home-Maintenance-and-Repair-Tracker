import eel
import sqlite3 as sql
import bcrypt
import os


class DB:
    conn = sql.connect("home_maintenance_and_repair_tracker.db")
    cur = conn.cursor()
    user_info = ""
    path_directory = os.getcwd().replace('/', '//')

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
        create_table_user_mode = '''CREATE TABLE IF NOT EXISTS user_mode(user_id INTEGER,mode_id INTEGER,FOREIGN KEY(user_id) REFERENCES login(id), FOREIGN KEY(mode_id) REFERENCES mode(mode_id),PRIMARY KEY(user_id, mode_id))'''
        self.cur.execute(create_table_user_mode)
        create_table_mode = '''CREATE TABLE IF NOT EXISTS mode(mode_id INTEGER PRIMARY KEY AUTOINCREMENT,mode_name TEXT NOT NULL)'''
        self.cur.execute(create_table_mode)

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
        rows = self.cur.fetchone()
        return rows

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

    def cookies_store(self, user_email, user_pass, username, status, id, mode):
        self.user_email = user_email
        self.user_pass = user_pass
        self.username = username
        self.status = status
        self.id = id
        self.mode = mode
        dics = {
            'ID': id,
            'Status': status,
            'UserName': username,
            'Email': user_email,
            'User_Password': user_pass,
            'Mode': mode
        }
        path = f'{db_conn.path_directory}//Web//src//'
        directory = 'Cookies'
        path_final = os.path.join(path, directory)
        if not os.path.exists(path_final):
            os.mkdir(path_final)
            with open(os.path.join(path_final, 'cookies.txt'), 'w') as fp:
                for (key, value) in dics.items():
                    fp.write(f'{key}: {value} \n')

    def update(self, bol):
        self.bol = bol
        if bol:
            query = '''UPDATE mode SET mode_name = ? WHERE mode_id = ?'''
            mode = "dark"
            mode_id = db_conn.user_info.get('Id')
            db_conn.cur.execute(query, (mode, mode_id))
            db_conn.conn.commit()
            # db_conn.conn.close()
        else:
            query = '''UPDATE mode SET mode_name = ? WHERE mode_id = ?'''
            mode = "default"
            mode_id = db_conn.user_info.get('Id')
            db_conn.cur.execute(query, (mode, mode_id))
            db_conn.conn.commit()
            # db_conn.conn.close()

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
        last_login_id = db_conn.cur.lastrowid
        insert_mode = '''INSERT INTO mode (mode_name) VALUES (?)'''
        data = "default"
        db_conn.insert_data(insert_mode, (data,))
        last_mode_id = db_conn.cur.lastrowid
        insert_user_mode = '''INSERT INTO user_mode (user_id, mode_id) VALUES (?,?)'''
        db_conn.insert_data(insert_user_mode, (last_login_id, last_mode_id))
        return True


@eel.expose
def button_login(user_email, user_pass):
    sql = '''SELECT * FROM login WHERE email = ? OR password = ?'''

    hashed_password = bcrypt.hashpw(user_pass.encode('utf-8'), bcrypt.gensalt())

    data = (user_email, hashed_password)

    user_info = db_conn.sql_data_check(sql, data)
    if db_conn.sql_data_check(sql, data):
        # print(user_info)
        if user_email == user_info[0][2] and db_conn.verify_password(user_pass, user_info[0][3]):
            id = user_info[0][0]
            sql_query = '''SELECT mode.mode_name  FROM login INNER JOIN user_mode ON login.id = user_mode.user_id INNER JOIN mode ON user_mode.mode_id = mode.mode_id WHERE id = ?'''
            value = db_conn.condition_search(sql_query, (id,))
            db_conn.user_info = {'Id': user_info[0][0], 'UserName': user_info[0][1], 'Email': user_info[0][2],
                                 'Status': user_info[0][5],'Mode': value[0]}
            db_conn.cookies_store(user_info[0][2], user_info[0][3], user_info[0][1], user_info[0][5], user_info[0][0],
                                  value[0])
            return {'UserName': user_info[0][1], 'Email': user_info[0][2], 'User_Verification': True, 'Mode': value[0]}
        elif not db_conn.verify_password(user_pass, user_info[0][3]):
            return {'User_Verification': False, 'Info': 'Your Password is incorrect.'}
    else:
        print(db_conn.user_info)
        return {'User_Verification': False, 'Info': 'Your email ID or password is incorrect.'}


# print(db_conn.path_directory)
@eel.expose
def user_profile_info():
    return db_conn.user_info


@eel.expose
def sign_out():
    path = f'{db_conn.path_directory}//Web//src//Cookies//'
    file = f'{db_conn.path_directory}//Web//src//Cookies//cookies.txt'
    if os.path.exists(path):
        os.remove(file)
        os.rmdir(path)
        return True
    db_conn.conn.close()

@eel.expose
def dark_mode(bol):
    db_conn.update(bol)
    id = db_conn.user_info.get('Id')
    # print(db_conn.user_info)
    sql_query = '''SELECT mode.mode_name  FROM login INNER JOIN user_mode ON login.id = user_mode.user_id INNER JOIN mode ON user_mode.mode_id = mode.mode_id WHERE id = ?'''
    value = db_conn.condition_search(sql_query, (id,))
    # print(value)
    file_path = f'{db_conn.path_directory}//Web//src//Cookies//cookies.txt'
    search_key = 'Mode'
    with open(file_path, 'r') as file:
        lines = file.readlines()
    updated = False
    updated_lines = []
    for line in lines:
        if search_key in line:
            if "Mode: default" == line:
                updated_lines.append(f'{search_key.split(": ")[0]}: {"dark"}\n')
            else:
                updated_lines.append(f'{search_key.split(": ")[0]}: {"default"}\n')
            updated = True
        else:
            updated_lines.append(line)
    if not updated:
        print(f"'{search_key}' not found in the file.")
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)


path = f'{db_conn.path_directory}//Web//src//Cookies//cookies.txt'
if (os.path.exists(path)):
    dic = {}
    with open(path, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ', 1)
            dic[key] = value
    db_conn.user_info = dic
    eel.start('src/components/home.html', size=(1366, 743))
else:
    eel.start('src/components/login_page.html', size=(1366, 743))
