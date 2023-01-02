import pygame
import sys

from const import *
from igra import Igra
from polje import Polje
from poteza import Poteza

class Main:

    def __init__(self):
        pygame.init()
        self.okno = pygame.display.set_mode((SIRINA,VISINA))
        pygame.display.set_caption('Šah')
        pygame.display.set_icon(kmet)
        self.igra = Igra()
    
    def mainloop(self):
        okno = self.okno
        igra = self.igra
        sahovnica = self.igra.sahovnica
        vlecenje = self.igra.vlecenje
        

        while True:
            # na zaslon
            igra.pokazi_sahovnico(okno)
            igra.pokazi_zadnjo_potezo(okno)
            igra.pokazi_poteze(okno)
            igra.pokazi_figure(okno)

            if vlecenje.vlecemo:
                # hover pokazemo med vlecenjem figure
                igra.polje_pod_misko(okno)
                vlecenje.blit_update(okno)

            for event in pygame.event.get():

                # klik
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    vlecenje.miska_update(event.pos)

                    kliknjena_vrstica = vlecenje.miskaY // VELIKOST_POLJA
                    kliknjen_stolpec = vlecenje.miskaX // VELIKOST_POLJA

                    # če je na kliknjenem polju figura
                    if sahovnica.kvadratki[kliknjena_vrstica][kliknjen_stolpec].ima_figuro():   
                        figura = sahovnica.kvadratki[kliknjena_vrstica][kliknjen_stolpec].figura

                        # če je igralec na potezi (barva)
                        if figura.barva == igra.na_potezi:
                            sahovnica.izracunaj_mozne_poteze(figura,kliknjena_vrstica,kliknjen_stolpec, bool = True)
                            

                            vlecenje.shrani_zacetek(event.pos)
                            vlecenje.vleci_figuro(figura)
                            # update zaslon
                            igra.pokazi_sahovnico(okno)
                            igra.pokazi_zadnjo_potezo(okno)
                            igra.pokazi_poteze(okno)
                            igra.pokazi_figure(okno)
                        
                
                # vlecenje
                elif event.type == pygame.MOUSEMOTION:  
                    vlecenje_vrstica = event.pos[1] // VELIKOST_POLJA
                    vlecenje_stolpec = event.pos[0] // VELIKOST_POLJA
                    # hover nad poljem
                    igra.nastavi_hover(vlecenje_vrstica,vlecenje_stolpec)

                    if vlecenje.vlecemo:
                        vlecenje.miska_update(event.pos)
                        # update zaslon
                        igra.pokazi_sahovnico(okno)
                        igra.pokazi_zadnjo_potezo(okno)
                        igra.pokazi_poteze(okno)
                        igra.pokazi_figure(okno)
                        igra.polje_pod_misko(okno)
                        vlecenje.blit_update(okno)

                # odklik
                elif event.type == pygame.MOUSEBUTTONUP: 
                    
                    if vlecenje.vlecemo:
                        vlecenje.miska_update(event.pos)

                        odklik_vrstica = vlecenje.miskaY // VELIKOST_POLJA
                        odklik_stolpec = vlecenje.miskaX // VELIKOST_POLJA

                        # ustvari možno potezo
                        zac = Polje(vlecenje.zac_vrstica,vlecenje.zac_stolpec)
                        kon = Polje(odklik_vrstica,odklik_stolpec)
                        poteza = Poteza(zac,kon)

                        # če je veljavna poteza premaknemo 
                        if sahovnica.mozna_poteza(vlecenje.figura,poteza):
                            # normalno jemanje
                            pojeden = sahovnica.kvadratki[odklik_vrstica][odklik_stolpec].ima_figuro()
                            sahovnica.poteza(vlecenje.figura,poteza)
                            
                            sahovnica.je_en_passant(vlecenje.figura)

                            # zvok
                            igra.predvajaj_zvok(pojeden)
                            # update zaslon
                            igra.pokazi_sahovnico(okno)
                            igra.pokazi_zadnjo_potezo(okno)
                            igra.pokazi_figure(okno)

                            # nasprotnikova poteza
                            igra.naslednja_poteza()   
                            # ali je šah mat
                            if igra.na_potezi == 'beli':
                                if sahovnica.je_matiran('beli'):
                                    print('\nČrni je zmagal s šah matom.\nZa novo igro pritisnite tipko R')
                            else:
                                if sahovnica.je_matiran('crni'):
                                    print('\nBeli je zmagal s šah matom.\nZa novo igro pritisnite tipko R')


                        vlecenje.odvleci_figuro(figura)
                    


                # pritisk tipke
                elif event.type == pygame.KEYDOWN:
                    # sprememba teme če kliknemo t
                    if event.key == pygame.K_t:
                        igra.spremeni_temo()
                    # restart če kliknemo r
                    if event.key == pygame.K_r:
                        igra.restart()
                        okno = self.okno
                        igra = self.igra
                        sahovnica = self.igra.sahovnica
                        vlecenje = self.igra.vlecenje
                      
                # konec
                elif event.type == pygame.QUIT:         
                    pygame.quit()
                    sys.exit()
            



            pygame.display.update()
    
main = Main()
main.mainloop()
