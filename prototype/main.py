import cv2
import numpy as np
from ultralytics import YOLO

import control
from sort.sort import *
import math
from control import getCar, readLP, write_csv

# Load model
model = YOLO('models/vanilla/yolov8x.pt')
lp_detector_model = YOLO('models/vanilla/yolov8x.pt')

# Load video source
cap = cv2.VideoCapture('sample.mp4')

# Declarations
vehicles = [2, 3, 5, 7]

classNames = {
    2: 'car',
    3: 'motorcycle',
    5: 'bus',
    7: 'truck'
}

results = {}
motTracker = Sort()

# Function to draw bounding box with class name and confidence
# Modify the bounding_box function to expect only bounding box coordinates
def bounding_box(frame, box, classNames):
    x1, y1, x2, y2, score, class_id = box
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 50, 50), 2)

    confidence = math.ceil((score * 100)) / 100

    org = [x1, y1]
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 2
    color = (255, 255, 255)
    thickness = 2

    cv2.putText(frame, classNames[class_id] + ' ' + str(confidence), tuple(org), font, fontScale, color, thickness)

    # Draw bounding boxes
    '''
    for detection in detections_:
        bounding_box(frame, detection, classNames)  # Pass classNames here


    # Display frame

    cv2.imshow('Frame', frame)
    cv2.waitKey(1)
    '''


# Read frames
frameNumber = -1
ret = True
while ret:
    frameNumber += 1
    ret, frame = cap.read()
    if ret and frameNumber < 10:
        results[frameNumber] = {}
        detections = model(frame)[0]
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                detections_.append([x1, y1, x2, y2, score, class_id])

        # Track vehicles
        trackIDs = motTracker.update(np.asarray(detections_))

        # Detect license plates
        licensePlates = lp_detector_model(frame)[0]
        for licensePlate in licensePlates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = licensePlate

            #assign LP
            xcar1, ycar1, xcar2, ycar2, carID = getCar(licensePlate, trackIDs)

            #if carID != -1:
            #crop LP
            licensePlateCrop = frame[int(y1): int(y2), int(x1): int(x2), :]

            #process LP
            licensePlateCropGray = cv2.cvtColor(licensePlateCrop, cv2.COLOR_BGR2GRAY)
            _, licensePlateCropThreshold = cv2.threshold(licensePlateCrop, 64, 255, cv2.THRESH_BINARY_INV)

            #read LP
            licensePlateText, licensePlateTextConfScore = readLP(licensePlateCropThreshold)


            if licensePlateText is not None:
                results[frameNumber][carID] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                              'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                'text': licensePlateText,
                                                                'bbox_score': score,
                                                                'text_score': licensePlateTextConfScore}}

#results
write_csv(results, './test.csv')