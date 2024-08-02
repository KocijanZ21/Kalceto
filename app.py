from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user


from Services.auth_service import AuthService
import os
import datetime


# Ustvarimo instance servisov, ki jih potrebujemo. 
# Če je število servisov veliko, potem je service bolj smiselno inicializirati v metodi in na
# začetku datoteke (saj ne rabimo vseh servisov v vseh metodah!)


auth = AuthService()


# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("uporabnik")
        if cookie:
            return f(*args, **kwargs)
        return template("prijava_up.html",uporabnik=None, rola=None, error ="Potrebna je prijava!")
        
    return decorated

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')

@get('/')
def zacetna_stran():
    return template('zacetna_stran.html')

@get('/registracija')
def registracija():
    return template('registracija.html', error=None)

@post('/registracija')
def registracija_post():
    emso = request.forms.get('emso')
    ime = request.forms.get('ime').encode('latin1').decode('utf-8') #dodala encode in decode, ker drugače ni pisalo šumnikov
    priimek = request.forms.get('priimek').encode('latin1').decode('utf-8')
    spol = request.forms.get('spol').encode('latin1').decode('utf-8')
    drzava = request.forms.get('drzava').encode('latin1').decode('utf-8')
    email = request.forms.get('email')
    rojstni_dan = request.forms.get('rojstni_dan')
    username = request.forms.get('username').encode('latin1').decode('utf-8')
    password = request.forms.get('password')
    role = request.forms.get('role')
    #emso = request.forms.get('emso')

    # Preveri, če uporabniško ime že obstaja
    if auth.obstaja_uporabnik(username):
        return template('registracija.html', error="Uporabniško ime že obstaja.")

    # Dodaj uporabnika in igralca/sodnika glede na role
    auth.dodaj_uporabnika(username, role, emso, password)
    if role == "igralec":
        auth.dodaj_igralca(emso, ime, priimek, spol, drzava, email, rojstni_dan)
    else: 
        auth.dodaj_sodnika(emso, ime, priimek, spol, drzava, email, rojstni_dan)
    

    redirect(url('/prijava'))

@get('/prijava')
def prijava():
    return template('prijava_up.html', error=None)

@post('/prijava')
def prijava_post():
    username = request.forms.get('username').encode('latin1').decode('utf-8')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
            return template("prijava_up.html", error="Uporabnik s tem imenom ne obstaja. Potrebna je registracija.")
    
    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)
        response.set_cookie("vloga", prijava.role)
        # redirect v večino primerov izgleda ne deluje
        redirect(url('/domov'))

    else:
        return template("prijava_up.html", uporabnik=None, rola=None, error="Neuspešna prijava. Napačno geslo ali uporabniško ime.")

@get('/domov')
def domov():
    uporabnik = request.get_cookie("uporabnik").encode('latin1').decode('utf-8')
    vloga = request.get_cookie("vloga")
    podatki = auth.dobi_uporabnika(uporabnik)
    emso = podatki.emso
    ime = podatki.ime
    priimek = podatki.priimek
    spol = podatki.spol
    drzava = podatki.drzava
    email = podatki.email
    rojstni_dan = podatki.rojstni_dan
    

    return template('domov.html', uporabnik = uporabnik, vloga = vloga, emso = emso, ime = ime, priimek = priimek, spol = spol, drzava = drzava, email = email, rojstni_dan = rojstni_dan)

@get('/prijava_na_turnir')
def prijava_na_turnir():
    return template('prijava_na_turnir.html') 

@get('/tekme')
def tekme():
    return template('tekme.html')  


if __name__ == "__main__":

   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)