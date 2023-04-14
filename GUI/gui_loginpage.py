import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import new_gui_model

class LoginScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Login")

        # create labels and entry widgets for username and password
        self.username_label = tk.Label(self.master, text="Username:")
        self.username_entry = tk.Entry(self.master)
        self.password_label = tk.Label(self.master, text="Password:")
        self.password_entry = tk.Entry(self.master, show="*")

        # create login button
        self.login_button = tk.Button(self.master, text="Login", command=self.login)

        # pack everything
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()

    def login(self):
        # check if username and password are correct
        if self.username_entry.get() == "admin" and self.password_entry.get() == "password":
            # if correct, destroy the login screen and start the cash register app
            self.master.destroy()
            CashRegister()
            CashRegister(self.master)
        else:
            # if incorrect, show an error message
            tk.messagebox.showerror("Error", "Incorrect username or password")

class CashRegister:
    def __init__(self, master=None):
        # initialize the app here
        self.master = master
        self.gui = new_gui_model.CashRegister(self.master)

# create the login screen
root = tk.Tk()
login_screen = LoginScreen(root)
login_screen.pack()
root.mainloop()