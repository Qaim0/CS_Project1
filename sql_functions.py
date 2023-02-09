import sqlite3, hashlib
from tkinter import messagebox

request_pointer = 0
conn = sqlite3.connect('SolarSys.db')

def create_table_users():
    conn.execute('''CREATE TABLE IF NOT EXISTS USERS
              (USER_ID   CHAR(15)   NOT NULL,
               ACCESS BOOLEAN  NOT NULL,
               PASSWORD CHAR(30) NOT NULL,
               PRIMARY KEY(USER_ID));
               ''')
    conn.commit()

def create_table_requests():
    conn.execute('''CREATE TABLE IF NOT EXISTS REQUESTS
                (USER_ID   CHAR(15)   NOT NULL,
                REQUEST  CHAR(20) NOT NULL,
                FOREIGN KEY(USER_ID) REFERENCES USERS(USER_ID));
                ''') # DONT NEED PRIMARY KEY AS FOREIGN KEY WILL STILL BE UNIQUE
    conn.commit()
def insert_record_users(id, password):
    script = "INSERT INTO USERS (USER_ID, ACCESS, PASSWORD) \
             VALUES (?, ?, ?);"
    hashed_encrypt = hashlib.md5(password.encode())
    hashed_password = hashed_encrypt.hexdigest()
    conn.execute(script, (id, True, hashed_password))
    conn.commit()



def insert_record_requests(id, request):
    script = "INSERT INTO REQUESTS (USER_ID, REQUEST) \
             VALUES (?, ?);"
    conn.execute(script, (id, request))
    conn.commit()

def count_records(table):
    cursor = conn.execute("SELECT * from " + table)
    return len(cursor.fetchall())

def num_of_records(access_type):
    cursor = conn.execute("SELECT * from USERS where ACCESS=?", (access_type,))
    return len(cursor.fetchall())

def show_request_records():
    cursor = conn.execute("SELECT * from REQUESTS")
    return cursor.fetchall()





def delete_record(table, id):
    conn.execute("DELETE FROM " + table + " WHERE USER_ID=?", (id,))
    conn.commit()

def access_permition(id, type):
    conn.execute("UPDATE USERS SET ACCESS = " + str(type) + " WHERE USER_ID=?", (id,))
    conn.commit()


def drop(table):
    conn.execute('DROP TABLE ' + table)
    conn.commit()

def is_unique_id(id):
    cursor = conn.execute("SELECT USER_ID from USERS")
    for record in cursor:
        if id == record[0]:
            return False
    return True





def user_exists(id, password):
    cursor = conn.execute("SELECT USER_ID, PASSWORD from USERS")
    hashed_encrypt = hashlib.md5(password.encode())
    hashed_password = hashed_encrypt.hexdigest()
    for record in cursor:
        if id == record[0]:
            if hashed_password == record[1]:
                return True
    return False

def username_exists_check(id, table):
    cursor = conn.execute("SELECT USER_ID from " + table)
    for record in cursor:
        if id == record[0]:
            return True
    return False

def user_has_access(id):
    cursor = conn.execute("SELECT ACCESS from USERS where USER_ID = ?", (id,))
    for record in cursor:
        if record[0] == 0:
            return False
    return True

print(user_has_access('hello'))
# drop('USERS')
# drop('REQUESTS')
# create_table_users()
# create_table_requests()
# insert_record_users('Admin01', '328782')

