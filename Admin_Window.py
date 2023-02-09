from tkinter import *
from mysql_functions import *
import hashlib
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
import random
from validation import is_capitalised, manage_user_login, is_string



global frames, notebook, f5, frame4, id_lst, int_vars


id_lst = []
int_vars = []


frame4 = 0
frames = 0
my_grey = "#333333"
my_orange = "#ee8968"
my_font = "Gotham"

main_labelx = 250
main_labely = 20

first_labelx = 250
first_labely = 85

f1 = 0
f2 = 0
f3 = 0
f4 = 0
f5 = 0


def submit_request_decision(w, request_lst):
    global int_vars, current_id

    for i in int_vars:
        print(i.get(), end=" ")
    count = 0
    for i in int_vars: # for every intvar value in intvars
        index = i.get() # intvar value
        try:
            current_id = id_lst[index]
        except:
            delete_record("REQUESTS", current_id)
            print(f"{current_id} has been denied")
        else:
            if index == id_lst.index(current_id):
                if request_lst[count][1] == "UNBAN":
                    delete_record("REQUESTS", current_id)
                    access_permition(current_id, True)
                else:
                    print("Password has been reset")
            else:
                print(f"{current_id} has been denied")
    refresh(w)


def refresh(w):
    admin_window(w)


def admin_window(w):
    global frame4
    w.destroy()
    window = Tk()
    window.geometry("800x400")
    window.title("Admin Window")
    window.config(bg='#333333')

    request_lst = show_request_records()

    notebook = ttk.Notebook(window, style='lefttab.TNotebook')

    frames = [f1, f2, f3, f4, f5]
    frame_options = ["Account Info", "Create account", "Manage account", "User Requests"]
    longest = max(frame_options, key=len)
    length = len(longest)
    for i in range(4):
        word = frame_options[i]
        frames[i] = Frame(notebook, bg='grey', width=900, height=500,background="#333333")
        space = length-len(word)
        notebook.add(frames[i], text=f'{frame_options[i]}')
    frame4 = frames[3]

    submit = Button(frame4, text="SUBMIT", padx=5, pady=5, width=10, bg=my_orange, fg="white",
                    font=(my_font, 12, 'bold'),
                    command=lambda: submit_request_decision(window, request_lst))  # this is the actual request of the user
    next_page = Button(frame4, text="NEXT PAGE", padx=5, pady=5, width=10, bg=my_orange, fg="white",
                       font=(my_font, 12, 'bold'))
    submit.place(x=650, y=320)
    next_page.place(x=500, y=320)
    #
    # refresh_btn = Button(frame4, text="REFRESH", padx=5, pady=5, width=10, bg=my_orange, fg="white",
    #                      font=(my_font, 12, 'bold'), command=lambda :refresh(window))
    # refresh_btn.place(x=350, y=320)

    create_account_page(frames[1]) # creating account page
    account_info_page(frames[0])
    manage_account_page1(frames[2])




    notebook.pack(expand=True, fill="both")

    request_page()
    window.mainloop()


x = 0
y = 110
checkbox_lst = []



def request_page():
    global x, y, checkbox_lst, frame4, first_run, k
    x = 0
    y = 110



    Label(frame4, text="User Requests", width=20, font=("Gotham", 20, 'bold'), fg="white", bg="#333333").place(x=main_labelx, y=main_labely)

    while x < count_records("REQUESTS"):
        request_lst = show_request_records()
        id_lst.append(request_lst[x][0])
        Label(frame4, text=f"{request_lst[x][0]: <50}{request_lst[x][1]: <50}", font=("Gotham", 12), fg="#0a95ad", bg="#333333").place(x=20, y=y)

        k = IntVar()
        int_vars.append(k)

        checkbox1 = Checkbutton(frame4, onvalue=x, text="Accept", variable=k)
        checkbox2 = Checkbutton(frame4, onvalue=x+1, text="Deny", variable=k)

        checkbox1.place(x=600, y=y)
        checkbox2.place(x=700, y=y)
        checkbox_lst.append(checkbox1)
        checkbox_lst.append(checkbox2)
        x += 1
        y+=40


