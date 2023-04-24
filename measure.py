import cv2
import numpy as np

# Load the image
img = cv2.imread('coins.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to the image
blur = cv2.GaussianBlur(gray, (9, 9), 0)

# Apply Canny edge detection to the image
canny = cv2.Canny(blur, 100, 200)

# Find contours in the image
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
