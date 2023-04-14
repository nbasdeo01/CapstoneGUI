import tkinter as tk
import tkinter.messagebox
import pyttsx3
from tkinter import ttk
from PIL import Image, ImageTk

class CashRegister(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.grid()
        self.master.title("C4Me Cash Register")
        
        # initialize pyttsx3 engine for audio output
        self.engine = pyttsx3.init()

        # add this line to open the output screen in fullscreen mode
        self.master.attributes('-fullscreen', True)

        item1_img = Image.open("item1.png")
        resized_img1 = item1_img.resize((150, 150), resample=Image.Resampling.NEAREST)
        item2_img = Image.open("item2.png")
        resized_img2 = item2_img.resize((150, 150), resample=Image.Resampling.NEAREST)
        item3_img = Image.open("item3.png")
        resized_img3 = item3_img.resize((150, 150), resample=Image.Resampling.NEAREST)
        item4_img = Image.open("item4.png")
        resized_img4 = item4_img.resize((150, 150), resample=Image.Resampling.NEAREST)
        item5_img = Image.open("item5.png")
        resized_img5 = item5_img.resize((150, 150), resample=Image.Resampling.NEAREST)
        item6_img = Image.open("item6.png")
        resized_img6 = item6_img.resize((150, 150), resample=Image.Resampling.NEAREST)
        item7_img = Image.open("item7.png")
        resized_img7 = item7_img.resize((150, 150), resample=Image.Resampling.NEAREST)
        item8_img = Image.open("item8.png")
        resized_img8 = item8_img.resize((150, 150), resample=Image.Resampling.NEAREST)
        item9_img = Image.open("item9.png")
        resized_img9 = item9_img.resize((150, 150), resample=Image.Resampling.NEAREST)

        # create item images
        self.item1_img = ImageTk.PhotoImage(resized_img1)
        self.item2_img = ImageTk.PhotoImage(resized_img2)
        self.item3_img = ImageTk.PhotoImage(resized_img3)
        self.item4_img = ImageTk.PhotoImage(resized_img4)
        self.item5_img = ImageTk.PhotoImage(resized_img5)
        self.item6_img = ImageTk.PhotoImage(resized_img6)
        self.item7_img = ImageTk.PhotoImage(resized_img7)
        self.item8_img = ImageTk.PhotoImage(resized_img8)
        self.item9_img = ImageTk.PhotoImage(resized_img9)

        # convert images to PhotoImage objects
        self.item1_photo = ImageTk.PhotoImage(item1_img)
        self.item2_photo = ImageTk.PhotoImage(item2_img)
        self.item3_photo = ImageTk.PhotoImage(item3_img)
        self.item4_photo = ImageTk.PhotoImage(item4_img)
        self.item5_photo = ImageTk.PhotoImage(item5_img)
        self.item6_photo = ImageTk.PhotoImage(item6_img)
        self.item7_photo = ImageTk.PhotoImage(item7_img)
        self.item8_photo = ImageTk.PhotoImage(item8_img)
        self.item9_photo = ImageTk.PhotoImage(item9_img)

        # create quantity labels
        self.item1_qty = tk.StringVar()
        self.item1_qty.set("0")
        self.item2_qty = tk.StringVar()
        self.item2_qty.set("0")
        self.item3_qty = tk.StringVar()
        self.item3_qty.set("0")
        self.item4_qty = tk.StringVar()
        self.item4_qty.set("0")
        self.item5_qty = tk.StringVar()
        self.item5_qty.set("0")
        self.item6_qty = tk.StringVar()
        self.item6_qty.set("0")
        self.item7_qty = tk.StringVar()
        self.item7_qty.set("0")
        self.item8_qty = tk.StringVar()
        self.item8_qty.set("0")
        self.item9_qty = tk.StringVar()
        self.item9_qty.set("0")

        # create item labels
        self.item1_nameandprice_label = tk.Label(self.master, text="Water: $1.99", font=("TkDefaultFont", 18))
        self.item2_nameandprice_label = tk.Label(self.master, text="Chips: $2.99", font=("TkDefaultFont", 18))
        self.item3_nameandprice_label = tk.Label(self.master, text="Soda: $3.99", font=("TkDefaultFont", 18))
        self.item4_nameandprice_label = tk.Label(self.master, text="Cookie: $1.99", font=("TkDefaultFont", 18))
        self.item5_nameandprice_label = tk.Label(self.master, text="Granola Bar: $2.99", font=("TkDefaultFont", 18))
        self.item6_nameandprice_label = tk.Label(self.master, text="Doughnut: $3.99", font=("TkDefaultFont", 18))
        self.item7_nameandprice_label = tk.Label(self.master, text="Chocolate Bar: $1.99", font=("TkDefaultFont", 18))
        self.item8_nameandprice_label = tk.Label(self.master, text="Chocolate Cake: $2.99", font=("TkDefaultFont", 18))
        self.item9_nameandprice_label = tk.Label(self.master, text="Pretzel: $3.99", font=("TkDefaultFont", 18))
        self.item1_name_label = tk.Label(self.master, text="Water", font=("TkDefaultFont", 18))
        self.item2_name_label = tk.Label(self.master, text="Chips", font=("TkDefaultFont", 18))
        self.item3_name_label = tk.Label(self.master, text="Soda", font=("TkDefaultFont", 18))
        self.item4_name_label = tk.Label(self.master, text="Cookie", font=("TkDefaultFont", 18))
        self.item5_name_label = tk.Label(self.master, text="Granola Bar", font=("TkDefaultFont", 18))
        self.item6_name_label = tk.Label(self.master, text="Doughnut", font=("TkDefaultFont", 18))
        self.item7_name_label = tk.Label(self.master, text="Chocolate Bar", font=("TkDefaultFont", 18))
        self.item8_name_label = tk.Label(self.master, text="Chocolate Cake", font=("TkDefaultFont", 18))
        self.item9_name_label = tk.Label(self.master, text="Pretzel", font=("TkDefaultFont", 18))
        
        # create item buttons
        self.item1_btn = tk.Button(self.master, image=self.item1_img, command=self.add_item1)
        self.item2_btn = tk.Button(self.master, image=self.item2_img, command=self.add_item2)
        self.item3_btn = tk.Button(self.master, image=self.item3_img, command=self.add_item3)
        self.item4_btn = tk.Button(self.master, image=self.item4_img, command=self.add_item4)
        self.item5_btn = tk.Button(self.master, image=self.item5_img, command=self.add_item5)
        self.item6_btn = tk.Button(self.master, image=self.item6_img, command=self.add_item6)
        self.item7_btn = tk.Button(self.master, image=self.item7_img, command=self.add_item7)
        self.item8_btn = tk.Button(self.master, image=self.item8_img, command=self.add_item8)
        self.item9_btn = tk.Button(self.master, image=self.item9_img, command=self.add_item9)

        # create subtotal, tax, and total labels
        self.subtotal_label = tk.Label(self.master, text="Subtotal: $0.00", font=("TkDefaultFont", 24))
        self.tax_label = tk.Label(self.master, text="Tax: $0.00", font=("TkDefaultFont", 24))
        self.total_label = tk.Label(self.master, text="Total: $0.00", font=("TkDefaultFont", 24))
        
        # create clear and calculate buttons
        self.clear_btn = tk.Button(self.master, text="Clear", command=self.clear_items, width=20, height=5, font=("TkDefaultFont", 18))
        self.proceed_to_checkout_btn = tk.Button(self.master, text="Proceed to Checkout", command=self.proceed_to_checkout, width=30, height=5, font=("TkDefaultFont", 18))
        
        # pack everything
        self.item1_btn.grid(row=3, column=0, padx=10, pady=10)
        self.item2_btn.grid(row=3, column=1, padx=10, pady=10)
        self.item3_btn.grid(row=3, column=2, padx=10, pady=10)
        self.item4_btn.grid(row=5, column=0, padx=10, pady=10)
        self.item5_btn.grid(row=5, column=1, padx=10, pady=10)
        self.item6_btn.grid(row=5, column=2, padx=10, pady=10)
        self.item7_btn.grid(row=7, column=0, padx=10, pady=10)
        self.item8_btn.grid(row=7, column=1, padx=10, pady=10)
        self.item9_btn.grid(row=7, column=2, padx=10, pady=10)

        self.item1_nameandprice_label.grid(row=4, column=0)
        self.item2_nameandprice_label.grid(row=4, column=1)
        self.item3_nameandprice_label.grid(row=4, column=2)
        self.item4_nameandprice_label.grid(row=6, column=0)
        self.item5_nameandprice_label.grid(row=6, column=1)
        self.item6_nameandprice_label.grid(row=6, column=2)
        self.item7_nameandprice_label.grid(row=8, column=0)
        self.item8_nameandprice_label.grid(row=8, column=1)
        self.item9_nameandprice_label.grid(row=8, column=2)
        
        self.subtotal_label.grid(row=96, column=30, padx=10, pady=10)
        self.tax_label.grid(row=97, column=30, padx=10, pady=10)
        self.total_label.grid(row=98, column=30, padx=10, pady=10)
        
        self.clear_btn.grid(row=99, column=28, padx=10, pady=10, sticky=tk.SE)
        self.proceed_to_checkout_btn.grid(row=99, column=30, padx=10, pady=10, sticky=tk.SE)
        
        # set initial values
        self.subtotal = 0.00
        self.tax = 0.00
        self.total = 0.00

        self.audio_output_enabled = True
        
    def add_item1(self):
        print(1)
        qty = int(self.item1_qty.get()) + 1
        self.item1_qty.set(str(qty))
        self.subtotal += 1.99
        self.update_totals()
        
    def add_item2(self):
        print(2)
        qty = int(self.item2_qty.get()) + 1
        self.item2_qty.set(str(qty))
        self.subtotal += 2.99
        self.update_totals()

    def add_item3(self):
        print(3)
        qty = int(self.item3_qty.get()) + 1
        self.item3_qty.set(str(qty))
        self.subtotal += 3.99
        self.update_totals()

    def add_item4(self):
        print(4)
        qty = int(self.item4_qty.get()) + 1
        self.item4_qty.set(str(qty))
        self.subtotal += 1.99
        self.update_totals()

    def add_item5(self):
        print(5)
        qty = int(self.item5_qty.get()) + 1
        self.item5_qty.set(str(qty))
        self.subtotal += 2.99
        self.update_totals()

    def add_item6(self):
        print(6)
        qty = int(self.item6_qty.get()) + 1
        self.item6_qty.set(str(qty))
        self.subtotal += 3.99
        self.update_totals()

    def add_item7(self):
        print(7)
        qty = int(self.item7_qty.get()) + 1
        self.item7_qty.set(str(qty))
        self.subtotal += 1.99
        self.update_totals()

    def add_item8(self):
        print(8)
        qty = int(self.item8_qty.get()) + 1
        self.item8_qty.set(str(qty))
        self.subtotal += 2.99
        self.update_totals()

    def add_item9(self):
        print(9)
        qty = int(self.item9_qty.get()) + 1
        self.item9_qty.set(str(qty))
        self.subtotal += 3.99
        self.update_totals()
    
    def clear_items(self):
        self.item1_qty.set("0")
        self.item2_qty.set("0")
        self.item3_qty.set("0")
        self.item4_qty.set("0")
        self.item5_qty.set("0")
        self.item6_qty.set("0")
        self.item7_qty.set("0")
        self.item8_qty.set("0")
        self.item9_qty.set("0")
        self.subtotal = 0.0
        self.tax = 0.0
        self.total = 0.0
        self.update_totals()
    
    def update_totals(self):
        self.subtotal_label.config(text="Subtotal: ${:.2f}".format(self.subtotal))
        self.tax = self.subtotal * 0.08875
        self.tax_label.config(text="Tax: ${:.2f}".format(self.tax))
        self.total = self.subtotal + self.tax
        self.total_label.config(text="Total: ${:.2f}".format(self.total))

    def proceed_to_checkout(self):
        items = [("Water", self.item1_qty.get()),
                 ("Chips", self.item2_qty.get()),
                 ("Soda", self.item3_qty.get()),
                 ("Cookie", self.item4_qty.get()),
                 ("Granola Bar", self.item5_qty.get()),
                 ("Doughnut", self.item6_qty.get()),
                 ("Chocolate Bar", self.item7_qty.get()),
                 ("Chocolate Cake", self.item8_qty.get()),
                 ("Pretzel", self.item9_qty.get())]
        
        items_with_qty = [(item, int(qty)) for item, qty in items if int(qty) != 0]
        
        # Speak out the quantity of each item, subtotal, and total if there are any items with non-zero quantities
        if self.audio_output_enabled and items_with_qty:
            for item, qty in items_with_qty:
                self.engine.say(f"{item}. Quantity: {qty}")
            self.engine.say(f"Subtotal: ${self.subtotal:.2f}")
            self.engine.say(f"Total: ${self.total:.2f}")
            self.engine.runAndWait()
        self.master.mainloop()


def main():
    root = tk.Tk()
    app = CashRegister(root)
    root.mainloop()
    root.__init__()

if __name__ == "__main__":
    root = tk.Tk()
    app = CashRegister(master=root)
    app.mainloop()
    main()