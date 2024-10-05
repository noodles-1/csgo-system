import cv2
import os
import sys
import numpy as np

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from ultralytics import YOLO
from controllers import controller
from controllers import s3controller

ai = controller.AIController()
"""
s3 = s3controller.S3Controller()
img = cv2.imread('test_images/1.jpg')
vehicle_results = ai.detect_vehicle(frame=img)

x1, y1, x2, y2 = vehicle_results[0].boxes[0].xyxy[0]
cropped_vehicle = img[int(y1.item()):int(y2.item()), int(x1.item()):int(x2.item())]
url = s3.uploadImage(image=cropped_vehicle, image_name='cropped')
print(url)
"""

img = cv2.imread('test_images/23.jpg')
lp_results = ai.detect_license_plate(frame=img)
x1, y1, x2, y2 = lp_results[0].boxes[0].xyxy[0]

cropped_lp = img[int(y1.item()):int(y2.item()), int(x1.item()):int(x2.item())]

# Convert to grayscale
gray = cv2.cvtColor(cropped_lp, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur to reduce noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply thresholding
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Apply dilation to connect text regions
kernel = np.ones((2, 2), np.uint8)
dilated = cv2.dilate(thresh, kernel, iterations=1)

# Optionally apply erosion to reduce noise
eroded = cv2.erode(dilated, kernel, iterations=1)

# Display the preprocessing results
cv2.imshow('Original Image', cropped_lp)
cv2.imshow('Grayscale', gray)
cv2.imshow('Blurred', blur)
cv2.imshow('Thresholded', thresh)
cv2.imshow('Dilated', dilated)
cv2.imshow('Eroded', eroded)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply CnOCR
results = ai.get_license_number_cnocr(frame=thresh)
temp = [results[i]['text'] for i in range(len(results))]
predicted = ''.join(temp)
predicted = predicted.replace(' ', '')
print('predicted: ', predicted)