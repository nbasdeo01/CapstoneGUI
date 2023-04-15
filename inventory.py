import tkinter as tk
from tkinter import messagebox
import sqlite3

def add_item(name, price, quantity):
    conn = sqlite3.connect("pythonsqlite.db")
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO ITEMS (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        conn.commit()
        messagebox.showinfo("Success", "Item added successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error adding item: {e}")
    finally:
        conn.close()

def on_submit():
    name = name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    if not name or not price or not quantity:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        float_price = float(price)
        int_quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Price must be a number and quantity must be an integer.")
        return

    add_item(name, float_price, int_quantity)

app = tk.Tk()
app.title("Add Item")

name_label = tk.Label(app, text="Item Name:")
name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
name_entry = tk.Entry(app)
name_entry.grid(row=0, column=1, padx=5, pady=5)

price_label = tk.Label(app, text="Price:")
price_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
price_entry = tk.Entry(app)
price_entry.grid(row=1, column=1, padx=5, pady=5)

quantity_label = tk.Label(app, text="Quantity:")
quantity_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
quantity_entry = tk.Entry(app)
quantity_entry.grid(row=2, column=1, padx=5, pady=5)

submit_button = tk.Button(app, text="Submit", command=on_submit)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

app.mainloop()