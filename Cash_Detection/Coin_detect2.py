import cv2
import numpy as np
from gtts import gTTS
import os
import playsound

def update_total_price(total_amount, target_amount):
    coin_values = {
        'penny': 0.01,
        'nickel': 0.05,
        'dime': 0.10,
        'quarter': 0.25
    }
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

    cv2.namedWindow("Coins")
    cv2.setMouseCallback("Coins", on_mouse_click)

    button_width = 150
    button_height = 50
    button_spacing = 20
    screen_width = 640
    screen_height = 480
    buttons_y = screen_height - button_height - 20

    detect_button_rect = ((screen_width - button_width * 2 - button_spacing) // 2, buttons_y, button_width, button_height)
    quit_button_rect = (detect_button_rect[0] + button_width + button_spacing, buttons_y, button_width, button_height) 

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
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)
    #cap = cv2.VideoCapture(0)
    total_amount = total_amount

    while total_amount < target_amount:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        keypoints = detector.detect(gray)
        frame_amount = 0

        for keypoint in keypoints:
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            r = int(keypoint.size / 2)
            coin_type = None

            if 36 <= r < 39:
                coin_type = 'dime'
            #elif 45 <= r < 47:
                #coin_type = 'nickel'
            elif 50 <= r < 53:
                coin_type = 'quarter'
            #elif 41 <= r < 43:
                #coin_type = 'penny'
            else:
                continue
            
            frame_amount += coin_values[coin_type]
            #print(coin_type)
            coin_name = str(coin_type)
            print(coin_name)
            #spoken_coin= f"{coin_name} detected."
            #tts = gTTS(spoken_coin, lang='en')
            #tts.save("change.mp3")
            #playsound("change.mp3")
            # Remove the temporary speech file
            #os.remove("change.mp3")
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)

        cv2.putText(frame, 'Current amount: ${:.2f}'.format(total_amount), (10, 30),

                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.rectangle(frame, (detect_button_rect[0], detect_button_rect[1]), (detect_button_rect[0] + detect_button_rect[2], detect_button_rect[1] + detect_button_rect[3]), (0, 255, 0), -1)        
        text_detect = "Detect"
        (text_width, text_height), _ = cv2.getTextSize(text_detect, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        text_x = detect_button_rect[0] + (detect_button_rect[2] - text_width) // 2
        text_y = detect_button_rect[1] + (detect_button_rect[3] + text_height) // 2
        cv2.putText(frame, text_detect, (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 2)

        cv2.rectangle(frame, (quit_button_rect[0], quit_button_rect[1]), (quit_button_rect[0] + quit_button_rect[2], quit_button_rect[1] + quit_button_rect[3]), (0, 0, 255), -1)
        text_quit = "Quit"
        (text_width, text_height), _ = cv2.getTextSize(text_quit, cv2.FONT_HERSHEY_DUPLEX, 0.6, 2)
        text_x = quit_button_rect[0] + (quit_button_rect[2] - text_width) // 2
        text_y = quit_button_rect[1] + (quit_button_rect[3] + text_height) // 2
        cv2.putText(frame, text_quit, (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 2)
        cv2.imshow('Coins', frame)
        key = cv2.waitKey(1) & 0xFF

        if detect_quit_flags[0]:
            total_amount += frame_amount
            print('Current amount: $%.2f' % total_amount)
        elif detect_quit_flags[1]:
            break

    print('Total amount: $%.2f' % total_amount)
    cap.release()
    cv2.destroyAllWindows()

    return total_amount, frame_amount
update_total_price(10, 20)