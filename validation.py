# from sql_functions import *
# from Admin_Window import account_action, admin_window
from simulation import start_sim
import pygame
from tkinter import messagebox
from mysql_functions import *
pygame.display.set_mode((1, 1))
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


def is_string(firstname, surname):
    if firstname.isalpha() and surname.isalpha():
        return True
    return False
