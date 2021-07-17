osnovna_poraba_kisika = 3.5 
from datetime import datetime

class MerilnikTeka:
   
    def __init__(self, dolzina, cas, nacin, strmina, teza):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        #Pri načinu tek predstavlja resnico, hoja pa laž
        self.strmina = strmina
        self.teza = teza

    

    osnovna_poraba_kisika = 3,5
    """za strmino nastavijo pri tekstovnemu vmesniku:"""
    """-brez = 0 %"""
    """-majhen klanec = 5 %"""
    """-srednje velik klanec = 10 %"""
    """-velik klanec = 15 %"""
    """-zelo velik klanec = 20 %"""
    
    def hitrost(self):
        return self.dolzina / self.cas

    def poraba_kisika_horizontalno(self):
        """nacin predstavlja obliko gibanja (tek ali hoja)"""
        if self.nacin:
            return 0.1
        else:
            return 0.2
        """enota za porabo kisika ml / kg min"""

    def poraba_kisika_vertikalno(self):
        return 1.8 
 
    def odvisnost_vertikalnega_gibanja_od_strmine(self):
        return self.poraba_kisika_vertikalno() * (self.strmina * 0.01)

    def poraba_kisika(self):
        if self.nacin:
            return self.hitrost() * self.poraba_kisika_horizontalno() + self.hitrost() * self.odvisnost_vertikalnega_gibanja_od_strmine() + osnovna_poraba_kisika
        else:
            return self.hitrost() * self.poraba_kisika_horizontalno() + self.hitrost() * self.odvisnost_vertikalnega_gibanja_od_strmine() + osnovna_poraba_kisika

    def poraba_kisika_s_tezo(self):
        return str(round(self.poraba_kisika() * self.teza * self.cas, 2)) + ' ml/(kg min)'

    def poraba_kalorij(self):
        return str(round(float(self.poraba_kisika_s_tezo()[:-12]) * 5, 2)) + ' kcal'
        

class Dnevnik_gibanja:
    def __init__(self, dolzina, cas, nacin, strmina, teza, datum):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        self.strmina = strmina
        self.teza = teza
        self.datum = datum
        self.slovar_gibanj = {key:set() for key in range(1, 13)}


    @staticmethod 
    def vrni_dan(danasnji_datum):
        danasnji_datum = datetime.now()
        return danasnji_datum.strftime("%d")
    
    @staticmethod 
    def vrni_mesec(danasnji_datum):
        danasnji_datum = datetime.now()
        return danasnji_datum.strftime("%m")
    
    @staticmethod 
    def vrni_leto(danasnji_datum):
        danasnji_datum = datetime.now()
        return danasnji_datum.strftime("%Y")


    def nov_vnos(self):
        danasnji_datum = datetime.now() 
        for i in range(1, 13):
            if danasnji_datum.strftime("%m") == i:
                self.slovar_gibanj['i'].add(danasnji_datum)
            else:
                continue
        return self.slovar_gibanj

        
    #kako delujejo datumi, kako iz dneva, meseca, leta naredis objekt datum, strftime, kako objekta datum dobis mesec,
    def izbris(self):
        danasnji_datum = datetime.now() 
        for i in range(1, 13):
            if danasnji_datum.strftime("%m") == i:
                self.slovar_gibanj['i'].pop()
            else:
                continue
        return self.slovar_gibanj

    def razdelitev(self):
        #strftime
        d = datetime.datetime.now()
        m = d.strftime('%m')
    
    #funkcija, ki iz slovarja gibanj, dobi seznam vseh gibanj, nardis unijo vseh values iz kljucov
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
        




danes1 = MerilnikTeka(4, 5, True, 5, 5)
danasnji_datum = datetime.now()
danes2 = Dnevnik_gibanja(4, 5, True, 5, 5, danasnji_datum)

#kako iz stringa dobis datum
#from datetime import datetime
#
#timestamp = 1528797322
#date_time = datetime.fromtimestamp(timestamp)
#
#print("Date time object:", date_time)
#
#d = date_time.strftime("%m/%d/%Y, %H:%M:%S")
#print("Output 2:", d)	
#
#d = date_time.strftime("%d %b, %Y")
#print("Output 3:", d)
#
#d = date_time.strftime("%d %B, %Y")
#print("Output 4:", d)
#
#d = date_time.strftime("%I%p")
#print("Output 5:", d)
