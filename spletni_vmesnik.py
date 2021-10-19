from model import *
from datetime import date, timedelta
import bottle

#MWC - model-view-controller
PISKOTEK_UPORABNISKO_IME = 'uporabnisko_ime'
SKRIVNOST = 'to je ena skrivnost'

kalorije = []

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if uporabnisko_ime:
        return podatki_uporabnika(uporabnisko_ime)
    else:
        bottle.redirect('/prijava/')

def podatki_uporabnika(uporabnisko_ime):
    return Uporabnik.uporabnik_preberi_iz_datoteke(uporabnisko_ime)


def shrani_stanje(uporabnik):
    uporabnik.shrani_v_datoteko_uporabnik()

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava.html', napaka=None)

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo_v_cistopisu = bottle.request.forms.getunicode('geslo')
    if not uporabnisko_ime:
        return bottle.template('registracija.html', napaka="Vnesi uporabniško ime!")
    try:  
        Uporabnik.prijava(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.redirect('/')
    except ValueError as e:
        return bottle.template("prijava.html", napaka=e.args[0])

@bottle.post('/odjava/')
def odjava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path='/')
    bottle.redirect('/')

@bottle.get('/')
def osnovna_stran():
    return bottle.template(
        'osnovna_stran.html',
        kalo = kalorije,
        uporabnik = trenutni_uporabnik()
    )

@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)

@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.registracija(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "registracija.html", napaka=e.args[0]
        )

@bottle.get('/dodaj-gibanje/')
def dodaj_gibanje():
    return bottle.template(
        "dodaj_gibanje.html",
        uporabnik = trenutni_uporabnik(),
        napaka=None)

@bottle.post("/dodaj-gibanje/")
def dodaj_gibanje_post():
    kalorije.clear()
    uporabnik = trenutni_uporabnik()
    dolzina = bottle.request.forms['dolzina']
    cas = bottle.request.forms['cas']
    nacin = bottle.request.forms['nacin']
    if nacin.lower() == 'tek':
        n_nacin = True
    elif nacin.lower() == 'hoja':
        n_nacin = False
    else:
        return bottle.template('dodaj_gibanje.html', uporabnik = trenutni_uporabnik(), napaka='Niste pravilno definirali načina gibanja.')
    strmina = bottle.request.forms['strmina']
    teza = bottle.request.forms['teza']
    if not ali_je_stevilo(dolzina) or not ali_je_stevilo(cas) or not ali_je_stevilo(strmina) or not ali_je_stevilo(teza):
        return bottle.template('dodaj_gibanje.html', uporabnik = trenutni_uporabnik(), napaka='Na enem izmed mest niste vpisali števila.')
    dolzina = float(dolzina)
    cas = float(bottle.request.forms['cas'])
    strmina = float(bottle.request.forms['strmina'])        
    teza = float(bottle.request.forms['teza'])
    datum = date.today().strftime('%Y-%m-%d')
    uporabnik.gibanja.dodaj(DnevnikGibanja(dolzina, cas, n_nacin, strmina, teza, datum))
    kalorija = MerilnikGibanja(dolzina, cas, n_nacin, strmina, teza).poraba_kalorij()
    kisik = MerilnikGibanja(dolzina, cas, n_nacin, strmina, teza).poraba_kisika_s_tezo()
    kalorije.append([kalorija, kisik])
    shrani_stanje(uporabnik)
    bottle.redirect("/")

@bottle.get('/izbris-zadnjega-gibanja/')
def izbris_zadnjega_gibanja_get():
    uporabnik = trenutni_uporabnik()
    if len(uporabnik.gibanja.seznam_gibanj) > 0:
        uporabnik.gibanja.izbris_zadnjega_elementa()
        shrani_stanje(uporabnik)
    return bottle.template(
        "izbris_gibanja.html",
        uporabnik = trenutni_uporabnik(),
        gibanja = trenutni_uporabnik().gibanja.seznam_gibanj,
        napaka=None)

@bottle.post('/izbris-zadnjega-gibanja/')
def izbris_zadnjega_gibanja_post():
    bottle.redirect('/')

@bottle.get("/analiza/")
def analiza():
    kalorije.clear()
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "analiza.html",
        vsota = uporabnik.gibanja.koncna_za_datume().vsota_gibanja(),
        povprecje_meseca = uporabnik.gibanja.koncna_za_datume().novo_povp_mesec(),
        maks_mesec = uporabnik.gibanja.koncna_za_datume().max_gibanja_za_vsak_mesec(),
        vsota_leta = uporabnik.gibanja.koncna_za_datume().vsota_gibanja_po_letih(),
        povprecje_leta = uporabnik.gibanja.koncna_za_datume().novo_povp(),
        maks_leta = uporabnik.gibanja.koncna_za_datume().max_gibanja_po_letih(),
        uporabnik = trenutni_uporabnik()
    )
def ali_je_stevilo(n):
    """ Vrne True če je niz število. """
    try:
        float(n)
        return True
    except ValueError:
        return False

@bottle.error(404)
def error_404(error):
    return 'Ta stran ne obstaja!'
 #TODO: Popravi dodajanje
bottle.run(reloader=True, debug=True)


