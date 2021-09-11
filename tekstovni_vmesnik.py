from model import *
from datetime import date, timedelta
import json
##################################################################################################################################
def krepko(niz):
    return f'\033[1m{niz}\033[0m'

DATOTEKA_S_STANJEM = "stanje.json"
try:
    gibanja = Uporabnik.preberi_iz_datoteke(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    gibanja = Uporabnik([])

DODAJ_GIBANJE = 1
IZBRIS_ZADNJEGA_GIBANJA = 2
IZPIS = 3
VSOTA = 4
POVPRECJE = 5
MAX_ZA_VSAK_MESEC = 6
VSOTA_PO_LETIH = 7
POVPRECJE_PO_LETIH = 8
MAX_PO_LETIH = 9
IZHOD = 10

def preberi_stevilo(stevilo):
    while True:
        vnos = input('> ')
        try:
            vnos = input(stevilo)
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")

def izberi(moznosti):
    """Uporabniku našteje možnosti ter vrne izbrano."""
    for indeks, (_moznost, opis) in enumerate(moznosti, 1):
        print(f"{indeks}) {opis}")
    while True:
        izbira = preberi_stevilo("> ")
        if 1 <= izbira <= len(moznosti):
            moznost, _opis = moznosti[izbira - 1]
            return moznost
        else:
            print(f"Izberi število med 1 in {len(moznosti)}")

######################## TEKSTOVNI VMESNIK #######################
def tekstovni_vmesnik():
    prikazi_pozdravno_sporocilo()
    while True:
        print(80 * "-")
        print(krepko('Kaj bi radi naredil?'))
        ukaz = izberi(
            [
                (DODAJ_GIBANJE, 'dodal novo gibanje'),
                (IZBRIS_ZADNJEGA_GIBANJA, 'izbrisal zadnje dodano gibanje'),
                (IZPIS, 'vrni slovar vseh gibanj'),
                (VSOTA, 'vrni slovar vsot vseh gibanj po mesecih'),
                (POVPRECJE, 'vrni slovar povprečij vseh gibanj po mesecih'),
                (MAX_ZA_VSAK_MESEC, 'vrni slovar maksimalnih vsot gibanj po mesecih'),
                (VSOTA_PO_LETIH, 'vrni slovar vsot gibanj po letih'),
                (POVPRECJE_PO_LETIH, 'vrni slovar povprečij gibanj po letih'),
                (MAX_PO_LETIH, 'vrni leto in maksimalno gibanje v danem letu'),
                (IZHOD, 'zapri program')
            ]
        )
        if ukaz == DODAJ_GIBANJE:
            dodaj()
        elif ukaz == IZBRIS_ZADNJEGA_GIBANJA:
            izbris_zadnjega_dodanega_elementa()
        elif ukaz == IZPIS:
            izpis_gibanja()
        elif ukaz == VSOTA:
            vsota_gibanja()
        elif ukaz == POVPRECJE:
            povprečje_gibanja()
        elif ukaz == MAX_ZA_VSAK_MESEC:
            max_gibanja_za_vsak_mesec()
        elif ukaz == VSOTA_PO_LETIH:
            vsota_gibanja_po_letih()
        elif ukaz == POVPRECJE_PO_LETIH:
            povprečje_gibanja_po_letih()
        elif ukaz == MAX_PO_LETIH:
            max_gibanja_po_letih()
        elif ukaz == IZHOD:
            gibanja.shrani_v_datoteko(DATOTEKA_S_STANJEM)
            print("Nasvidenje!")
            print(80 * "-")
            break
            
def prikazi_pozdravno_sporocilo():
    print(krepko("Dobrodošli!"))
    print("Za izhod pritisnite Ctrl-C.")

# TODO: Dodaj funkcijo, ki ti vrne kalorije in kisik, zrihtaj da bo, ko vpises stevilko funkcijo delovala,
# dodaj se funkcije, ki ti vrnejo povprečje, maksimum (funkcije definirane v model) in kje bi se sklical nanje
def dodaj():
    print('Vnesite podatke novega gibanja')
    dolzina = input('Koliko ste pretekli (v kilometrih)?> ')
    cas = input('Koliko časa ste tekli (v urah)?> ')
    nacin = input('Kako ste se gibali (za hojo napišite: False, za tek pa: True)?> ')
    strmina = input('Kakšen je bil klanec (napišite za ustrezno strmino (v odstotkih); zelo velik: 20, velik: 15, srednje velik: 10, majhen: 5, brez klanca: 0)?> ')
    teza = input('Kakšna je vaša telesna teža (v kilogramih)?> ')
    datum = date.today()
    novo_gibanje = DnevnikGibanja(dolzina, cas, nacin, strmina, teza, datum)
    gibanja_za_kalorije = MerilnikTeka(dolzina, cas, nacin, strmina, teza)
    gibanja.dodaj(novo_gibanje)
    gibanja_za_kalorije.poraba_kalorij()
    gibanja_za_kalorije.poraba_kisika_s_tezo()

def izbris_zadnjega_dodanega_elementa():
    if gibanja.seznam_gibanj == []:
        return print('Niste dodali še nobenega gibanja')
    else:
        gibanje = gibanja.seznam_gibanj.pop()
        gibanje

def izpis_gibanja():
    gibanja.izpis_gibanja()

def vsota_gibanja():
    gibanja.vsota_gibanja()

def povprečje_gibanja():
    gibanja.povprečje_gibanja()

def max_gibanja_za_vsak_mesec():
    gibanja.max_gibanja_za_vsak_mesec()

def povprečje_gibanja_po_letih():
    gibanja.povprečje_gibanja_po_letih()

def max_gibanja_po_letih():
    gibanja.max_gibanja_po_letih()

def vsota_gibanja_po_letih():
    gibanja.vsota_gibanja_po_letih()

def prikazi_dosedanja_gibanja():
    if gibanja.seznam_gibanj:
        print(f"- {gibanja.izpisi_gibanja_teka(), gibanja.izpisi_gibanja_hoje()}")
    else:
        print("Niste vpisali še nobenega gibanja")
        dodaj()

tekstovni_vmesnik()



