import math
import os

class Figura:

    def  __init__(self,vrsta,barva,vrednost,slika=None, slika_prav=None):
        self.vrsta=vrsta
        self.barva=barva
        self.slika=slika
        self.slika_prav=slika_prav
        self.mozne_poteze=[]
        self.premaknjena=False

        if barva == 'beli': beliCrni = 1            
        else: beliCrni = -1

        self.vrednost = vrednost * beliCrni     #črne figure imajo negativno, bele pa pozitivno vrednost
        self.nastavi_sliko()
    
    def nastavi_sliko(self,velikost='manjsi'):
        self.slika = os.path.join(f'source/images/ChessCom/{velikost}/{self.barva}_{self.vrsta}.png')

    def dodaj_potezo(self,moznaPoteza):
        self.mozne_poteze.append(moznaPoteza)

    def pocisti_poteze(self):
        self.mozne_poteze = []
        
#classi posameznih figur
class Kmet(Figura):
    def __init__(self,barva):
        if barva == 'beli': self.smer = -1
        else: self.smer = 1
        self.en_passant = False
        super().__init__('kmet', barva, 1.0)
        
class Skakac(Figura):
    def __init__(self,barva):
        super().__init__('skakac', barva, 2.99)        	
    
class Lovec(Figura):
    def __init__(self,barva):
        super().__init__('lovec', barva, 3.0)      

class Top(Figura):
    def __init__(self,barva):
        super().__init__('top', barva, 5.0)     

class Dama(Figura):
    def __init__(self,barva):
        super().__init__('dama', barva, 9.0)     

class Kralj(Figura):
    def __init__(self,barva):
        self.levi_top = None
        self.desni_top = None
        super().__init__('kralj', barva, math.inf)     

