import mysql.connector
from tkinter import messagebox
from tkinter import Tk

try:
    conn = mysql.connector.connect(user='qaimmiah', password='Goldenhill1', host='db4free.net',
                                                               database='pyorbit_db')
    cursor = conn.cursor()
    print('Connected to the database')
except:
    window = Tk()
    window.withdraw()
    messagebox.showerror(message='Error! Could not connect to the database')
    quit()
    window.mainloop()

def create_table_users():
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS USERS
                  (USER_ID   VARCHAR(15)   NOT NULL,
                   ACCESS BOOLEAN  NOT NULL,
                   PASSWORD CHAR(32) NOT NULL,
                   PRIMARY KEY(USER_ID));
                   ''')

        conn.commit()



        print('table USERS created successfully')

    except:
        messagebox.showerror(message='Error! Could not connect to the database')

def create_table_requests():
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS REQUESTS
                (USER_ID   VARCHAR(15)   NOT NULL PRIMARY KEY,
                REQUEST  VARCHAR(20) NOT NULL,
                FOREIGN KEY(USER_ID) REFERENCES USERS(USER_ID));
                ''')
        # Primary key USER_ID from USERS table used here as foreign key
        # Can do this as the tables have a one-to-one relationship
        conn.commit()
        print('table REQUESTS created successfully')

    except:
        messagebox.showerror(message='Error! Could not connect to the database')

# def insert_user(id, password):
#     script = "INSERT INTO USERS (USER_ID, ACCESS, PASSWORD) \
#              VALUES (%s, %s, %s);"
#     hashed_encrypt = hashlib.md5(password.encode())
#     hashed_password = hashed_encrypt.hexdigest()
#
#     cursor.execute(script, (id, True, hashed_password))
#     conn.commit()
#
#
# def insert_request(id, request):
#     script = "INSERT INTO REQUESTS (USER_ID, REQUEST) \
#              VALUES (%s, %s);"
#     cursor.execute(script, (id, request))
#     conn.commit()
#
# def count_records(table):
#     cursor.execute("SELECT * from " + table)
#     return len(cursor.fetchall())
#
# def num_of_records(access_type):
#     cursor.execute("SELECT * from USERS where ACCESS=%s", (access_type,))
#     return len(cursor.fetchall())
#
# def show_request_records():
#     cursor.execute("SELECT * from REQUESTS")
#     return cursor.fetchall()
#
#
#
#
#
# def delete_record(table, id):
#     cursor.execute("DELETE FROM " + table + " WHERE USER_ID=%s", (id,))
#     conn.commit()
#
# def access_permition(id, type):
#     cursor.execute("UPDATE USERS SET ACCESS = " + str(type) + " WHERE USER_ID=%s", (id,))
#     conn.commit()
#
#
# def drop(table):
#     cursor.execute('DROP TABLE ' + table)
#     conn.commit()
#
# def is_unique_id(id):
#     cursor.execute("SELECT USER_ID FROM USERS;")
#     for record in cursor.fetchall():
#         if id == record[0]:
#             return False
#     return True
#
# x = [('Admin01', '66436c1419633969515bcbd98a4a5951')]
#
#
#
#
#
#
# def username_exists_check(id, table):
#     cursor.execute("SELECT USER_ID from " + table)
#     for record in cursor.fetchall():
#         if id == record[0]:
#             return True
#     return False
#
# def user_has_access(id):
#     if username_exists_check(id, 'USERS'):
#         cursor.execute("SELECT ACCESS from USERS where USER_ID = %s", (id,))
#         for record in cursor.fetchall():
#             if record[0] == 0:
#                 return False
#         return True
#     return False
# #
# is_unique_id('Admin01')
# # username_exists_check('Admin01', 'USERS')
# # count_records('USERS')
# # drop('REQUESTS')
# # drop('USERS')
# # create_table_users()
# # create_table_requests()
# # insert_user('PyAdmin727', '328782')
#
