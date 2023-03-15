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

# set variables to desired test values
#
# id = ''
# request = ''
#
# script = "INSERT INTO REQUESTS (USER_ID, REQUEST) \
#          VALUES (%s, %s);"
# # attempt to insert into the database
#
# cursor.execute(script, (id, request))
# conn.commit()
# print('Record has been created')
# #
