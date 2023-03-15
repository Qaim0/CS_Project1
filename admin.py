from tkinter import *
import hashlib
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
import random
from validation import validate_user_details
from database_init import conn, cursor
from authentication import username_exists

my_grey = "#333333"
my_orange = "#ee8968"


def submit_request_decision(w, intvariables, id_lst):
    request_lst = show_request_records()  # get list of requests

    for i in range(len(intvariables)):  # for every intvariable in intvariable list
        value = intvariables[i].get()  # intvar value: 0 or 1
        current_id = id_lst[i]  # the current ID in the ID list

        if value == 0:  # if accept checkbox selected
            delete_record("REQUESTS", current_id)  # delete record from requests
            change_access(current_id, True)  # give access to user

        else:  # if deny checkbox selected
            delete_record("REQUESTS", current_id)  # delete record from requests
    # refresh admin window
    w.destroy()
    admin_window()


# ======================= TESTING ADMIN WINDOW #####################################
def admin_window():
    # Initialising frames
    f1 = f2 = f3 = f4 = f5 = 0
    # Initialising List of frames
    frames = [f1, f2, f3, f4, f5]
    # Tabs
    frame_options = ["Database overview", "Create account", "Manage account", "User requests"]

    # creating window
    window = Toplevel()
    window.geometry("800x400")
    window.title("Admin Window")
    window.config(bg=my_grey)
    window.resizable(width=0, height=0)
    window.mainloop()

    # creating notebook
    notebook = ttk.Notebook(window)

    for i in range(4):
        frames[i] = Frame(notebook, bg='grey', width=900, height=500, background=my_grey)
        notebook.add(frames[i], text=f'{frame_options[i]}')

    # display notebook
    notebook.pack()
    window.mainloop()

    # creating database overview page
    overview_page(frames[0])

    window.mainloop()
    # creating account creation page
    create_account_page(frames[1])
    # creating account management page
    manage_account_page(frames[2])
    # creating user request page
    request_page(frames[3], window)
    window.mainloop()

    # Create the overview page


# def admin_window():
#     global frames
#     # Initialising frames
#     f1 = f2 = f3 = f4 = f5 = 0
#     # Initialising List of frames
#     frames = [f1, f2, f3, f4, f5]
#
#     # w.destroy()
#     window = Toplevel()
#     window.geometry("800x400")
#     window.title("Admin Window")
#     window.config(bg=my_grey')
#
#     notebook = ttk.Notebook(window, style='lefttab.TNotebook')
#     #
#     frame_options = ["Database overview", "Create account", "Manage account", "User requests"]
#     longest = max(frame_options, key=len)
#     # length = len(longest)
#     for i in range(4):
#         frames[i] = Frame(notebook, bg='grey', width=900, height=500,background="#333333")
#         notebook.add(frames[i], text=f'{frame_options[i]}')
#
#
#     #
#     # refresh_btn = Button(frame4, text="REFRESH", padx=5, pady=5, width=10, bg=my_orange, fg="white",
#     #                      font=(my_font, 12, 'bold'), command=lambda :refresh(window))
#     # refresh_btn.place(x=350, y=320)
#
#     create_account_page(frames[1]) # creating account page
#     overview_page(frames[0])
#     manage_account_page1(frames[2])
#
#
#     notebook.pack(expand=True, fill="both")
#
#     request_page(window)
#     window.mainloop()


