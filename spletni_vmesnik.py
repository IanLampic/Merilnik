from re import template
from model import *
from datetime import date, timedelta
import json
import bottle

#MWC - model-view-controller
DATOTEKA_S_STANJEM = "stanje.json"
PISKOTEK_UPORABNISKO_IME = 'uporabnisko_ime'
SKRIVNOST = 'to je ena skrivnost'

kalorije = []

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if uporabnisko_ime:
        try:
            return Uporabnik.uporabnik_preberi_iz_datoteke(uporabnisko_ime)
        except:
            return Uporabnik(uporabnisko_ime, Analiza([]))
    else:
        bottle.redirect('/prijava/')

def podatki_uporabnika(uporabnisko_ime):
    return Uporabnik.uporabnik_preberi_iz_datoteke(uporabnisko_ime)

def shrani_stanje(uporabnik):
    uporabnik.shrani_v_datoteko_uporabnik()

@bottle.get('/prijava/')
def prijava():
    return bottle.template('prijava.html', napaka=None)

@bottle.post('/prijava/')
def prijava():
    geslo = bottle.request.forms.getunicode('geslo')
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    if geslo == 'geslo':
        bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path='/', secret=SKRIVNOST)
        bottle.redirect('/')
    else:
        return bottle.template('prijava.html', napaka='Geslo ni pravilno!')

@bottle.post('/odjava/')
def prijava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path='/')
    bottle.redirect('/')

@bottle.get('/')
def osnovna_stran():
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        'osnovna_stran.html',
        vsota_mesec = uporabnik.gibanja.koncna_za_datume().vsota_gibanja(),
        povp_mesec = uporabnik.gibanja.koncna_za_datume().novo_povp_mesec(),
        max_mesec = uporabnik.gibanja.koncna_za_datume().max_gibanja_za_vsak_mesec(),
        vsota_leta = uporabnik.gibanja.koncna_za_datume().vsota_gibanja_po_letih(),
        povp_leto = uporabnik.gibanja.koncna_za_datume().novo_povp(),
        max_leto = uporabnik.gibanja.koncna_za_datume().max_gibanja_po_letih(),
        kalo = kalorije,
        uporabnik = uporabnik
    )

@bottle.get('/dodaj-gibanje/')
def dodaj_gibanje():
    uporabnik = trenutni_uporabnik()
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    return bottle.template("dodaj_gibanje.html", uporabnik=uporabnik)
#TODO: Popravi in poglej si glede napak

@bottle.post("/dodaj-gibanje/")
def dodaj_gibanje_post():
    uporabnik = trenutni_uporabnik()
    dolzina = float(bottle.request.forms['dolzina'])
    cas = float(bottle.request.forms['cas'])
    nacin = bool(bottle.request.forms['nacin'])
    strmina = float(bottle.request.forms['strmina'])
    teza = float(bottle.request.forms['teza'])
    datum = date.today().strftime('%Y-%m-%d')
    uporabnik.gibanja.dodaj(DnevnikGibanja(dolzina, cas, nacin, strmina, teza, datum))
    kalorija = MerilnikGibanja(dolzina, cas, nacin, strmina, teza).poraba_kalorij()
    kisik = MerilnikGibanja(dolzina, cas, nacin, strmina, teza).poraba_kisika_s_tezo()
    kalorije.append([kalorija, kisik])
    shrani_stanje(uporabnik)
    bottle.redirect("/")

@bottle.get('/izbris-zadnjega-gibanja/')
def izbris_zadnjega_gibanja():
    uporabnik = trenutni_uporabnik()
    if uporabnik.gibanja.seznam_gibanj == []:
        'Niste dodali še nobenega gibanja'
    else:
        uporabnik.gibanja.izbris_zadnjega_elementa()
    bottle.redirect('/')

@bottle.error(404)
def error_404(error):
    return 'Ta stran ne obstaja!'

bottle.run(reloader=True, debug=True)

#github v zgornji desni kot zraven uporabniškega imena, malo olepšaj, naredi da dela izbris gibanja