def generate_id(firstname, surname):
    user_id = ''
    unique = False
    while not unique:
        random_num = random.randint(100, 999)
        user_id = f"{surname[0:4]}{firstname[0].lower()}{random_num}" # uses 4 letters of surname + first letter of first name and one random digit
        if is_unique_id(user_id):
            unique = True
    return user_id



def create_account(entry1, entry2, entry3):
    global user_id
    firstname = entry1.get()
    surname = entry2.get()
    if len(firstname) == 0 or len(surname) == 0:
        messagebox.showerror(message='Error: entry box must not be empty')
        return
    if is_string(firstname, surname):
        if not is_capitalised(firstname, surname):
            messagebox.showerror(message='Error: firstname and surname need to be capitalized')
            return
    else:
        messagebox.showerror(message='Error: firstname and surname should be letters only!')
        return
    dob = entry3.get()
    print(dob)
    dob = dob.split("/")

    user_id = generate_id(firstname, surname)

    password = f"Py{dob[0]}{dob[1]}{dob[2]}"

    messagebox.showinfo(message=f"User ID: {user_id}\n\n"
                                f"password: {password}")

    insert_record_users(user_id, password)


def change_tab():
    notebook.select(frames[3])






def account_action(intvar, id):
    print(intvar.get())
    if intvar.get() == 1: # Reset password radiobutton selected
        pass
    elif intvar.get() == 2:
        answer = messagebox.askquestion(message=f"ID: {id}\n Would you like to delete this account?")
        if answer == "yes":
            print("delete")
            delete_record("USERS", id)
            if username_exists_check(id, "REQUESTS"):
                delete_record("REQUESTS", id)
            messagebox.showinfo(message="Account has been deleted")
    elif intvar.get() == 3:
        answer = messagebox.askquestion(message=f"ID: {id}\n Would you like to deny access for this account?")
        if answer == "yes":
            access_permition(id, False)
            messagebox.showinfo(message="Account no longer has access")
    elif intvar.get() == 4:
        answer = messagebox.askquestion(message=f"ID: {id}\n Would you like to grant access for this account?")
        if answer == "yes":
            access_permition(id, True)
            messagebox.showinfo(message="Account now has access")





def create_account_page(frame):
    main_label = Label(frame, text="Create Student Account", width=20, font=("Gotham", 20, 'bold'), fg="white", bg="#333333")
    firstname = Label(frame, text="Firstname", font=("Gotham", 9), fg=my_orange, bg="#333333")
    surname = Label(frame, text="Surname", font=("Gotham", 9), fg=my_orange, bg="#333333") # fg = blue, bg= perfect grey
    dob = Label(frame, text="DoB", font=("Gotham", 9), fg=my_orange, bg="#333333")
    submit = Button(frame,text="Create", padx=5, pady=5, width=10, bg=my_orange, fg="white", font=(my_font, 12, 'bold'), command=lambda :create_account(entry1, entry2, dob_entry))



    main_label.place(x=main_labelx, y=main_labely)
    firstname.place(x=first_labelx, y=first_labely)
    surname.place(x=250, y=175)
    dob.place(x=250, y=270)
    submit.place(x=350, y=330)
    entry1 = Entry(frame, width=20, font=("Gotham", 15), fg=my_grey) # firstname
    entry2 = Entry(frame,width=20, font=("Gotham", 15), fg=my_grey) # surname
    dob_entry = DateEntry(frame, width=33, background=my_grey, foreground="white", maxdate=date.today())

    entry1.place(x=250, y=110)
    entry2.place(x=250, y=200)
    dob_entry.place(x=250, y=290)