def request_page(frame, w):
    y = 110
    x = 40
    request_id_lst = []  # initialise list of user IDs that sent requests
    checkbox_lst = []  # initialise list of checkboxes
    int_vars = []  # initialise list of intvariables
    page_labels = ["ID", "    Request", "Accept / deny"]  # description labels

    # title label
    Label(frame, text="User Requests", width=20, font=("Gotham", 20, 'bold'),
          fg="white", bg=my_grey).place(x=250, y=20)
    # display description labels
    for i in range(3):
        Label(frame, text=page_labels[i], font=("Gotham", 12), fg=my_orange, bg=my_grey) \
            .place(x=x, y=80)
        x += 295

    # submit button
    submit = Button(frame, text="SUBMIT", padx=5, pady=5, width=10, bg=my_orange, fg="white",
                    font=("Gotham", 12, 'bold'),
                    command=lambda: submit_request_decision(w, int_vars, request_id_lst))
    # display submit button
    submit.place(x=650, y=320)

    for x in range(0, count_requests()):  # iterate for every request in REQUESTS table
        request_lst = show_request_records()  # generate request list
        request_id_lst.append(request_lst[x][0])

        # display user ID and request for every request
        Label(frame, text=f"{request_lst[x][0]}",
              font=("Gotham", 12), fg="white", bg=my_grey).place(x=20, y=y)

        Label(frame, text=f"{request_lst[x][1]}",
              font=("Gotham", 12), fg="white", bg=my_grey).place(x=320, y=y)

        # # creating an intvariable for every request
        k = IntVar()
        int_vars.append(k)
        # accept and deny checkboxes for every request
        checkbox1 = Checkbutton(frame, onvalue=0, text="Accept", variable=k)
        checkbox2 = Checkbutton(frame, onvalue=1, text="Deny", variable=k)

        # displaying check buttons
        checkbox1.place(x=600, y=y)
        checkbox2.place(x=700, y=y)
        # appending to checkbox list
        checkbox_lst.append(checkbox1)
        checkbox_lst.append(checkbox2)
        # lowering widgets for next iteration
        y += 40


# def generate_id(firstname, surname):
#     user_id = '' # initialise user ID
#     unique = False
#     while not unique: # keep creating new ID until unique
#         try:
#             random_num = random.randint(100, 999) # generates random number between 100 and 999
#             user_id = f"{surname[0:4]}{firstname[0].lower()}{random_num}"
#         if is_unique_id(user_id):
#             unique = True
#     return user_id


def create_account(entry1, entry2, entry3):
    user_id = ''  # initialise user ID
    firstname = entry1.get()  # get inputted first name
    surname = entry2.get()  # get inputted surname
    unique = False
    if not validate_user_details(firstname, surname):  # if entered details invalid
        return  # exit the function
    dob = entry3.get()
    dob = dob.split("/")  # split DOB into 3 item list [day, month, year]

    while not unique:  # keep creating new ID until unique
        try:
            random_num = random.randint(100, 999)  # generates random number between 100 and 999
            user_id = f"{surname[0:4]}{firstname[0].lower()}{random_num}"
            password = f"Py{dob[0]}{dob[1]}{dob[2]}"
            insert_user(user_id, password)  # will return error if not unique
            messagebox.showinfo(message=f"User ID: {user_id}\n\n"
                                        f"password: {password}")
            unique = True
        except:  # if the generated user ID not unique
            pass  # do nothing


# def change_tab():
#     notebook.select(frames[3])


def apply_option(id, option):
    error = False
    if not username_exists(id, "USERS") or id == "PyAdmin727":  # invalid user IDs
        error = True
    else:  # valid user ID
        if option.get() == 0:  # if delete account radiobutton selected
            answer = messagebox.askquestion(
                message=f"ID: {id}\n Would you like to delete this account?")
            if answer == "yes":
                delete_record("USERS", id)  # delete user from the users table
                if username_exists(id, "REQUESTS"):
                    delete_record("REQUESTS", id)  # delete user from requests table
                messagebox.showinfo(message="Account has been deleted")
        elif option.get() == 1:  # if restrict access radiobutton selected
            answer = messagebox.askquestion(
                message=f"ID: {id}\n Would you like to deny access for this account?")
            if answer == "yes":
                change_access(id, False)  # restrict access
                messagebox.showinfo(message="Account no longer has access")
        elif option.get() == 2:  # if allow access radiobutton selected
            answer = messagebox.askquestion(
                message=f"ID: {id}\n Would you like to grant access for this account?")
            if answer == "yes":
                change_access(id, True)  # allow access
                messagebox.showinfo(message="Account now has access")

    if error:
        messagebox.showerror(message="User does not exist")


