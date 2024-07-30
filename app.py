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
        return template("prijava.html",uporabnik=None, rola=None, napaka="Potrebna je prijava!")
        
    return decorated

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')

@get('/')
@cookie_required
def index():
    return template_user('prijava.html')

@post('/dodaj_uporabnika')
def dodaj_uporabnika():
    username = request.forms.get("username")
    password = request.forms.get("password")
    #password_hash = hashlib.md5(password.encode())
    role = request.forms.get("role")
    last_login = datetime.datetime.now()
    oseba = ''
    auth.dodaj_uporabnika(username, role, oseba, password)
    #return template_user('prijava_igralec.html', uporabnik = username)



if __name__ == "__main__":

   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)