import cv2
import numpy as np

# Open the camera
cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=640,height=480,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)


while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Show the frame
    cv2.imshow('Coins', frame)

    # Wait for the user to press the space bar
    if cv2.waitKey(1) & 0xFF == ord(' '):
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to the frame
        blur = cv2.GaussianBlur(gray, (9, 9), 0)

        # Apply Canny edge detection to the frame
        canny = cv2.Canny(blur, 100, 200)

        # Find contours in the frame
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Define a list to store the radii of the coins
        radii = []

        # Loop through the contours
        for cnt in contours:
            # Find the area of the contour
            area = cv2.contourArea(cnt)
            # Find the perimeter of the contour
            perimeter = cv2.arcLength(cnt, True)
            # Calculate the circularity of the contour
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            # If the circularity is greater than 0.8, it is likely a coin
            if circularity > 0.8:
                # Find the minimum enclosing circle of the contour
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                # Add the radius to the list
                radii.append(radius)

        # Sort the radii in descending order
        radii.sort(reverse=True)

        # Print the radii
        for radius in radii:
            print('Coin radius:', radius, 'pixels.')

    # Wait for the user to press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
