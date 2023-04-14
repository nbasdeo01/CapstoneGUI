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
        self.cart_qty_label = tk.Label(self.master, text="CART QUANTITY", font=("TkDefaultFont", 18))
        self.item1_qty_label = tk.Label(self.master, textvariable=self.item1_qty, font=("TkDefaultFont", 18))
        self.item2_qty_label = tk.Label(self.master, textvariable=self.item2_qty, font=("TkDefaultFont", 18))
        self.item3_qty_label = tk.Label(self.master, textvariable=self.item3_qty, font=("TkDefaultFont", 18))
        self.item4_qty_label = tk.Label(self.master, textvariable=self.item4_qty, font=("TkDefaultFont", 18))
        self.item5_qty_label = tk.Label(self.master, textvariable=self.item5_qty, font=("TkDefaultFont", 18))
        self.item6_qty_label = tk.Label(self.master, textvariable=self.item6_qty, font=("TkDefaultFont", 18))
        self.item7_qty_label = tk.Label(self.master, textvariable=self.item7_qty, font=("TkDefaultFont", 18))
        self.item8_qty_label = tk.Label(self.master, textvariable=self.item8_qty, font=("TkDefaultFont", 18))
        self.item9_qty_label = tk.Label(self.master, textvariable=self.item9_qty, font=("TkDefaultFont", 18))

        self.item1_name_label = tk.Label(self.master, text="Water", font=("TkDefaultFont", 18))
        self.item2_name_label = tk.Label(self.master, text="Chips", font=("TkDefaultFont", 18))
        self.item3_name_label = tk.Label(self.master, text="Soda", font=("TkDefaultFont", 18))
        self.item4_name_label = tk.Label(self.master, text="Cookie", font=("TkDefaultFont", 18))
        self.item5_name_label = tk.Label(self.master, text="Granola Bar", font=("TkDefaultFont", 18))
        self.item6_name_label = tk.Label(self.master, text="Doughnut", font=("TkDefaultFont", 18))
        self.item7_name_label = tk.Label(self.master, text="Chocolate Bar", font=("TkDefaultFont", 18))
        self.item8_name_label = tk.Label(self.master, text="Chocolate Cake", font=("TkDefaultFont", 18))
        self.item9_name_label = tk.Label(self.master, text="Pretzel", font=("TkDefaultFont", 18))

        self.checkcam_btn = tk.Button(self.master, text="Checkout", command=self.proceed_to_checkout, width=30, height=5, font=("TkDefaultFont", 18))
        self.checkcam_btn = tk.Button(self.master, text="Proceed to Payment", command=self.object_detection, width=30, height=5, font=("TkDefaultFont", 18))

        # create subtotal, tax, and total labels
        self.subtotal_label = tk.Label(self.master, text="Subtotal: $0.00", font=("TkDefaultFont", 24))
        self.tax_label = tk.Label(self.master, text="Tax: $0.00", font=("TkDefaultFont", 24))
        self.total_label = tk.Label(self.master, text="Total: $0.00", font=("TkDefaultFont", 24))

        # pack everything
        self.cart_qty_label.grid(row=96, column=30, padx=5, pady=5)

        self.item1_name_label.grid(row=7, column=28, padx=10, pady=10)
        self.item2_name_label.grid(row=8, column=28, padx=10, pady=10)
        self.item3_name_label.grid(row=9, column=28, padx=10, pady=10)
        self.item4_name_label.grid(row=10, column=28, padx=10, pady=10)
        self.item5_name_label.grid(row=11, column=28, padx=10, pady=10)
        self.item6_name_label.grid(row=12, column=28, padx=10, pady=10)
        self.item7_name_label.grid(row=13, column=28, padx=10, pady=10)
        self.item8_name_label.grid(row=14, column=28, padx=10, pady=10)
        self.item9_name_label.grid(row=15, column=28, padx=10, pady=10)

        self.item1_qty_label.grid(row=97, column=30, padx=10, pady=10)
        self.item2_qty_label.grid(row=98, column=30, padx=10, pady=10)
        self.item3_qty_label.grid(row=99, column=30, padx=10, pady=10)
        self.item4_qty_label.grid(row=97, column=30, padx=10, pady=10)
        self.item5_qty_label.grid(row=98, column=30, padx=10, pady=10)
        self.item6_qty_label.grid(row=99, column=30, padx=10, pady=10)
        self.item7_qty_label.grid(row=97, column=30, padx=10, pady=10)
        self.item8_qty_label.grid(row=98, column=30, padx=10, pady=10)
        self.item9_qty_label.grid(row=99, column=30, padx=10, pady=10)

        self.subtotal_label.grid(row=96, column=30, padx=10, pady=10)
        self.tax_label.grid(row=97, column=30, padx=10, pady=10)
        self.total_label.grid(row=98, column=30, padx=10, pady=10)

        self.checkcam_btn.grid(row=100, column=30, padx=10, pady=10)

        # set initial values
        self.subtotal = 0.00
        self.tax = 0.00
        self.total = 0.00

        self.audio_output_enabled = True

    #def object_detection(self):
        #codes to be implemented later

    #def payment_process(self):

    #def open_checkout_window(self):
        #checkout_window = tk.Toplevel(self.master)
        #checkout_window.title("Checkout")
        #self.master.attributes('-fullscreen', True)
        #checkout_window.resizable(False, False)
        #checkout_label = tk.Label(checkout_window, text="Checkout Window", font=("TkDefaultFont", 18))
        #checkout_label.pack()

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
