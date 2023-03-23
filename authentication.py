from database_init import conn, cursor
import hashlib

def user_exists(id, password):
    cursor.execute("SELECT USER_ID, PASSWORD FROM USERS")
    hashed_encrypt = hashlib.md5(password.encode())
    hashed_password = hashed_encrypt.hexdigest()
    for record in cursor.fetchall():
        if id == record[0]:
            if hashed_password == record[1]:
                return True
    return False

def username_exists(id, table):
    print(id)
    cursor.execute("SELECT USER_ID FROM " + table) # gets all user IDs from a table
    for record in cursor.fetchall():
        if id == record[0]:
            return True
    return False

def user_has_access(id):
    cursor.execute("SELECT ACCESS from USERS where USER_ID = %s", (id,))
    for record in cursor.fetchall():
        if record[0] == 1: # record[0]: Access boolean
            return True
    return False
# print(user_has_access('mytest3'))
#

def authenticated_login(id, password):
    if user_exists(id, password):
        if user_has_access(id):
            return True
    else:
        return False