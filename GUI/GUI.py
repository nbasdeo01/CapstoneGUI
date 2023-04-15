import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import subprocess

class CashRegisterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cash Register")
        self.geometry("1024x600") 
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", self.exit_fullscreen)

 
        self.correct_passcode = "1234" 
        self.admin_page = tk.Frame(self)
        self.passcode_page = tk.Frame(self)
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

    def exit_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)
        self.geometry("1024x600")


    def back_to_passcode_page(self):
        self.admin_page.grid_remove()
        self.passcode_page.grid()

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
        self.clear_button = tk.Button(self.cash_register_page, text="Clear", font=("Open Sans", 20), command=self.clear_items, bg="#FF5722", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.clear_button.grid(row=4, column=1, padx=20, pady=20, ipadx=20, ipady=10)

        # Logout button
        self.logout_button_admin = tk.Button(self.admin_page, text="Logout", font=("Open Sans", 16), command=self.logout)
        self.logout_button_admin.grid(row=4, column=1, padx=10, pady=10)

        # Initialize total
        self.total = 0.0

    def create_cart(self):
        self.cart = tk.Listbox(self.cash_register_page, font=("Open Sans", 20), height=10, width=10)
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
        self.passcode_label = tk.Label(self.passcode_page, text="Enter passcode:", font=("Open Sans", 28), bg="#F5F5F5", fg="#333333")
        self.passcode_label.grid(row=0, column=1, padx=20, pady=(50, 10))
        self.passcode_entry = tk.Entry(self.passcode_page, font=("Open Sans", 18), show="*", width=10, relief="groove", borderwidth=2)
        self.passcode_entry.grid(row=1, column=1, padx=20, pady=10)

        

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

        def on_enter(event):
            event.widget.config(bg="#64B5F6")

        def on_leave(event):
            event.widget.config(bg="#2196F3")

        for button_text, row, column in buttons:
            button = tk.Button(self.passcode_page, text=button_text, font=("Open Sans", 50), command=lambda text=button_text: self.update_passcode_entry(text), bg="#2196F3", fg="#FFFFFF", relief="groove", borderwidth=2)
            button.grid(row=row, column=column, padx=(0, 0) if column != 2 else (0, 0), pady=0, ipadx=135, ipady=30)
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)


        # Submit button
        self.submit_button = tk.Button(self.passcode_page, text="Enter", font=("Open Sans", 20), command=self.submit_passcode, bg="#4CAF50", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.submit_button.grid(row=5, column=2, padx=0, pady=0, ipadx=110, ipady=30)

        # Clear button
        self.clear_button = tk.Button(self.passcode_page, text="Clear", font=("Open Sans", 20), command=self.clear_passcode_entry, bg="#FF5722", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.clear_button.grid(row=5, column=0, padx=0, pady=0, ipadx=110, ipady=30)


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
        try:
            main_py_path = "//home//jetson//Desktop//CapstoneGUI//Cash_Detection//main.py"
            subprocess.run(["python", main_py_path, str(self.total)], check=True)
            self.clear_items()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running main.py: {e}")



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

    def clear_items(self):
        response = messagebox.askyesno("Clear items", "Are you sure you want to clear all items?")
        if response:
            self.cart.delete(0, tk.END)
            self.total = 0.0
            self.total_var.set(f"${self.total:.2f}")


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
        self.item_mgmt_label = tk.Label(self.admin_page, text="Item Management", font=("Open Sans", 16))
        self.item_mgmt_label.grid(row=0, column=0, padx=10, pady=10)

        # Item listbox
        self.item_listbox = tk.Listbox(self.admin_page, font=("Open Sans", 16), height=10, width=30)
        self.item_listbox.grid(row=1, column=0, padx=10, pady=10)
        self.populate_item_listbox()

        # Edit item button
        self.edit_item_button = tk.Button(self.admin_page, text="Edit Item", font=("Open Sans", 16), command=self.edit_item)
        self.edit_item_button.grid(row=2, column=0, padx=10, pady=10)

        # Delete item entry
        self.delete_item_name_entry = tk.Entry(self.admin_page, font=("Open Sans", 16), width=30)
        self.delete_item_name_entry.grid(row=4, column=1, padx=10, pady=10)

        # Delete item button
        self.delete_item_button = tk.Button(self.admin_page, text="Delete Item", font=("Open Sans", 16), command=self.delete_item)
        self.delete_item_button.grid(row=3, column=0, padx=10, pady=10)

        # Add item label
        self.add_item_label = tk.Label(self.admin_page, text="Add Item", font=("Open Sans", 16))
        self.add_item_label.grid(row=0, column=1, padx=10, pady=10)

        # Add item inputs
        self.new_item_name_label = tk.Label(self.admin_page, text="Item name:", padx=10, pady=10, font=("Open Sans", 16), bg="#FFFFFF", fg="#000000")
        self.new_item_name_label.grid(row=1, column=1, padx=10, pady=10)
        self.new_item_name_entry = tk.Entry(self.admin_page, font=("Open Sans", 16))
        self.new_item_name_entry.grid(row=1, column=2, padx=10, pady=10)

        self.new_item_price_label = tk.Label(self.admin_page, text="Item price:", padx=10, pady=10, font=("Open Sans", 16), bg="#FFFFFF", fg="#000000")
        self.new_item_price_label.grid(row=2, column=1, padx=10, pady=10)
        self.new_item_price_entry = tk.Entry(self.admin_page, font=("Open Sans", 16))
        self.new_item_price_entry.grid(row=2, column=2, padx=10, pady=10)

        # Add item button
        self.add_item_button = tk.Button(self.admin_page, text="Add Item", font=("Open Sans", 16), command=self.add_item)
        self.add_item_button.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

        # Passcode Management
        self.admin_label = tk.Label(self.admin_page, text="Enter new passcode:")
        self.admin_label.grid(row=4, column=1, padx=10, pady=10)
        self.admin_entry = tk.Entry(self.admin_page, font=("Open Sans", 16), show="*", width=10)
        self.admin_entry.grid(row=4, column=2, padx=10, pady=10)

        # Update passcode button
        self.update_passcode_button = tk.Button(self.admin_page, text="Update Passcode", font = ("Open Sans", 16), command=self.change_password)
        self.update_passcode_button.grid(row=5, column=1, padx=10, pady=10, columnspan=2)

        # Logout button
        self.logout_button = tk.Button(self.admin_page, text="Logout", font=("Open Sans", 16), command=self.logout, bg="#FF5722", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.logout_button.grid(row=4, column=2, padx=20, pady=20, ipadx=20, ipady=10)

    def populate_item_listbox(self):
        self.item_listbox.delete(0, tk.END)
        for item in self.items:
            item_name, item_price = item[:2]
            self.item_listbox.insert(tk.END, f"{item_name} - ${item_price:.2f}")


    def update_item_buttons(self):
        self.populate_item_listbox()

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
            if item[0].strip() == item_name.strip():
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

    def logout(self):
        self.admin_page.grid_remove()
        self.cash_register_page.grid_remove()
        self.passcode_page.grid()
        self.passcode_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = CashRegisterApp()
    app.mainloop()
