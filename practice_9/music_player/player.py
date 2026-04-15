import pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        self.playlist = [
            "music/track1.wav",
            "music/track2.wav"
        ]
        self.current = 0

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.current = (self.current + 1) % len(self.playlist)
        self.play()

    def previous(self):
        self.current = (self.current - 1) % len(self.playlist)
        self.play()