# def create_account_page(frame):
#     main_label = Label(frame, text="Create an account", width=20, font=("Gotham", 20, 'bold'), fg="white", bg=my_grey")
#     firstname = Label(frame, text="Firstname", font=("Gotham", 9), fg=my_orange, bg=my_grey)
#     surname = Label(frame, text="Surname", font=("Gotham", 9), fg=my_orange, bg=my_grey) # fg = blue, bg= perfect grey
#     dob = Label(frame, text="DoB", font=("Gotham", 9), fg=my_orange, bg=my_grey)
#     submit = Button(frame,text="Create", padx=5, pady=5, width=10, bg=my_orange, fg="white", font=(my_font, 12, 'bold'), command=lambda :create_account(entry1, entry2, dob_entry))
#
#
#
#     main_label.place(x=250, y=20)
#     firstname.place(x=250, y=85)
#     surname.place(x=250, y=175)
#     dob.place(x=250, y=270)
#     submit.place(x=350, y=330)
#     entry1 = Entry(frame, width=20, font=("Gotham", 15), fg=my_grey) # firstname
#     entry2 = Entry(frame,width=20, font=("Gotham", 15), fg=my_grey) # surname
#     dob_entry = DateEntry(frame, width=33, background=my_grey, foreground="white", maxdate=date.today())
#
#     entry1.place(x=250, y=110)
#     entry2.place(x=250, y=200)
#     dob_entry.place(x=250, y=290)
#
#
# def manage_account_page1(frame):
#     x=20
#     radio_options1 = ["DELETE ACCOUNT", "RESTRICT ACCESS", "ALLOW ACCESS"]
#
#     intvariable = IntVar()
#     Label(frame, text="Manage Accounts", width=20, font=("Gotham", 20, 'bold'), fg="white", bg=my_grey).place(x=250, y=20)
#     Label(frame, text="Enter Student ID", font=("Gotham", 9), fg="#ee8968", bg=my_grey, bd=0, activebackground="#333333").place(x=150, y=100)
#     student_ID_entry = Entry(frame, width=35, font=("Gotham", 20), fg="white", bg=my_grey)
#
#
#     for i in range(3): # 1st set of radio buttons
#         Radiobutton(frame, text=radio_options1[i], variable=intvariable, value=i, bg=my_grey, fg=my_orange, activebackground=my_grey).place(x=x, y=200)
#         x+=200
#
#
#     submit = Button(frame, text="SUBMIT", padx=5, pady=5, width=10, bg="#ee8968", fg="white",
#                     font=(my_font, 12, 'bold'), command=lambda :admin_options(student_ID_entry.get(), "ADMIN_SEARCH", intvariable))
#
#
#     #reset_password.place(x=120, y=200)
#
#     #delete_account = Radiobutton(frame, text="DELETE ACCOUNT", variable=intvar, value=2, bg=my_grey, fg=my_blue, activebackground=my_grey)
#     #delete_account.place(x=350, y=200)
#
#     #restrict_access  = Radiobutton(frame, text="RESTRICT ACCESS", variable=intvar, value=3, bg=my_grey, fg=my_blue, activebackground=my_grey)
#     #restrict_access.place(x=580, y=200)
#
#     student_ID_entry.place(x=150, y=130)
#     submit.place(x=350, y=300)

# ========================== TESTING ==========================#
def create_account_page(frame):
    main_label = Label(frame, text="Create an account", width=20, font=("Gotham", 20, 'bold'),
                       fg="white", bg=my_grey)
    # firstname label
    firstname = Label(frame, text="Firstname", font=("Gotham", 9), fg=my_orange, bg=my_grey)
    # surname label
    surname = Label(frame, text="Surname", font=("Gotham", 9), fg=my_orange, bg=my_grey)
    # date of birth label
    dob = Label(frame, text="DoB", font=("Gotham", 9), fg=my_orange, bg=my_grey)
    # submit button
    submit = Button(frame, text="Create", padx=5, pady=5, width=10, bg=my_orange, fg="white",
                    font=("Gotham", 12, 'bold'), command=
                    lambda: create_account(entry1, entry2, dob_entry))
    # entry box for firstname
    entry1 = Entry(frame, width=20, font=("Gotham", 15), fg=my_grey)  # firstname
    # entry box for surname
    entry2 = Entry(frame, width=20, font=("Gotham", 15), fg=my_grey)
    # entry box for date of birth
    dob_entry = DateEntry(frame, width=33, background=my_grey, foreground="white",
                          maxdate=date.today())
    # latest date that can be selected is the current

    main_label.place(x=220, y=20)
    firstname.place(x=270, y=85)
    surname.place(x=270, y=175)
    dob.place(x=270, y=270)
    submit.place(x=330, y=325)

    entry1.place(x=270, y=110)
    entry2.place(x=270, y=200)
    dob_entry.place(x=270, y=290)