def manage_account_page1(frame):
    x=20
    radio_options1 = ["RESET PASSWORD", "DELETE ACCOUNT", "RESTRICT ACCESS", "ALLOW ACCESS"]

    intvariable = IntVar()
    Label(frame, text="Manage Accounts", width=20, font=("Gotham", 20, 'bold'), fg="white", bg="#333333").place(x=250, y=20)
    Label(frame, text="Enter Student ID", font=("Gotham", 9), fg="#ee8968", bg="#333333", bd=0, activebackground="#333333").place(x=150, y=100)
    student_ID_entry = Entry(frame, width=35, font=("Gotham", 20), fg="white", bg=my_grey)
    submit = Button(frame, text="SUBMIT", padx=5, pady=5, width=10, bg="#ee8968", fg="white",
                    font=(my_font, 12, 'bold'), command=lambda :admin_options(student_ID_entry.get(), "ADMIN_SEARCH", intvariable))

    for i in range(4): # 1st set of radio buttons
        Radiobutton(frame, text=radio_options1[i], variable=intvariable, value=i+1, bg=my_grey, fg=my_orange, activebackground=my_grey).place(x=x, y=200)
        x+=200


    #reset_password.place(x=120, y=200)

    #delete_account = Radiobutton(frame, text="DELETE ACCOUNT", variable=intvar, value=2, bg=my_grey, fg=my_blue, activebackground=my_grey)
    #delete_account.place(x=350, y=200)

    #restrict_access  = Radiobutton(frame, text="RESTRICT ACCESS", variable=intvar, value=3, bg=my_grey, fg=my_blue, activebackground=my_grey)
    #restrict_access.place(x=580, y=200)

    student_ID_entry.place(x=150, y=130)
    submit.place(x=350, y=300)


def account_info_page(frame): # need to add parameters of entries
    xcord = 250
    ycord=75
    labels = ["ACCOUNT NAME:", "NUMBER OF ACTIVE ACCOUNTS: ", "NUMBER OF DISABLED ACCOUNTS:"]
    account_infos = ["Admin01", (num_of_records(True))-1, num_of_records(False)] #-1 to take away admin account as being accounted for
    main_label = Label(frame, text="Account Information", width=20, font=("Gotham", 20, 'bold'), fg="white", bg="#333333")
    main_label.place(x=250, y=20)

    for i in range(3):
        Label(frame, text=labels[i], font=("Gotham", 12), fg="#919191", bg="#333333").place(x=xcord, y=ycord)
        entry = Entry(frame, width=30, font=("Gotham", 15), fg="black")
        entry.insert(0, account_infos[i])
        if i > 0:
            entry.config(state="disabled")
        entry.place(x=xcord, y=ycord+30)

        ycord += 90
    change_pass_button = Button(frame, text="change password", font=("Gotham", 9), fg="#ee8968", bg="#333333", bd=0, activebackground="#333333", command=change_tab)
    change_pass_button.place(x=480, y=320)

#
def admin_options(id, option, int_var):
    error = False
    if option == "RESET" or option == "ADMIN_SEARCH":  # table is required for first option as username check can be used for several tables
        if username_exists_check(id, "USERS"):
            if id == "Admin01":
                error = True
            if option == "RESET":
                if username_exists_check(id, "REQUESTS"):# checks to see if request already sent
                    messagebox.showerror(message="Error: Already sent request \n please wait until current request fulfilled")
                else:
                    insert_record_requests(id, "RESET PASSWORD")
                    reset_question = messagebox.askquestion(message="Are you sure you would like to reset password?")
                    if reset_question == "yes":
                        messagebox.showinfo(message="Password reset request has been sent")
            else: # means admin is searching
                account_action(int_var, id)

        else:
            error = True
    if error:
        messagebox.showerror(message="User does not exist")
def login_entry(entry_id, entry_password, w):
    if manage_user_login(entry_id, entry_password, w):
        admin_window(w)
