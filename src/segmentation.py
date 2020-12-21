import cv2 as cv
import numpy as np


def find_roi(image, frame_name, size):
    res = cv.flip(image, 1)
    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(res, 8, cv.CV_32S)
    largest_area = 0
    index_largest_area = 0
    for i, row in enumerate(stats):
        if row[4] > largest_area and i != 0:
            largest_area = row[4]
            index_largest_area = i
    labels = labels.astype(np.uint8)

    if largest_area >= size and num_labels > 1:  # Ignore ROI if the largest ROI is smaller than some minimum size.
        roi_object = stats[index_largest_area], centroids[index_largest_area]
        labels[labels != index_largest_area] = 0
        labels[labels == index_largest_area] = 255
        return make_roi_image(labels, roi_object)
    else:
        return np.zeros([1, 1], dtype=np.uint8), None


def make_roi_image(image, roi_object):
    x, y, w, h, _ = roi_object[0]
    if 0 <= x <= image.shape[0] and 0 <= y <= image.shape[1]:
        x_boundary, y_boundary = int(w*0.05), int(h*0.05)
        if 0 <= x - x_boundary <= x + x_boundary <= image.shape[0] and 0 <= y - y_boundary <= y + y_boundary <= image.shape[1]:
            x_start = x-x_boundary
            y_start = y-y_boundary
            roi_object = roi_object[0], (int(roi_object[1][0]-x_start), int(roi_object[1][1]-y_start))
            return image[y - y_boundary: y + h + y_boundary, x - x_boundary: x + w + x_boundary], roi_object
        else:
            return image[y:y+h, x:x+w], roi_object
    else:
        return None, None
