import vlc
import os
import tkinter as tk


class VLC_controller:

    def __init__(self):
        self.media_player = vlc.MediaPlayer()
        self.med = []
        self.volume_cont = 50
        self.index = 0
        self.directory = r"C:\Users\thoma\Documents\3rd sem\Project\SemP3\src\ressources\medias"
        self.path = "ressources\\medias\\"
        self.inpts = None



    def load_media(self):
        for filename in os.listdir(self.directory):
            if filename.endswith(".mp4") or filename.endswith(".mp3"):
                self.med.append(filename)

    def start_media(self):
        if self.inpts == "s":
            self.media_player.play()

    def stop_media(self):
        if self.inpts == "x":
            self.media_player.stop()
            exit()


    def volume_up(self):
        if self.inpts == "u":
            self.volume_cont += 10
            self.media_player.audio_set_volume(self.volume_cont)

    def volume_down(self):
        if self.inpts == "j":
            self.volume_cont -= 10
            self.media_player.audio_set_volume(self.volume_cont)

    def channel_back(self):
        if self.inpts == "k":
            if self.index <= 0:
                self.index = len(self.med) - 1
                self.media_player.set_media(vlc.Media(self.path + self.med[self.index]))
                self.media_player.play()
            else:
                self.index -= 1
                self.media_player.set_media(vlc.Media(self.path + self.med[self.index]))
                self.media_player.play()

    def channel_forth(self):
        if self.inpts == "l":
            if self.index < len(self.med) - 1:
                self.index += 1
                self.media_player.set_media(vlc.Media(self.path + self.med[self.index]))
                self.media_player.play()
            else:
                self.index = 0
                self.media_player.set_media(vlc.Media(self.path + self.med[self.index]))
                self.media_player.play()

    def media_loop(self):
        self.media_player.set_media(vlc.Media(self.path + self.med[self.index]))
        self.media_player.video_set_scale(0.3)
        while True:
            self.inpts = input("press s to start, u/j to turn volume up/down, k/l to change channels and x to stop: ")
            self.media_player.audio_set_volume(self.volume_cont)
            self.start_media()
            self.stop_media()
            self.volume_up()
            self.volume_down()
            self.channel_back()
            self.channel_forth()

    def vlc(self):
        self.load_media()
        self.media_loop()



