import sqlite3, hashlib
from tkinter import messagebox

request_pointer = 0
conn = sqlite3.connect('users.db')

def create_table_users():
    conn.execute('''CREATE TABLE IF NOT EXISTS USERS
              (ID   CHAR(15)   NOT NULL,
               DOB  DATE         NOT NULL,
               FIRSTNAME CHAR(15) NOT NULL,
               SURNAME CHAR(15) NOT NULL,
               EMAIL  CHAR(40),
               ACCESS BOOLEAN NOT NULL,
               PASSWORD CHAR(30) NOT NULL,
               PRIMARY KEY(ID));
               ''')
    conn.commit()

def create_table_requests():
    conn.execute('''CREATE TABLE IF NOT EXISTS REQUESTS
                (ID   CHAR(15)   NOT NULL,
                REQUEST  CHAR(20) NOT NULL,
                APPROVED BOOLEAN  NOT NULL,
                PRIMARY KEY(ID));
                ''')
    conn.commit()
def insert_record_users(id, dob, firstname, surname, password):
    script = "INSERT INTO USERS (ID, DOB, FIRSTNAME, SURNAME, EMAIL, ACCESS, PASSWORD) \
             VALUES (?, ?, ?, ?, ?, ?, ?);"
    conn.execute(script, (id, dob, firstname, surname, None, True, password))
    conn.commit()



def insert_record_requests(id, request, approved):
    script = "INSERT INTO REQUESTS (ID, REQUEST, APPROVED) \
             VALUES (?, ?, ?);"
    conn.execute(script, (id, request, approved))
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
print(show_request_records())




def delete_record(table, id):
    conn.execute("DELETE FROM " + table + " WHERE ID=?", (id,))
    conn.commit()

def access_permition(id, type):
    conn.execute("UPDATE USERS SET ACCESS = " + str(type) + " WHERE ID=?", (id,))
    conn.commit()


def drop(table):
    conn.execute('DROP TABLE ' + table)
    conn.commit()

def is_unique_id(id):
    cursor = conn.execute("SELECT ID from USERS")
    for record in cursor:
        if id == record[0]:
            return False
    return True





def user_exists(id, password):
    cursor = conn.execute("SELECT ID, PASSWORD from USERS")
    hashed_encrypt = hashlib.md5(password.encode())
    hashed_password = hashed_encrypt.hexdigest()
    for record in cursor:
        if id == record[0]:
            if hashed_password == record[1]:
                return True
    return False

def username_exists_check(id, table):
    cursor = conn.execute("SELECT ID from " + table)
    for record in cursor:
        if id == record[0]:
            return True
    return False

def user_has_access(id):
    cursor = conn.execute("SELECT ACCESS from USERS where ID = ?", (id,))
    for record in cursor:
        if record[0] == 0:
            return False
    return True



create_table_users()
create_table_requests()