def manage_account_page(frame):
    # initial x co-ordinate for the radiobuttons
    x = 150
    # radio button labels
    radio_options1 = ["DELETE ACCOUNT", "RESTRICT ACCESS", "ALLOW ACCESS"]

    intvariable = IntVar()  # value holder for integer variables

    # labels
    Label(frame, text="Manage Accounts", width=20, font=("Gotham", 20, 'bold'),
          fg="white", bg=my_grey).place(x=250, y=20)
    Label(frame, text="Enter ID", font=("Gotham", 9), fg=my_orange, bg=my_grey,
          bd=0, activebackground=my_grey).place(x=150, y=100)
    # main entry
    id_entry = Entry(frame, width=35, font=("Gotham", 20), fg="white", bg=my_grey)

    # creating 3 radiobuttons
    for i in range(3):
        Radiobutton(frame, text=radio_options1[i], variable=intvariable, value=i, bg=my_grey,
                    fg=my_orange, activebackground=my_grey).place(x=x, y=200)
        x += 200

    submit = Button(frame, text="SUBMIT", padx=5, pady=5, width=10, bg=my_orange, fg="white",
                    font=('Gotham', 12, 'bold'),
                    command=lambda: apply_option(id_entry.get(), intvariable))

    # display entry and submit button
    id_entry.place(x=150, y=130)
    submit.place(x=350, y=300)


def overview_page(frame):
    xcord = 250
    ycord = 75
    # description labels
    labels = ["ACCOUNT NAME:", "NUMBER OF ACTIVE ACCOUNTS: ", "NUMBER OF DISABLED ACCOUNTS:"]
    # labels with name, no. of active accounts, no. of disabled accounts
    info = ["PyAdmin727", (num_of_records(True)) - 1, num_of_records(False)]
    main_label = Label(frame, text="Database overview", width=20, font=("Gotham", 20, 'bold'),
                       fg="white", bg=my_grey)
    # button to start the simulation
    start_sim = Button(frame, text="START SIMULATION", padx=5, pady=5, width=15, bg=my_orange,
                       fg="white", font=('Gotham', 10, 'bold'), command=None)
    main_label.place(x=250, y=20)
    start_sim.place(x=640, y=320)

    for i in range(3):
        # loop through each label in the labels list
        Label(frame, text=labels[i], font=("Gotham", 12), fg=my_orange, bg=my_grey) \
            .place(x=xcord, y=ycord)
        # labels with the information
        Label(frame, width=30, font=("Gotham", 15), fg="black", text=info[i]) \
            .place(x=xcord, y=ycord + 30)
        # lower the next created label
        ycord += 90


def insert_user(id, password):
    script = "INSERT INTO USERS (USER_ID, ACCESS, PASSWORD) \
             VALUES (%s, %s, %s);"
    hashed_encrypt = hashlib.md5(password.encode())  # ms5 hash
    hashed_password = hashed_encrypt.hexdigest()  # convert to 32 character hex representation

    cursor.execute(script, (id, True, hashed_password))
    conn.commit()


def count_requests():
    cursor.execute("SELECT * from REQUESTS")
    return len(cursor.fetchall())


def num_of_records(access_type):
    # getting all records with access / no access
    cursor.execute("SELECT * from USERS where ACCESS=%s", (access_type,))
    # Number of records fetched
    return len(cursor.fetchall())

print(num_of_records(True)-1)

print(num_of_records(False))

def show_request_records():
    cursor.execute("SELECT * from REQUESTS")
    return cursor.fetchall()


def delete_record(table, id):
    cursor.execute("DELETE FROM " + table + " WHERE USER_ID=%s", (id,))
    conn.commit()


def change_access(id, type):
    cursor.execute("UPDATE USERS SET ACCESS =%s WHERE USER_ID=%s", (type, id,))
    conn.commit()


# change_access('mytest2', True)
# admin_window()
#
# print(num_of_records(True))
# print(num_of_records(False))
# admin_window()

script = "INSERT INTO USERS (USER_ID, ACCESS, PASSWORD) \
             VALUES (%s, %s, %s);"

password = 'MyAdmin328782'
hashed_encrypt = hashlib.md5(password.encode())  # md5 hash 128 bits
hashed_password = hashed_encrypt.hexdigest()  # md5 hash to 32 character hexadecimal string
cursor.execute(script, ('PyAdmin727', True, hashed_password))
# # #
# insert_user(0, 'MyAdmin328782')

#
#
# print(num_of_records(True)-1)
# print(num_of_records(False))

# admin_window()
