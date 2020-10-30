import cv2 as cv


def pre_process(image, frame_name):
    # hue_low, hue_up, sat_low, sat_up, val_low, val_up, closing_count = 0, 33, 70, 189, 61, 206, 10

    hue_low = cv.getTrackbarPos("hue lower", frame_name)
    hue_up = cv.getTrackbarPos("hue upper", frame_name)
    sat_low = cv.getTrackbarPos("sat lower", frame_name)
    sat_up = cv.getTrackbarPos("sat upper", frame_name)
    val_low = cv.getTrackbarPos("val lower", frame_name)
    val_up = cv.getTrackbarPos("val upper", frame_name)
    closing_count = cv.getTrackbarPos("Closing count", frame_name)

    frame_masked = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    frame_masked = cv.inRange(frame_masked, (hue_low, sat_low, val_low), (hue_up, sat_up, val_up))
    struct = cv.getStructuringElement(cv.MORPH_RECT, ksize=(3, 3))
    frame_masked = cv.dilate(frame_masked, struct, iterations=2)
    frame_masked = cv.erode(frame_masked, struct)
    for i in range(closing_count):
        frame_masked = cv.dilate(frame_masked, struct, iterations=2)
    return cv.bitwise_and(image, image, mask=frame_masked)
