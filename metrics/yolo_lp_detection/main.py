import cv2
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from controllers import controller

ai = controller.AIModel()

img = cv2.imread('test_images/8.jpg')
lp_results = ai.detect_license_plate(frame=img)
x1, y1, x2, y2 = lp_results[0].boxes[0].xyxy[0]
cropped_lp = img[int(y1.item()):int(y2.item()), int(x1.item()):int(x2.item())]
cropped_lp = cv2.resize(cropped_lp, (0,0), fx=3, fy=3)
cropped_lp = cv2.cvtColor(cropped_lp, cv2.COLOR_BGR2GRAY)
_, cropped_lp = cv2.threshold(cropped_lp, 64, 255, cv2.THRESH_BINARY_INV)
cropped_lp = cv2.GaussianBlur(cropped_lp, (11,11), 0)
cv2.imwrite('cropped_lp.jpg', cropped_lp)

predicted = ai.validate_license_number(frame=cropped_lp)
print('predicted: ', predicted)