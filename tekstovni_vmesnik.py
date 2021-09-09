from model import MerilnikTeka, Uporabnik, DnevnikGibanja
from datetime import date, timedelta
import json


# danesss = MerilnikTeka(5.6, 6, True, 5, 60)
# danes_poskus1 = DnevnikGibanja(4.5, 5, True, 5, 5, date.today())
# danes_poskus2 = DnevnikGibanja(5.2, 6, False, 3, 4, date.today())
# danes_poskus3 = DnevnikGibanja(6.4, 2, False, 2, 4, date.today())
# danes_poskus4 = DnevnikGibanja(8.2, 2, False, 2, 4, date.today())
##danes_poskus5 = DnevnikGibanja(1, 2, True, 2, 4, date.today())
# danes_poskus6 = DnevnikGibanja(9, 2, True, 2, 4, date.today())
# danes_poskus7 = DnevnikGibanja(10.23, 2, False, 2, 4, date.today())
# prejsnji_mesec = DnevnikGibanja(12, 3, True, 4, 5, date.today() - timedelta(days=30))
# vcerajsnji_datum = date.today() - timedelta(days=1)
# vcerajsnji_dan = DnevnikGibanja(12, 4, True, 43, 5, vcerajsnji_datum)
# prejsnji_mesec_datum = date.today() - timedelta(days=30)
##dve_leti_naprej = date.today() + timedelta(days=2 * 330)
# dve_leti_naprej_poskus = DnevnikGibanja(46, 3, True, 4, 70, dve_leti_naprej)
# tri_leta_naprej = date.today() + timedelta(days=3 * 330)
# tri_leta_naprej_poskus = DnevnikGibanja(23, 4, True, 5, 66, tri_leta_naprej)

# u = Uporabnik([danes_poskus1, danes_poskus2, danes_poskus3, danes_poskus4, danes_poskus5, danes_poskus6, danes_poskus7,
#              prejsnji_mesec, tri_leta_naprej_poskus, vcerajsnji_dan, dve_leti_naprej_poskus])
# w = Uporabnik([danes_poskus1, vcerajsnji_dan, prejsnji_mesec])
##################################################################################################################################
def krepko(niz):
    return f'\033[1m{niz}\033[0m'


DATOTEKA_S_STANJEM = "stanje.json"
try:
    gibanja = Uporabnik.preberi_iz_datoteke(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    gibanja = Uporabnik([])


def preberi_stevilo(stevilo):
    while True:
        vnos = input('> ')
        try:
            vnos = input(stevilo)
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")


def izberi(seznam):
    """Uporabniku našteje možnosti ter vrne izbrano."""
    if len(seznam) == 1:
        opis, element = seznam[0]
        print(f"Na voljo je samo možnost {opis}, zato sem jo izbral.")
        return element
    for indeks, (oznaka, _) in enumerate(seznam, 1):
        print(f"{indeks}) {oznaka}")
    while True:
        izbira = preberi_stevilo("> ")
        if 1 <= izbira <= len(seznam):
            _, element = seznam[izbira - 1]
            return element
        else:
            print(f"Izberi število med 1 in {len(seznam)}")


######################## TEKSTOVNI VMESNIK #######################
def tekstovni_vmesnik():
    prikazi_pozdravno_sporocilo()
    while True:
        try:
            print(80 * "#")
            print()
            print(krepko('Kaj bi radi naredil?'))
            moznosti = [
                ('vnesel novo gibanje', dodaj),
                ('izbrisal zadnje dodano gibanje', izbris_zadnjega_dodanega_elementa),
                ('zanima me maksimum gibanja po letih', dodaj_to_funkcijo),
                ('zanima me maksimum gibanja po mesecih', dodaj_to_funkcijo),
                ('zanima me povprečje po letih', dodaj_to_funkcijo),
                ('zanima me povprečje po mesecih', dodaj_to_funkcijo)
            ]
            izbira = izberi(moznosti)
            print(80 * "-")
            izbira()
            print()
            input("Pritisnite Enter za shranjevanje in vrnitev v osnovni meni...")
            gibanja.shrani_v_datoteko(DATOTEKA_S_STANJEM)
        except ValueError as e:
            print(e.args[0])
        except KeyboardInterrupt:
            print()
            print("Nasvidenje!")
            return

        # prikazi_dosedanja_gibanja()


def prikazi_pozdravno_sporocilo():
    print(krepko("Dobrodošli!"))
    print("Za izhod pritisnite Ctrl-C.")


def izpis_gibanja(self):
    slovar = self.urejena_funkcija_po_mesecih()
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


# TODO: Dodaj funkcijo, ki ti vrne kalorije in kisik, zrihtaj da bo, ko vpises stevilko funkcijo delovala,
# dodaj se funkcije, ki ti vrnejo povprečje, maksimum (funkcije definirane v model) in kje bi se sklical nanje
def dodaj():
    dolzina = preberi_stevilo('Koliko ste pretekli (v kilometrih)?> ')
    cas = preberi_stevilo('Koliko časa ste tekli (v urah)?> ')
    nacin = preberi_stevilo('Kako ste se gibali (za hojo napišite: False, za tek pa: True)?> ')
    strmina = preberi_stevilo(
        'Kakšen je bil klanec (napišite za ustrezno strmino (v odstotkih); zelo velik: 20, velik: 15, srednje velik: 10, majhen: 5, brez klanca: 0)?> ')
    teza = preberi_stevilo('Kakšna je vaša telesna teža (v kilogramih)?> ')
    datum = date.today()
    novo_gibanje = DnevnikGibanja(dolzina, cas, nacin, strmina, teza, datum)
    gibanja.dodaj(novo_gibanje)


def prikazi_dosedanja_gibanja():
    if gibanja.seznam_gibanj:
        print(f"- {gibanja.izpisi_gibanja_teka(), gibanja.izpisi_gibanja_hoje()}")
    else:
        print("Niste vpisali še nobenega gibanja")
        dodaj()


def izbris_zadnjega_dodanega_elementa():
    if gibanja.seznam_gibanj == []:
        return print('Niste dodali še nobenega gibanja')
    else:
        gibanje = gibanja.seznam_gibanj.pop()
        gibanje


def dodaj_to_funkcijo():
    None


# sez  = [(dodaj()), (izbris_zadnjega_dodanega_elementa())]


tekstovni_vmesnik()

# shranjevanje dodatek(da ne rabiš vsakič vsa gibanja napisat)
# treba uporabit zapis json, za naredit json-
# json.loads(element), prej napises import json, iz jsona pretvor v python
# json.dumps(None)-iz pythona v json


