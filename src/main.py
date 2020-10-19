import cv2 as cv
import numpy as np
import CVHandler as cvh
if __name__ == "__main__":
    cvh.image_cropper("ressources/raw-captures/color/0.png")
    # cvh.live_feed_capture()


    # img = cv.imread("shapes.png",0)

    # retval, ccs = cv.connectedComponents(img)
    # ccs = np.asarray(ccs, dtype=np.uint8)
    #
    # i = 0
    # for x in range(1, retval, 1):
    #     temp = np.copy(ccs)
    #     temp[temp != x] = 0
    #     temp[temp > 0] = 255
    #     cv.imshow("cc", temp)
    #     cv.waitKey()