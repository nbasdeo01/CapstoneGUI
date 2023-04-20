import tkinter as tk
from tkinter import ttk
import sqlite3
import subprocess
import os
import datetime
import pytz
from tkinter import messagebox
from PIL import Image, ImageTk
from gtts import gTTS
from playsound import playsound
import cv2
import os
import uuid

class CashRegisterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Cash Register")
        self.geometry("1024x600") 
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", self.exit_fullscreen)
        self.admin = False
        self.correct_passcode = "1234" 
        self.user_password = tk.StringVar()
        self.admin_page = tk.Frame(self)
        self.passcode_page = tk.Frame(self)
        self.create_database()
        self.create_add_passcode_page()
        self.create_passcode_page()
        self.create_transactions_page()
        self.create_cash_register_page()
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
        water_image = ImageTk.PhotoImage(Image.open("GUI/item_images/item1.png").resize((150, 150)))
        chips_image = ImageTk.PhotoImage(Image.open("GUI/item_images/item2.png").resize((150, 150)))
        soda_image = ImageTk.PhotoImage(Image.open("GUI/item_images/item3.png").resize((150, 150)))

        # Create a list of items with their respective prices
        self.items = [
            ("Water", 1.00, water_image),
            ("Chips", 1.50, chips_image),
            ("Soda", 2.00, soda_image),
        ]
        self.item_buttons = []

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
        # self.total_label = tk.Label(self.cash_register_page, text="Total:", font=("Open Sans", 18), bg="#F5F5F5", fg="#333333")
        # self.total_label.grid(row=3, column=0, padx=20, pady=20)
        self.total_var = tk.StringVar()
        self.total_var.set("0.00")
        # self.total_display = tk.Label(self.cash_register_page, textvariable=self.total_var, font=("Open Sans", 16), width=10, bg="#FFFFFF", relief="groove", borderwidth=2)
        # self.total_display.grid(row=3, column=1, padx=20, pady=20)

        # Pay button
        self.pay_button = tk.Button(self.cash_register_page, text="Pay", font=("Open Sans", 16), command=self.process_payment, bg="#2196F3", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.pay_button.grid(row=4, column=0, padx=20, pady=20, ipadx=30, ipady=10)

        # Clear button
        self.clear_button = tk.Button(self.cash_register_page, text="Clear", font=("Open Sans", 16), command=self.clear_items, bg="#FF5722", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.clear_button.grid(row=4, column=1, padx=20, pady=20, ipadx=20, ipady=10)

        # Logout button
        self.logout_button = tk.Button(self.cash_register_page, text="Logout", font=("Open Sans", 16), command=self.logout, bg="red", fg = "white")
        self.logout_button.grid(row=4, column=2, padx=20, pady=20, ipadx=20, ipady=10)

        # Read Cart button
        self.read_cart_button = tk.Button(self.cash_register_page, text="Read Cart", font=("Open Sans", 16), command=self.read_cart_description, bg="#4CAF50", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.read_cart_button.grid(row=3, column=0, padx=20, pady=20, ipadx=20, ipady=10)

    
        # Access Add Passcode Page button
        self.add_user_button = tk.Button(self.cash_register_page, text="Add User", font=("Open Sans", 16), command=self.show_add_passcode_page, bg="#4CAF50", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.add_user_button.grid(row=3, column=1, padx=20, pady=20, ipadx=20, ipady=10)

        # Access Transactions Page button
        self.transactions_button = tk.Button(self.cash_register_page, text="Transactions", font=("Open Sans", 16), command=self.show_transactions, bg="#4CAF50", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.transactions_button.grid(row=3, column=2, padx=20, pady=10, ipadx=20, ipady=10)

        # Place this code within your create_cash_register_page() function
        self.add_item_label = tk.Label(self.cash_register_page, text="Enter Item Name: ", font=("Open Sans", 16))
        self.add_item_label.grid(row=5, column=0, pady=10)

        # Item name entry
        self.item_name_entry = ttk.Entry(self.cash_register_page)
        self.item_name_entry.grid(row=5, column=1, pady=10)

        # Item price entry
        self.item_price_entry = ttk.Entry(self.cash_register_page)
        self.item_price_entry.grid(row=6, column=1, pady=10)
        self.item_price_label = tk.Label(self.cash_register_page, text="Price", font=("Open Sans", 16))
        self.item_price_label.grid(row=6, column=0)

        # Item image path entry
        self.item_image_entry = ttk.Entry(self.cash_register_page)
        self.item_image_entry.grid(row=7, column=1, pady=10)

        self.new_item_quantity_entry = tk.Entry(self.cash_register_page)
        self.new_item_quantity_entry.grid(row=7, column=1, pady=10)
        self.new_item_quantity_label = tk.Label(self.cash_register_page, text="Quantity", font=("Open Sans", 16))
        self.new_item_quantity_label.grid(row=7, column=0)

        # Add item button
        self.add_item_button = tk.Button(self.cash_register_page, text="Add Item", font=("Open Sans", 16), command=lambda: self.add_item_to_db(self.item_name_entry.get(), self.item_price_entry.get(), self.item_image_entry.get()))
        self.add_item_button.grid(row=5, column=2, padx=20, pady=20, ipadx=20, ipady=10)

        # Initialize total
        self.total = 0.0
        self.update_items()

    def capture_image(self, save_directory="GUI/item_images"):
        # Create the save directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        # Open the camera
        #cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Display the resulting frame
            cv2.imshow("Press spacebar to take a photo, 'q' to exit", frame)

            key = cv2.waitKey(1) & 0xFF

            # If the spacebar is pressed, save the image and break the loop
            if key == ord(" "):
                # Generate a unique file name and save the image
                file_name = f"{uuid.uuid4().hex}.png"
                file_path = os.path.join(save_directory, file_name)
                cv2.imwrite(file_path, frame)
                break
            # If 'q' is pressed, exit without saving the image
            elif key == ord("q"):
                file_path = None
                break

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

        return file_path
    
    def add_item_to_db(self, item_name, item_price, image_path):
        image_path = self.capture_image()

        if image_path is None:
            messagebox.showerror("Error", "No image captured")
            return
        # Insert the new item into the database
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO items (name, price, image_path) VALUES (?, ?, ?)", (item_name, item_price, image_path))
        
        conn.commit()
        conn.close()

        # Update the GUI with the new item
        self.update_items()

    def update_items(self):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, price, image_path FROM items")
        self.items = []
        for name, price, image_path in cursor.fetchall():
            try:
                item_image = ImageTk.PhotoImage(Image.open(image_path).resize((150, 150)))
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open image for item {name}: {e}")
                continue  # Skip this item and move to the next one

            self.items.append((name, price, item_image))

        conn.close()

        # Clear the current buttons
        for button in self.item_buttons:
            button.destroy()

        # Create buttons for each item
        self.item_buttons = []
        for i, (item_name, item_price, item_image) in enumerate(self.items):
            button = tk.Button(
                self.cash_register_page,
                text=f"{item_name}\n${item_price:.2f}",
                font=("Open Sans", 20),
                command=lambda price=item_price, name=item_name: self.add_item_price(price, name),
                image=item_image,
                compound="top",
                width=200, height=200,
            )
            button.image = item_image
            button.grid(row=i // 3, column=i % 3, padx=10, pady=10)
            self.item_buttons.append(button)

    def insert_transaction(self, transaction_data, total):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (transaction_data, total, timestamp) VALUES (?, ?, ?)", (transaction_data, total, self.est_now()))
        conn.commit()
        conn.close()

    def show_transactions(self):
        self.cash_register_page.grid_remove()
        self.transactions_page.grid()
        self.transactions_text.delete(1.0, tk.END)
        transactions = self.get_transactions()
        for transaction in transactions:
            self.transactions_text.insert(tk.END, f"ID: {transaction[0]}\nTransaction Data: {transactions[1]}\nTotal: {transaction[2]}\nTimestamp: {transaction[3]}\n\n")

    def get_transactions(self):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        conn.close()
        return transactions

    def create_transactions_page(self):
        self.transactions_page = tk.Frame(self)
        self.transactions_text = tk.Text(self.transactions_page, wrap=tk.WORD, font=("Open Sans", 12), bg="#F5F5F5", fg="#333333")
        self.transactions_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        back_button = tk.Button(self.transactions_page, text="Back", font=("Open Sans", 12), bg="#FFFFFF", fg="#333333", command=self.hide_transactions_page)
        back_button.pack(side=tk.BOTTOM, pady=(0, 20))

    def hide_transactions_page(self):
        self.transactions_page.grid_remove()
        self.cash_register_page.grid()

    def create_add_passcode_page(self):
        self.add_passcode_page = tk.Frame(self)
        self.add_passcode_page.grid(row=0, column=0, sticky="nsew")
        tk.Label(self.add_passcode_page, text="Add User", font=("Arial", 24)).grid(row=0, column=0, pady=20)
        tk.Label(self.add_passcode_page, text="Enter a 4-digit Code: ", font=("Arial", 14)).grid(row=1, column=0, pady=5)
        self.new_passcode_entry = tk.Entry(self.add_passcode_page, font=("Arial", 14))
        self.new_passcode_entry.grid(row=1, column=1, pady=5)
        tk.Button(self.add_passcode_page, text="Add", font=("Arial", 14), command=self.add_passcode).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(self.add_passcode_page, text="Back", font=("Arial", 14), command=self.back_to_cash_register_page).grid(row=3, column=0, columnspan=2, pady=5)
        self.add_passcode_page.grid_remove()

    def create_cart(self):
        self.cart = tk.Listbox(self.cash_register_page, font=("Open Sans", 20), height=10, width=10)
        self.cart.grid(row=0, column=3, rowspan=3, padx=20, pady=20)

    def read_cart_description(self):
        cart_items = self.cart.get(0, 'end')
        if len(cart_items) == 0:
            speech = "The cart is currently empty."
        else:
            speech = "The cart contains: "
            for item in cart_items:
                speech += f"{item}, "
        tts = gTTS(speech, lang='en')
        tts.save("cart_description.mp3")
        playsound("cart_description.mp3")
        os.remove("cart_description.mp3")

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
        self.passcode_label = tk.Label(self.passcode_page, text="Enter User ID:", font=("Open Sans", 28), bg="#F5F5F5", fg="#333333")
        self.passcode_label.grid(row=0, column=1, padx=20, pady=(50, 10))
        self.passcode_entry = tk.Entry(self.passcode_page, font=("Open Sans", 18), width=10, relief="groove", borderwidth=2)
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
        cursor.execute("INSERT OR IGNORE INTO passwords (name, password) VALUES (?, ?)", ("passcode1", self.correct_passcode))
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_data TEXT,
                total REAL,
                timestamp DATETIME DEFAULT (datetime('now', 'localtime'))
            )
        """)
        conn.commit()
        conn.close()

    def est_now(self):
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        est = pytz.timezone('US/Eastern')
        return utc_now.astimezone(est).strftime('%Y-%m-%d | %H:%M:%S')

    def insert_transaction(self, transaction_data, total):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (transaction_data, total, timestamp) VALUES (?, ?, ?)", (transaction_data, total, self.est_now()))
        conn.commit()
        conn.close()

    def process_payment(self):
        try:
            main_py_path = "//home//jetson//CapstoneGUI//Cash_Detection//main.py"
            subprocess.run(["python", main_py_path, str(self.total)], check=True)
            # Insert the transaction data into the database
            print(f"Items: {self.items}")
            transaction_data = ", ".join([f"{item[0]} x {item[1]}" for item in self.items])
            print(f"Transaction data: {transaction_data}")
            print(f"Total: {self.total}")
            print(f"Timestamp: {self.est_now()}")
            self.insert_transaction(transaction_data, self.total)
            self.clear_items()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running main.py: {e}")

    def load_password(self):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM passwords WHERE name=?", ("passcode1",))
        result = cursor.fetchone()
        
        if result:
            self.correct_passcode = result[0]
            self.user_password = self.correct_passcode
        else:
            self.correct_passcode = None
            self.user_password = ""
            # Handle the case where no matching record is found, e.g., log an error message, raise an exception, or set a default value.
        conn.close()

    def update_passcode(self):
        new_passcode = self.admin_entry.get()
        if len(new_passcode) > 0:
            self.correct_passcode = new_passcode
            conn = sqlite3.connect("cash_register.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE passwords SET password=? WHERE name=?", (new_passcode, "passcode1"))
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

    def toggle_add_item_button(self, show=True):
        if show:
            self.add_item_button.grid()
            self.add_item_label.grid()
            self.item_name_entry.grid()
            self.item_price_entry.grid()
            self.item_price_label.grid()
            self.item_image_entry.grid_remove()
            self.new_item_quantity_entry.grid()
            self.new_item_quantity_label.grid()
        else:
            self.add_item_button.grid_remove()
            self.add_item_label.grid_remove()
            self.item_name_entry.grid_remove()
            self.item_price_entry.grid_remove()
            self.item_image_entry.grid_remove()
            self.new_item_quantity_entry.grid_remove()
            self.new_item_quantity_label.grid_remove()
            self.item_price_label.grid_remove()

    def check_passcode(self):
        admin_password = "1234"
        entered_passcode = self.passcode_entry.get()
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwords WHERE password=?", (entered_passcode,))
        result = cursor.fetchone()
        conn.close()
        if result is not None:
            self.passcode_page.grid_remove()
            self.cash_register_page.grid()
            if entered_passcode == admin_password:
                self.admin = True
            else:
                self.admin = False

            if self.admin:
                self.add_user_button.grid()  # Show the "Add User" button for the admin user
                self.transactions_button.grid()  # Show the "Transactions" button for the admin user
                self.toggle_add_item_button()  # Show the "Add Item" button for the admin user
            else:
                self.add_user_button.grid_remove()  # Hide the "Add User" button for other users
                self.transactions_button.grid_remove()  # Hide the "Transactions" button for other users
                self.toggle_add_item_button(False)  # Hide the "Add Item" button for other users

            return True
        else:
            messagebox.showerror("Error", "Incorrect passcode, please try again.")
            self.passcode_entry.delete(0, tk.END)

    def update_add_item_button_visibility(self):
        if self.user_password == "1234":
            self.add_item_button.config(command=lambda: self.add_item_to_db(self.item_name_entry.get(), self.item_price_entry.get(), self.item_image_entry.get()))  # Update the command for the Add Item button
            self.add_item_button.grid(row=8, column=1, padx=20, pady=20, ipadx=20, ipady=10)
        else:
            self.add_item_button.grid_remove()

    def show_add_passcode_page(self):
        self.cash_register_page.grid_remove()
        self.add_passcode_page.grid()

    def back_to_cash_register_page(self):
        self.add_passcode_page.grid_remove()
        self.cash_register_page.grid()

    def add_passcode(self):
        new_passcode = self.new_passcode_entry.get()
        if len(new_passcode) > 0:
            conn = sqlite3.connect("cash_register.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO passwords (name, password) VALUES (?, ?)", (f"passcode{new_passcode}", new_passcode))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "New user added successfully.")
            self.new_passcode_entry.delete(0, tk.END)
            self.back_to_cash_register_page()
        else:
            messagebox.showerror("Error", "Please enter a valid user ID.")
            self.new_passcode_entry.delete(0, tk.END)

    def submit_passcode(self):
        if self.check_passcode():
            print("Access granted.")
        else:
            print("Incorrect passcode.")

    def add_non_admin_password(self):
        new_password = self.non_admin_entry.get()
        if len(new_password) > 0:
            conn = sqlite3.connect("cash_register.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO passwords (password) VALUES (?)", (new_password,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Non-admin password added successfully.")
            self.non_admin_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a valid password.")

    def populate_item_listbox(self):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, quantity FROM items")  # Add the quantity column here
        items = cursor.fetchall()
        conn.close()

        for item in items:
            item_name, item_price, item_quantity = item  # Add the item_quantity variable here
            self.item_listbox.insert(tk.END, f"{item_name} - ${item_price:.2f} - Quantity: {item_quantity}")  # Show the quantity


    def update_item_buttons(self):
        self.populate_item_listbox()
        self.item_buttons_frame.grid_forget()
        self.item_buttons_frame.destroy()
        self.item_buttons_frame = tk.Frame(self.item_page)
        self.create_item_buttons()
        self.item_buttons_frame.grid(row=2, column=0, padx=20, pady=20)

    def update_item_listbox(self):
        self.item_listbox.delete(0, tk.END)
        for item in self.items:
            if len(item) == 2:
                item_name, item_price = item
            elif len(item) == 3:
                item_name, item_price, _ = item
            else:
                continue
            self.item_listbox.insert(tk.END, f"{item_name} - ${item_price:.2f}")

    def add_item(self):
        item_name = self.new_item_name_entry.get()
        item_price = float(self.new_item_price_entry.get())
        item_quantity = int(self.new_item_quantity_entry.get())  # Add this line to get the quantity

        # Check if the item already exists
        for existing_item in self.items:
            if existing_item[0] == item_name:
                messagebox.showerror("Error", "Item already exists.")
                return

        # Add item to the items list
        self.items.append((item_name, item_price, item_quantity))  # Add the item_quantity variable here

        # Update item buttons
        self.update_item_buttons()
        self.update_item_listbox()

        # Clear the input fields
        self.new_item_name_entry.delete(0, tk.END)
        self.new_item_price_entry.delete(0, tk.END)
        self.new_item_quantity_entry.delete(0, tk.END)  # Clear the quantity input field

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
        self.populate_item_listbox()

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
        self.cash_register_page.grid_remove()
        self.passcode_page.grid()
        self.passcode_entry.delete(0, tk.END)

    def create_items_table(self):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL
            quantity INTEGER NOT NULL
        )
        """)

        conn.commit()
        conn.close()

if __name__ == "__main__":
    app = CashRegisterApp()
    app.mainloop()