import cv2 as cv
import numpy as np


def find_roi(image, frame_name, size):
    res = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    res = cv.flip(res, 1)

    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(res, 8, cv.CV_32S)
    largest_area = 0
    index_largest_area = 0
    for i, row in enumerate(stats):
        if row[4] > largest_area and i != 0:
            largest_area = row[4]
            index_largest_area = i
    labels = labels.astype(np.uint8)
    roi_object = stats[index_largest_area], centroids[index_largest_area]
    if largest_area >= size and num_labels > 1:  # Ignore ROI if the largest ROI is smaller than some minimum size.
        labels[labels != index_largest_area] = 0
        labels[labels == index_largest_area] = 255
        return make_roi_image(labels, stats[index_largest_area]), roi_object
    else:
        return np.zeros([1, 1], dtype=np.uint8), None


def make_roi_image(image, pos):
    x, y, w, h, _ = pos
    if 0 <= x <= image.shape[0] and 0 <= y <= image.shape[1]:
        x_boundary, y_boundary = int(w*0.05), int(h*0.05)
        if 0 <= x - x_boundary <= x + x_boundary <= image.shape[0] and 0 <= y - y_boundary <= y + y_boundary <= image.shape[1]:
            return image[y - y_boundary: y + h + y_boundary, x - x_boundary: x + w + x_boundary]
        else:
            return image[y:y+h, x:x+w]
    else:
        return None
