import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk

def detect_cash(target_amount):
    def iou(box1, box2):
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        xi1, yi1, xi2, yi2 = max(x1, x2), max(y1, y2), min(x1 + w1, x2 + w2), min(y1 + h1, y2 + h2)
        if xi2 <= xi1 or yi2 <= yi1:
            return 0.0
        intersection_area = (xi2 - xi1) * (yi2 - yi1)
        box1_area = w1 * h1
        box2_area = w2 * h2
        union_area = box1_area + box2_area - intersection_area
        iou = intersection_area / union_area
        return iou
    # Load YOLOv3 network
    net = cv2.dnn.readNetFromDarknet("/home/jetson/Desktop/CapstoneGUI/Cash_Detection/yolov3-tiny_testing.cfg", "/home/jetson/Desktop/CapstoneGUI/Cash_Detection/yolov3-tiny_training_final.weights")

    # Load list of classes
    with open("/home/jetson/Desktop/CapstoneGUI/Cash_Detection/classes.txt") as f:
        classes = [line.strip() for line in f.readlines()]

    # Initialize variables
    total_amount = 0
    detected_objects = []
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)
    frames_to_live = 30
    target_reached = False
    
    while True:
        # Check for keypress
        ret, frame = cap.read()

        if ret:
            # Convert frame to a blob to feed into YOLOv3
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)

            # Feed the blob into the neural network and get the output predictions
            net.setInput(blob)
            layer_outputs = net.forward(net.getUnconnectedOutLayersNames())

            # Initialize lists for detected cash objects and their corresponding monetary values
            cash_objects = []
            cash_values = []

            # Loop through each output layer and detect cash objects
            for output in layer_outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5 and (classes[class_id].startswith("dollar_") or classes[class_id].startswith("coin_")):
                        # Extract bounding box coordinates and monetary value of cash object
                        box = detection[:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                        cash_objects.append(box.astype("int"))
                        if classes[class_id].startswith("dollar_"):
                            cash_values.append(int(classes[class_id].split("_")[1]))
                        else:
                            cash_values.append(0.01 if classes[class_id] == "coin_penny" else 0.05 if classes[class_id] == "coin_nickel" else 0.1 if classes[class_id] == "coin_dime" else 0.25)

        # Loop through each detected cash object and add its monetary value to the total amount
            Sindices = []
            if len(cash_objects) > 0:
                indices = cv2.dnn.NMSBoxes(cash_objects, [1.0]*len(cash_objects), 0.5, 0.5)
            else: 
                indices=[]
        

            for i in np.array(indices).flatten():
                current_box = cash_objects[i]
                matched_prev_box = False

                # Compare current_box to each box in prev_cash_objects using the Intersection over Union (IoU) metric
                for detected_obj in detected_objects:
                    if iou(current_box[:4], detected_obj['box'][:4]) > 0.5:
                        matched_prev_box = True
                        break
                            
        # Only add the cash value if current_box does not match any box in prev_cash_objects
                if not matched_prev_box:
                    total_amount += cash_values[i]
                    print("Total amount: ${:.2f}".format(total_amount))
                    detected_objects.append({"box": current_box, "ttl": frames_to_live})
            detected_objects = [{"box": obj["box"], "ttl": obj["ttl"] - 1} for obj in detected_objects if obj["ttl"] > 0]


            if len(indices)>0:
                cash_values = [cash_values[int(i)]for i in indices]
            else:
                cash_values=[] 

        
        # Check if target amount has been reached
        if total_amount >= target_amount:
            target_reached = True

            # Display message when target amount is reached
            cv2.putText(frame, "Target amount reached!", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            break
        # Display the total amount and change required on the frame
        # Display the total amount and change required on the frame
        cv2.putText(frame, "Total amount: ${:.2f}".format(total_amount), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, "Amount needed: ${:.2f}".format(target_amount - total_amount), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'd' to detect, 'q' to add coins", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


        # Display the frame
        cv2.imshow("Cash Detection", frame)

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
    return total_amount

def detect_cash_with_buttons(target_amount):
    def on_detect_button_click():
        nonlocal detect_flag
        detect_flag = True

    def on_quit_button_click():
        nonlocal quit_flag
        quit_flag = True

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Cash Detection")

    video_label = ttk.Label(root)
    video_label.grid(column=0, row=0, columnspan=2)

    # Create a button to start detecting cash
    detect_button = ttk.Button(root, text="Detect", command=on_detect_button_click)
    detect_button.grid(column=0, row=0)

    # Create a button to quit the program
    quit_button = ttk.Button(root, text="Quit", command=on_quit_button_click)
    quit_button.grid(column=1, row=0)

    # Initialize flags for button clicks
    detect_flag = False
    quit_flag = False

    cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)

    def update_video_feed():
        nonlocal cap
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.config(image=imgtk)
            video_label.image = imgtk

    def update_loop():
        nonlocal detect_flag, quit_flag
        while not quit_flag:
            if detect_flag:
                detect_flag = False
                total_amount = detect_cash(target_amount)
                # Do something with total_amount, e.g., display it in the GUI
                update_video_feed()
            root.update_idletasks()
            root.update()

    # Start the update loop in a separate thread
    update_thread = Thread(target=update_loop)
    update_thread.start()

    # Start the Tkinter main loop
    root.mainloop()

# Call the modified function with buttons
detect_cash_with_buttons(20)

