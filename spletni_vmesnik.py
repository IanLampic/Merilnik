from re import template
from model import *
from datetime import date, timedelta
import json
import bottle

#MWC - model-view-controller
DATOTEKA_S_STANJEM = "stanje.json"

try:
    gibanja = Uporabnik.preberi_iz_datoteke(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    gibanja = Uporabnik([])

kalorije = []

def shrani_stanje():
    gibanja.shrani_v_datoteko(DATOTEKA_S_STANJEM)

@bottle.get('/')
def osnovna_stran():
    return bottle.template(
        'osnovna_stran.html',
        vsota_mesec = gibanja.koncna_za_datume().vsota_gibanja(),
        povp_mesec = gibanja.koncna_za_datume().novo_povp_mesec(),
        max_mesec = gibanja.koncna_za_datume().max_gibanja_za_vsak_mesec(),
        vsota_leta = gibanja.koncna_za_datume().vsota_gibanja_po_letih(),
        povp_leto = gibanja.koncna_za_datume().novo_povp(),
        max_leto = gibanja.koncna_za_datume().max_gibanja_po_letih(),
        kalo = kalorije
    )

@bottle.get('/dodaj-gibanje/')
def dodaj_gibanje():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    return bottle.template("dodaj_gibanje.html", napake={}, polja={}, uporabnisko_ime=uporabnisko_ime)
#TODO: Popravi in poglej si glede napak

@bottle.post("/dodaj-gibanje/")
def dodaj_gibanje_post():
    dolzina = float(bottle.request.forms['dolzina'])
    cas = float(bottle.request.forms['cas'])
    nacin = bool(bottle.request.forms['nacin'])
    strmina = float(bottle.request.forms['strmina'])
    teza = float(bottle.request.forms['teza'])
    datum = date.today().strftime('%Y-%m-%d')
    gibanja.dodaj(DnevnikGibanja(dolzina, cas, nacin, strmina, teza, datum))
    kalorija = MerilnikGibanja(dolzina, cas, nacin, strmina, teza).poraba_kalorij()
    kisik = MerilnikGibanja(dolzina, cas, nacin, strmina, teza).poraba_kisika_s_tezo()
    kalorije.append([kalorija, kisik])
    shrani_stanje()
    bottle.redirect("/")
    #TODO: Kako ta response deluje

@bottle.get('/izbris-zadnjega-gibanja/')
def izbris_zadnjega_gibanja():
    if gibanja.seznam_gibanj == []:
        'Niste dodali še nobenega gibanja'
    else:
        gibanja.izbris_zadnjega_elementa()
    bottle.redirect('/')

@bottle.error(404)
def error_404(error):
    return 'Ta stran ne obstaja!'

bottle.run(reloader=True, debug=True)

#github v zgornji desni kot zraven uporabniškega imena, malo olepšaj, naredi da dela izbris gibanja

