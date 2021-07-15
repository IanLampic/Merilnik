osnovna_poraba_kisika = 3.5 

class Merilnik_teka:
   
    def __init__(self, dolzina, cas, nacin, strmina, teza):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        self.strmina = strmina
        self.teza = teza
    
    osnovna_poraba_kisika = 3,5
    #za strmino nastavijo pri tekstovnemu vmesniku:
    #-brez = 0 %
    #-majhen klanec = 5 %
    #-srednje velik klanec = 10 %
    #-velik klanec = 15 %
    #-zelo velik klanec = 20 %

    #enota za porabo kisiko ml / kg min
    
    def hitrost(self):
        return self.dolzina / self.cas

    def poraba_kisika_horizontalno(self):
        #nacin predstavlja obliko gibanja (tek ali hoja)#
        if self.nacin == 'hoja':
            return 0.1
        elif self.nacin == 'tek':
            return 0.2
        else:
            return 0
    
    def poraba_kisika_vertikalno(self):
        return 1.8 
 
    def odvisnost_vertikalnega_gibanja_od_strmine(self):
        return Merilnik_teka.poraba_kisika_vertikalno(self) * (self.strmina * 0.01)

    def poraba_kisika(self):
        if self.nacin == 'hoja':
            return Merilnik_teka.hitrost(self) * Merilnik_teka.poraba_kisika_horizontalno(self) + Merilnik_teka.hitrost(self) * Merilnik_teka.odvisnost_vertikalnega_gibanja_od_strmine(self) + osnovna_poraba_kisika
        elif self.nacin == 'tek':
            return Merilnik_teka.hitrost(self) * Merilnik_teka.poraba_kisika_horizontalno(self) + Merilnik_teka.hitrost(self) * Merilnik_teka.odvisnost_vertikalnega_gibanja_od_strmine(self) + osnovna_poraba_kisika
        else:
            return 0

    def poraba_kisika_s_tezo(self):
        return Merilnik_teka.poraba_kisika(self) * self.teza * self.cas

    
    def poraba_kalorij(self):
        return f'{Merilnik_teka.poraba_kisika_s_tezo(self) * 5} kcal'

danes = Merilnik_teka(4, 5, 'hoja', 5, 5)