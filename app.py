from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.turnir_service import TurnirService
from Services.auth_service import AuthService
import os
from datetime import datetime, date, time
from datetime import timedelta
import random


# Ustvarimo instance servisov, ki jih potrebujemo. 
# Če je število servisov veliko, potem je service bolj smiselno inicializirati v metodi in na
# začetku datoteke (saj ne rabimo vseh servisov v vseh metodah!)


auth = AuthService()
service = TurnirService()


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

@get('/turnirji')
def turnir():
    uporabnik = request.get_cookie("uporabnik").encode('latin1').decode('utf-8')
    turnirji = service.dobi_turnir()
    danasnji_datum = date.today()
    st_vseh = []
    for t in turnirji:
        st_oseb = service.sestej_prijave_turnir(t.id_turnirja)
        print(st_oseb)
        st_vseh.append(st_oseb)
    turnir_st = zip(turnirji, st_vseh)    
    return template_user('turnirji.html', turnirji = turnir_st, danasnji_datum = danasnji_datum)

@post('/prijava_na_turnir/<id_turnirja>')
def prijavi_se_na_turnir(id_turnirja):
    uporabnik = request.get_cookie("uporabnik").encode('latin1').decode('utf-8')
    
    try:
        if service.dobi_prijave_turnir_oseba(id_turnirja, uporabnik):
            return "Uporabnik je že prijavljen na ta turnir!"
        
        # Dodaj uporabnika v tabelo prijava_turnir
        service.dodaj_prijavo_turnir(id_turnirja, uporabnik)
        return "Prijava je bila uspešna!"
    except Exception as e:
        print(f"Napaka pri prijavi na turnir: {e}")
        return "Prišlo je do napake pri prijavi."

@get('/tekme')
def tekme():
    turnirji = service.dobi_turnir()
    return template('tekme.html', turnirji = turnirji)

@get('/tekme/<id_turnirja>')
def tekme(id_turnirja):
    id_turnirja = id_turnirja.replace('%20', ' ')
    en_turnir = service.dobi_turnir_en(id_turnirja)
    vloga = request.get_cookie("vloga")
    ime_turnirja1 = [ime.id_turnirja for ime in en_turnir]
    ime_turnirja = ime_turnirja1[0]
    datum_turnirja = [datum.datum_pricetka for datum in en_turnir]
    datum_konca = [dat.datum_konca_prijav for dat in en_turnir]
    datum_konca_prijav = datum_konca[0]
    danasnji_datum = date.today()
    st_prijavljenih = service.sestej_prijave_turnir(id_turnirja)
    
    

    if vloga == 'sodnik':

        if st_prijavljenih == 16:
            tekme = service.dobi_tekmo_turnir(id_turnirja)

            if tekme:
                prvi_krog = service.dobi_trenutni_krog(id_turnirja)
                vsi_izidi_vpisani = service.ali_so_vsi_zmagovalci_vpisani(id_turnirja, prvi_krog)
                return template('tekme_na_turnirju.html', tekme=tekme, danasnji_datum = danasnji_datum, datum_konca_prijav = datum_konca_prijav, vsi_izidi_vpisani = vsi_izidi_vpisani, ime_turnirja = ime_turnirja, st_prijavljenih = st_prijavljenih)

            prijavljeni = service.dobi_prijave_turnir(id_turnirja)
            prijavljene_osebe = [oseba.up_ime for oseba in prijavljeni]
            sodniki = auth.dobi_vse_sodnike()
            emso_sodnikov = [sodni.emso for sodni in sodniki]
            sodniki_up = []
            for st in emso_sodnikov:
                sodnik1 = auth.dobi_uporabnika_emso(st)
                sodniki_up.append(sodnik1)
            sodniki_up    

            up_ime_sodniki = [up_imena.username for up_imena in sodniki_up]

            zeljena_ura = time(10, 0)
            cas_tekme = datetime.combine(datum_turnirja[0], zeljena_ura)
            miza = 1
            krog = 1
            izid = ''
            random.shuffle(prijavljene_osebe)

            while len(prijavljene_osebe) > 1:
                igralec1 = prijavljene_osebe.pop()
                igralec2 = prijavljene_osebe.pop()
                sodnik_tekme = random.choice(up_ime_sodniki) 

                service.dodaj_tekmo(cas_tekme, miza, izid, id_turnirja, sodnik_tekme, igralec1, igralec2, krog)    

                cas_tekme += timedelta(hours=1)

            prvi_krog = service.dobi_trenutni_krog(id_turnirja)
            vsi_izidi_vpisani = service.ali_so_vsi_zmagovalci_vpisani(id_turnirja, prvi_krog)
            tekme = service.dobi_tekmo_turnir(id_turnirja)
            return template('tekme_na_turnirju.html', tekme = tekme, danasnji_datum = danasnji_datum, datum_konca_prijav = datum_konca_prijav, vsi_izidi_vpisani = vsi_izidi_vpisani, ime_turnirja = ime_turnirja, st_prijavljenih = st_prijavljenih)
        else:
            tekme = service.dobi_tekmo_turnir(id_turnirja)
            return template('tekme_na_turnirju.html', tekme = tekme, danasnji_datum = danasnji_datum, datum_konca_prijav = datum_konca_prijav,  ime_turnirja = ime_turnirja)
    else: 
        if service.sestej_prijave_turnir(id_turnirja) == 16:
            tekme = service.dobi_tekmo_turnir(id_turnirja)

            if tekme:
                return template('tekme_na_turnirju_igralec.html', tekme=tekme,  st_prijavljenih = st_prijavljenih)

            prijavljeni = service.dobi_prijave_turnir(id_turnirja)
            prijavljene_osebe = [oseba.up_ime for oseba in prijavljeni]
            sodniki = auth.dobi_vse_sodnike()
            emso_sodnikov = [sodni.emso for sodni in sodniki]
            sodniki_up = []
            for st in emso_sodnikov:
                sodnik1 = auth.dobi_uporabnika_emso(st)
                sodniki_up.append(sodnik1)
            sodniki_up    

            up_ime_sodniki = [up_imena.username for up_imena in sodniki_up]

            zeljena_ura = time(10, 0)
            cas_tekme = datetime.combine(datum_turnirja[0], zeljena_ura)
            miza = 1
            izid = ''
            krog = 1
            random.shuffle(prijavljene_osebe)

            while len(prijavljene_osebe) > 1:
                igralec1 = prijavljene_osebe.pop()
                igralec2 = prijavljene_osebe.pop()
                sodnik_tekme = random.choice(up_ime_sodniki) 

                service.dodaj_tekmo(cas_tekme, miza, izid, id_turnirja, sodnik_tekme, igralec1, igralec2, krog)    

                cas_tekme += timedelta(hours=1)
            
            tekme = service.dobi_tekmo_turnir(id_turnirja)
            return template('tekme_na_turnirju_igralec.html', tekme = tekme, vloga = vloga, danasnji_datum = danasnji_datum, datum_konca_prijav = datum_konca_prijav,  st_prijavljenih = st_prijavljenih)
        else:
            tekme = service.dobi_tekmo_turnir(id_turnirja)
            return template('tekme_na_turnirju_igralec.html', tekme = tekme,danasnji_datum = danasnji_datum, datum_konca_prijav = datum_konca_prijav, st_prijavljenih = st_prijavljenih)

