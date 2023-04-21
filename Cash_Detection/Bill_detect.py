import cv2
import numpy as np

def detect_cash(target_amount):
    # Load YOLOv3 network
    net = cv2.dnn.readNetFromDarknet("/home/jetson/CapstoneGUI/Cash_Detection/yolov3-tiny_testing.cfg", "/home/jetson/CapstoneGUI/Cash_Detection/yolov3-tiny_training_final.weights")

    # Load list of classes
    with open("/home/jetson/CapstoneGUI/Cash_Detection/classes.txt") as f:
        classes = [line.strip() for line in f.readlines()]

    # Initialize variables
    total_amount = 0
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)
    target_reached = False
    

    while True:
        # Check for keypress
        ret, frame = cap.read()
        key = cv2.waitKey(1)

        # If "q" key is pressed, quit the program and close all windows
        if key == ord("q"):
            break

        # If "d" key is pressed, process a single frame
        elif key == ord("d"):
            detection_running = True
            target_reached = False
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
            for value in cash_values:
                total_amount += value

           
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

