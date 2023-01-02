import pygame
from const import *


class Vlecenje:

    def __init__(self):
        self.figura = None
        self.vlecemo = False
        self.miskaX = 0
        self.miskaY = 0
        self.zac_vrstica = 0
        self.zac_stolpec = 0



    def blit_update(self, povrsina):
        # povecamo figuro
        self.figura.nastavi_sliko('vecji')
        slika = pygame.image.load(self.figura.slika)

        # v pravokotnik
        slika_center = (self.miskaX,self.miskaY)
        self.figura.slika_prav = slika.get_rect(center=slika_center)
        # na zaslon
        povrsina.blit(slika,self.figura.slika_prav)



    def miska_update(self, polozaj):
        self.miskaX,self.miskaY = polozaj
    
    def shrani_zacetek(self,polozaj):
        self.zac_vrstica = polozaj[1] // VELIKOST_POLJA
        self.zac_stolpec = polozaj[0] // VELIKOST_POLJA 

    def vleci_figuro(self,figura):
        self.figura = figura
        self.vlecemo = True
    
    def odvleci_figuro(self,figura):
        self.figura = None
        self.vlecemo = False
    