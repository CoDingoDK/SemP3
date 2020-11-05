import cv2 as cv
import numpy as np

capture = cv.VideoCapture(0)
backSub = cv.createBackgroundSubtractorMOG2(history=1000,varThreshold=20, detectShadows=False)
cv.imshow('FG Mask', capture.read()[1])

cv.createTrackbar("iter", "FG Mask", 1, 200, lambda x: x)

while True:
    ret, frame = capture.read()
    if frame is None:
        break
    iterations = cv.getTrackbarPos("iter", "FG Mask")
    fgMask = backSub.apply(frame)
    kernel = np.ones((3, 3), np.uint8)
    fgMask = cv.erode(fgMask, kernel, iterations=2)
    # fgMask = cv.dilate(fgMask, kernel,iterations=iterations)
    # closing = cv.morphologyEx(fgMask, cv.MORPH_CLOSE, kernel)

    cv.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break