@post('/dodaj_izid')
def dodaj_izid():
    tekma_id = request.forms.get('tekma_id')
    zmagovalec = request.forms.get('zmagovalec')

    # Klic funkcije za posodobitev izida tekme v bazi
    service.posodobi_izid_tekme(tekma_id, zmagovalec)

    redirect('/domov')   

@get('/nov_krog/<id_turnirja>')
def nov_krog(id_turnirja):
    print(id_turnirja)
    ime_turnirja = id_turnirja
    print(ime_turnirja)
    vsi_sodniki = auth.dobi_vse_sodnike()
    emso_sodnik = [sodni.emso for sodni in vsi_sodniki]
    sodniki_uporab = []
    for st in emso_sodnik:
        sodnik2 = auth.dobi_uporabnika_emso(st)
        sodniki_uporab.append(sodnik2)
    sodniki_uporab    
    uporab_ime_sodniki = [up_imena.username for up_imena in sodniki_uporab]
    
   
    # Pridobitev trenutnega kroga in zmagovalcev
    zadnji_krog = service.dobi_trenutni_krog(id_turnirja)
    print(zadnji_krog)
    
    
    cas_tekme = service.dobi_tekmo_krog(ime_turnirja, zadnji_krog)
    datum = datetime.strptime(cas_tekme, '%Y-%m-%d %H:%M:%S')
    

    zmagovalci_vse = service.dobi_zmagovalci(id_turnirja, zadnji_krog)
    zmagovalci = [zmagov.izid for zmagov in zmagovalci_vse]
    st_prijavljenih =  len(zmagovalci)
  
    print(zmagovalci)

    # Določimo nov krog
    nov_krog = zadnji_krog + 1

    vsi_izidi_vpisani = service.ali_so_vsi_zmagovalci_vpisani(id_turnirja, nov_krog)
   
    ali_so_tekme = service.ali_tekmo_krog_je(ime_turnirja, nov_krog)
    
    if ali_so_tekme:
        tekme = service.dobi_tekmo_krog_je(ime_turnirja,nov_krog)
        return template('tekme_na_turnirju.html', tekme=tekme, ime_turnirja = ime_turnirja, vsi_izidi_vpisani = vsi_izidi_vpisani, st_prijavljenih = st_prijavljenih)
    else:
        # Glede na število zmagovalcev prilagodimo koliko jih naj vnesemo
        if  len(zmagovalci) == 1:
            zmagovalec_turnirja = zmagovalci[0]
            service.posodobi_zmagovalca_turnirja(id_turnirja, zmagovalec_turnirja)
            tekme = service.dobi_tekmo_turnir(ime_turnirja)
            return template('tekme_na_turnirju.html',tekme = tekme, zmagovalec_turnirja = zmagovalec_turnirja, st_prijavljenih = st_prijavljenih)
        else:
            service.ustvari_nov_krog(zmagovalci, id_turnirja, datum, nov_krog, uporab_ime_sodniki)
            tekme = service.dobi_tekmo_krog_je(ime_turnirja, nov_krog)
        return template('tekme_na_turnirju.html', tekme = tekme, vsi_izidi_vpisani = vsi_izidi_vpisani, ime_turnirja = ime_turnirja, st_prijavljenih = st_prijavljenih)

    
    

if __name__ == "__main__":

   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)