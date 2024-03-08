import cv2
import numpy as np
from ultralytics import YOLO

import control
from sort.sort import *
import math
from control import getCar, readLP, write_csv

# Load model
model = YOLO('models/vanilla/yolov8x.pt')
#model = YOLO('models/trained/trained_yolov8s.pt')
lp_detector_model = YOLO('models/vanilla/yolov8x.pt')
lp_detector_model = YOLO('./models/lp/trained_yolov8n_1.pt')

# Load video source
cap = cv2.VideoCapture('testing_video/sample_lp_videoplayback.mp4')

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

            if carID != -1:
                #crop LP
                licensePlateCrop = frame[int(y1): int(y2), int(x1): int(x2), :]

                #process LP
                licensePlateCropGray = cv2.cvtColor(licensePlateCrop, cv2.COLOR_BGR2GRAY)
                _, licensePlateCropThreshold = cv2.threshold(licensePlateCrop, 64, 255, cv2.THRESH_BINARY_INV)

                #read LP
                licensePlateText, licensePlateTextConfScore = readLP(licensePlateCropThreshold)

                if licensePlateText is not None:
                    results[frameNumber][carID] = {'car': {'carBox': [xcar1, ycar1, xcar2, ycar2]},
                                                  'license_Plate': {'lpBox': [x1, y1, x2, y2],
                                                                    'text': licensePlateText,
                                                                    'boxScore': score,
                                                                    'textScore': licensePlateTextConfScore}}

#results
write_csv(results, './test.csv')

