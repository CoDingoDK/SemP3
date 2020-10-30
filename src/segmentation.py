import cv2 as cv
import numpy as np

def segmentation(image, frame_name):
    res = image
    variable_tracker = cv.getTrackbarPos("type variable info here", frame_name)
    # Do stuff from here

    return res