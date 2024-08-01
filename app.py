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

#@get('/')
#def index():
    """
    Domača stran.
    """
    rola = request.get_cookie("rola")
    uporabnik = request.get_cookie("uporabnik")
    return template('prijava_up.html', rola = rola, uporabnik=uporabnik)


@get('/')
def zacetna_stran():
    return template('zacetna_stran.html')

@get('/registracija')
def registracija():
    return template('registracija.html', error=None)

@post('/registracija')
def registracija_post():
    emso = request.forms.get('emso')
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    spol = request.forms.get('spol')
    drzava = request.forms.get('drzava')
    email = request.forms.get('email')
    rojstni_dan = request.forms.get('rojstni_dan')
    username = request.forms.get('username')
    password = request.forms.get('password')
    role = request.forms.get('role')
    oseba = ''

    # Preveri, če uporabniško ime že obstaja
    if auth.obstaja_uporabnik(username):
        return template('registracija.html', error="Uporabniško ime že obstaja.")

    # Dodaj uporabnika in igralca/sodnika glede na role
    auth.dodaj_uporabnika(username, role, oseba, password)
    if role == "igralec":
        auth.dodaj_igralca(emso, ime, priimek, spol, drzava, email, rojstni_dan)
    else: #dela oki ampak ne vnese v bazo če je sodnik
        auth.dodaj_sodnika(emso, ime, priimek, spol, drzava, email, rojstni_dan)
    

    redirect(url('zacetna_stran'))

@get('/prijava')
def prijava():
    return template('prijava_up.html', error=None)

@post('/prijava')
def prijava_post():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
            return template("prijava_up.html", error="Uporabnik s tem imenom ne obstaja. Potrebna je registracija.")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        
        # redirect v večino primerov izgleda ne deluje
        redirect(url('/'))

    else:
        return template("prijava_up.html", uporabnik=None, rola=None, error="Neuspešna prijava. Napačno geslo ali uporabniško ime.")






#@get('/')#get podatke dobim iz url
#@cookie_required
#def index():
    return template_user('prijava.html', up = "", passw = "", izbira = False)

#@post('/') #post podatke dobim iz forme
#def dodaj_uporabnika():
    username = request.forms.get("username")
    password = request.forms.get("password")
    #password_hash = hashlib.md5(password.encode())
    role = request.forms.get("role")
    last_login = datetime.datetime.now()
    oseba = ''
    if not auth.obstaja_uporabnik(username): #ta se zgodi ko uporabnik še ne obstaja
        auth.dodaj_uporabnika(username, '', oseba, password)
        return template("prijava.html", up = username, passw = password, izbira = True)
    else: #ta se zgodi, če uporabnik obstaja ali pa če ni obstajal in je submital formo (nima še role)
        preusmeritev = "prijava_" + role
        if len(role) > 0:
            auth.posodobi_vlogo(username, role)
        print(preusmeritev, username)
        return template_user(preusmeritev)



if __name__ == "__main__":

   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)