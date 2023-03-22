from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from database_init import conn, cursor
from admin import admin_window
from authentication import user_exists, user_has_access, username_exists
from main_simulation import main
my_grey = "#333333"
my_orange = "#ee8968"
my_font = "Gotham"



def login_page():
    # creating the window
    window = Tk()
    window.title('Welcome to PyOrbit')
    window.geometry("800x400")
    window.config(bg=my_grey)

    # creating the logo
    logo = ImageTk.PhotoImage(Image.open('sim logo2.png'))

    canvas = Canvas(window, width=800, height=110, bg='#333333', highlightbackground='#333333')
    canvas.pack()
    # place image on tkinter canvas
    canvas.create_image(400, 60, image=logo)

    # ID and password labels
    Label(window, text="ID", font=("Gotham", 9), fg=my_orange, bg=my_grey).place(x=250, y=105)
    Label(window, text="PASSWORD", font=("Gotham", 9), fg=my_orange, bg=my_grey)\
        .place(x=250, y=195)



    # ID and password entry boxes
    id_entry = Entry(window, width=30, font=("Gotham", 15), fg="white", bg=my_grey)
    password_entry = Entry(window, width=30, font=("Gotham", 15), fg="white", bg=my_grey,
                           show='*') # hide password

    # submit button
    submit = Button(window, text="Submit", padx=5, pady=5, width=10, bg=my_orange, fg="white",
                    font=(my_font, 12, 'bold'), command = lambda :
                    attempt_login(window, id_entry.get(), password_entry.get()))
    # displaying widgets
    id_entry.place(x=250, y=130)
    password_entry.place(x=250, y=220)
    submit.place(x=350, y=330)
    window.mainloop()


def insert_request(id, request):
    script = "INSERT INTO REQUESTS (USER_ID, REQUEST) \
             VALUES (%s, %s);"
    cursor.execute(script, (id, request))
    conn.commit()



def attempt_login(w, entry_id, entry_password):
    if user_exists(entry_id, entry_password):
        if user_has_access(entry_id):
            # Valid login
            messagebox.showinfo(message='Login Successful')
            w.destroy()  # remove the login window
            if entry_id == "PyAdmin727": # if the admin logs in
                admin_window() # open admin window
            else: # if user logs in
                main(entry_id)

        else: # if user doesn't have access
            answer = messagebox.askquestion(message=
                "You no longer have Access. Would you like to request Access?")
            if answer == "yes":
                if username_exists(entry_id, "REQUESTS"): # check if request already sent
                    messagebox.showerror(message=
                        "Request already sent, wait until current request approved")
                else:
                    insert_request(entry_id, "ACCESS") # insert a new request
                    messagebox.showinfo(message="Access request has been sent")
    else: # if user details incorrect
        messagebox.showinfo(message='Incorrect user ID or password')


# attempt_login('Miahq498', 'Py3523')
# login_page()
# insert_request('Miahq498', 20.2)