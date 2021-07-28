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


class Uporabnik:

    def __init__(self, seznam_gibanj):
        self.seznam_gibanj = seznam_gibanj
        """
        Seznam gibanj kot elemente vsebuje posamezna gibanja, 1 uporabnik ima več gibanj.
        """

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

    # TODO: Se tukaj uredi po datumih
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

    ############################################################################################################################################################
    # TODO: Ugotovi, kako znotraj meseca razvrstiti po dnevih.

    def izpisi_gibanja_teka(self):
        slovar_po_letih = self.razdeli_po_letih()
        for leto in slovar_po_letih.keys():
            vrednosti = slovar_po_letih[leto]
            seznam_za_mesece = [[] for i in range(1, 13)]
            if vrednosti == []:
                slovar_po_letih[leto] = seznam_za_mesece
            else:
                for vnos in vrednosti:
                    if vnos.nacin:
                        if int(vnos.datum.strftime("%Y")) == leto:
                            seznam_za_mesece[int(vnos.datum.strftime("%m")) - 1].append(vnos.dolzina)
                        slovar_po_letih[leto] = seznam_za_mesece
        return slovar_po_letih

    # TODO: Spet potrebno urediti podatke po datumih
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

    def povprečje_teka_po_mesecih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        slovar_frekvenc_po_letih = self.naredi_slovar_aktualnih_let()
        slovar_povprecij = self.naredi_slovar_aktualnih_let()
        seznam_izpisov = self.izpisi_gibanja_teka()
        for leto in seznam_izpisov.keys():
            stevilo = 0
            seznam_vsot_gibanj = []
            vrednosti = seznam_izpisov[leto]
            for mesec in vrednosti:
                if mesec == []:
                    seznam_vsot_gibanj.append([])
                else:
                    for posamezen_tek in mesec:
                        stevilo += round(float(posamezen_tek), 2)
                    seznam_vsot_gibanj.append([round(stevilo, 2)])
            slovar_let[leto] = seznam_vsot_gibanj
        for leto in seznam_izpisov.keys():
            frekvenca = 0
            seznam_frekvenc_gibanj = []
            vrednosti = seznam_izpisov[leto]
            for mesec in vrednosti:
                if mesec == []:
                    seznam_frekvenc_gibanj.append([])
                else:
                    for posamezen_tek in mesec:
                        frekvenca += mesec.count(posamezen_tek)
                    seznam_frekvenc_gibanj.append([frekvenca])
            slovar_frekvenc_po_letih[leto] = seznam_frekvenc_gibanj
        for leto in slovar_let.keys():
            vrednosti = slovar_let[leto]
            frekvenca = slovar_frekvenc_po_letih[leto]
            stevilo = 0
            if vrednosti == []:
                slovar_povprecij[leto] = []
            else:
                seznam_mesecov = []
                for i in range(len(vrednosti)):
                    if vrednosti[i] == []:
                        seznam_mesecov.append([])
                    else:
                        stevilo = round(vrednosti[i].pop() / frekvenca[i].pop(), 2)
                        seznam_mesecov.append([stevilo])
                slovar_povprecij[leto] = seznam_mesecov
        return slovar_povprecij

    def max_teka_za_vsak_mesec(self):
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
    Naslednje tri funkcije, vrnejo analizo podatkov za leta za tek.
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

    """
    Vse to funkcije, delujejo samo, kadar je oseba tekla, torej da je gibanje.nacin == True.
    """

    ###################################################### ###################################################### ######################################################
    def izpisi_gibanja_hoje(self):
        slovar_po_letih = self.razdeli_po_letih()
        for leto in slovar_po_letih.keys():
            vrednosti = slovar_po_letih[leto]
            seznam_izpisov_gibanj = [[] for i in range(1, 13)]
            if vrednosti == []:
                slovar_po_letih[leto] = seznam_izpisov_gibanj
            else:
                for vnos in vrednosti:
                    if not vnos.nacin:
                        if int(vnos.datum.strftime("%Y")) == leto:
                            seznam_izpisov_gibanj[int(vnos.datum.strftime("%m")) - 1].append(vnos.dolzina)
                    else:
                        pass
                        slovar_po_letih[leto] = seznam_izpisov_gibanj
        return slovar_po_letih

    def vsota_gibanja_hoje_po_mesecih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        seznam_izpisov = self.izpisi_gibanja_hoje()
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

    def povprečje_hoje_po_mesecih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        slovar_frekvenc_po_letih = self.naredi_slovar_aktualnih_let()
        slovar_povprecij = self.naredi_slovar_aktualnih_let()
        seznam_izpisov = self.izpisi_gibanja_hoje()
        for leto in seznam_izpisov.keys():
            stevilo = 0
            seznam_vsot_gibanj = []
            vrednosti = seznam_izpisov[leto]
            for mesec in vrednosti:
                if mesec == []:
                    seznam_vsot_gibanj.append([])
                else:
                    for posamezen_tek in mesec:
                        stevilo += round(float(posamezen_tek), 2)
                    seznam_vsot_gibanj.append([round(stevilo, 2)])
            slovar_let[leto] = seznam_vsot_gibanj
        for leto in seznam_izpisov.keys():
            frekvenca = 0
            seznam_frekvenc_gibanj = []
            vrednosti = seznam_izpisov[leto]
            for mesec in vrednosti:
                if mesec == []:
                    seznam_frekvenc_gibanj.append([])
                else:
                    for posamezen_tek in mesec:
                        frekvenca += mesec.count(posamezen_tek)
                    seznam_frekvenc_gibanj.append([frekvenca])
            slovar_frekvenc_po_letih[leto] = seznam_frekvenc_gibanj
        for leto in slovar_let.keys():
            vrednosti = slovar_let[leto]
            frekvenca = slovar_frekvenc_po_letih[leto]
            stevilo = 0
            if vrednosti == []:
                slovar_povprecij[leto] = []
            else:
                seznam_mesecov = []
                for i in range(len(vrednosti)):
                    if vrednosti[i] == []:
                        seznam_mesecov.append([])
                    else:
                        stevilo = round(vrednosti[i].pop() / frekvenca[i].pop(), 2)
                        seznam_mesecov.append([stevilo])
                slovar_povprecij[leto] = seznam_mesecov
        return slovar_povprecij

    def max_hoje_za_vsak_mesec(self):
        slovar_izpisov = self.izpisi_gibanja_hoje()
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

    def povprečje_hoje_po_letih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        slovar_frekvenc_po_letih = self.naredi_slovar_aktualnih_let()
        seznam_izpisov = self.izpisi_gibanja_hoje()
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

    def vsote_hoje_po_letih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        seznam_izpisov = self.izpisi_gibanja_hoje()
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

    def max_hoje_po_letih(self):
        slovar_povprečij = self.vsote_hoje_po_letih()
        maks = 0
        prazen_seznam = []
        for leto, vrednost in slovar_povprečij.items():
            maks = max(maks, vrednost)
            if slovar_povprečij[leto] == maks:
                prazen_seznam.append((leto, maks))
        return prazen_seznam

    """
    Te funkcije vrnejo vrednosti v primeru, ko oseba hodi.
    """
    ##################################################################################################################################
    """
    Ta funkcija dodaja nova gibanja v naš seznam gibanj
    """

    def dodaj(self):
        self.dolzina = input('Koliko ste pretekli (v kilometrih)? ')
        self.cas = input('Koliko časa ste tekli (v urah)? ')
        self.nacin = input('Kako ste se gibali (za hojo napišite: False, za tek pa: True)? ')
        self.strmina = input(
            'Kakšen je bil klanec (napišite za ustrezno strmino (v odstotkih); zelo velik: 20, velik: 15, srednje velik: 10, majhen: 5, brez klanca: 0)? ')
        self.teza = input('Kakšna je vaša telesna teža (v kilogramih)? ')
        self.datum = date.today()
        self.seznam_gibanj.append(
            DnevnikGibanja(self.dolzina, self.cas, self.nacin, self.strmina, self.teza, self.datum))
        return self.seznam_gibanj

    def izbris_zadnjega_dodanega_elementa(self):
        self.seznam_gibanj.pop()
        return self.seznam_gibanj

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


