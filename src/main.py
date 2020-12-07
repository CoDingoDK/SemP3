import cv2 as cv
import numpy as np
import time
import os
from vlc_controllenator import VLC_controller as vc
import CVHandler as cvh
from tkinter import *
if __name__ == "__main__":
        cvh.live_feed_capture()
        player = vc()
        player.vlc()

    # cvh.live_feed_capture()
