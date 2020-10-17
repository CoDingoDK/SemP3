import cv2 as cv
from time import time
from src import SaveSystem as ss

mouse_x, mouse_y = 0, 0


def cropper(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv.EVENT_LBUTTONDOWN:
        mouse_x, mouse_y = x, y
    if event == cv.EVENT_LBUTTONUP:
        ss.save(param[mouse_y: y, mouse_x:x], ss.SAVE_CROP)


def image_cropper(im):
    image = im
    if type(image) == str:
        image = cv.imread(image)
    cv.imshow("Image", image)
    cv.setMouseCallback("Image", cropper, image)
    cv.waitKey()
    print("crop saved")

def live_feed_capture():
    # Fetch the webcam feed
    capture = cv.VideoCapture(0)

    # time since the last capture
    last_cap = time()

    # Read the first image from the feed
    ret, frame = capture.read()

    # Initialize the openCV window so its AutoSize property becomes != -1
    cv.imshow("CameraFeed", frame)

    # If the user presses X on the window, this loop breaks and the program exits
    while cv.getWindowProperty("CameraFeed", cv.WND_PROP_AUTOSIZE) != -1:
        ret, frame = capture.read()

        cv.imshow("CameraFeed", frame)
        frame_time = time()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        key = cv.waitKey(1) & 0xFF
        if  key == ord('q'):
            break
        if key == ord('c'):
            if frame_time - last_cap > 1:
                ss.save(frame, ss.SAVE_VIDEOCAP)
                last_cap = time()
        if key == ord('g'):
            if frame_time - last_cap > 1:
                ss.save(gray, ss.SAVE_VIDEOCAP)
                last_cap = time()
    capture.release()
    cv.destroyAllWindows()
