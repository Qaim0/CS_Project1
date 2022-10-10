from tkinter import *
from validate_user import validate
my_grey = "#333333"
my_blue = "#0a95ad"
my_font = "Gotham"

main_labelx = 250
main_labely = 20

first_labelx = 250
first_labely = 85

def login():
    window = Tk()
    window.geometry("800x400")
    window.config(bg=my_grey)
    Label(window, text="Enter the following details", width=20, font=("Gotham", 20, 'bold'), fg="white", bg="#333333").place(
        x=main_labelx, y=main_labely)
    Label(window, text="ID NUMBER", font=("Gotham", 9), fg=my_blue, bg=my_grey).place(x=first_labelx, y=first_labely)
    Label(window, text="PASSWORD", font=("Gotham", 9), fg=my_blue, bg=my_grey).place(x=first_labelx, y=first_labely+90)





    id_entry = Entry(window, width=30, font=("Gotham", 15), fg="white", bg=my_grey)
    password_entry = Entry(window, width=30, font=("Gotham", 15), fg="white", bg=my_grey)

    reset_password = Button(window, text="RESET PASSWORD", font=("Gotham", 7), fg=my_blue, bg=my_grey, relief=FLAT, activebackground=my_grey, bd=0, command=lambda :validate(id_entry.get(), "RESET", None, None, ""))
    submit = Button(window, text="Submit", padx=5, pady=5, width=10, bg="#0a95ad", fg="white",
                    font=(my_font, 12, 'bold'), command=lambda: validate(id_entry.get(), "LOGIN", password_entry.get(), None, window))
    reset_password.place(x=480, y=240)


    id_entry.place(x=250, y=110)
    password_entry.place(x=250, y=200)
    submit.place(x=350, y=330)
    window.mainloop()
login()