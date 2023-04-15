import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

class CashRegisterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cash Register")
        self.geometry("1024x600")  
        self.correct_passcode = "1234" 
        self.create_passcode_page()
        self.create_cash_register_page()
        self.create_admin_page()
        self.create_database()
        self.load_password()
        self.create_cart()
        self.create_remove_button()
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
        water_image = ImageTk.PhotoImage(Image.open("GUI/item1.png").resize((150, 150)))
        chips_image = ImageTk.PhotoImage(Image.open("GUI/item2.png").resize((150, 150)))
        soda_image = ImageTk.PhotoImage(Image.open("GUI/item3.png").resize((150, 150)))

        # Create a list of items with their respective prices
        self.items = [
            ("Water", 1.00, water_image),
            ("Chips", 1.50, chips_image),
            ("Soda", 2.00, soda_image),
        ]

        # Create buttons for each item
        for i, (item_name, item_price, item_image) in enumerate(self.items):
            button = tk.Button(
                self.cash_register_page,
                text=f"{item_name}\n${item_price:.2f}",
                font=("Open Sans", 20),
                command=lambda price=item_price, name=item_name: self.add_item_price(price, name),
                image=item_image,
                compound="top",  # Display image on top and text at the bottom
                width=200, height=200,
            )
            button.image = item_image  # Store a reference to the image to avoid garbage collection
            button.grid(row=i // 3, column=i % 3, padx=10, pady=10)


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

    def create_cart(self):
        self.cart = tk.Listbox(self.cash_register_page, font=("Open Sans", 20), height=10, width=20)
        self.cart.grid(row=0, column=3, rowspan=3, padx=20, pady=20)

    def create_remove_button(self):
        remove_label = tk.Label(self.cash_register_page, text="Tap an item in the cart\nto remove it", font=("Open Sans", 16), bg="#F5F5F5", fg="#333333")
        remove_label.grid(row=3, column=3, padx=20, pady=10)
        self.remove_button = tk.Button(self.cash_register_page, text="Remove", font=("Open Sans", 20), command=self.remove_item, bg="#FF5722", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.remove_button.grid(row=4, column=3, padx=20, pady=10, ipadx=20, ipady=10)

    def add_item_price(self, price, item_name):
        self.total += price
        self.total_var.set(f"${self.total:.2f}")
        self.cart.insert(tk.END, f"{item_name} (${price:.2f})")

    def remove_item(self):
        try:
            selected_item = self.cart.get(self.cart.curselection())
            item_price = float(selected_item.split("($")[-1].rstrip(")"))
            self.total -= item_price
            self.total_var.set(f"${self.total:.2f}")
            self.cart.delete(self.cart.curselection())
        except:
            messagebox.showerror("Error", "Please select an item to remove.")


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
        cursor.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_data TEXT, total REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        conn.commit()
        conn.close()

    def save_transaction(self, transaction_data, total):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (transaction_data, total) VALUES (?, ?)", (transaction_data, total))
        conn.commit()
        conn.close()

    def process_payment(self):
        transaction_data = "\n".join(self.cart.get(0, tk.END))
        total = self.total
        self.save_transaction(transaction_data, total)
        messagebox.showinfo("Payment", f"Payment of ${self.total:.2f} received.")
        self.cart.delete(0, tk.END)
        self.clear()

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

    def clear(self):
        self.total = 0.0
        self.total_var.set("0.00")

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
        # Item management label
        self.item_mgmt_label = tk.Label(self.admin_page, text="Item Management")
        self.item_mgmt_label.grid(row=0, column=0, padx=10, pady=10)

        # Item listbox
        self.item_listbox = tk.Listbox(self.admin_page, font=("Open Sans", 16), height=10, width=30)
        self.item_listbox.grid(row=1, column=0, padx=10, pady=10)
        self.populate_item_listbox()
        # Add item label and entry
        self.add_item_label = tk.Label(self.admin_page, text="Add item:")
        self.add_item_label.grid(row=1, column=1, padx=10, pady=5)
        self.add_item_entry = tk.Entry(self.admin_page, font=("Open Sans", 16), width=10)
        self.add_item_entry.grid(row=1, column=2, padx=10, pady=5)

        # Edit item label and entry
        self.edit_item_label = tk.Label(self.admin_page, text="Edit item:")
        self.edit_item_label.grid(row=2, column=1, padx=10, pady=5)
        self.edit_item_entry = tk.Entry(self.admin_page, font=("Open Sans", 16), width=10)
        self.edit_item_entry.grid(row=2, column=2, padx=10, pady=5)

        # Delete item label and entry
        self.delete_item_label = tk.Label(self.admin_page, text="Delete item:")
        self.delete_item_label.grid(row=3, column=1, padx=10, pady=5)
        self.delete_item_entry = tk.Entry(self.admin_page, font=("Open Sans", 16), width=10)
        self.delete_item_entry.grid(row=3, column=2, padx=10, pady=5)

        # Add item button
        self.add_item_button = tk.Button(self.admin_page, text="Add Item", font=("Open Sans", 16), command=self.add_item)
        self.add_item_button.grid(row=1, column=3, padx=10, pady=10)

        # Edit item button
        self.edit_item_button = tk.Button(self.admin_page, text="Edit Item", font=("Open Sans", 16), command=self.edit_item)
        self.edit_item_button.grid(row=2, column=3, padx=10, pady=10)

        # Delete item button
        self.delete_item_button = tk.Button(self.admin_page, text="Delete Item", font=("Open Sans", 16), command=self.delete_item)
        self.delete_item_button.grid(row=3, column=3, padx=10, pady=10)

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
        
    def populate_item_listbox(self):
        self.item_listbox.delete(0, tk.END)
        for item_name, item_price, _ in self.items:
            self.item_listbox.insert(tk.END, f"{item_name} - ${item_price:.2f}")

    def add_item(self):
        item_name = self.new_item_name_entry.get()
        item_price = float(self.new_item_price_entry.get())

        # Check if the item already exists
        for existing_item in self.items:
            if existing_item[0] == item_name:
                messagebox.showerror("Error", "Item already exists.")
                return

        # Add item to the items list
        self.items.append((item_name, item_price))

        # Update item buttons
        self.update_item_buttons()

        # Clear the input fields
        self.new_item_name_entry.delete(0, tk.END)
        self.new_item_price_entry.delete(0, tk.END)

    def edit_item(self):
        old_item_name = self.edit_item_name_entry.get()
        new_item_name = self.new_edit_item_name_entry.get()
        new_item_price = float(self.new_edit_item_price_entry.get())

        # Find the item in the list
        for i, item in enumerate(self.items):
            if item[0] == old_item_name:
                # Update the item
                self.items[i] = (new_item_name, new_item_price)

                # Update item buttons
                self.update_item_buttons()

                # Clear the input fields
                self.edit_item_name_entry.delete(0, tk.END)
                self.new_edit_item_name_entry.delete(0, tk.END)
                self.new_edit_item_price_entry.delete(0, tk.END)
                return

        messagebox.showerror("Error", "Item not found.")

    def delete_item(self):
        item_name = self.delete_item_name_entry.get()

        # Find the item in the list
        for i, item in enumerate(self.items):
            if item[0] == item_name:
                # Remove the item from the list
                self.items.pop(i)
                # Update item buttons
                self.update_item_buttons()
                # Clear the input field
                self.delete_item_name_entry.delete(0, tk.END)
                return

        messagebox.showerror("Error", "Item not found.")

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
