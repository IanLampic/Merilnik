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

    #enota za porabo kisika ml / kg min
    
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
        return '%.2f'%(Merilnik_teka.poraba_kisika(self) * self.teza * self.cas) + ' ml/(kg min)'

    
    def poraba_kalorij(self):
        return '%.2f'%(Merilnik_teka.poraba_kisika_s_tezo(self) * 5) + ' kcal'


class Dnevnik_gibanja:
    def __init__(self, dolzina, cas, nacin, strmina, teza, datum):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        self.strmina = strmina
        self.teza = teza
        self.datum = datum
        self.seznam_gibanj = []

    def nov_vnos(self):
        return self.seznam_gibanj.append((self.dolzina, self.cas, self.nacin, self.strmina, self.teza, self.datum))

    def izbris(self):
        return self.seznam_gibanj.pop()

    def razdelitev_po_mesecih(self):
        januar = []
        februar = []
        marec = []
        april = []
        maj = []
        junij = []
        julij = []
        avgust = []
        september = []
        oktober = []
        november = []
        december = []
        datumi = []
        for podatki in self.seznam_gibanj:
            datumi.append(podatki[-1])
            for element in datumi:
                dan, mesec, leto = element.split('.')
            if int(mesec) == 1:
                januar.append((int(dan), int(mesec), int(leto)))
            elif int(mesec) == 2:
                februar.append((int(dan), int(mesec), int(leto)))
            elif int(mesec) == 3:
                marec.append((int(dan), int(mesec), int(leto)))
            elif int(mesec) == 4:
                april.append((int(dan), int(mesec), int(leto)))
            elif int(mesec) == 5:
                maj.append((int(dan), int(mesec), int(leto)))
            elif int(mesec) == 6:
                junij.append((int(dan), int(mesec), int(leto)))
            elif int(mesec) == 7:
                julij.append((int(dan), int(mesec), int(leto)))
            elif int(mesec) == 8:
                avgust.append((int(dan), int(mesec), int(leto)))
            elif int(mesec) == 9:
                september.append((int(dan), int(mesec), int(leto)))
            elif int(mesec) == 10:
                oktober.append((int(dan), int(mesec), int(leto)))
            elif int(mesec) == 11:
                november.append((int(dan), int(mesec), int(leto)))
            else:
                december.append((int(dan), int(mesec), int(leto)))
        return [januar, februar, marec, april, maj, junij, julij, avgust, september, oktober, november, december]
        




danes1 = Merilnik_teka(4, 5, 'hoja', 5, 5)
danes2 = Dnevnik_gibanja(4, 5, 'hoja', 5, 5, '3. 4. 2021')