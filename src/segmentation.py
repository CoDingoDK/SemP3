import cv2 as cv
import numpy as np

def segmentation(image, frame_name):
    #Find ROI
    res = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(res, 8, cv.CV_32S)
    largest_area = 0
    index_largest_area = 0
    for i, row in enumerate(stats):
        if row[4] > largest_area and i != 0:
            largest_area = row[4]
            index_largest_area = i
    x, y, width, height, _ = stats[index_largest_area]
    # res = cv.bitwise_and(image, res[x:x+width, y:y+height])
    #
    res = cv.rectangle(res, (x, y), (x+width, y+height), 255)

    return res