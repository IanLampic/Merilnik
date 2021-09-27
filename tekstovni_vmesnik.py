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
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")

def izberi(moznosti):
    """Uporabniku našteje možnosti ter vrne izbrano."""
    for indeks, (moznost, opis) in enumerate(moznosti, 1):
        print(f"{indeks}) {opis}")
    while True:
        izbira = preberi_stevilo("> ")
        if 1 <= izbira <= len(moznosti):
            moznost, opis = moznosti[izbira - 1]
            return moznost
        else:
            print(f"Izberi število med 1 in {len(moznosti)}")

######################## TEKSTOVNI VMESNIK ##########################
"""
Seznam gibanj, ki imajo datum nazaj v formatu datetime in ne v jsonu.
"""

def tekstovni_vmesnik():
    prikazi_pozdravno_sporocilo()
    while True:
        print(80 * "-")
        print(krepko('Kaj bi radi naredil?'))
        ukaz = izberi(
            [
                (DODAJ_GIBANJE, 'vpisal novo gibanje'),
                (IZBRIS_ZADNJEGA_GIBANJA, 'izbrisal zadnje dodano gibanje'),
                (IZPIS, 'vrni slovar vseh gibanj'),
                (VSOTA, 'vrni slovar vsot vseh gibanj po mesecih'),
                (POVPRECJE, 'vrni slovar povprečij vseh gibanj po mesecih'),
                (MAX_ZA_VSAK_MESEC, 'vrni slovar maksimalnih vsot gibanj po mesecih'),
                (VSOTA_PO_LETIH, 'vrni slovar vsot gibanj po letih'),
                (POVPRECJE_PO_LETIH, 'vrni slovar povprečij gibanj po letih'),
                (MAX_PO_LETIH, 'vrni leto, ko si se največ gibal(tek ali hoja) in maksimalno gibanje v danem letu'),
                (IZHOD, 'zapri program')
            ]
        )
        if ukaz == DODAJ_GIBANJE:
            dodaj()
        elif ukaz == IZBRIS_ZADNJEGA_GIBANJA:
            izbris_zadnjega_elementa()
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

def dodaj():
    print('Vnesite podatke novega gibanja (pišite cela števila).')
    dolzina = int(input('Koliko ste pretekli (v kilometrih)?> '))
    cas = int(input('Koliko časa ste tekli (v urah)?> '))
    nacin = (input('Kako ste se gibali (za hojo napišite: False, za tek pa: True)?> '))
    while nacin != True and nacin != False:
        if nacin == 'True':
            nacin = True
        elif nacin == 'False':
            nacin = False
        else:
            print('Niste pravilno definiralni načina.')
            nacin = (input('Kako ste se gibali (za hojo napišite: False, za tek pa: True)?> '))
    strmina = int(input('Kakšen je bil klanec (napišite za ustrezno strmino (v odstotkih); zelo velik: 20, velik: 15, srednje velik: 10, majhen: 5, brez klanca: 0)?> '))
    teza = int(input('Kakšna je vaša telesna teža (v kilogramih)?> '))
    datum = date.today()
    novo_gibanje = DnevnikGibanja(dolzina, cas, nacin, strmina, teza, datum)
    gibanja_za_kalorije = MerilnikGibanja(dolzina, cas, nacin, strmina, teza)
    gibanja.dodaj(novo_gibanje)
    print(f'Porabili ste {gibanja_za_kalorije.poraba_kalorij()} in {gibanja_za_kalorije.poraba_kisika_s_tezo()}(kisika).')

def izbris_zadnjega_elementa():
    if gibanja.seznam_gibanj == []:
        return print('Niste dodali še nobenega gibanja')
    else:
        gibanja.izbris_zadnjega_elementa()

def izpis_gibanja():
    gib = gibanja.koncna_za_datume()
    print(gib.izpis_gibanja())

def vsota_gibanja():
    gib = gibanja.koncna_za_datume()
    print(gib.vsota_gibanja())

def povprečje_gibanja():
    gib = gibanja.koncna_za_datume()
    print(gib.novo_povp_mesec())

def max_gibanja_za_vsak_mesec():
    gib = gibanja.koncna_za_datume()
    print(gib.max_gibanja_za_vsak_mesec())

def vsota_gibanja_po_letih():
    gib = gibanja.koncna_za_datume()
    print(gib.vsota_gibanja_po_letih())

def povprečje_gibanja_po_letih():
    gib = gibanja.koncna_za_datume()
    print(gib.novo_povp())

def max_gibanja_po_letih():
    gib = gibanja.koncna_za_datume()
    print(gib.max_gibanja_po_letih())

tekstovni_vmesnik()



