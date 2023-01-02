from barva import Barva

class Tema:

    def __init__(self,svetlo_oz,temno_oz,svetlo_trace,temno_trace,svetlo_poteze,temno_poteze):
        self.ozadje = Barva(svetlo_oz,temno_oz)
        self.trace = Barva(svetlo_trace,temno_trace)
        self.poteze = Barva(svetlo_poteze,temno_poteze)
