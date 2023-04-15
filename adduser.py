import tkinter as tk
from sqlite3 import Error
from tkinter import messagebox
from initialize import create_connection
from initialize import add_new_user

def submit_form():
    passcode = passcode_entry.get()
    is_admin = admin_var.get()

    if len(passcode) != 4:
        messagebox.showerror("Error", "Passcode must be 4 digits.")
        return

    # Call the add_new_user function from your previous code
    try:
        conn = create_connection("pythonsqlite.db")
        cur = conn.cursor()
        add_new_user(cur, passcode, is_admin)
        conn.commit()
        messagebox.showinfo("Success", "User added successfully!")
    except Error as e:
        messagebox.showerror("Error", f"Error adding user: {e}")
        return

app = tk.Tk()
app.title("Add New User")

frame = tk.Frame(app, padx=20, pady=20)
frame.pack()

passcode_label = tk.Label(frame, text="Enter a 4-digit code to be used as the user's Passcode :")
passcode_label.grid(row=1, column=0)
passcode_entry = tk.Entry(frame)
passcode_entry.grid(row=1, column=1)

admin_label = tk.Label(frame, text="Admin:")
admin_label.grid(row=2, column=0)
admin_var = tk.IntVar()
admin_check = tk.Checkbutton(frame, variable=admin_var)
admin_check.grid(row=2, column=1)

submit_button = tk.Button(frame, text="Submit", command=submit_form)
submit_button.grid(row=3, columnspan=2)

app.mainloop()
