import tkinter as tk
import sqlite3
import subprocess
import datetime
import tempfile
import pytz
import cv2
import os
import uuid 
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from PIL import Image, ImageTk
from gtts import gTTS
from playsound import playsound

class CashRegisterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Cash Register")
        self.geometry("1024x600") 
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", self.exit_fullscreen)
        self.admin = False
        self.correct_passcode1 = "1234"
        self.correct_passcode2 = "5678" 
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
        self.item_quantities = {}
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

        # Modify the water_image button command to show the items page
        #self.water_button = tk.Button(
        #   self.cash_register_page,
        #   text=f"{'Water'}\n${1.00:.2f}",
        #    font=("Open Sans", 20),
        #   command=self.show_items_page,
        #   image=water_image,
        #   compound="top",
        #   width=200, height=200,
        #)
        #self.water_button.image = water_image
        #self.water_button.grid(row=0, column=0, padx=10, pady=10)

        # Total label and display
        # self.total_label = tk.Label(self.cash_register_page, text="Total:", font=("Open Sans", 18), bg="#F5F5F5", fg="#333333")
        # self.total_label.grid(row=3, column=0, padx=20, pady=20)
        self.total_var = tk.StringVar()
        self.total_var.set("0.00")
        # self.total_display = tk.Label(self.cash_register_page, textvariable=self.total_var, font=("Open Sans", 16), width=10, bg="#FFFFFF", relief="groove", borderwidth=2)
        # self.total_display.grid(row=3, column=1, padx=20, pady=20)

        parent_bg_color = self.cash_register_page.cget("bg")

        # Read Cart button
        self.read_cart_button_frame = tk.Frame(self.cash_register_page, bg=parent_bg_color)
        self.read_cart_button_frame.grid(row=2, column=0, padx=20, pady=20, sticky="w")
        self.read_cart_button = tk.Button(self.read_cart_button_frame, text="Read Cart", font=("Open Sans", 16), command=self.read_cart_description, bg="#4CAF50", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.read_cart_button.pack(side="left", padx=20, ipadx=20, ipady=10)

        # Pay button
        self.pay_button = tk.Button(self.read_cart_button_frame, text="Pay", font=("Open Sans", 16), command=self.process_payment, bg="#2196F3", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.pay_button.pack(side="left", padx=20, ipadx=20, ipady=10)

        # Clear button
        self.clear_button = tk.Button(self.read_cart_button_frame, text="Clear", font=("Open Sans", 16), command=self.clear_items, bg="#2196F3", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.clear_button.pack(side="left", padx=20, ipadx=20, ipady=10)

        # Logout button
        self.logout_button = tk.Button(self.read_cart_button_frame, text="Logout", font=("Open Sans", 16), command=self.logout, bg="#2196F3", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.logout_button.pack(side="left", padx=20, ipadx=20, ipady=10)

        # Frame for Admin buttons
        self.admin_buttons_frame = tk.Frame(self.cash_register_page, bg=parent_bg_color)
        self.admin_buttons_frame.grid(row=3, column=0, padx=20, pady=20, sticky="w")

        self.add_user_button = tk.Button(self.admin_buttons_frame, text="Add User", font=("Open Sans", 16), command=self.show_add_passcode_page, bg="#4CAF50", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.add_user_button.pack(side="left", padx=20, ipadx=20, ipady=10)

        # Delete a User
        self.delete_user_button = tk.Button(self.admin_buttons_frame, text="Delete User", font=("Open Sans", 16), command=self.delete_user_from_db, bg="#4CAF50", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.delete_user_button.pack(side="left", padx=20, ipadx=20, ipady=10)

        # Access Transactions Page button
        self.transactions_button = tk.Button(self.admin_buttons_frame, text="Transactions", font=("Open Sans", 16), command=self.show_transactions, bg="#4CAF50", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.transactions_button.pack(side="left", padx=20, ipadx=20, ipady=10)

        # Place this code within your create_cash_register_page() function
        # Create a frame to contain labels and text fields
        input_frame = tk.Frame(self.cash_register_page, bg=parent_bg_color)
        input_frame.grid(row=4, column=0, pady=10, sticky="w")

        self.add_item_label = tk.Label(input_frame, text="Enter Item Name: ", font=("Open Sans", 16))
        self.add_item_label.grid(row=0, column=0, pady=3, padx=5)

        # Item name entry
        self.item_name_entry = ttk.Entry(input_frame)
        self.item_name_entry.grid(row=0, column=1, pady=3, padx=5)

        # Item price entry
        self.item_price_entry = ttk.Entry(input_frame)
        self.item_price_entry.grid(row=1, column=1, pady=3, padx=5)
        self.item_price_label = tk.Label(input_frame, text="Price", font=("Open Sans", 16))
        self.item_price_label.grid(row=1, column=0, pady=3, padx=5)

        # Item image path entry
        self.item_image_entry = ttk.Entry(input_frame)
        self.item_image_entry.grid(row=2, column=1, pady=3, padx=5)

        self.new_item_quantity_entry = tk.Entry(input_frame)
        self.new_item_quantity_entry.grid(row=3, column=1, pady=3, padx=5)
        self.new_item_quantity_label = tk.Label(input_frame, text="Quantity", font=("Open Sans", 16))
        self.new_item_quantity_label.grid(row=3, column=0, pady=3, padx=5)

        # Add item button
        self.add_item_button = tk.Button(input_frame, text="Add Item", font=("Open Sans", 16), command=lambda: self.add_item_to_db(self.item_name_entry.get(), self.item_price_entry.get(), self.item_image_entry.get(), self.new_item_quantity_entry.get()))
        self.add_item_button.grid(row=1, column=3, padx=5, pady=20, ipadx=20, ipady=10)

        # Delete item button
        self.delete_item_button = tk.Button(input_frame, text="Delete Item", font=("Open Sans", 16), command=self.delete_item_from_db, bg="#4CAF50", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.delete_item_button.grid(row=1, column=4, padx=5, pady=20, ipadx=20, ipady=10)

        # Initialize total
        self.total = 0.0
        self.update_items()

    def show_items_page(self):
        # Create a new Toplevel window
        self.items_page = tk.Toplevel(self)
        self.items_page.title("Items Page")
        self.items_page.configure(bg="#F5F5F5")
        # Add a "Back" button
        back_button = tk.Button(self.items_page, text="Back", font=("Open Sans", 16), command=self.items_page.destroy, bg="red", fg="white")
        back_button.grid(row=0, column=0, padx=20, pady=20, ipadx=20, ipady=10)
        self.load_items()

    def show_cash_register_page(self):
        self.items_page.grid_remove()
        self.cash_register_page.grid(row=0, column=0, sticky="nsew")

    def load_items(self):
        # Load items from the database
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, image_path FROM items_ordered")
        items = cursor.fetchall()
        conn.close()
        # Create a button for each item with the add_item_to_cart command
        for i, (item_name, item_price, image_path) in enumerate(items):
            item_image = ImageTk.PhotoImage(Image.open(image_path).resize((150, 150)))
            button = tk.Button(
                self.items_page,
                text=f"{item_name}\n${item_price:.2f}",
                font=("Open Sans", 20),
                command=lambda price=item_price, name=item_name: self.add_item_price(price, name),
                image=item_image,
                compound="top",
                width=150, height=200,
            )
            button.image = item_image
            button.grid(row=(i // 3) + 1, column=i % 3, padx=10, pady=10)

    def capture_image(self, save_directory="GUI/item_images"):
        def is_inside(pos, rect):
            x, y, w, h = rect
            px, py = pos
            return x < px < x + w and y < py < y + h
        detect_quit_flags = [False, False]
        def on_mouse_click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                if is_inside((x, y), take_pic_rect):
                    detect_quit_flags[0] = True
                elif is_inside((x, y), quit_button_rect):
                    detect_quit_flags[1] = True
        cv2.namedWindow("Take picture of item")
        cv2.setMouseCallback("Take picture of item", on_mouse_click)

        take_pic_rect = (245, 360, 150, 50)
        quit_button_rect = (245, 420, 150, 50)
        # Create the save directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        # Open the camera
        #cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)

        # Check if the camera is opened successfully
        if not cap.isOpened():
            print("Error: Camera not opened")
            return None

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            original_frame = frame.copy()

            # Display the resulting frame
            cv2.rectangle(frame, (take_pic_rect[0], take_pic_rect[1]), (take_pic_rect[0] + take_pic_rect[2], take_pic_rect[1] + take_pic_rect[3]), (0, 255, 0), -1)
            text_detect = "Take picture"
            (text_width, text_height), _ = cv2.getTextSize(text_detect, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            text_x = take_pic_rect[0] + (take_pic_rect[2] - text_width) // 2
            text_y = take_pic_rect[1] + (take_pic_rect[3] + text_height) // 2
            cv2.putText(frame, text_detect, (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 2)

            cv2.rectangle(frame, (quit_button_rect[0], quit_button_rect[1]), (quit_button_rect[0] + quit_button_rect[2], quit_button_rect[1] + quit_button_rect[3]), (0, 0, 255), -1)
            text_quit = "Exit"
            (text_width, text_height), _ = cv2.getTextSize(text_quit, cv2.FONT_HERSHEY_DUPLEX, 0.6, 2)
            text_x = quit_button_rect[0] + (quit_button_rect[2] - text_width) // 2
            text_y = quit_button_rect[1] + (quit_button_rect[3] + text_height) // 2
            cv2.putText(frame, text_quit, (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 2)
            cv2.imshow("Take picture of item", frame)

            key = cv2.waitKey(1) & 0xFF

            # If the spacebar is pressed, save the image and break the loop
            if detect_quit_flags[0]:
                # Generate a unique file name and save the image
                file_name = f"{uuid.uuid4().hex}.png"
                file_path = os.path.join(save_directory, file_name)
                cv2.imwrite(file_path, original_frame)
                break
            # If 'q' is pressed, exit without saving the image
            elif detect_quit_flags[1]:
                file_path = None
                break

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

        return file_path
    
    def add_item_to_db(self, item_name, item_price, image_path, new_item_quantity):
        image_path = self.capture_image()
        if image_path is None:
            messagebox.showerror("Error", "No image captured")
            return
        # Insert the new item into the database
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, price, image_path, quantity) VALUES (?, ?, ?, ?)", (item_name, item_price, image_path, new_item_quantity))
        conn.commit()
        conn.close()
        # Update the GUI with the new item
        self.update_items()

    def delete_item_from_db(self):
        # Get all the item names from the items table
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM items")
        result = cursor.fetchall()
        conn.close()
        if not result:
            messagebox.showerror("Error", "No items found in the database")
            return
        # Display the list of item names and prompt the user to enter the item name to delete
        item_names = [item[0] for item in result]
        dialog = DeleteItemDialog(self, item_names)
        item_name = dialog.result
        if not item_name:
            messagebox.showerror("Error", "Please enter the name of the item you want to delete")
            return
        # Check if the item exists
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM items WHERE name = ?", (item_name,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Item not found")
            conn.close()
            return

        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the item '{item_name}'?")
        if confirm:
            cursor.execute("DELETE FROM items WHERE name = ?", (item_name,))
            conn.commit()
            messagebox.showinfo("Item Deleted", f"Item '{item_name}' has been deleted")
            self.update_items()
        conn.close()

    def delete_user_from_db(self):
        # Get all the user names from the passwords table
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, password FROM passwords")
        result = cursor.fetchall()
        conn.close()
        if not result:
            messagebox.showerror("Error", "No users found in the database")
            return
        # Display the list of user names and prompt the user to enter the user name to delete
        user_names = [f"{user[0]} - {user[1]}" for user in result]
        dialog = DeleteUserDialog(self, user_names)
        user_input = dialog.result
        if not user_input:
            messagebox.showerror("Error", "Please enter the name of the user you want to delete")
            return
        # Check if the user exists
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM passwords WHERE name = ? OR password = ?", (user_input, user_input))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "User not found")
            conn.close()
            return
        user_name = result[0]  # Get the user name from the query result
        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the user '{user_name}'?")
        if confirm:
            cursor.execute("DELETE FROM passwords WHERE name = ?", (user_name,))
            conn.commit()
            messagebox.showinfo("User Deleted", f"User '{user_name}' has been deleted")
        conn.close()

    def update_items(self):
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, image_path FROM items_ordered")
        self.items = []
        for name, price, image_path in cursor.fetchall():
            try:
                item_image = ImageTk.PhotoImage(Image.open(image_path).resize((150, 150)))
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open image for item {name}: {e}")
                continue
            self.items.append((name, price, item_image))
        conn.close()

        # Clear the current buttons
        for button in self.item_buttons:
            button.destroy()
        
        parent_bg_color = self.cash_register_page.cget("bg")

        # Create a frame for the buttons
        self.buttons_frame = tk.Frame(self.cash_register_page, bg=parent_bg_color)
        self.buttons_frame.grid(row=0, column=0)

        # Create a canvas inside the frame
        self.buttons_canvas = tk.Canvas(self.buttons_frame, height=230, width=675)
        self.buttons_canvas.grid(row=0, column=0)

        # Create a scrollbar for the canvas
        self.scrollbar = ttk.Scrollbar(self.buttons_frame, orient="vertical", command=self.buttons_canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.buttons_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create an inner frame to place the buttons on the canvas
        self.inner_frame = tk.Frame(self.buttons_canvas)
        self.buttons_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Create buttons for each item
        self.item_buttons = []
        for i, (item_name, item_price, item_image) in enumerate(self.items):
            button = tk.Button(
                self.inner_frame,
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

        # Update the canvas scroll region after creating the buttons
        self.inner_frame.update_idletasks()
        self.buttons_canvas.configure(scrollregion=self.buttons_canvas.bbox("all"))

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
        self.cart = tk.Listbox(self.cash_register_page, font=("Open Sans", 20), height=10, width=13)
        self.cart.grid(row=0, column=3, rowspan=2, padx=20, pady=10, sticky="n")

    def create_remove_button(self):
        remove_label = tk.Label(self.cash_register_page, text="Tap an item\nto remove it", font=("Open Sans", 16), bg="#F5F5F5", fg="#333333")
        remove_label.grid(row=2, column=3, padx=0, pady=0, sticky="n")
        self.remove_button = tk.Button(self.cash_register_page, text="Remove Item", font=("Open Sans", 16), command=self.remove_item, bg="#FF5722", fg="#FFFFFF", relief="groove", borderwidth=2)
        self.remove_button.grid(row=3, column=3, padx=20, pady=(0, 10), ipadx=20, ipady=10, sticky="n")

    def read_cart_description(self):
        cart_items = self.cart.get(0, 'end')
        if len(cart_items) == 0:
            speech = "The cart is currently empty."
        else:
            speech = "The cart contains: "
            unique_items = set()
            for item in cart_items:
                item_name = item.split(" (")[0]  # Extract the item name from the item string
                unique_items.add(item_name)
        
            for unique_item in unique_items:
                speech += f"{unique_item}. Quantity {self.item_quantities[unique_item]}. "
        
            speech = speech[:-2] + ". "  # Remove the last comma and space, add a period
            # Round the total to 2 decimal places to avoid floating-point arithmetic issues
            rounded_total = round(self.total, 2)
            # Format the total as dollars and cents
            total_dollars, total_cents = divmod(int(rounded_total * 100), 100)
            speech += f"The cart total is: {total_dollars} dollars and {total_cents} cents, "
        tts = gTTS(speech, lang='en')
        tts.save("cart_description.mp3")
        playsound("cart_description.mp3")
        os.remove("cart_description.mp3")

    def add_item_price(self, price, item_name):
        self.total += price
        self.total_var.set(f"${self.total:.2f}")

        # Update the item quantity in the cart
        if item_name not in self.item_quantities:
            self.item_quantities[item_name] = 0
        self.item_quantities[item_name] += 1

        self.cart.insert(tk.END, f"{item_name} (${price:.2f})")

        # Generate spoken text using gTTS
        tts_text = f"{item_name}. Quantity {self.item_quantities[item_name]}."
        tts = gTTS(tts_text, lang="en")

        # Save the audio file temporarily and play it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            tts.save(temp_file.name)
            playsound(temp_file.name)

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
        cursor.execute("INSERT OR IGNORE INTO passwords (name, password) VALUES (?, ?)", ("User ID 1", self.correct_passcode1))
        cursor.execute("INSERT OR IGNORE INTO passwords (name, password) VALUES (?, ?)", ("User ID 2", self.correct_passcode2))
        cursor.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_data TEXT, total REAL, timestamp DATETIME DEFAULT (datetime('now', 'localtime')))")
        cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL, image_path TEXT NOT NULL, quantity INTEGER NOT NULL)")
        cursor.execute("CREATE VIEW IF NOT EXISTS items_ordered AS SELECT * FROM items ORDER BY name")
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
            subprocess.run(["/usr/bin/python3", main_py_path, str(self.total)], check=True)
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
            self.item_quantities = {}  # Clear the item quantities dictionary

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
        admin_password1 = "1234"
        admin_password2 = "5678"
        entered_passcode = self.passcode_entry.get()
        conn = sqlite3.connect("cash_register.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwords WHERE password=?", (entered_passcode,))
        result = cursor.fetchone()
        conn.close()
        if result is not None:
            self.passcode_page.grid_remove()
            self.cash_register_page.grid()
            if entered_passcode == admin_password1:
                self.admin = True
            elif entered_passcode == admin_password2:
                self.admin = True
            else:
                self.admin = False

            if self.admin:
                self.add_user_button.pack(side="left", padx=20, ipadx=20, ipady=10)
                self.delete_user_button.pack(side="left", padx=20, ipadx=20, ipady=10)
                self.transactions_button.pack(side="left", padx=20, ipadx=20, ipady=10)
                self.delete_item_button.grid()
                self.toggle_add_item_button()
            else:
                self.add_user_button.pack_forget()
                self.delete_user_button.pack_forget()
                self.transactions_button.pack_forget()
                self.delete_item_button.grid_remove()
                self.toggle_add_item_button(False)

            return True
        else:
            messagebox.showerror("Error", "Incorrect passcode, please try again.")
            self.passcode_entry.delete(0, tk.END)

    def update_add_item_button_visibility(self):
        if self.user_password == "1234" or "5678":
            self.add_item_button.config(command=lambda: self.add_item_to_db(self.item_name_entry.get(), self.item_price_entry.get(), self.item_image_entry.get(), self.new_item_quantity_entry.get()))  # Update the command for the Add Item button
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
            # Fetch the maximum user ID from the database
            cursor.execute("SELECT MAX(CAST(SUBSTR(name, 9) AS INTEGER)) FROM passwords WHERE name LIKE 'User ID %'")
            max_user_id = cursor.fetchone()[0]
            # If there is no user ID in the database, set max_user_id to 0
            if max_user_id is None:
                max_user_id = 2
            # Increment the user ID by 1 and add the new user
            new_user_id = max_user_id + 1
            new_user_name = f"User ID {new_user_id}"
            cursor.execute("INSERT INTO passwords (name, password) VALUES (?, ?)", (new_user_name, new_passcode))
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

class DeleteItemDialog(simpledialog.Dialog):
    def __init__(self, parent, items):
        self.items = items
        super().__init__(parent, title="Delete Item")
    def body(self, master):
        tk.Label(master, text="Items in the database:").grid(row=0, column=0, sticky="w")
        tk.Label(master, text="\n".join(self.items), justify="left").grid(row=1, column=0, sticky="w")
        tk.Label(master, text="Please enter the name of the item you want to delete:").grid(row=2, column=0, sticky="w")
        self.entry = tk.Entry(master)
        self.entry.grid(row=3, column=0)
        return self.entry
    def apply(self):
        self.result = self.entry.get()

class DeleteUserDialog(simpledialog.Dialog):
    def __init__(self, parent, users):
        self.users = users
        super().__init__(parent, title="Delete User")
    def body(self, master):
        tk.Label(master, text="Users in the database:").grid(row=0, column=0, sticky="w")
        tk.Label(master, text="\n".join(self.users), justify="left").grid(row=1, column=0, sticky="w")
        tk.Label(master, text="Please enter the name of the user you want to delete:").grid(row=2, column=0, sticky="w")
        self.entry = tk.Entry(master)
        self.entry.grid(row=3, column=0)
        return self.entry
    def apply(self):
        self.result = self.entry.get()

if __name__ == "__main__":
    app = CashRegisterApp()
    app.mainloop()