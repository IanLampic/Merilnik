from datetime import datetime


class MerilnikTeka:

    def __init__(self, dolzina, cas, nacin, strmina, teza):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        """ Pri načinu tek predstavlja resnico, hoja pa laž """
        self.strmina = strmina
        self.teza = teza

    osnovna_poraba_kisika = 3.5
    """za strmino nastavijo pri tekstovnemu vmesniku:"""
    """-brez = 0 %"""
    """-majhen klanec = 5 %"""
    """-srednje velik klanec = 10 %"""
    """-velik klanec = 15 %"""
    """-zelo velik klanec = 20 %"""

    def hitrost(self):
        return self.dolzina / self.cas

    def poraba_kisika_horizontalno(self):
        """
        nacin predstavlja obliko gibanja (tek ali hoja)
        """
        if self.nacin:
            return 0.1
        else:
            return 0.2
        """ 
        enota za porabo kisika ml / kg min 
        """

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


"""

gibanje1 = DnevnikGibanja(...)
gibanje2 = DnevnikGibanja(...)

u = Uporabnik( (gibanje1, gibanje2) )

"""


class Uporabnik:

    def __init__(self, seznam_gibanj):
        # seznam gibanj kot elemente vsebuje posamezna gibanja
        # 1 uporabnik ima več gibanj.
        self.seznam_gibanj = seznam_gibanj

    @staticmethod
    def vrni_dan():
        danasnji_datum = datetime.now()
        return danasnji_datum.strftime("%d")

    @staticmethod
    def vrni_mesec():
        danasnji_datum = datetime.now()
        return danasnji_datum.strftime("%m")

    @staticmethod
    def vrni_leto():
        danasnji_datum = datetime.now()
        return danasnji_datum.strftime("%Y")

    def dodaj_v_mesec(self):
        danasnji_datum = datetime.now()
        n = int(danasnji_datum.strftime("%m"))
        seznam_mesecov = []
        for i in range(1, 13):
            seznam_mesecov.append([])
        for gibanje in self.seznam_gibanj:
            seznam_mesecov[n - 1].append(gibanje)
        return seznam_mesecov

    def nov_vnos(self):
        danasnji_datum = datetime.now()
        for i in range(1, 13):
            if int(danasnji_datum.strftime("%m")) == i:
                self.seznam_gibanj[i].add(danasnji_datum)
            else:
                continue
        return self.seznam_gibanj

    def izbris(self):
        danasnji_datum = datetime.now()
        for i in range(1, 13):
            if int(danasnji_datum.strftime("%m")) == i:
                self.slovar_gibanj['i'].pop()
            else:
                continue
        return self.slovar_gibanj

    """ 
    marec = (gibanje for gibanje in self.seznam_gibanj if gibanje.dobi_mesec() == 3) 
    """


class DnevnikGibanja:
    def __init__(self, dolzina, cas, nacin, strmina, teza):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        self.strmina = strmina
        self.teza = teza
        # TODO: ključe slovarja sem spremenil v seznam. Popravi, kjer je to potrebno.
        # to ibriši
        self.slovar_gibanj = {key: set() for key in range(1, 13)}

    @staticmethod
    def vrni_dan():
        danasnji_datum = datetime.now()
        return danasnji_datum.strftime("%d")

    @staticmethod
    def vrni_mesec():
        danasnji_datum = datetime.now()
        return danasnji_datum.strftime("%m")

    @staticmethod
    def vrni_leto():
        danasnji_datum = datetime.now()
        return danasnji_datum.strftime("%Y")

    # TODO: Prestavi

    # TODO: To je test.
    # TODO: Prestavi

    """
    def v_datoteko(): ...
    iz_slovarja je statična
    def iz_slovarja(slovar): ...
    """

    # def __init__(self, dolzina, cas, nacin, strmina, teza):
    # TODO: implementiraj še pri ostalih razredih.
    @staticmethod
    def iz_slovar(slovar):
        return DnevnikGibanja(
            dolzina=int(slovar["dolzina"]),
            cas=int(slovar["cas"]),
            nacin=int(slovar["nacin"]),
            strmina=slovar["strmina"],
            teza=int(slovar["teza"]),
        )

    def v_slovar(self):
        return {
            "dolzina": self.dolzina,
            "cas": self.cas,
            "nacin": self.nacin,
            "strmina": self.strmina,
            "teza": self.teza
        }


"""
    def razdelitev(self):
        """
# {1: []}

# strftime
# d = datetime.datetime.now()
# m = d.strftime('%m')

# funkcija, ki iz slovarja gibanj, dobi seznam vseh gibanj, nardis unijo vseh values iz kljucov


danes1 = MerilnikTeka(4, 5, True, 5, 5)
danasnji_datum = datetime.now()
danes_poskus1 = DnevnikGibanja(4, 5, True, 5, 5)
danes_poskus2 = DnevnikGibanja(5, 6, False, 3, 4)
u = Uporabnik([danes_poskus1, danes_poskus2])

# kako iz stringa dobis datum
# from datetime import datetime
#
# timestamp = 1528797322
# date_time = datetime.fromtimestamp(timestamp)
#
# print("Date time object:", date_time)
#
# d = date_time.strftime("%m/%d/%Y, %H:%M:%S")
# print("Output 2:", d)
#
# d = date_time.strftime("%d %b, %Y")
# print("Output 3:", d)
#
# d = date_time.strftime("%d %B, %Y")
# print("Output 4:", d)
#
# d = date_time.strftime("%I%p")
# print("Output 5:", d)
