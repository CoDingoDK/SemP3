import time
import pre_processing as ppr
import segmentation as seg
import representation as rpr
import classification as clf
from representation import *
from vlc_impl import VLC_Controller
import cv2 as cv


def live_feed_capture(mediaplayer: VLC_Controller):
    capture = cv.VideoCapture(0)
    frame_name = "CameraFeed"
    last_cap = time.time()
    ret, frame = capture.read()
    cv.imshow(frame_name, frame)

    # Pre-processing Trackers
    cv.createTrackbar("hue lower", frame_name, 23, 360, lambda x: x)
    cv.createTrackbar("hue upper", frame_name, 102, 360, lambda x: x)

    cv.createTrackbar("sat lower", frame_name, 18, 255, lambda x: x)
    cv.createTrackbar("sat upper", frame_name, 255, 255, lambda x: x)

    cv.createTrackbar("val lower", frame_name, 0, 255, lambda x: x)
    cv.createTrackbar("val upper", frame_name, 255, 255, lambda x: x)
    # Segmentation Trackers
    # cv.createTrackbar("type variable info here", frame_name, 1, 10, lambda x: x)
    counter = 0
    seconds = 8
    start_time = time.time()
    while cv.getWindowProperty(frame_name, cv.WND_PROP_VISIBLE) != 0:
        ret, frame = capture.read()
        hand = None
        frame_masked = ppr.hsv_threshhold(frame, frame_name)
        hand_roi = seg.find_roi(frame_masked, frame_name, 50)
        if hand_roi is not None:
            hand = rpr.classify_hand(hand_roi, frame_name, 50, hand)
            im_size = 700
            if hand_roi.shape[0] <= im_size and hand_roi.shape[1] <= im_size:
                image = np.zeros([im_size, im_size], dtype=np.uint8)
                image[0:hand_roi.shape[0], 0:hand_roi.shape[1]] = hand_roi
        estimated_sign = clf.classify_hand_over_time(hand)
        mediaplayer.perform_action(estimated_sign)
        cv.waitKey(1)
        counter += 1
        if (time.time() - start_time) > seconds:
            fps = int(counter / (time.time() - start_time))
            print(f"FPS: {fps} || Response time: {int((1/fps)*1000)} ms")
            counter = 0
            start_time = time.time()
        if hand_roi is not None:
            cv.imshow(frame_name, image)
    capture.release()
    cv.destroyAllWindows()
