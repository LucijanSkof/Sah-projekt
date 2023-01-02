import pygame

class Zvok:

    def __init__(self,path):
        self.path = path
        self.zvok = pygame.mixer.Sound(path)

    def igraj(self):
        pygame.mixer.Sound.play(self.zvok)