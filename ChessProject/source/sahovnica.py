from const import *
from polje import Polje
from figure import *
from poteza import Poteza
from zvok import Zvok
import copy
import os


class Sahovnica:

    def __init__(self):
        self.kvadratki = [[0,0,0,0,0,0,0,0] for stolpec in range(STOLPCI)]
        self.zadnja_poteza = None
        self.ustvari_2dArray()
        self.dodaj_figure('beli')
        self.dodaj_figure('crni')

 

    def poteza(self,figura,poteza,bool=False):
        zac = poteza.zac
        kon = poteza.kon

        en_passant_prazno = self.kvadratki[kon.vrstica][kon.stolpec].je_prazno()

        # update sahovnice
        self.kvadratki[zac.vrstica][zac.stolpec].figura = None
        self.kvadratki[kon.vrstica][kon.stolpec].figura = figura

        # en passant in promoviranje kmeta
        if isinstance(figura,Kmet):
            # en passant jemanje
            raz = kon.stolpec - zac.stolpec
            # če se kmet premakne za stolpec in je tam polje prazno
            if raz != 0 and en_passant_prazno:
                # update sahovnice
                self.kvadratki[zac.vrstica][zac.stolpec + raz].figura = None
                self.kvadratki[kon.vrstica][kon.stolpec].figura = figura
                if not bool:
                    zvok = Zvok(os.path.join('source/sounds/capture.mp3'))
                    zvok.igraj()

            # promoviranje kmeta
            else: self.ali_promovira(figura,kon)

        # rošada 
        if isinstance(figura,Kralj):
            if self.rosada(zac,kon) and not bool:
                raz = kon.stolpec - zac.stolpec
                if raz < 0: top = figura.levi_top 
                else: top = figura.desni_top
                self.poteza(top,top.mozne_poteze[-1])

             
                
        # update figure
        figura.premaknjena = True        
        
        # počisti trenutne veljavne poteze (ker smo na novi poziciji)
        figura.pocisti_poteze()

        # zapomni si zadnjo potezo figure
        self.zadnja_poteza = poteza


    def mozna_poteza(self,figura,poteza):
        return poteza in figura.mozne_poteze

    def ali_promovira(self,figura,kon):
        if kon.vrstica == 0 or kon.vrstica == 7:
            self.kvadratki[kon.vrstica][kon.stolpec].figura = Dama(figura.barva)

    def rosada(self,zac,kon):
        return abs(zac.stolpec-kon.stolpec) == 2

    # en passant ni veljaven če ni zadnja poteza 
    def je_en_passant(self,figura):
        if not isinstance(figura, Kmet):
            return

        for vrstica in range(VRSTICE):
            for stolpec in range(STOLPCI):
                if isinstance(self.kvadratki[vrstica][stolpec].figura, Kmet):
                    self.kvadratki[vrstica][stolpec].figura.en_passant = False
        
        figura.en_passant = True

    def v_sahu(self,figura,poteza):
        # začasne figure in šahovnica
        temp_figura = copy.deepcopy(figura)
        temp_sahovnica = copy.deepcopy(self) # self je šahovnica
        temp_sahovnica.poteza(temp_figura,poteza,bool=True)

        # za vsako nasprotnikovo figuro na šahovnici
        for vrstica in range(VRSTICE):
            for stolpec in range(STOLPCI):
                if temp_sahovnica.kvadratki[vrstica][stolpec].ima_naspr_figuro(figura.barva):
                    fig = temp_sahovnica.kvadratki[vrstica][stolpec].figura
                    # izracunaj vse njene možne poteze
                    temp_sahovnica.izracunaj_mozne_poteze(fig,vrstica,stolpec,bool=False)
                    # če katera izmed teh potez požre kralja smo v šahu
                    for pot in fig.mozne_poteze:
                        if isinstance(pot.kon.figura,Kralj):
                            return True
        # drugače nismo                
        return False

    def je_matiran(self,barva):
        for vrstica in range(VRSTICE):
            for stolpec in range(STOLPCI):
                if self.kvadratki[vrstica][stolpec].ima_figuro():
                    fig=self.kvadratki[vrstica][stolpec].figura
                    if fig.barva == barva:
                        if self.izracunaj_mozne_poteze(fig,vrstica,stolpec,bool=True,iscemo_mat=True):
                            return False
        return True
        

    #določi vse možne poteze za figuro na določeni poziciji   (bool da se ne zaciklamo s klici v_sahu())
    def izracunaj_mozne_poteze(self,figura,vrstica,stolpec,bool=True,iscemo_mat=False):
        
        figura.pocisti_poteze()

        def skakac_poteze():
            mozne_poteze = [
                (vrstica-2,stolpec+1),
                (vrstica-1,stolpec+2),
                (vrstica+1,stolpec+2),
                (vrstica+2,stolpec+1),
                (vrstica+2,stolpec-1),
                (vrstica+1,stolpec-2),
                (vrstica-1,stolpec-2),
                (vrstica-2,stolpec-1)
            ]
            for mozna_poteza in mozne_poteze:
                mozna_poteza_vrstica,mozna_poteza_stolpec = mozna_poteza
                if Polje.na_sahovnici(mozna_poteza_vrstica,mozna_poteza_stolpec):
                    if self.kvadratki[mozna_poteza_vrstica][mozna_poteza_stolpec].je_prazno_ali_naspr(figura.barva):
                        # polja mozne poteze
                        zac = Polje(vrstica,stolpec)
                        kon_figura = self.kvadratki[mozna_poteza_vrstica][mozna_poteza_stolpec].figura
                        kon = Polje(mozna_poteza_vrstica,mozna_poteza_stolpec,kon_figura)
                        # nova mozna poteza
                        poteza = Poteza(zac, kon)
                        # če še nismo, preverimo šah
                        if bool:
                            if not self.v_sahu(figura,poteza):
                                if iscemo_mat and bool: return True
                                # dodamo mozno potezo če ni šaha
                                figura.dodaj_potezo(poteza)
                                # čim najdemo možno potezo ni mat

                        else:
                            # drugace samo dodamo potezo
                            figura.dodaj_potezo(poteza)
            return False
                                              
        def kmet_poteze():
            # prvi premik kmeta je lahko za 2
            if figura.premaknjena: korak = 1
            else: korak = 2

            # korak navzgor
            zac1 = vrstica + figura.smer
            kon1 = vrstica + (figura.smer * (1 + korak))
            for mozen_premik_vrstica in range(zac1, kon1, figura.smer):
                if Polje.na_sahovnici(mozen_premik_vrstica):
                    if self.kvadratki[mozen_premik_vrstica][stolpec].je_prazno():
                        # polja mozne poteze
                        zac = Polje(vrstica,stolpec)
                        kon = Polje(mozen_premik_vrstica,stolpec)
                        # nova mozna poteza
                        poteza = Poteza(zac, kon)

                        # če še nismo, preverimo šah
                        if bool:
                            if not self.v_sahu(figura,poteza):
                                if iscemo_mat and bool: return True
                                # dodamo mozno potezo če ni šaha
                                figura.dodaj_potezo(poteza)
                        else:
                            # drugace samo dodamo potezo
                            figura.dodaj_potezo(poteza)
                        
                        

                    # ne moremo naprej, ker je pred nami figura
                    else: break
                # ne moremo naprej, ker je konec sahovnice
                else: break

            # diagonalno 
            mozen_premik_vrstica = vrstica + figura.smer
            mozen_premik_stolpca = [stolpec-1,stolpec+1]
            for mozen_premik_stolpec in mozen_premik_stolpca:
                if Polje.na_sahovnici(mozen_premik_vrstica,mozen_premik_stolpec):
                    if self.kvadratki[mozen_premik_vrstica][mozen_premik_stolpec].ima_naspr_figuro(figura.barva):
                        # polja mozne poteze
                        zac = Polje(vrstica,stolpec)
                        kon_figura = self.kvadratki[mozen_premik_vrstica][mozen_premik_stolpec].figura
                        kon = Polje(mozen_premik_vrstica,mozen_premik_stolpec, kon_figura)
                        # nova poteza
                        poteza = Poteza(zac, kon)
                        # če še nismo, preverimo šah
                        if bool:
                            if not self.v_sahu(figura,poteza):
                                if iscemo_mat and bool: return True
                                # dodamo mozno potezo če ni šaha
                                figura.dodaj_potezo(poteza)
                        else:
                            # drugace samo dodamo potezo
                            figura.dodaj_potezo(poteza)
                        
                        

            
            # en passant 
            if figura.barva == 'beli': 
                vrs = 3
                kon_vrs = 2
            else: 
                vrs = 4
                kon_vrs = 5
            
                # levo
            if Polje.na_sahovnici(stolpec-1) and vrstica == vrs:
                if self.kvadratki[vrstica][stolpec-1].ima_naspr_figuro(figura.barva):
                    fig = self.kvadratki[vrstica][stolpec-1].figura
                    if isinstance(fig, Kmet):
                        if fig.en_passant:
                            # polja mozne poteze
                            zac = Polje(vrstica,stolpec)
                            kon = Polje(kon_vrs,stolpec-1, fig)
                            # nova poteza
                            poteza = Poteza(zac, kon)

                            # če še nismo, preverimo šah
                            if bool:
                                if not self.v_sahu(figura,poteza):
                                    if iscemo_mat and bool: return True
                                    # dodamo mozno potezo če ni šaha
                                    figura.dodaj_potezo(poteza)
                            else:
                                # drugace samo dodamo potezo
                                figura.dodaj_potezo(poteza)    
                            

                # desno
            if Polje.na_sahovnici(stolpec+1) and vrstica == vrs:
                if self.kvadratki[vrstica][stolpec+1].ima_naspr_figuro(figura.barva):
                    fig = self.kvadratki[vrstica][stolpec+1].figura
                    if isinstance(fig, Kmet):
                        if fig.en_passant:
                            # polja mozne poteze
                            zac = Polje(vrstica,stolpec)
                            kon = Polje(kon_vrs,stolpec+1, fig)
                            # nova poteza
                            poteza = Poteza(zac, kon)

                            # če še nismo, preverimo šah
                            if bool:
                                if not self.v_sahu(figura,poteza):
                                    if iscemo_mat and bool: return True
                                    # dodamo mozno potezo če ni šaha
                                    figura.dodaj_potezo(poteza)
                                    
                            else:
                                # drugace samo dodamo potezo
                                figura.dodaj_potezo(poteza)
            return False

        def premica_poteze(smeri): 
            for smer in smeri:
                smer_vrstica, smer_stolpec = smer
                mozen_premik_vrstica = vrstica + smer_vrstica
                mozen_premik_stolpec = stolpec + smer_stolpec

                while True:
                    if Polje.na_sahovnici(mozen_premik_vrstica,mozen_premik_stolpec):
                        # polja mozne poteze
                        zac = Polje(vrstica,stolpec)
                        kon_figura = self.kvadratki[mozen_premik_vrstica][mozen_premik_stolpec].figura
                        kon = Polje(mozen_premik_vrstica,mozen_premik_stolpec,kon_figura)
                        # nova mozna poteza
                        poteza = Poteza(zac, kon)
                        
                        # če je prazno dodajamo nove poteze
                        if self.kvadratki[mozen_premik_vrstica][mozen_premik_stolpec].je_prazno():
                            
                            # če še nismo, preverimo šah
                            if bool:
                                if not self.v_sahu(figura,poteza):
                                    if iscemo_mat and bool: return True
                                    # dodamo mozno potezo če ni šaha
                                    figura.dodaj_potezo(poteza)
                                    
                            else:
                                # drugace samo dodamo potezo
                                figura.dodaj_potezo(poteza)
                            

                        # če je naspr figura dodamo trenutno potezo in se potem ustavimo (break)
                        elif self.kvadratki[mozen_premik_vrstica][mozen_premik_stolpec].ima_naspr_figuro(figura.barva):
                            # če še nismo, preverimo šah
                            if bool:
                                if not self.v_sahu(figura,poteza):
                                    if iscemo_mat and bool: return True
                                    # dodamo mozno potezo če ni šaha
                                    figura.dodaj_potezo(poteza)
                            else:
                                # drugace samo dodamo potezo
                                figura.dodaj_potezo(poteza)
                            

                            break 

                        # če je nasa figura se ustavimo (break)
                        elif self.kvadratki[mozen_premik_vrstica][mozen_premik_stolpec].ima_naso_figuro(figura.barva):
                            break 
                        
                    # konec sahovnice
                    else: break
                    mozen_premik_vrstica = mozen_premik_vrstica + smer_vrstica
                    mozen_premik_stolpec = mozen_premik_stolpec + smer_stolpec

            return False

        def kralj_poteze():
            mozne_poteze = [
                (vrstica-1,stolpec+0),
                (vrstica-1,stolpec+1),
                (vrstica+0,stolpec+1),
                (vrstica+1,stolpec+1),
                (vrstica+1,stolpec+0),
                (vrstica+1,stolpec-1),
                (vrstica+0,stolpec-1),
                (vrstica-1,stolpec-1)
            ]
            
            # normalno
            for mozna_poteza in mozne_poteze:
                mozna_poteza_vrstica,mozna_poteza_stolpec = mozna_poteza
                if Polje.na_sahovnici(mozna_poteza_vrstica,mozna_poteza_stolpec):
                    if self.kvadratki[mozna_poteza_vrstica][mozna_poteza_stolpec].je_prazno_ali_naspr(figura.barva):
                        # polja mozne poteze
                        zac = Polje(vrstica,stolpec)
                        kon = Polje(mozna_poteza_vrstica,mozna_poteza_stolpec) #piece=piece
                        # nova mozna poteza
                        poteza = Poteza(zac, kon)
                        # če še nismo, preverimo šah
                        if bool:
                            if not self.v_sahu(figura,poteza):
                                if iscemo_mat and bool: return True
                                # dodamo mozno potezo če ni šaha
                                figura.dodaj_potezo(poteza)
                                
                        else:
                            # drugace samo dodamo potezo
                            figura.dodaj_potezo(poteza)

                        

            # ali smo v šahu tudi če ne naredimo poteze
            zac = Polje(vrstica,stolpec)
            potezaK = Poteza(zac,zac)
            # rošada
            if bool and not figura.premaknjena and not self.v_sahu(figura,potezaK):
                # damina rošada
                # če je levi top na pravi poziciji in se ni premaknil
                levi_top = self.kvadratki[vrstica][0].figura
                if isinstance(levi_top,Top) and not levi_top.premaknjena:
                    je_prazno = True
                    # če med topom in kraljem ni figur in šaha
                    for stolp in range(1,4):
                        if self.kvadratki[vrstica][stolp].ima_figuro():
                            je_prazno = False
                            break
                    if je_prazno:
                        for stolp in range(2,4):
                            zac = Polje(vrstica,stolpec)
                            kon = Polje(vrstica,stolp)
                            potezaK = Poteza(zac,kon)
                            if self.v_sahu(figura,potezaK):
                                je_prazno = False
                                break
                        
                    if je_prazno:
                        if iscemo_mat and bool: return True
                        # kralju dodamo levi top
                        figura.levi_top = levi_top

                        # poteza topa
                        zac = Polje(vrstica,0)
                        kon = Polje(vrstica,3)
                        potezaT = Poteza(zac,kon)

                        # poteza kralja
                        zac = Polje(vrstica,stolpec)
                        kon = Polje(vrstica,2)
                        potezaK = Poteza(zac,kon)
                                               
                        # samo dodamo potezo (k in t)
                        levi_top.dodaj_potezo(potezaT)
                        figura.dodaj_potezo(potezaK)
                        
                # kraljeva rošada
                # če je desni top na pravi poziciji in se ni premaknil
                desni_top = self.kvadratki[vrstica][7].figura
                if isinstance(desni_top,Top) and not desni_top.premaknjena:
                    je_prazno = True
                    # če med topom in kraljem ni figur in šaha
                    for stolp in range(5,7):
                        zac = Polje(vrstica,stolpec)
                        kon = Polje(vrstica,stolp)
                        potezaK = Poteza(zac,kon)
                        if self.kvadratki[vrstica][stolp].ima_figuro() or self.v_sahu(figura,potezaK):
                            je_prazno = False
                            break                   
                        
                    
                    if je_prazno:
                        if iscemo_mat and bool: return True
                        # kralju dodamo desni top
                        figura.desni_top = desni_top

                        # premik topa
                        zac = Polje(vrstica,7)
                        kon = Polje(vrstica,5)
                        potezaT = Poteza(zac,kon)

                        # premik kralja
                        zac = Polje(vrstica,stolpec)
                        kon = Polje(vrstica,6)
                        potezaK = Poteza(zac,kon)

                        desni_top.dodaj_potezo(potezaT)
                        figura.dodaj_potezo(potezaK)
            return False
                                
        if isinstance(figura,Kmet): 
            if iscemo_mat==True and bool: 
                if kmet_poteze(): return True
            kmet_poteze()
        elif isinstance(figura,Skakac):
            if iscemo_mat==True and bool: 
                if skakac_poteze(): return True 
            skakac_poteze()
        elif isinstance(figura,Lovec):   
            if iscemo_mat==True and bool: 
                if premica_poteze([
                (-1,1), # gor-desno
                (-1,-1),# gor-levo
                (1,1),  # dol-desno
                (1,-1)  # dol-levo
            ]): return True  
            premica_poteze([
                (-1,1), # gor-desno
                (-1,-1),# gor-levo
                (1,1),  # dol-desno
                (1,-1)  # dol-levo

            ])     
        elif isinstance(figura,Top): 
            if iscemo_mat==True and bool: 
                if premica_poteze([
                (-1,0), # gor
                (0,1),  # desno
                (1,0),  # dol
                (0,-1) # levo
            ]): return True
            premica_poteze([
                (-1,0), # gor
                (0,1),  # desno
                (1,0),  # dol
                (0,-1) # levo
            ])        
        elif isinstance(figura,Dama): 
            if iscemo_mat==True and bool: 
                if premica_poteze([
                (-1,0), # gor
                (0,1),  # desno
                (1,0),  # dol
                (0,-1), # levo
                (-1,1), # gor-desno
                (-1,-1),# gor-levo
                (1,1),  # dol-desno
                (1,-1)  # dol-levo
            ]): return True
            premica_poteze([
                (-1,0), # gor
                (0,1),  # desno
                (1,0),  # dol
                (0,-1), # levo
                (-1,1), # gor-desno
                (-1,-1),# gor-levo
                (1,1),  # dol-desno
                (1,-1)  # dol-levo
            ])        
        elif isinstance(figura,Kralj): 
            if iscemo_mat==True and bool: 
                if kralj_poteze(): return True
            kralj_poteze()

        return False
    


    def ustvari_2dArray(self):
        for vrstica in range(VRSTICE):
            for stolpec in range(STOLPCI):
                self.kvadratki[vrstica][stolpec] = Polje(vrstica,stolpec)

    def dodaj_figure(self,barva):
        if barva == 'beli': vrstica_kmetov,vrstica_ostalih = (6,7)
        else: vrstica_kmetov,vrstica_ostalih = (1,0)

        #kmetje
        for stolpec in range(STOLPCI):
            self.kvadratki[vrstica_kmetov][stolpec] = Polje(vrstica_kmetov,stolpec,Kmet(barva))
        #skakača
        self.kvadratki[vrstica_ostalih][1] = Polje(vrstica_ostalih,1,Skakac(barva))
        self.kvadratki[vrstica_ostalih][6] = Polje(vrstica_ostalih,6,Skakac(barva))
        #lovca
        self.kvadratki[vrstica_ostalih][2] = Polje(vrstica_ostalih,2,Lovec(barva))
        self.kvadratki[vrstica_ostalih][5] = Polje(vrstica_ostalih,5,Lovec(barva))

        #topa
        self.kvadratki[vrstica_ostalih][0] = Polje(vrstica_ostalih,0,Top(barva))
        self.kvadratki[vrstica_ostalih][7] = Polje(vrstica_ostalih,7,Top(barva))

        #dama
        self.kvadratki[vrstica_ostalih][3] = Polje(vrstica_ostalih,3,Dama(barva))
        #kralj
        self.kvadratki[vrstica_ostalih][4] = Polje(vrstica_ostalih,4,Kralj(barva))