class DnevnikGibanja:
    def __init__(self, dolzina, cas, nacin, strmina, teza, datum):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        self.strmina = strmina
        self.teza = teza
        self.datum = datum

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


danes_poskus1 = DnevnikGibanja(4.5, 5, False, 5, 5, date.today())
danes_poskus2 = DnevnikGibanja(5.2, 6, False, 3, 4, date.today())
danes_poskus3 = DnevnikGibanja(6.4, 2, False, 2, 4, date.today())
danes_poskus4 = DnevnikGibanja(8.2, 2, False, 2, 4, date.today())
danes_poskus5 = DnevnikGibanja(1, 2, True, 2, 4, date.today())
danes_poskus6 = DnevnikGibanja(9, 2, True, 2, 4, date.today())
danes_poskus7 = DnevnikGibanja(10, 2, False, 2, 4, date.today())
prejsnji_mesec = DnevnikGibanja(12, 3, True, 4, 5, date.today() - timedelta(days=30))
vcerajsnji_datum = date.today() - timedelta(days=1)
vcerajsnji_dan = DnevnikGibanja(12, 4, True, 43, 5, vcerajsnji_datum)
prejsnji_mesec_datum = date.today() - timedelta(days=30)
dve_leti_naprej = date.today() + timedelta(days=2 * 330)
dve_leti_naprej_poskus = DnevnikGibanja(46, 3, True, 4, 70, dve_leti_naprej)
tri_leta_naprej = date.today() + timedelta(days=3 * 330)
tri_leta_naprej_poskus = DnevnikGibanja(23, 4, True, 5, 66, tri_leta_naprej)

u = Uporabnik([danes_poskus1, danes_poskus2, danes_poskus3, danes_poskus4, danes_poskus5, danes_poskus6, danes_poskus7,
               prejsnji_mesec, tri_leta_naprej_poskus, vcerajsnji_dan, dve_leti_naprej_poskus])

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
