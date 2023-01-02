class Polje: 

    LEGENDA = {0: 'a',1: 'b',2: 'c',3: 'd',4: 'e',5: 'f',6: 'g',7: 'h',}

    def __init__(self,vrstica,stolpec,figura=None):
        self.vrstica = vrstica
        self.stolpec = stolpec
        self.figura = figura
        self.crka = self.LEGENDA[stolpec]

    # ročno zapisan kriterij za primerjanje polj med sabo
    def __eq__(self, drug):
        return self.vrstica == drug.vrstica and self.stolpec == drug.stolpec

    def ima_figuro(self):
        return self.figura != None
    
    def je_prazno(self):
        return not self.ima_figuro()

    def ima_naso_figuro(self,barva):
        return self.ima_figuro() and self.figura.barva == barva 

    def ima_naspr_figuro(self,barva):
        return self.ima_figuro() and self.figura.barva != barva

    def je_prazno_ali_naspr(self,barva):
        return self.je_prazno() or self.ima_naspr_figuro(barva)

    @staticmethod #funkcijo lahko poklicemo brez instanca class-a
    #ali so x in y veljavne koordinate
    def na_sahovnici(*args): 
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    def get_crka(stolpec):
        LEGENDA = {0: 'a',1: 'b',2: 'c',3: 'd',4: 'e',5: 'f',6: 'g',7: 'h',}
        return LEGENDA[stolpec]
    
