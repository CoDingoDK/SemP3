import vlc
import os
from hand import LEFT, RIGHT, UP, DOWN, PLAY_PAUSE


class VLC_Controller:
    def __init__(self):
        self.media_player: vlc.MediaPlayer = vlc.MediaPlayer()
        self.med = []
        self.volume_cont = 50
        self.index = 0
        self.directory = r"res\medias"
        self.path = "res\\medias\\"
        self.inpts = None
        self.load_media()
        self.media_player.play()

    def perform_action(self, sign):
        if sign == LEFT:
            print("LEFT")
            self.channel_back()
        if sign == RIGHT:
            print("RIGHT")
            self.channel_forth()
        if sign == UP:
            print("UP")
            self.volume_up()
        if sign == DOWN:
            print("DOWN")
            self.volume_down()
        if sign == PLAY_PAUSE:
            print("PLAY_PAUSE")
            if self.media_player.is_playing():
                self.media_player.pause()
            else:
                self.media_player.play()

    def load_media(self):
        for filename in os.listdir(self.directory):
            if filename.endswith(".mp4") or filename.endswith(".mp3"):
                self.med.append(filename)
        self.media_player.set_media(vlc.Media(self.path + self.med[self.index]))

    def start_media(self):
        self.media_player.play()

    def stop_media(self):
        self.media_player.stop()
        exit()

    def volume_up(self):
        self.volume_cont += 20
        self.media_player.audio_set_volume(self.volume_cont)

    def volume_down(self):
        self.volume_cont -= 20
        self.media_player.audio_set_volume(self.volume_cont)

    def channel_back(self):
        if self.index <= 0:
            self.index = len(self.med) - 1
            self.media_player.set_media(vlc.Media(self.path + self.med[self.index]))
            self.media_player.play()
        else:
            self.index -= 1
            self.media_player.set_media(vlc.Media(self.path + self.med[self.index]))
            self.media_player.play()

    def channel_forth(self):
        if self.index < len(self.med) - 1:
            self.index += 1
            self.media_player.set_media(vlc.Media(self.path + self.med[self.index]))
            self.media_player.play()
        else:
            self.index = 0
            self.media_player.set_media(vlc.Media(self.path + self.med[self.index]))
            self.media_player.play()
