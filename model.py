from datetime import *
import json
import datetime


class MerilnikTeka:
    OSNOVNA_PORABA_KISIKA = 3.5

    def __init__(self, dolzina, cas, nacin, strmina, teza):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        """ Pri načinu tek predstavlja resnico, hoja pa laž """
        self.strmina = strmina
        self.teza = teza

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
            return self.hitrost() * self.poraba_kisika_horizontalno() + self.hitrost() * self.odvisnost_vertikalnega_gibanja_od_strmine() + OSNOVNA_PORABA_KISIKA
        else:
            return self.hitrost() * self.poraba_kisika_horizontalno() + self.hitrost() * self.odvisnost_vertikalnega_gibanja_od_strmine() + OSNOVNA_PORABA_KISIKA

    def poraba_kisika_s_tezo(self):
        return str(round(self.poraba_kisika() * self.teza * self.cas, 2)) + ' ml/(kg min)'

    def poraba_kalorij(self):
        return str(round(float(self.poraba_kisika_s_tezo()[:-12]) * 5, 2)) + ' kcal'


class Uporabnik:
    def __init__(self, seznam_gibanj):
        self.seznam_gibanj = sorted(seznam_gibanj, key=lambda x: x.datum)
        """
        Seznam gibanj kot elemente vsebuje posamezna gibanja, 1 uporabnik ima več gibanj.
        """

    @staticmethod
    def vrni_dan():
        danasnji_datum = datetime.date.today()
        return danasnji_datum.strftime("%d")

    @staticmethod
    def vrni_mesec():
        danasnji_datum = datetime.date.today()
        return int(danasnji_datum.strftime("%m"))

    @staticmethod
    def vrni_leto():
        danasnji_datum = datetime.date.today()
        return int(danasnji_datum.strftime("%Y"))

    def naredi_slovar_aktualnih_let(self):
        slovar_let = {}
        for leto in range(2021, Uporabnik.vrni_leto() + 6):
            slovar_let[leto] = {'tek': [[] for i in range(1, 13)], 'hoja': [[] for i in range(1, 13)]}
        return slovar_let

    def razdeli_po_letih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        for gibanje in self.seznam_gibanj:
            leto_gibanja = int(gibanje.datum.strftime("%Y"))
            for leto in slovar_let.keys():
                if leto_gibanja == leto:
                    if gibanje.nacin:
                        slovar_let[leto]['tek'].append(gibanje)
                    else:
                        slovar_let[leto]['hoja'].append(gibanje)
                else:
                    pass
        return slovar_let

    def razdeli_po_mesecih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        for gibanje in self.seznam_gibanj:
            leto_gibanja = int(gibanje.datum.strftime("%Y"))
            for leto in slovar_let.keys():
                if leto_gibanja == leto:
                    if gibanje.nacin:
                        slovar_let[leto]['tek'][int(gibanje.datum.strftime("%m")) - 1].append(gibanje)
                    else:
                        slovar_let[leto]['hoja'][int(gibanje.datum.strftime("%m")) - 1].append(gibanje)
        return slovar_let

    def izpis_gibanja(self):
        slovar = self.razdeli_po_mesecih()
        for leto in slovar.keys():
            posamezno_leto = slovar[leto]
            for nacin in posamezno_leto.keys():
                meseci = posamezno_leto[nacin]
                for i in range(12):
                    gibanja = meseci[i]
                    prazen = []
                    for gibanje in gibanja:
                        prazen.append(gibanje.dolzina)
                        meseci[i] = prazen
                    posamezno_leto[nacin] = meseci
                slovar[leto] = posamezno_leto
        return slovar

    def vsota_gibanja(self):
        slovar_dolzin = self.izpis_gibanja()
        for leto in slovar_dolzin.keys():
            slovar_posameznega = slovar_dolzin[leto]
            for nacin in slovar_posameznega:
                meseci = slovar_posameznega[nacin]
                for i in range(12):
                    gibanja = meseci[i]
                    vsota = 0
                    for gibanje in gibanja:
                        if gibanje == []:
                            continue
                        else:
                            vsota += float(gibanje)
                    meseci[i] = [vsota]
                slovar_posameznega[nacin] = meseci
            slovar_dolzin[leto] = slovar_posameznega
        return slovar_dolzin

    def povprečje_gibanja(self):
        slovar_dolzin = self.izpis_gibanja()
        for leto in slovar_dolzin.keys():
            slovar_posameznega = slovar_dolzin[leto]
            for nacin in slovar_posameznega:
                meseci = slovar_posameznega[nacin]
                for i in range(12):
                    gibanja = meseci[i]
                    vsota = 0
                    frekvenca = 0
                    if gibanja == []:
                        frekvenca = 1
                    else:
                        for gibanje in gibanja:
                            if gibanje == []:
                                continue
                            else:
                                vsota += float(gibanje)
                                frekvenca += 1
                    meseci[i] = [round(vsota / frekvenca, 2)]
                slovar_posameznega[nacin] = meseci
            slovar_dolzin[leto] = slovar_posameznega
        return slovar_dolzin

    def max_gibanja_za_vsak_mesec(self):
        slovar_dolzin = self.vsota_gibanja()
        for leto in slovar_dolzin.keys():
            slovar_posameznega = slovar_dolzin[leto]
            for nacin in slovar_posameznega:
                meseci = slovar_posameznega[nacin]
                for i in range(12):
                    gibanja = meseci[i]
                    maks = 0
                    if gibanja == []:
                        maks = 0
                    else:
                        for gibanje in gibanja:
                            maks = max(maks, gibanje)
                    meseci[i] = [maks]
                slovar_posameznega[nacin] = meseci
            slovar_dolzin[leto] = slovar_posameznega
        return slovar_dolzin

    """
    Naslednje tri funkcije, vrnejo analizo podatkov za leta
    """

    def vsota_gibanja_po_letih(self):
        slovar_dolzin = self.izpis_gibanja()
        for leto in slovar_dolzin.keys():
            slovar_posameznega = slovar_dolzin[leto]
            for nacin in slovar_posameznega:
                meseci = slovar_posameznega[nacin]
                vsota = 0.0
                for gibanja in meseci:
                    if gibanja == []:
                        continue
                    else:
                        for gibanje in gibanja:
                            vsota += float(gibanje)
                slovar_posameznega[nacin] = vsota
            slovar_dolzin[leto] = slovar_posameznega
        return slovar_dolzin

    def povprečje_gibanja_po_letih(self):
        slovar_dolzin = self.izpis_gibanja()
        for leto in slovar_dolzin.keys():
            slovar_posameznega = slovar_dolzin[leto]
            for nacin in slovar_posameznega:
                meseci = slovar_posameznega[nacin]
                vsota = 0.0
                frekvenca = 0
                if meseci == [[] for i in range(12)]:
                    frekvenca = 1
                else:
                    for gibanja in meseci:
                        if gibanja == []:
                            continue
                        else:
                            for gibanje in gibanja:
                                vsota += float(gibanje)
                                frekvenca += 1
                slovar_posameznega[nacin] = round(vsota / frekvenca, 2)
            slovar_dolzin[leto] = slovar_posameznega
        return slovar_dolzin

    def max_gibanja_po_letih(self):
        slovar_vsot = self.vsota_gibanja_po_letih()
        tek = []
        hoja = []
        prazen_seznam = []
        prazen_seznam2 = []
        prazen_seznam3 = []
        for leto, slovar in slovar_vsot.items():
            tek.append(slovar['tek'])
            hoja.append(slovar['hoja'])
            maks_tek = max(tek)
            maks_hoje = max(hoja)
            if slovar_vsot[leto]['tek'] == maks_tek:
                prazen_seznam.append(('tek', leto, maks_tek))
            if slovar_vsot[leto]['hoja'] == maks_hoje:
                prazen_seznam2.append(('hoja', leto, maks_hoje))
        prazen_seznam3.append(prazen_seznam.pop())
        prazen_seznam3.append(prazen_seznam2.pop())
        return prazen_seznam3

    """
    Ta funkcija dodaja nova gibanja v naš seznam gibanj
    """

    def dodaj(self, gibanje):
        self.seznam_gibanj.append(gibanje)

    def izbris_zadnjega_dodanega_elementa(self):
        self.seznam_gibanj.pop()
        return self.seznam_gibanj

    @staticmethod
    def iz_slovarja(slovar):
        return DnevnikGibanja(
            dolzina=int(slovar["dolzina"]),
            cas=int(slovar["cas"]),
            nacin=bool(slovar["nacin"]),
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

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as dat:
            slovar = json.load(dat)
            return Uporabnik.iz_slovarja(slovar)


class DnevnikGibanja:
    def __init__(self, dolzina, cas, nacin, strmina, teza, datum):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        self.strmina = strmina
        self.teza = teza
        self.datum = datum

    @staticmethod
    def iz_slovarja(slovar):
        return DnevnikGibanja(
            dolzina=int(slovar["dolzina"]),
            cas=int(slovar["cas"]),
            nacin=bool(slovar["nacin"]),
            strmina=int(slovar["strmina"]),
            teza=int(slovar["teza"]),
            # datum=slovar["datum"]
            datum=datetime.datetime.strptime(slovar["datum"], "%Y-%m-%d").date()
        )

    def v_slovar(self):
        return {
            "dolzina": self.dolzina,
            "cas": self.cas,
            "nacin": self.nacin,
            "strmina": self.strmina,
            "teza": self.teza,
            "datum": str(self.datum)
        }

    # Naredi za shranjevanje gibanja v eno datoteko.
    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as dat:
            # json.dump({"dolzina": self.dolzina}, dat, ensure_ascii=False, indent=4)
            json.dump(self.v_slovar(), dat, ensure_ascii=False, indent=4)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as dat:
            slovar = json.load(dat)
            return DnevnikGibanja.iz_slovarja(slovar)

    @staticmethod
    def iz_slovarja_v_seznam(slo):
        prazen = []
        for element in slo.values():
            prazen.append(element)
        return prazen

    @staticmethod
    def iz_seznama_v_slovar(sez):
        slo = {}
        slo['dolzina'] = sez[0]
        slo['cas'] = sez[1]
        slo['nacin'] = sez[2]
        slo['strmina'] = sez[3]
        slo['teza'] = sez[4]
        slo['datum'] = sez[5]
        return slo


#    @staticmethod
#   def iz_slovarja(slovar):
#      gibanja = Uporabnik()
#     gibanja.seznam_gibanj = [
#        Spisek.iz_slovarja(sl_spiska) for sl_spiska in slovar["spiski"]
#   ]
#  if slovar["aktualni_spisek"] is not None:
#     stanje.aktualni_spisek = stanje.spiski[slovar["aktualni_spisek"]]
# return stanje


danesss = MerilnikTeka(5.6, 6, True, 5, 60)
danes_poskus1 = DnevnikGibanja(4.5, 5, True, 5, 5, date.today())
danes_poskus2 = DnevnikGibanja(5.2, 6, False, 3, 4, date.today())
danes_poskus3 = DnevnikGibanja(6.4, 2, False, 2, 4, date.today())
danes_poskus4 = DnevnikGibanja(8.2, 2, False, 2, 4, date.today())
danes_poskus5 = DnevnikGibanja(1, 2, True, 2, 4, date.today())
danes_poskus6 = DnevnikGibanja(9, 2, True, 2, 4, date.today())
danes_poskus7 = DnevnikGibanja(10.23, 2, False, 2, 4, date.today())
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
w = Uporabnik([danes_poskus1, vcerajsnji_dan, prejsnji_mesec])