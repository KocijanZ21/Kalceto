from Data.repository import Repo
from Data.models import *
from typing import List
import bcrypt
from datetime import date


class AuthService:
    repo : Repo
    def __init__(self):
         self.repo = Repo()


    """def zakodiraj_sumnik(self, besedilo : str) -> str:
        sumniki = {'š': 's-','č': 'c-','ž' : 'z-'}
        besedilo2 = ''
        for crka in besedilo:
            if crka.lower() in sumniki.keys():
                for sumnik in sumniki.keys():
                    if sumnik == crka.lower():
                        if crka.isupper():
                            besedilo2 += sumniki[sumnik][0].upper() +'-'  
                        else:  
                            besedilo2 += sumniki[sumnik]
            else:
                besedilo2 += crka
        return besedilo2
            
    def odkodiraj_sumnik(self, besedilo : str) -> str:
        besedilo2 = ''
        for i in range(len(besedilo)):
            if besedilo[i] == '-':
                prejsna = besedilo[i-1]
                besedilo2 = besedilo2[ : -1]
                match(prejsna.lower()):
                    case 'z':
                        if prejsna.isupper():
                            besedilo2 += 'ž'.upper() 
                        else:
                            besedilo2 += 'ž'
                    case 's':
                        if prejsna.isupper():
                            besedilo2 += 'š'.upper() 
                        else:
                            besedilo2 += 'š'
                    case 'c':
                        if prejsna.isupper():
                            besedilo2 += 'č'.upper() 
                        else:
                            besedilo2 += 'č'   
            else:
                besedilo2 += besedilo[i]
        return besedilo2"""

    def obstaja_uporabnik(self, uporabnik: str) -> bool:
        try:
            user = self.repo.dobi_uporabnika(uporabnik)
            return True
        except:
            return False
       

    def prijavi_uporabnika(self, uporabnik : str, geslo: str) -> UporabnikDto | bool :

        # Najprej dobimo uporabnika iz baze
        user = self.repo.dobi_uporabnika(uporabnik)

        geslo_bytes = geslo.encode('utf-8')
        # Ustvarimo hash iz gesla, ki ga je vnesel uporabnik
        succ = bcrypt.checkpw(geslo_bytes, user.password_hash.encode('utf-8'))

        if succ:
            # popravimo last login time
            user.last_login = date.today().isoformat()
            self.repo.posodobi_uporabnika(user)
            return UporabnikDto(username=user.username, role=user.role)
        
        return False

    def dodaj_uporabnika(self, uporabnik: str, rola: str, emso: str, geslo: str) -> UporabnikDto:

        # zgradimo hash za geslo od uporabnika
       # Najprej geslo zakodiramo kot seznam bajtov
        bytes = geslo.encode('utf-8')
  
        # Nato ustvarimo salt
        salt = bcrypt.gensalt()
        
        # In na koncu ustvarimo hash gesla
        password_hash = bcrypt.hashpw(bytes, salt)

        # Sedaj ustvarimo objekt Uporabnik in ga zapišemo bazo

        u = Uporabnik(
            username=uporabnik,#self.zakodiraj_sumnik(uporabnik), 
            role=rola,
            password_hash=password_hash.decode(),
            last_login= date.today().isoformat(),
            emso = emso
        )

        self.repo.dodaj_uporabnika(u)

        return UporabnikDto(username=uporabnik, role=rola)
    
    def dodaj_igralca(self, emso: str, ime: str, priimek: str, spol: str, drzava: str, email: str, rojstni_dan: str) -> igralec: #todo 
        i = igralec(
            emso = emso,
            ime = ime,
            priimek=priimek,
            spol=spol,
            drzava=drzava,
            email=email,
            rojstni_dan=rojstni_dan
        )
        try:
            self.repo.dodaj_igralca(i)
            return True
        except:
            return False
        
    def dobi_uporabnika(self, username: str) -> igralec|sodnik:
        uporabnik = self.repo.dobi_uporabnika(username)
        vloga = uporabnik.role
        if vloga == 'igralec':
            return self.repo.dobi_igralca(uporabnik.emso)
        
        return  self.repo.dobi_sodnika(uporabnik.emso)
    
    def dobi_uporabnika_emso(self, emso:str) -> Uporabnik:
        uporab = self.repo.dobi_uporabnika_emso(emso)
        return uporab

    def dobi_igralca(self, emso: str) -> igralec:
        igralec = self.repo.dobi_igralca(emso)
        return igralec
    
    def odstrani_igralca(self, emso: str):
        self.repo.odstrani_igralca(emso)

    def dodaj_sodnika(self, emso: str, ime: str, priimek: str, spol: str, drzava: str, email: str, rojstni_dan: str) -> sodnik: #todo 
        s = sodnik(
            emso = emso,
            ime = ime,
            priimek=priimek,
            spol=spol,
            drzava=drzava,
            email=email,
            rojstni_dan=rojstni_dan
        )
        try:
           self.repo.dodaj_sodnika(s)
           return True
        except:
           return False

    def dobi_sodnika(self, emso: str)  -> sodnik:
        sodnik = self.repo.dobi_sodnika(emso)
        #priimek1 = self.repo.odkodiraj_sumnik(sodnik.priimek) 
        #sodnik.priimek = priimek1
        return sodnik
    
    def dobi_vse_sodnike(self) -> sodnik:
        sod = self.repo.dobi_vse_sodnike()
        return sod

    def odstrani_sodnika(self, emso: str):
        self.repo.odstrani_sodnika(emso)   

   
   


    
