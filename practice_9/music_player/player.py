import pygame

class Player:
    def __init__(self):
        pygame.mixer.init()

        self.playlist = ["music/track1.wav", "music/track2.wav"]
        self.index = 0

    def play(self):
        pygame.mixer.music.load(self.playlist[self.index])
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.index = (self.index + 1) % len(self.playlist)
        self.play()

    def back(self):
        self.index = (self.index - 1) % len(self.playlist)
        self.play()