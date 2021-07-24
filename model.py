from datetime import date, datetime, timedelta


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
        return int(danasnji_datum.strftime("%m"))

    @staticmethod
    def vrni_leto():
        danasnji_datum = datetime.now()
        return int(danasnji_datum.strftime("%Y"))

    def naredi_slovar_aktualnih_let(self):
        slovar_let = {}
        for leto in range(2021, Uporabnik.vrni_leto() + 6):
            slovar_let[leto] = []
        return slovar_let

    def razdeli_po_letih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        for gibanje in self.seznam_gibanj:
            datum = gibanje.datum
            leto_gibanja = int(datum.strftime("%Y"))
            for leto in slovar_let.keys():
                if leto_gibanja == leto:
                    slovar_let[leto].append(gibanje)
                else:
                    pass
        return slovar_let

    def razdeli_po_mesecih(self):
        slovar_po_letih = self.razdeli_po_letih()
        for leto in slovar_po_letih.keys():
            vrednosti = slovar_po_letih[leto]
            seznam_za_mesece = [[] for i in range(1, 13)]
            for vnos in vrednosti:
                if int(vnos.datum.strftime("%Y")) == leto:
                    seznam_za_mesece[int(vnos.datum.strftime("%m")) - 1].append(vnos)  # .datum, da preverjas
                    # seznam_za_mesece.sort()
                slovar_po_letih[leto] = seznam_za_mesece
        return slovar_po_letih

    # TODO: Ugotovi, kako znotraj meseca razvrstiti po dnevih.
    """
    Doda katerokoli gibanje.
    """

    def izpisi_gibanja_teka(self):
        slovar_po_letih = self.razdeli_po_letih()
        for leto in slovar_po_letih.keys():
            vrednosti = slovar_po_letih[leto]
            seznam_za_mesece = [[] for i in range(1, 13)]
            for vnos in vrednosti:
                if int(vnos.datum.strftime("%Y")) == leto:
                    seznam_za_mesece[int(vnos.datum.strftime("%m")) - 1].append(vnos.dolzina)
                slovar_po_letih[leto] = seznam_za_mesece
        return slovar_po_letih

    # Spet potrebno urediti podatke po datumih
    def vsota_gibanja_teka_po_mesecih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        seznam_izpisov = self.izpisi_gibanja_teka()
        for leto in seznam_izpisov.keys():
            stevilo = 0
            seznam_vsot_gibanj = [[] for i in range(1, 13)]
            vrednosti = seznam_izpisov[leto]
            for mesec in vrednosti:
                for posamezen_tek in mesec:
                    stevilo += round(float(posamezen_tek), 2)
                for i in range(1, 13):
                    if i == vrednosti.index(mesec):
                        seznam_vsot_gibanj[i].append(round(stevilo, 2))
            slovar_let[leto] = seznam_vsot_gibanj
        return slovar_let

    ######################################################
    """
    Naslednje tri funkcije, vrnejo analizo podatkov za leta.
    """

    def povprečje_teka_po_letih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        slovar_frekvenc_po_letih = self.naredi_slovar_aktualnih_let()
        seznam_izpisov = self.izpisi_gibanja_teka()
        slovar_povprecij = self.naredi_slovar_aktualnih_let()
        for leto in seznam_izpisov.keys():
            stevilo = 0
            seznam_vsot_gibanj = [[] for i in range(1, 13)]
            vrednosti = seznam_izpisov[leto]
            for mesec in vrednosti:
                for posamezen_tek in mesec:
                    stevilo += round(float(posamezen_tek), 2)
                for i in range(1, 13):
                    if i == vrednosti.index(mesec):
                        seznam_vsot_gibanj[i].append(round(stevilo, 2))
            slovar_let[leto] = seznam_vsot_gibanj
        for leto in seznam_izpisov.keys():
            frekvenca = 0
            seznam_frekvenc_gibanj = [[] for i in range(1, 13)]
            vrednosti = seznam_izpisov[leto]
            for mesec in vrednosti:
                for posamezen_tek in mesec:
                    frekvenca += mesec.count(posamezen_tek)
                for i in range(1, 13):
                    if i == vrednosti.index(mesec):
                        seznam_frekvenc_gibanj[i].append(round(frekvenca, 2))
            slovar_frekvenc_po_letih[leto] = seznam_frekvenc_gibanj
        for leto in slovar_let.keys():
            vrednosti = slovar_let[leto]
            frekvenca = slovar_frekvenc_po_letih[leto]
            stevilo = 0
            if vrednosti == []:
                slovar_povprecij[leto] = []
            else:
                seznam_mesecov = [[] for i in range(1, 13)]
                for i in range(len(vrednosti)):
                    if vrednosti[i] == []:
                        seznam_mesecov.append([])
                    else:
                        stevilo = round(vrednosti[i].pop() / frekvenca[i].pop(), 2)
                        seznam_mesecov.append(stevilo)
                slovar_povprecij[leto] = stevilo
        return slovar_povprecij

    def vsote_teka_po_letih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        seznam_izpisov = self.izpisi_gibanja_teka()
        slovar_vsote = self.naredi_slovar_aktualnih_let()
        for leto in seznam_izpisov.keys():
            stevilo = 0
            seznam_vsot_gibanj = [[] for i in range(1, 13)]
            vrednosti = seznam_izpisov[leto]
            for mesec in vrednosti:
                for posamezen_tek in mesec:
                    stevilo += round(float(posamezen_tek), 2)
                for i in range(1, 13):
                    if i == vrednosti.index(mesec):
                        seznam_vsot_gibanj[i].append(round(stevilo, 2))
            slovar_let[leto] = seznam_vsot_gibanj
        for leto in slovar_vsote.keys():
            vrednosti = slovar_let[leto]
            vsota = 0
            for mesec in vrednosti:
                if mesec == []:
                    continue
                else:
                    vsota += float(mesec[0])
            slovar_vsote[leto] = vsota
        return slovar_vsote

    def max_teka_po_letih(self):
        slovar_povprečij = self.vsote_teka_po_letih()
        maks = 0
        prazen_seznam = []
        for leto, vrednost in slovar_povprečij.items():
            maks = max(maks, vrednost)
            if slovar_povprečij[leto] == maks:
                prazen_seznam.append((leto, maks))
        return prazen_seznam

    # TODO: Popravit povprečje tako, da res vzame samo tiste vrednosti, ki predstavljajo to leto, ne pa vseh,
    # pomagaj si z povprečjem za leta, potrebna le rahla sprememba
    def povprečje_teka_po_mesecih(self):
        slovar_frekvenc_po_letih = self.naredi_slovar_aktualnih_let()
        slovar_povprečij_po_letih = self.naredi_slovar_aktualnih_let()
        seznam_vsot = self.vsota_gibanja_teka()
        slovar_izpisov = self.izpisi_gibanja_teka()
        seznam_frekvenc_gibanj = [[] for i in range(1, 13)]
        seznam_frekvenc_gibanj_nov = []
        slovar_povprečji_gibanj = self.naredi_slovar_aktualnih_let()
        for leto in slovar_izpisov.keys():
            vrednosti = slovar_izpisov[leto]
            if vrednosti == []:
                slovar_frekvenc_po_letih[leto] = []
            else:
                for mesec in vrednosti:
                    indeks = vrednosti.index(mesec)
                    for gibanje in mesec:
                        frekvenca = mesec.count(gibanje)
                        seznam_frekvenc_gibanj[indeks].append(frekvenca)
                        slovar_frekvenc_po_letih[leto] = seznam_frekvenc_gibanj
            # for mesec in seznam_frekvenc_gibanj:
            #   stevilo = 0
            #  if mesec == []:
            #     seznam_frekvenc_gibanj_nov.append([])
            # else:
            #   for element in mesec:
            #      stevilo = mesec.count(element)
            # seznam_frekvenc_gibanj_nov.append([stevilo])
            # slovar_frekvenc_po_letih[leto] = seznam_frekvenc_gibanj_nov
        # for leto in seznam_vsot.keys():
        #   vrednosti_vsot = seznam_vsot[leto]
        #  vrednosti_frekvenc = slovar_frekvenc_po_letih[leto]
        # seznam_povprečji_gibanj = slovar_povprečji_gibanj[leto]
        # for i in range(len(vrednosti_frekvenc) - 1):
        #   if vrednosti_frekvenc[i] == []:
        #      seznam_povprečji_gibanj.append([])
        # else:
        #    seznam_povprečji_gibanj.append([round(vrednosti_vsot[i].pop() / vrednosti_frekvenc[i].pop(), 2)])
        # slovar_povprečij_po_letih[leto] = seznam_povprečji_gibanj
        return slovar_frekvenc_po_letih

    def maksimum_teka_za_vsak_mesec(self):
        slovar_izpisov = self.izpisi_gibanja_teka()
        slovar_maksimov = self.naredi_slovar_aktualnih_let()
        stevilo = 0
        for leto in slovar_izpisov.keys():
            vrednosti = slovar_izpisov[leto]
            for mesec in vrednosti:
                if mesec == []:
                    slovar_maksimov[leto].append([])
                else:
                    stevilo = max(mesec)
                    slovar_maksimov[leto].append([stevilo])
        return slovar_maksimov

    """
    Vse to funkcije, delujejo samo, kadar je oseba tekla, torej da je gibanje.nacin == True.
    """

    def izpisi_gibanja_hoje(self):
        seznam_izpisov_gibanj = [[] for i in range(1, 13)]
        for gibanje in self.seznam_gibanj:
            for i in range(1, 13):
                if not gibanje.nacin:
                    d = gibanje.datum
                    if int(d.strftime("%m")) == i:
                        seznam_izpisov_gibanj[i - 1].append(gibanje.dolzina)
        return seznam_izpisov_gibanj

    def vsota_gibanja_hoje(self):
        seznam_vsot_gibanj = [[] for i in range(1, 13)]
        stevilo = 0
        seznam_izpisov = self.izpisi_gibanja_hoje()
        for mesec in seznam_izpisov:
            for posamezen_tek in mesec:
                stevilo += round(float(posamezen_tek), 2)
            for i in range(1, 13):
                if i == seznam_izpisov.index(mesec):
                    seznam_vsot_gibanj[i].append(round(stevilo, 2))
        return seznam_vsot_gibanj

    def povprečje_mesecov_hoje(self):
        seznam_vsot = self.vsota_gibanja_hoje()
        seznam_izpisov = self.izpisi_gibanja_hoje()
        seznam_frekvenc_gibanj = [[] for i in range(1, 13)]
        seznam_frekvenc_gibanj_nov = []
        seznam_povprečji_gibanj = []
        for mesec in seznam_izpisov:
            indeks = seznam_izpisov.index(mesec)
            frekvenca = 0
            for gibanje in mesec:
                frekvenca = mesec.count(gibanje)
                seznam_frekvenc_gibanj[indeks].append(frekvenca)
        for mesec in seznam_frekvenc_gibanj:
            stevilo = 0
            if mesec == []:
                seznam_frekvenc_gibanj_nov.append([])
            else:
                for element in mesec:
                    stevilo = mesec.count(element)
                seznam_frekvenc_gibanj_nov.append([stevilo])
        for i in range(len(seznam_vsot) - 1):
            if seznam_frekvenc_gibanj_nov[i] == []:
                seznam_povprečji_gibanj.append([])
            else:
                seznam_povprečji_gibanj.append([round(seznam_vsot[i].pop() / seznam_frekvenc_gibanj_nov[i].pop(), 2)])
        return seznam_povprečji_gibanj

    def maksimum_vsakega_meseca_za_hojo(self):
        seznam_izpisov = self.izpisi_gibanja_hoje()
        seznam_maksimov = []
        stevilo = 0
        for mesec in seznam_izpisov:
            if mesec == []:
                seznam_maksimov.append([])
            else:
                stevilo = max(mesec)
                seznam_maksimov.append([stevilo])
        return seznam_maksimov

    """
    Te funkcije vrnejo vrednosti v primeru, ko oseba hodi.
    """

    # treba še popravit
    def nov_vnos(self):
        self.seznam_gibanj.append(self.DnevnikGibanja)
        return self.seznam_gibanj

        """
        Ta funkcija dodaja nova gibanja v naš seznam gibanj
        """

    def izbris(self):
        danasnji_datum = datetime.now()
        for i in range(1, 13):
            if int(danasnji_datum.strftime("%m")) == i:
                self.slovar_gibanj['i'].pop()
            else:
                continue
        return self.slovar_gibanj

    @staticmethod
    def iz_slovar(slovar):
        return DnevnikGibanja(
            dolzina=int(slovar["dolzina"]),
            cas=int(slovar["cas"]),
            nacin=bool(slovar["nacin"]),
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
    marec = (gibanje for gibanje in self.seznam_gibanj if gibanje.dobi_mesec() == 3) 
    """


class DnevnikGibanja:
    def __init__(self, dolzina, cas, nacin, strmina, teza, datum):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        self.strmina = strmina
        self.teza = teza
        # TODO: ključe slovarja sem spremenil v seznam. Popravi, kjer je to potrebno.
        # to ibriši
        self.slovar_gibanj = {key: set() for key in range(1, 13)}
        self.datum = datum

    @staticmethod
    def vrni_dan(datum):
        return datum.strftime("%d")

    @staticmethod
    def vrni_mesec(datum):
        return datum.strftime("%m")

    @staticmethod
    def vrni_leto(datum):
        return datum.strftime("%Y")

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
            datum=slovar["datum"]
        )

    def v_slovar(self):
        return {
            "dolzina": self.dolzina,
            "cas": self.cas,
            "nacin": self.nacin,
            "strmina": self.strmina,
            "teza": self.teza,
            "datum": self.datum
        }


"""
    def razdelitev(self):
        """
# {1: []}

# strftime
# d = datetime.datetime.now()
# m = d.strftime('%m')

# funkcija, ki iz slovarja gibanj, dobi seznam vseh gibanj, nardis unijo vseh values iz kljucov

slovar1 = {"dolzina": 42, "cas": 10, "nacin": True, "strmina": 10, "teza": 70, "datum": datetime.now()}
danasnji_datum = date.today()
danes1 = MerilnikTeka(4, 5, True, 5, 5)
danasnji_datum = date.today()
danes_poskus1 = DnevnikGibanja(4.5, 5, True, 5, 5, date.today())
danes_poskus2 = DnevnikGibanja(5.2, 6, True, 3, 4, date.today())
danes_poskus3 = DnevnikGibanja(6.4, 2, True, 2, 4, date.today())
danes_poskus4 = DnevnikGibanja(8.2, 2, False, 2, 4, date.today())
danes_poskus5 = DnevnikGibanja(1, 2, True, 2, 4, date.today())
danes_poskus6 = DnevnikGibanja(9, 2, True, 2, 4, date.today())
danes_poskus7 = DnevnikGibanja(10, 2, False, 2, 4, date.today())
prejsnji_mesec = DnevnikGibanja(12, 3, True, 4, 5, date.today() - timedelta(days=30))
vcerajsnji_datum = date.today() - timedelta(days=1)
vcerajsnji_dan = DnevnikGibanja(12, 4, True, 43, 5, vcerajsnji_datum)
prejsnji_mesec_datum = date.today() - timedelta(days=30)
tri_leta_naprej = date.today() + timedelta(days=3 * 330)
tri_leta_naprej_poskus = DnevnikGibanja(23, 4, True, 5, 66, tri_leta_naprej)

u = Uporabnik([danes_poskus1, danes_poskus2, danes_poskus3, danes_poskus4, danes_poskus5, danes_poskus6, danes_poskus7,
               prejsnji_mesec, tri_leta_naprej_poskus, vcerajsnji_dan])

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
