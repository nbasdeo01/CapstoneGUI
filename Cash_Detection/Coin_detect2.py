import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread

def update_total_price(total_amount, target_amount):
    total_amount = total_amount
    target_amount = target_amount
    frame_amount = 0
    frame_label = None
    coin_values = {
        'penny': 0.01,
        'nickel': 0.05,
        'dime': 0.10,
        'quarter': 0.25
    }

    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 10
    params.maxThreshold = 200
    params.filterByArea = True
    params.minArea = 1000
    params.maxArea = 100000
    params.filterByCircularity = True
    params.minCircularity = 0.8
    params.filterByConvexity = True
    params.minConvexity = 0.8
    params.filterByInertia = True
    params.minInertiaRatio = 0.1
    detector = cv2.SimpleBlobDetector_create(params)
    cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)
    #cap = cv2.VideoCapture(0)
    def on_detect_click():
        global frame_amount, total_amount
        total_amount += frame_amount

    def on_quit_click():
        global running
        running = False
        window.destroy()  

    total_amount = total_amount

    def update_image_label():
        global frame_label, photo
        while running:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            keypoints = detector.detect(gray)
            frame_amount = 0

            for keypoint in keypoints:
                x = int(keypoint.pt[0])
                y = int(keypoint.pt[1])
                r = int(keypoint.size / 2)
                coin_type = None

                if 37 <= r < 41:
                    coin_type = 'dime'
                elif 46 <= r < 49:
                    coin_type = 'nickel'
                elif 50 <= r < 60:
                    coin_type = 'quarter'
                elif 42 <= r < 48:
                    coin_type = 'penny'
                else:
                    continue
                
                frame_amount += coin_values[coin_type]
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)

                cv2.putText(frame, 'Current amount: ${:.2f}'.format(total_amount), (10, 30),

                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                photo = ImageTk.PhotoImage(image)
                frame_label.config(image=photo)
                frame_label.photo = photo
                window.update_idletasks()

    running = True

    window = tk.Tk()
    window.title("Coin Detection")
    window.geometry("800x480")
    window.configure(bg="white")

    frame_label = tk.Canvas(window, width=640, height=480)
    frame_label.pack(pady=(10, 0))

    control_frame = tk.Frame(window, bg="white")
    control_frame.pack(pady=(10, 0))

    detect_button = tk.Button(control_frame, text="Detect", command=on_detect_click, width=20, height=2, bg="dodger blue", fg="white", font=("Helvetica", 12))
    detect_button.pack(side="left", padx=(10, 10))

    quit_button = tk.Button(control_frame, text="Quit", command=on_quit_click, width=20, height=2, bg="red", fg="white", font=("Helvetica", 12))
    quit_button.pack(side="left", padx=(10, 10))

    update_image_thread = Thread(target=update_image_label)
    update_image_thread.start()

    window.mainloop()

    print('Total amount: $%.2f' % total_amount)
    cap.release()
    cv2.destroyAllWindows()

    return total_amount, frame_amount
