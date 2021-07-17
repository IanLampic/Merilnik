# from _typeshed import Self

from model import MerilnikTeka
from datetime import date

razdalja = input('Koliko ste pretekli (v kilometrih)? ')
čas = input('Koliko časa ste tekli (v urah)? ')
način_gibanja = input('Kako ste se gibali (hoja ali tek)? ')
strmina = input('Kakšen je bil klanec (izbirate lahko med: zelo velik, velik, srednje velik, majhen, ni bilo klanca)? ')
teža = input('Kakšna je vaša telesna teža (v kilogramih)? ')

print('Porabili ste ' + str(self.poraba_kisika_s_tezo()) + ' kilometrov')
print('Tekli ste ' + str(čas) + ' ur')