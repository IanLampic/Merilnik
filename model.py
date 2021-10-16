from datetime import date, datetime, timedelta
import json
import hashlib
import random


class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, gibanja):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.gibanja = gibanja

    def v_slovar_uporabnik(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            'zasifrirano_geslo': self.zasifrirano_geslo,
            "gibanja": self.gibanja.v_slovar_uporabnik_gibanje(),
        }

    def shrani_v_datoteko_uporabnik(self):
        """podatke shrani v datoteko"""
        with open(self.ime_uporabnikove_datoteke(self.uporabnisko_ime), "w") as dat:
            json.dump(self.v_slovar_uporabnik(), dat, ensure_ascii=False, indent=4)

    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
         return f'{uporabnisko_ime}.json'

    @staticmethod
    def iz_slovarja_uporabnik(slovar):
        uporabnisko_ime = slovar['uporabnisko_ime']
        zasifrirano_geslo = slovar['zasifrirano_geslo']
        gibanja = Analiza.iz_slovarja_vsi(slovar)
        return Uporabnik(uporabnisko_ime, zasifrirano_geslo, gibanja)

    @staticmethod
    def uporabnik_preberi_iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime), 'r') as dat:
                slovar = json.load(dat)
                return Uporabnik.iz_slovarja_uporabnik(slovar)
        except FileNotFoundError:
            return None

    def _zasifriraj_geslo(geslo_v_cistopisu, sol=None):
        if sol is None:
            sol = str(random.getrandbits(32))
        posoljeno_geslo = sol + geslo_v_cistopisu
        h = hashlib.blake2b()
        h.update(posoljeno_geslo.encode(encoding="utf-8"))
        return f"{sol}${h.hexdigest()}"

    def preveri_geslo(self, geslo_v_cistopisu):
        sol, _ = self.zasifrirano_geslo.split("$")
        return self.zasifrirano_geslo == Uporabnik._zasifriraj_geslo(geslo_v_cistopisu, sol)


    @staticmethod
    def prijava(uporabnisko_ime, geslo_v_cistopisu):
        uporabnik = Uporabnik.uporabnik_preberi_iz_datoteke(uporabnisko_ime)
        if uporabnik is None:
            raise ValueError("Uporabniško ime ne obstaja")
        elif uporabnik.preveri_geslo(geslo_v_cistopisu):
            return uporabnik
        else:
            raise ValueError("Geslo je napačno")

    @staticmethod
    def registracija(uporabnisko_ime, geslo_v_cistopisu):
        if Uporabnik.uporabnik_preberi_iz_datoteke(uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            zasifrirano_geslo = Uporabnik._zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, Analiza([]))
            uporabnik.shrani_v_datoteko_uporabnik()
            return uporabnik


    def v_slovar_uporabnik_gibanje(self):
        sez = []
        for gibanje in self.gibanja.seznam_gibanj:
            d = gibanje.datum
            if not isinstance(d, str):
                d = d.isoformat()
            else:
                d = gibanje.datum
            json_datum = json.dumps(d)
            gib = {
                "dolzina": gibanje.dolzina,
                "cas": gibanje.cas,
                "nacin": gibanje.nacin,
                "strmina": gibanje.strmina,
                "teza": gibanje.teza,
                "datum": json_datum
            }
            sez.append(gib)
        return sez
    

class MerilnikGibanja:

    def __init__(self, dolzina, cas, nacin, strmina, teza):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        """ Pri načinu tek predstavlja resnico(True), hoja pa laž(False) """
        self.strmina = strmina
        self.teza = teza
        self.OSNOVNA_PORABA_KISIKA = 3.5
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
            return self.hitrost() * self.poraba_kisika_horizontalno() + self.hitrost() * self.odvisnost_vertikalnega_gibanja_od_strmine() + self.OSNOVNA_PORABA_KISIKA
        else:
            return self.hitrost() * self.poraba_kisika_horizontalno() + self.hitrost() * self.odvisnost_vertikalnega_gibanja_od_strmine() + self.OSNOVNA_PORABA_KISIKA

    def poraba_kisika_s_tezo(self):
        return str(round(self.poraba_kisika() * self.teza * self.cas, 2)) + ' ml/(kg min)'

    def poraba_kalorij(self):
        return str(round(float(self.poraba_kisika_s_tezo()[:-12]) * 5, 2)) + ' kcal'

