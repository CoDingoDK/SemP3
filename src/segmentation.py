import cv2 as cv
import numpy as np

def segmentation(image, frame_name, size):
    #Find ROI
    res = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, labels, stats, _ = cv.connectedComponentsWithStats(res, 8, cv.CV_32S)
    largest_area = 0
    index_largest_area = 0
    for i, row in enumerate(stats):
        if row[4] > largest_area and i != 0:
            largest_area = row[4]
            index_largest_area = i
    labels = labels.astype(np.uint8)
    if largest_area >= size:
        labels[labels != index_largest_area] = 0
        labels[labels == index_largest_area] = 255
        return labels, stats[index_largest_area]
    else:
        return np.zeros(labels.shape,dtype=np.uint8), stats[0]