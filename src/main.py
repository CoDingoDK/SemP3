from src import GrassFire
import cv2 as cv

if __name__ == "__main__":
    # cvh.image_cropper("ressources/raw-captures/color/0.png")
    img = cv.imread("ressources/raw-captures/color/0.png",0)
    res = GrassFire.findAllComponents(img, 50, 5)
    cv.imshow("yea", res[0])
    cv.waitKey()