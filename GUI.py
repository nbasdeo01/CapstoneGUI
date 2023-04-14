import tkinter as tk
from tkinter import messagebox
import sqlite3

class CashRegisterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cash Register")
        self.geometry("600x400")
        self.correct_passcode = "1234"  # Set your desired passcode here
        self.create_passcode_page()
        self.create_cash_register_page()
        self.create_admin_page()
        self.create_database()
        self.load_password()
        self.cash_register_page.grid_remove()
        self.admin_page.grid_remove()

        # Center the application on the screen
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width // 2 - size[0] // 2
        y = screen_height // 2 - size[1] // 2
        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

    def back_to_passcode_page(self):
        self.admin_page.grid_remove()
        self.passcode_page.grid()

    def logout(self):
        self.cash_register_page.grid_remove()
        self.passcode_page.grid()
        self.clear_passcode_entry()


    def clear_passcode_entry(self):
        self.passcode_entry.delete(0, 'end')


    def create_cash_register_page(self):
        self.cash_register_page = tk.Frame(self, bg="#F5F5F5")
        self.cash_register_page.grid(row=0, column=0, sticky="nsew")

        # Create a list of items with their respective prices
        items = [
            ("Burger", 4.99),
            ("Fries", 2.49),
            ("Pizza", 9.99),
            ("Soda", 1.99),
            ("Coffee", 3.49),
            ("Water", 0.99)
        ]

        # Create buttons for each item
        for index, (item_name, item_price) in enumerate(items):
            item_button = tk.Button(
                self.cash_register_page,
                text=f"{item_name}: ${item_price}",
                font=("Open Sans", 16),
                command=lambda price=item_price: self.add_item_price(price),
                bg="#4CAF50",
                fg="#FFFFFF",
                relief="groove",
                borderwidth=2
            )
            item_button.grid(row=index // 2, column=index % 2, padx=20, pady=20, ipadx=20, ipady=10, sticky="nsew")

        # Total label and display
        self.total_label = tk.Label(self.cash_register_page, text="Total:", font=("Open Sans", 18), bg="#F5F5F5", fg="#333333")
        self.total_label.grid(row=3, column=0, padx=20, pady=20)
        self.total_var = tk.StringVar()
        self.total_var.set("0.00")
        self.total_display = tk.Label(self.cash_register_page, textvariable=self.total_var, font=("Open Sans", 16), width=10, bg="#FFFFFF", relief="groove", borderwidth=2)
        self.total_display.grid(row=3, column=1, padx=20, pady=20)

        # Pay button
        self.pay_button = tk.Button(self.cash_register_page, text="Pay", font=("Open Sans", 16), command=self.process_payment, bg="#2196F3", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.pay_button.grid(row=4, column=0, padx=20, pady=20, ipadx=30, ipady=10)

        # Clear button
        self.clear_button = tk.Button(self.cash_register_page, text="Clear", font=("Open Sans", 16), command=self.clear, bg="#FF5722", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.clear_button.grid(row=4, column=1, padx=20, pady=20, ipadx=20, ipady=10)

        # Logout button
        self.logout_button = tk.Button(self.cash_register_page, text="Logout", font=("Open Sans", 16), command=self.logout, bg="#9C27B0", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.logout_button.grid(row=4, column=2, padx=20, pady=20, ipadx=20, ipady=10)

        # Initialize total
        self.total = 0.0

    def add_item_price(self, price):
        self.total += price
        self.total_var.set("{:.2f}".format(self.total))


    def create_passcode_page(self):
        self.passcode_page = tk.Frame(self, bg="#F5F5F5")
        self.passcode_page.grid(row=0, column=0, sticky="nsew")
        self.passcode_page.columnconfigure(0, weight=1)
        self.passcode_page.columnconfigure(2, weight=1)

        # Passcode label and entry
        self.passcode_label = tk.Label(self.passcode_page, text="Enter passcode:", font=("Open Sans", 18), bg="#F5F5F5", fg="#333333")
        self.passcode_label.grid(row=0, column=1, padx=10, pady=10)
        self.passcode_entry = tk.Entry(self.passcode_page, font=("Open Sans", 16), show="*", width=10, relief="groove", borderwidth=2)
        self.passcode_entry.grid(row=1, column=1, padx=10, pady=10)

        # Keypad buttons
        buttons = [
            ("1", 2, 0),
            ("2", 2, 1),
            ("3", 2, 2),
            ("4", 3, 0),
            ("5", 3, 1),
            ("6", 3, 2),
            ("7", 4, 0),
            ("8", 4, 1),
            ("9", 4, 2),
            ("0", 5, 1),
        ]

        for button_text, row, column in buttons:
            button = tk.Button(self.passcode_page, text=button_text, font=("Open Sans", 16), command=lambda text=button_text: self.update_passcode_entry(text), bg="#2196F3", fg="#FFFFFF", relief="groove", borderwidth=2)
            button.grid(row=row, column=column, padx=10, pady=10, ipadx=20, ipady=20)

        # Submit button
        self.submit_button = tk.Button(self.passcode_page, text="Submit", font=("Open Sans", 18), command=self.submit_passcode, bg="#4CAF50", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.submit_button.grid(row=6, column=1, padx=10, pady=10, ipadx=20, ipady=10)

        # Clear button
        self.clear_button = tk.Button(self.passcode_page, text="Clear", font=("Open Sans", 18), command=self.clear_passcode_entry, bg="#FF5722", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.clear_button.grid(row=6, column=2, padx=10, pady=10, ipadx=20, ipady=10)


    def update_passcode_entry(self, text):
        current_text = self.passcode_entry.get()
        self.passcode_entry.delete(0, tk.END)
        self.passcode_entry.insert(0, current_text + text)

    def create_database(self):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS passwords (name TEXT PRIMARY KEY, password TEXT)")
        cursor.execute("INSERT OR IGNORE INTO passwords (name, password) VALUES (?, ?)", ("default", self.correct_passcode))
        conn.commit()
        conn.close()
    def load_password(self):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM passwords WHERE name=?", ("default",))
        self.correct_passcode = cursor.fetchone()[0]
        conn.close()
    def update_passcode(self):
        new_passcode = self.admin_entry.get()
        if len(new_passcode) > 0:
            self.correct_passcode = new_passcode
            conn = sqlite3.connect("cash_register.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE passwords SET password=? WHERE name=?", (new_passcode, "default"))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Passcode updated successfully.")
            self.admin_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a valid passcode.")

    def process_payment(self):
        messagebox.showinfo("Payment", f"Payment of ${self.total_var.get()} received.")
        self.clear()

    def clear(self):
        self.total = 0.0
        self.total_var.set("0.00")
        self.item_entry.delete(0, tk.END)

    def check_passcode(self):
        admin_password = "1111"  # Set your desired admin password here
        entered_passcode = self.passcode_entry.get()

        if entered_passcode == self.correct_passcode:
            self.passcode_page.grid_remove()
            self.cash_register_page.grid()
            return True
        elif entered_passcode == admin_password:
            self.passcode_page.grid_remove()
            self.admin_page.grid()
            return True
        else:
            messagebox.showerror("Error", "Incorrect passcode, please try again.")
            self.passcode_entry.delete(0, tk.END)
            return False


    def submit_passcode(self):
        if self.check_passcode():
            print("Access granted.")
        else:
            print("Incorrect passcode.")


    def create_admin_page(self):
        self.admin_page = tk.Frame(self)
        self.admin_page.grid(row=0, column=0, sticky="nsew")

        # Admin label and entry
        self.admin_label = tk.Label(self.admin_page, text="Enter new passcode:")
        self.admin_label.grid(row=0, column=1, padx=10, pady=10)
        self.admin_entry = tk.Entry(self.admin_page, font=("Open Sans", 16), show="*", width=10)
        self.admin_entry.grid(row=1, column=1, padx=10, pady=10)

        # Update passcode button
        self.update_passcode_button = tk.Button(self.admin_page, text="Update Passcode", font=("Open Sans", 16), command=self.update_passcode)
        self.update_passcode_button.grid(row=2, column=1, padx=10, pady=10)

        # Back button
        self.back_button = tk.Button(self.admin_page, text="Back", font=("Open Sans", 16), command=self.back_to_passcode_page)
        self.back_button.grid(row=3, column=1, padx=10, pady=10)

        # Logout button
        self.logout_button_admin = tk.Button(self.admin_page, text="Logout", font=("Open Sans", 16), command=self.back_to_passcode_page)
        self.logout_button_admin.grid(row=4, column=1, padx=10, pady=10)



    def change_password(self):
        new_password = self.new_password_entry.get()
        confirm_new_password = self.confirm_new_password_entry.get()

        if new_password == confirm_new_password:
            self.correct_passcode = new_password
            messagebox.showinfo("Success", "Password changed successfully.")
            self.new_password_entry.delete(0, tk.END)
            self.confirm_new_password_entry.delete(0, tk.END)
            self.back_to_passcode_page()
        else:
            messagebox.showerror("Error", "Passwords do not match, please try again.")
            self.new_password_entry.delete(0, tk.END)
            self.confirm_new_password_entry.delete(0, tk.END)



if __name__ == "__main__":
    app = CashRegisterApp()
    app.mainloop()