class Analiza:
    def __init__(self, seznam_gibanj):
        self.seznam_gibanj = seznam_gibanj
        """
        Seznam gibanj kot elemente vsebuje posamezna gibanja, 1 uporabnik ima več gibanj.
        """

    @staticmethod
    def vrni_dan():
        danasnji_datum = datetime.today()
        return danasnji_datum.strftime("%d")

    @staticmethod
    def vrni_mesec():
        danasnji_datum = datetime.today()
        return int(danasnji_datum.strftime("%m"))

    @staticmethod
    def vrni_leto():
        danasnji_datum = datetime.today()
        return int(danasnji_datum.strftime("%Y"))

    def naredi_slovar_aktualnih_let(self):
        slovar_let = {}
        for leto in range(2021, Analiza.vrni_leto() + 1):
            slovar_let[leto] = {'tek': [[] for i in range(1, 13)], 'hoja': [[] for i in range(1, 13)]}
        return slovar_let

    def razdeli_po_letih(self):
        slovar_let = self.naredi_slovar_aktualnih_let()
        gibanja = sorted(self.seznam_gibanj, key=lambda x: x.datum)
        for gibanje in gibanja:
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
        gibanja = sorted(self.seznam_gibanj, key=lambda x: x.datum)
        for gibanje in gibanja:
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
                    vsota = 0.0
                    for gibanje in gibanja:
                        if gibanje == []:
                            continue
                        else:
                            vsota += float(gibanje)
                    meseci[i] = [vsota]
                slovar_posameznega[nacin] = meseci
            slovar_dolzin[leto] = slovar_posameznega
        return slovar_dolzin

    def novo_povp_mesec(self):
        slovar = self.vsota_gibanja()
        for leto in slovar.keys():
            slovar_posameznega = slovar[leto]
            for nacin in slovar_posameznega:
                meseci = slovar_posameznega[nacin]
                for i in range(len(meseci)):
                    nov = meseci[i]
                    meseci[i] = [round(nov.pop() / 30, 2)]
        return slovar

    def max_gibanja_za_vsak_mesec(self):
        slovar_dolzin = self.izpis_gibanja()
        for leto in slovar_dolzin.keys():
            slovar_posameznega = slovar_dolzin[leto]
            for nacin in slovar_posameznega:
                meseci = slovar_posameznega[nacin]
                for i in range(12):
                    gibanja = meseci[i]
                    maks = 0.0
                    if gibanja == []:
                        maks = 0.0
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

    def novo_povp(self):
        slovar = self.vsota_gibanja_po_letih()
        for leto in slovar.keys():
            slovar_posameznega = slovar[leto]
            for nacin in slovar_posameznega:
                nov = slovar_posameznega[nacin]
                slovar_posameznega[nacin] = round(nov / 365, 2)
        return slovar

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
    def dodaj(self, novo_gibanje):
        self.seznam_gibanj.append(novo_gibanje)

    def izbris_zadnjega_elementa(self):
        del self.seznam_gibanj[-1]

    @staticmethod
    def iz_slovarja(slovar):
        return DnevnikGibanja(
            dolzina=int(slovar["dolzina"]),
            cas=int(slovar["cas"]),
            nacin=bool(slovar["nacin"]),
            strmina=int(slovar["strmina"]),
            teza=int(slovar["teza"]),
            datum=slovar["datum"]
        )

    def v_slovar(self):
        slo = {'gibanja': []}
        for gibanje in self.seznam_gibanj:
            d = gibanje.datum
            if not isinstance(d, str):
                d = d.isoformat()
            else:
                d = gibanje.datum
            json_datum = json.dumps(d)
            gib = {
                "dolzina": gibanje.dolzina,
                "cas": gibanje.cas,
                "nacin": gibanje.nacin,
                "strmina": gibanje.strmina,
                "teza": gibanje.teza,
                "datum": json_datum
            }
            slo["gibanja"].append(gib)
        return slo

    @staticmethod
    def iz_slovarja_vsi(slovar):
        sez = []
        for gibanje in slovar['gibanja']:
            sez.append(Analiza.iz_slovarja(gibanje))
        for gib in Analiza(sez).seznam_gibanj:
            gib.datum = gib.datum.replace('"', '')
        return Analiza(sez)


    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        sez = []
        with open(ime_datoteke, 'r') as dat:
            seznam = json.load(dat)
            gibanja = seznam['gibanja']
            for gibanje in gibanja:
                sez.append(Analiza.iz_slovarja(gibanje))
        for gib in Analiza(sez).seznam_gibanj:
            gib.datum = gib.datum.replace('"', '')
        return Analiza(sez)
    
    def v_slovar_uporabnik_gibanje(self):
        sez = []
        for gibanje in self.seznam_gibanj:
            d = gibanje.datum
            if not isinstance(d, str):
                d = d.isoformat()
            else:
                d = gibanje.datum
            json_datum = json.dumps(d)
            gib = {
                "dolzina": gibanje.dolzina,
                "cas": gibanje.cas,
                "nacin": gibanje.nacin,
                "strmina": gibanje.strmina,
                "teza": gibanje.teza,
                "datum": json_datum
            }
            sez.append(gib)
        return sez

    @staticmethod
    def pretvori_datum_iz_jsona_v_datetime(gibanje):
        gibanje.datum.replace('\\', '').replace('"', '')
        gibanje.datum = datetime.strptime(gibanje.datum[:10], '%Y-%m-%d')
        return gibanje

    @staticmethod
    def ali_je_v_datetime(seznam):
        for gibanje in seznam.seznam_gibanj:
            if gibanje.datum != datetime.strptime(gibanje.datum, "%Y-%m-%d").strftime('%Y-%m-%d'):
                return False
        return True

    def koncna_za_datume(self):
        prava = self.seznam_gibanj
        sez = Analiza([])
        if prava != []:
            prvi = prava[0]
            zadnji = prava[-1]
            if type(prvi.datum) is str:
                for i in range(len(prava) - 1):
                    sez.seznam_gibanj.append(Analiza.pretvori_datum_iz_jsona_v_datetime(prava[i]))
            else:
                for i in range(len(prava) - 1):
                    sez.seznam_gibanj.append(prava[i])
            if type(zadnji.datum) is str:
                sez.seznam_gibanj.append(Analiza.pretvori_datum_iz_jsona_v_datetime(prava[-1]))
            else:
                sez.seznam_gibanj.append(prava[-1])
        return sez

class DnevnikGibanja:
    def __init__(self, dolzina, cas, nacin, strmina, teza, datum):
        self.dolzina = dolzina
        self.cas = cas
        self.nacin = nacin
        self.strmina = strmina
        self.teza = teza
        self.datum = datum
    
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

danesss = MerilnikGibanja(5.6, 6, True, 5, 60)
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

u = Analiza([danes_poskus1, danes_poskus2, danes_poskus3, danes_poskus4, danes_poskus5, danes_poskus6, danes_poskus7,
               prejsnji_mesec, tri_leta_naprej_poskus, vcerajsnji_dan, dve_leti_naprej_poskus])
w = Analiza([danes_poskus1, vcerajsnji_dan, prejsnji_mesec])
k = Analiza([])
o = None

