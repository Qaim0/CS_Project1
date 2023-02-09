from tkinter import *
# from validate_user import validate
from PIL import ImageTk, Image
from Admin_Window import login_entry
my_grey = "#333333"
my_orange = "#ee8968"
my_font = "Gotham"

main_labelx = 100
main_labely = 20

first_labelx = 250
first_labely = 105

def login():
    window = Tk()
    window.geometry("800x400")
    window.config(bg=my_grey)
    # Label(window, text="Welcome to Pyorbit solar system simulation", width=40, font=("Gotham", 20, 'bold'), fg="white", bg="#333333").place(
    #     x=main_labelx, y=main_labely)
    logo = ImageTk.PhotoImage(Image.open('sim logo2.png'))

    # canvas = Canvas(window, width=100, height=110, bg='#333333', highlightbackground='#333333')
    # canvas.pack()
    # canvas.create_image(50, 60, image=logo)
    Label(window, text="ID NUMBER", font=("Gotham", 9), fg=my_orange, bg=my_grey).place(x=first_labelx, y=first_labely)
    Label(window, text="PASSWORD", font=("Gotham", 9), fg=my_orange, bg=my_grey).place(x=first_labelx, y=first_labely + 90)





    id_entry = Entry(window, width=30, font=("Gotham", 15), fg="white", bg=my_grey)
    password_entry = Entry(window, width=30, font=("Gotham", 15), fg="white", bg=my_grey)

    submit = Button(window, text="Submit", padx=5, pady=5, width=10, bg=my_orange, fg="white",
                    font=(my_font, 12, 'bold'), command=lambda: (login_entry(id_entry.get(), password_entry.get(), window)))


    id_entry.place(x=250, y=130)
    password_entry.place(x=250, y=220)
    submit.place(x=350, y=330)
    window.mainloop()

login()