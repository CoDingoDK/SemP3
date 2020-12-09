from vlc_controllenator import VLC_controller as vc
import threading
import CVHandler as cvh
if __name__ == "__main__":
        player = vc()
        player.vlc()
        cvh.live_feed_capture(player)
