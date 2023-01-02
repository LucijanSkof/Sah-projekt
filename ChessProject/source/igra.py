import pygame

from const import *
from sahovnica import Sahovnica
from polje import *
from vlecenje import Vlecenje
from prilagajanje import Prilagodi

class Igra:

    def __init__(self):
        self.na_potezi = 'beli'
        self.hovered_polje = None
        self.sahovnica = Sahovnica()
        self.vlecenje = Vlecenje()
        self.prilagajanje = Prilagodi()
        print('\n'*12 +'Dobrodošli v igri šah.\nZa spremembo teme pritisnite tipko T.\nZa novo igro pritisnite tipko R.')

    # prikazemo uporabniku

    def pokazi_sahovnico(self,povrsina):
        tema = self.prilagajanje.tema

        for vrstica in range(VRSTICE):
            for stolpec in range(STOLPCI):
                # svetlo-temno vzorec
                if (vrstica+stolpec) % 2:
                    barva = tema.ozadje.temno 
                else:
                    barva = tema.ozadje.svetlo 
                # v pravokotnik (stolpec in vrstica inverted) 
                prav = (stolpec * VELIKOST_POLJA, vrstica * VELIKOST_POLJA,VELIKOST_POLJA,VELIKOST_POLJA)
                # na zaslon
                pygame.draw.rect(povrsina,barva,prav)

                # oštevilčenje vrstic 
                if stolpec == 0:
                    # barva
                    if vrstica % 2:
                        barva = tema.ozadje.svetlo
                    else:
                        barva = tema.ozadje.temno
                    # label
                    label = self.prilagajanje.font.render(str(VRSTICE-vrstica),1,barva)
                    label_poz = (5,5 + vrstica * VELIKOST_POLJA)
                    # na zaslon
                    povrsina.blit(label,label_poz)
                
                # oštevilčenje stolpcev
                if vrstica == 7:
                    # barva
                    if (vrstica+stolpec) % 2:
                        barva = tema.ozadje.svetlo
                    else:
                        barva = tema.ozadje.temno
                    # label
                    label = self.prilagajanje.font.render(Polje.get_crka(stolpec),1,barva)
                    label_poz = (stolpec * VELIKOST_POLJA + VELIKOST_POLJA - 20,VISINA - 20)
                    # na zaslon
                    povrsina.blit(label,label_poz)
                
    def pokazi_figure(self,povrsina):
        for vrstica in range(VRSTICE):
            for stolpec in range(STOLPCI):
                # ali je tu figura
                if self.sahovnica.kvadratki[vrstica][stolpec].ima_figuro():
                    figura = self.sahovnica.kvadratki[vrstica][stolpec].figura

                    #vse figure razen tiste ki jo vlečemo
                    if figura != self.vlecenje.figura:
                        figura.nastavi_sliko('manjsi')
                        slikica = pygame.image.load(figura.slika)
                        # v pravokotnik 
                        slikica_center = stolpec * VELIKOST_POLJA + VELIKOST_POLJA // 2, vrstica * VELIKOST_POLJA + VELIKOST_POLJA // 2      
                        figura.slika_rect = slikica.get_rect(center=slikica_center)
                        # na zaslon
                        povrsina.blit(slikica,figura.slika_rect)

    def pokazi_poteze(self,povrsina):
        tema = self.prilagajanje.tema

        if self.vlecenje.vlecemo:
            figura = self.vlecenje.figura

            # izrišemo vse možne poteze
            for poteza in figura.mozne_poteze:
                # barva
                if (poteza.kon.vrstica + poteza.kon.stolpec) % 2:
                    barva = tema.poteze.temno
                else:
                    barva = tema.poteze.svetlo
                # središče kroga
                koordinata = (poteza.kon.stolpec * VELIKOST_POLJA + VELIKOST_POLJA/2,poteza.kon.vrstica * VELIKOST_POLJA + VELIKOST_POLJA/2)
                # na zaslon 
                pygame.draw.circle(povrsina,barva,koordinata,16)
            

    
    def pokazi_zadnjo_potezo(self,povrsina):
        tema = self.prilagajanje.tema

        if self.sahovnica.zadnja_poteza:
            zac = self.sahovnica.zadnja_poteza.zac
            kon = self.sahovnica.zadnja_poteza.kon

            for poz in [zac,kon]:
                # barva
                if (poz.vrstica + poz.stolpec) % 2:
                    barva = tema.trace.temno
                else: barva = tema.trace.svetlo
                # v pravokotnik 
                prav = (poz.stolpec * VELIKOST_POLJA,poz.vrstica * VELIKOST_POLJA,VELIKOST_POLJA,VELIKOST_POLJA)
                # na zaslon 
                pygame.draw.rect(povrsina,barva,prav)
                
    def polje_pod_misko(self,povrsina): 
        if self.hovered_polje:
             # barva
                barva = (192, 201, 179)
                # v pravokotnik 
                prav = (self.hovered_polje.stolpec * VELIKOST_POLJA,self.hovered_polje.vrstica * VELIKOST_POLJA,VELIKOST_POLJA,VELIKOST_POLJA)
                # na zaslon 
                pygame.draw.rect(povrsina,barva,prav,width=4)

    def naslednja_poteza(self):
        if self.na_potezi == 'crni': self.na_potezi = 'beli'
        else: self.na_potezi = 'crni'

    def nastavi_hover(self,vrstica,stolpec):
        self.hovered_polje = self.sahovnica.kvadratki[vrstica][stolpec]

    def spremeni_temo(self):
        self.prilagajanje.spremeni_temo()
    
    def predvajaj_zvok(self,pojeden = False):
        if pojeden:
            self.prilagajanje.zvok_capture.igraj()
        else: 
            self.prilagajanje.zvok_premik.igraj()

    def restart(self):
        self.__init__()
