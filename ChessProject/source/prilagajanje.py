import pygame
import os

from zvok import Zvok
from teme import Tema

class Prilagodi:

    def __init__(self):
        self.teme = []
        self.dodaj_temo()
        self.index = 0
        self.tema = self.teme[self.index]
        self.font = pygame.font.SysFont('arial',18,bold = True)
        self.zvok_premik = Zvok(os.path.join('source/sounds/move.mp3'))
        self.zvok_capture = Zvok(os.path.join('source/sounds/capture.mp3'))

    
    def spremeni_temo(self):
        self.index += 1
        # če smo na zadnji temi, bo naslednja prva
        self.index %= len(self.teme) 
        self.tema = self.teme[self.index]

    def dodaj_temo(self):
        zelena = Tema((234,235,200),(119,154,88),(244,247,116),(172,195,51),'#cecfb0','#64824a')
        rjava = Tema((235,209,166),(165,117,80),(245,234,100),(209,189,59),'#bda784','#805b3e')
        modra = Tema((229,228,200),(60,95,135),(123,187,227),(43,119,191),'#b5b49f','#2d4866')
        siva = Tema((120,119,118),(86,85,84),(99,126,143),(82,102,128),'#61605f','#474746')

        self.teme = [zelena, rjava, modra,siva]
        180, 181, 154