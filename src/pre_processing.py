import cv2 as cv


def hsv_threshhold(image, frame_name):
    # hue_low, hue_up, sat_low, sat_up, val_low, val_up = 40, 105, 40, 255, 0, 255
    hue_low = cv.getTrackbarPos("hue lower", frame_name)
    hue_up = cv.getTrackbarPos("hue upper", frame_name)
    sat_low = cv.getTrackbarPos("sat lower", frame_name)
    sat_up = cv.getTrackbarPos("sat upper", frame_name)
    val_low = cv.getTrackbarPos("val lower", frame_name)
    val_up = cv.getTrackbarPos("val upper", frame_name)

    res_frame = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    res_frame = cv.inRange(res_frame, (hue_low, sat_low, val_low), (hue_up, sat_up, val_up))
    struct = cv.getStructuringElement(cv.MORPH_RECT, ksize=(3, 3))
    res_frame = cv.erode(res_frame, struct)
    res_frame = cv.dilate(res_frame, struct)
    return res_frame
