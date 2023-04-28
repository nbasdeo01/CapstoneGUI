import sys 
sys.path.append('/Users/nicholasbasdeo/CapstoneGUI/Cash_Detection/yolov5')

import cv2
import numpy as np
import os
from gtts import gTTS
from playsound import playsound
import torch
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import check_img_size, non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device
import torch.nn.functional as F


def detect_cash(target_amount):
    def is_inside(pos, rect):
        x, y, w, h = rect
        px, py = pos
        return x < px < x + w and y < py < y + h
    
    detect_quit_flags = [False, False]
    def on_mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if is_inside((x, y), detect_button_rect):
                detect_quit_flags[0] = True
            elif is_inside((x, y), quit_button_rect):
                detect_quit_flags[1] = True

    # Create the OpenCV window and set the mouse callback
    cv2.namedWindow("Cash Detection")
    cv2.setMouseCallback("Cash Detection", on_mouse_click)

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
    
    def nms_boxes(boxes, scores, iou_threshold):
        if not boxes:
            return [], []

        # Convert boxes to numpy array and extract box areas
        boxes = np.array(boxes)
        box_areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])

        # Sort box scores in descending order and get the sorted indices
        sorted_indices = np.argsort(scores)[::-1]

        keep = []
        while sorted_indices.size > 0:
            i = sorted_indices[0]  # Get the index of the current box with the highest score
            keep.append(i)  # Keep this box

            # Calculate IoU between the current box and the remaining boxes
            ious = iou(boxes[i], boxes[sorted_indices[1:]])

            # Remove indices of the boxes that have IoU greater than the threshold with the current box
            sorted_indices = sorted_indices[np.where(ious <= iou_threshold)[0] + 1]

        return [boxes[keep].tolist(), [scores[i] for i in keep]]

    # Load YOLOv5s network
    device = select_device()
    half = device.type != 'cpu'
    model = attempt_load('/Users/nicholasbasdeo/CapstoneGUI/Cash_Detection/best.pt').to(device)  # Update the path to the YOLOv5s weights
    imgsz = check_img_size(640, s=model.stride.max())
    if half:
        model.half()

    with open("/Users/nicholasbasdeo/CapstoneGUI/Cash_Detection/classes.yaml") as f:
        classes = [line.strip() for line in f.readlines()]

    # Initialize variables
    total_amount = 0
    detected_objects = []
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)
    frames_to_live = 30
    target_reached = False
    button_width = 150
    button_height = 50
    button_spacing = 20
    screen_width = 640
    screen_height = 480
    buttons_y = screen_height - button_height - 20
    detect_button_rect = ((screen_width - button_width * 2 - button_spacing) // 2, buttons_y, button_width, button_height)
    quit_button_rect = (detect_button_rect[0] + button_width + button_spacing, buttons_y, button_width, button_height)

    while True:
        # Check for keypress
        ret, frame = cap.read()

        # If "q" key is pressed, quit the program and close all windows
        if detect_quit_flags[1]:
            break

        # If "d" key is pressed, process a single frame
        elif detect_quit_flags[0]:
            detection_running = True
            target_reached = False
            ret, frame = cap.read()

            if ret:
                # Convert frame to a tensor to feed into YOLOv5s
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_tensor = torch.from_numpy(frame_rgb).to(device).float()
                img_tensor = img_tensor.permute(2, 0, 1).unsqueeze(0)
                img_tensor /= 255.0  # Normalize pixel values to the range [0, 1]
                if imgsz != model.stride.max():
                    img_tensor = F.interpolate(img_tensor, size=imgsz, mode='bilinear', align_corners=False)

                # Feed the tensor into the neural network and get the output predictions
                with torch.no_grad():
                    pred = model(img_tensor, augment=False)[0]
                    pred = non_max_suppression(pred, 0.5, 0.5, classes=None, agnostic=True)

                # Initialize lists for detected cash objects and their corresponding monetary values
                cash_objects = []
                cash_values = []

                # Loop through each output layer and detect cash objects
                for i, det in enumerate(pred):  # Loop through detections
                    if len(det):
                        det[:, :4] = scale_boxes(img_tensor.shape[2:], det[:, :4], frame_rgb.shape).round()
                        for *xyxy, conf, cls in reversed(det):
                            # Process each detection here
                            x1, y1, x2, y2 = [int(x.item()) for x in xyxy]  # Extract the bounding box coordinates
                            class_id = int(cls.item())  # Extract the class ID
                            confidence = float(conf.item())  # Extract the confidence score

                            # Check if the detected object belongs to the cash classes
                            cash_class = classes[class_id]
                            if cash_class.startswith("dollar_") or cash_class.startswith("coin_"):
                                cash_objects.append((x1, y1, x2 - x1, y2 - y1))  # Add the bounding box to the cash_objects list
                                # Determine the monetary value of the detected cash object
                                if cash_class.startswith("dollar_"):
                                    cash_value = int(cash_class.split("_")[1])
                                else:
                                    cash_value = (0.01 if cash_class == "coin_penny"
                                                else 0.05 if cash_class == "coin_nickel"
                                                else 0.1 if cash_class == "coin_dime"
                                                else 0.25 if cash_class == "coin_quarter"
                                                else 0)  # Set to 0 if the coin class is unknown
                                cash_values.append(cash_value)  # Add the monetary value to the cash_values list


                # Perform non-maximum suppression to remove overlapping detections
                cash_objects, cash_values = nms_boxes(cash_objects, cash_values, 0.5)

                # Loop through each detected cash object and add its monetary value to the total amount
                for i in range(len(cash_objects)):
                    current_box = cash_objects[i]
                    matched_prev_box = False

                    # Compare current_box to each box in prev_cash_objects using the Intersection over Union (IoU) metric
                    for detected_obj in detected_objects:
                        if iou(current_box, detected_obj['box']) > 0.5:
                            matched_prev_box = True
                            break

                    # Only add the cash value if current_box does not match any box in prev_cash_objects
                    if not matched_prev_box:
                        total_amount += cash_values[i]
                        print("Total amount: ${:.2f}".format(total_amount))
                        detected_objects.append({"box": current_box, "ttl": frames_to_live})
                        spoken_bill = f"{cash_values[i]} dollars detected."
                        tts = gTTS(spoken_bill, lang='en')
                        tts.save("bill.mp3")
                        playsound("bill.mp3")
                        # Remove the temporary speech file
                        os.remove("bill.mp3")

                detected_objects = [{"box": obj["box"], "ttl": obj["ttl"] - 1} for obj in detected_objects if obj["ttl"] > 0]

                # Check if target amount has been reached
                if total_amount >= target_amount:
                    target_reached = True

                    # Display message when target amount is reached
                    cv2.putText(frame, "Target amount reached!", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    break
            detect_quit_flags[0] = False
        detect_quit_flags[1] = False   
        button_color = (200, 200, 200)
        text_color = (0, 0, 0)
        font = cv2.FONT_HERSHEY_TRIPLEX
        # Draw the "Detect" button
        cv2.rectangle(frame, (detect_button_rect[0], detect_button_rect[1]), (detect_button_rect[0] + detect_button_rect[2], detect_button_rect[1] + detect_button_rect[3]), button_color, -1)
        cv2.rectangle(frame, (detect_button_rect[0], detect_button_rect[1]), (detect_button_rect[0] + detect_button_rect[2], detect_button_rect[1] + detect_button_rect[3]), (0, 255, 0), 2)
        (text_width, text_height), _ = cv2.getTextSize("Detect", font, 0.6, 2)
        cv2.putText(frame, "Detect", (detect_button_rect[0] + (detect_button_rect[2] - text_width) // 2, detect_button_rect[1] + (detect_button_rect[3] + text_height) // 2), font, 0.6, text_color, 2)

        # Draw the "Coins" button
        cv2.rectangle(frame, (quit_button_rect[0], quit_button_rect[1]), (quit_button_rect[0] + quit_button_rect[2], quit_button_rect[1] + quit_button_rect[3]), button_color, -1)
        cv2.rectangle(frame, (quit_button_rect[0], quit_button_rect[1]), (quit_button_rect[0] + quit_button_rect[2], quit_button_rect[1] + quit_button_rect[3]), (255, 0, 0), 2)
        (text_width, text_height), _ = cv2.getTextSize("Coins", font, 0.6, 2)
        cv2.putText(frame, "Coins", (quit_button_rect[0] + (quit_button_rect[2] - text_width) // 2, quit_button_rect[1] + (quit_button_rect[3] + text_height) // 2), font, 0.6, text_color, 2)

        # Display the total amount and change required on the frame
        cv2.putText(frame, "Total amount: ${:.2f}".format(total_amount), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, "Amount needed: ${:.2f}".format(target_amount - total_amount), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        #cv2.putText(frame, "Press 'd' to detect, 'q' to add coins", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        # Display the frame
        cv2.imshow("Cash Detection", frame)
        key = cv2.waitKey(1) & 0xFF
    
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
    return total_amount
detect_cash(10)