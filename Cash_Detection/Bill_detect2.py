import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread, Lock

def detect_cash(target_amount):
    # Variables
    cap = None
    target_reached = False
    frame_label = None
    window = None
    running = True
    total_amount = 0
    process_frame = False
    frame_lock = Lock()
    shared_frame = None

    # Button Functions
    def on_detect_click():
        nonlocal process_frame
        process_frame = True

    def on_quit_click():
        nonlocal target_reached, running
        target_reached = True
        running = False
        if cap is not None:
            cap.release()
        window.destroy()

    # Capture Frames
    def capture_frames():
        nonlocal cap, running, shared_frame
        cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)  # Change this to your camera source
        running = True
        while running:
            ret, frame = cap.read()
            if ret:
                with frame_lock:
                    shared_frame = frame.copy()
            else:
                break
        cap.release()

    # Display Frames
    def update_image_label():
        nonlocal frame_label, shared_frame
        while not target_reached and running:
            with frame_lock:
                if shared_frame is not None:
                    image = Image.fromarray(cv2.cvtColor(shared_frame, cv2.COLOR_BGR2RGB))
                    image = image.resize((640, 360), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    frame_label.config(image=photo)
                    frame_label.image = photo
            window.update_idletasks()

    # Main Function
    def main_function():
        global total_amount
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
        net = cv2.dnn.readNetFromDarknet("Cash_Detection/yolov3-tiny_testing.cfg", "Cash_Detection/yolov3-tiny_training_final.weights")

        # Load list of classes
        with open("Cash_Detection/classes.txt") as f:
            classes = [line.strip() for line in f.readlines()]

        # Initialize variables
        total_amount = 0
        detected_objects = []
        frames_to_live = 30
        #cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)
        process_frame = False
        target_reached = False
        
        while not target_reached and running:
            with frame_lock:
                if shared_frame is not None:
                    frame = shared_frame.copy()
            if process_frame:
                process_frame = False
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
                    indices = []
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
            frame_lock.acquire()
            cv2.putText(frame, "Total amount: ${:.2f}".format(total_amount), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, "Amount needed: ${:.2f}".format(target_amount - total_amount), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'Detect' to detect, 'Quit' to add coins", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(image)
            frame_label.config(image=photo)
            frame_label.photo = photo
            frame_lock.release()
            pass
        window.update_idletasks()
    # Release the camera and close all windows
        cap.release()
        cv2.destroyAllWindows()
        
    # Create GUI
    window = tk.Tk()
    window.title("Cash Detection")
    window.geometry("800x480")
    window.configure(bg="white")

    frame_label = tk.Label(window)
    frame_label.pack(pady=(10, 0))

    control_frame = tk.Frame(window, bg="white")
    control_frame.pack(pady=(10, 0))

    detect_button = tk.Button(control_frame, text="Detect", command=on_detect_click, width=20, height=2, bg="dodger blue", fg="white", font=("Helvetica", 12))
    detect_button.pack(side="left", padx=(10, 10))

    quit_button = tk.Button(control_frame, text="Quit", command=on_quit_click, width=20, height=2, bg="red", fg="white", font=("Helvetica", 12))
    quit_button.pack(side="left", padx=(10, 10))

    # Start Threads
    capture_frames_thread = Thread(target=capture_frames)
    capture_frames_thread.start()

    main_function_thread = Thread(target=main_function)
    main_function_thread.start()

    update_image_thread = Thread(target=update_image_label)
    update_image_thread.start()

    window.mainloop()
    return total_amount

detect_cash(10)
