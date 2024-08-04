from Data.repository import Repo
from Data.models import *
from typing import List


# V tej datoteki bomo definirali razred za obdelavo in delo s transakcijami

class TurnirService:
    def __init__(self) -> None:
        # Potrebovali bomo instanco repozitorija. Po drugi strani bi tako instanco 
        # lahko dobili tudi kot input v konstrukturju.
        self.repo = Repo()


    def dobi_turnir(self) -> turnir:
        tur = self.repo.dobi_turnir()
        return tur
    
    def dobi_turnir_en(self, id_turnirja: str) -> List[turnir]:
       tur_en = self.repo.dobi_turnir_en(id_turnirja)
       return tur_en
    
    def dodaj_prijavo_turnir(self, kateri_turnir : str, up_ime : str) -> prijave_turnir:
        p = prijave_turnir(
            kateri_turnir=kateri_turnir,
            up_ime=up_ime
        )
        try:
          self.repo.dodaj_prijavo_turnir(p)
          return True
        except:
          return False

    def dobi_prijave_turnir(self,kateri_turnir: str) -> prijave_turnir:
       prijave = self.repo.dobi_prijave_turnir(kateri_turnir)
       return prijave
    
    def dobi_prijave_turnir_oseba(self, kateri_turnir: str, up_ime : str) -> prijave_turnir:
       prijave_oseba = self.repo.dobi_prijave_turnir_oseba(kateri_turnir, up_ime)
       return prijave_oseba
    
    def sestej_prijave_turnir(self,kateri_turnir: str) -> prijave_turnir:
       st_prijavljenih = self.repo.sestej_prijave_turnir(kateri_turnir)[0]
       return st_prijavljenih
    
    def dodaj_tekmo(self, cas: str, miza: int, izid: str, ime_turnirja: str, sodnik_tekme: str, igralec1: str, igralec2: str) -> tekma:
        t = tekma(
          cas=cas,
          miza=miza,
          izid=izid,
          ime_turnirja=ime_turnirja,
          sodnik_tekme=sodnik_tekme,
          igralec1=igralec1,
          igralec2=igralec2 
        )
        try:
          self.repo.dodaj_tekmo(t)
          return True
        except:
          return False
        
    def dobi_tekmo(self) -> List[tekma]:
       tekme = self.repo.dobi_tekmo()
       return tekme
    
    def dobi_tekmo_turnir(self, ime_turnirja : str ) -> List[tekma]:
       tekme_turnir = self.repo.dobi_tekmo_turnir(ime_turnirja)
       return tekme_turnir
    
    def posodobi_izid_tekme(self, id_tekme, izid):
       nova_tekma = self.repo.posodobi_izid_tekme(id_tekme, izid)
       return nova_tekma