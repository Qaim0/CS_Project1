# from sql_functions import *
# from Admin_Window import account_action, admin_window
# import pygame
from tkinter import messagebox
from database_init import conn, cursor
import hashlib
#
# go = True
# def validate(window, id, option, password, int_var, w):
#     error = False
#     if option == "RESET" or option == "ADMIN_SEARCH":  # table is required for first option as username check can be used for several tables
#         if username_exists_check(id, "USERS"):
#             if id == "Admin01":
#                 error = True
#             if option == "RESET":
#                 if username_exists_check(id, "REQUESTS"):# checks to see if request already sent
#                     messagebox.showerror(message="Error: Already sent request \n please wait until current request fulfilled")
#                 else:
#                     insert_record_requests(id, "RESET PASSWORD", 0)
#                     reset_question = messagebox.askquestion(message="Are you sure you would like to reset password?")
#                     if reset_question == "yes":
#                         messagebox.showinfo(message="Password reset request has been sent")
#             else: # means admin is searching
#                 account_action(int_var, id)
#
#         else:
#             error = True
#     if error:
#         messagebox.showerror(message="User does not exist")
#     elif option == "LOGIN":
#         if user_exists(id, password):
#             if user_has_access(id):
#                 if id == "Admin01":
#                     admin_window(w)
#                 else:
#                     window.destroy()
#                     start_sim(id)
#
#
#             else:
#                 answer = messagebox.askquestion("You no longer have Access. Would you like to request Access?")
#                 if answer == "yes":
#                     if username_exists_check(id, "REQUESTS"):  # checks to see if request already sent
#                         messagebox.showerror(message="Error: Already sent request \n please wait until current request fulfilled")
#                     else:
#                         insert_record_requests(id, "UNBAN", 0)
#                         messagebox.showinfo("Access request has been sent")
#
#         else:
#             messagebox.showerror(message="Username/Password invalid")
def is_capitalised(firstname, surname):
    if not firstname[0].isupper() or not surname[0].isupper():  # checks if firstname AND surname are capitalised
        return False
    return True


def letters_only(firstname, surname):
    if firstname.isalpha() and surname.isalpha(): # if alphabetical letters only
        return True
    return False


def entries_filled(firstname, surname):
    # also checks if spaces in firstname and surname
    if len(firstname) == 0 or len(surname) == 0 or ' ' in firstname or ' ' in surname:
        return False
    return True

def validate_user_details(firstname, surname):
    if not entries_filled(firstname, surname): # if any entry boxes empty
        messagebox.showerror(message='Error: Entry box(s) must not be empty')
        return False
    elif letters_only(firstname, surname): # if first name and surname contain letters only
        if is_capitalised(firstname, surname): # if they are  capitalised
            return True # first name and surname are valid
        else:
            messagebox.showerror(message='Error: firstname and surname should be capitalized')
            return False

    else:
        messagebox.showerror(message=
                             'Error: firstname & surname should consist of letters only!')
        return False