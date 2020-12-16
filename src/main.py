from vlc_impl import VLC_Controller
import CVHandler as cvh

if __name__ == "__main__":
    player = VLC_Controller()
    cvh.live_feed_capture(player)
