import tkinter as tk
from Bill_detect2 import detect_cash

def detect_button_pressed():
    global total_amount
    total_amount = detect_cash(target_amount)
    print("Total amount after bills detection: ${:.2f}".format(total_amount))

def quit_button_pressed():
    root.quit()

# Set your target amount here
target_amount = 10

root = tk.Tk()

detect_button = tk.Button(root, text="Detect", command=detect_button_pressed)
detect_button.pack()

quit_button = tk.Button(root, text="Quit", command=quit_button_pressed)
quit_button.pack()

root.mainloop()
