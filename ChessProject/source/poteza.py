class Poteza:

    def __init__(self,zac,kon):
        # zacetno in koncno polje poteze
        self.zac = zac
        self.kon = kon

    def __str__(self):
        s = ''
        s += f'({self.zac.stolpec},{self.zac.vrstica})'
        s += f' -> ({self.kon.stolpec},{self.kon.vrstica})'
    
    # ročno zapisan kriterij za primerjanje potez med sabo
    def __eq__(self, drug):
        return self.zac == drug.zac and self.kon == drug.kon
