from Data.repository import Repo
from Data.models import *
from typing import List
import bcrypt
from datetime import date


class AuthService:
    repo : Repo
    def __init__(self):
         self.repo = Repo()

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

    def dodaj_uporabnika(self, uporabnik: str, rola: str, oseba: str, geslo: str) -> UporabnikDto:

        # zgradimo hash za geslo od uporabnika

        # Najprej geslo zakodiramo kot seznam bajtov
        bytes = geslo.encode('utf-8')
  
        # Nato ustvarimo salt
        salt = bcrypt.gensalt()
        
        # In na koncu ustvarimo hash gesla
        password_hash = bcrypt.hashpw(bytes, salt)

        # Sedaj ustvarimo objekt Uporabnik in ga zapišemo bazo

        u = Uporabnik(
            username=uporabnik,
            role=rola,
            password_hash=password_hash.decode(),
            last_login= date.today().isoformat(),
            oseba=oseba
        )

        self.repo.dodaj_uporabnika(u)

        return UporabnikDto(username=uporabnik, role=rola)
    
    def dodaj_igralca(self, emso: str, ime: str, priimek: str, spol: str, drzava: str, email: str, rojstni_dan: str) -> igralec:
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
        

    def dobi_igralca(self, emso: str) -> igralec:
        igralec = self.repo.dobi_igralca(emso)
        return igralec
    
    def odstrani_igralca(self, emso: str):
        self.repo.odstrani_igralca(emso)

    def dodaj_sodnika(self, emso: str, ime: str, priimek: str) -> sodnik:
        s = sodnik(
            emso=emso,
            ime=ime,
            priimek=priimek
        )
        try:
           self.repo.dodaj_sodnika(s)
           return True
        except:
           return False

    def dobi_sodnika(self, emso: str)  -> sodnik:
        sodnik = self.repo.dobi_sodnika(emso) 
        return sodnik

    def odstrani_sodnika(self, emso: str):
        self.repo.odstrani_sodnika(emso)    
    
