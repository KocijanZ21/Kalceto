from Data.repository import Repo
from Data.models import *
from typing import List
from datetime import datetime, date, time
from datetime import timedelta
import random


# V tej datoteki bomo definirali razred za obdelavo in delo s turnirji in tekmami

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
    
    def posodobi_zmagovalca_turnirja(self, id_turnirja, zmagovalec):
       nova_turnir = self.repo.posodobi_zmagovalca_turnirja(id_turnirja, zmagovalec)
       return nova_turnir
    
    
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
    
    def dodaj_tekmo(self, cas: str, miza: int, izid: str, ime_turnirja: str, sodnik_tekme: str, igralec1: str, igralec2: str, krog: int) -> tekma:
        t = tekma(
          cas=cas,
          miza=miza,
          izid=izid,
          ime_turnirja=ime_turnirja,
          sodnik_tekme=sodnik_tekme,
          igralec1=igralec1,
          igralec2=igralec2, 
          krog = krog
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
    
    def dobi_trenutni_krog(self, ime_turnirja):
       trenutni_krog = self.repo.dobi_trenutni_krog(ime_turnirja)
       return trenutni_krog
    
    def dobi_zmagovalci(self, ime_turnirja, krog):
      zmag = self.repo.dobi_zmagovalci(ime_turnirja, krog)
      return zmag
    
    def ustvari_nov_krog(self, zmagovalci, ime_turnirja, datum, nov_krog, sodniki_up_ime):
      nov_datum = datum + timedelta(days=1)
      zeljena_ura = time(10, 0)
      nov_cas = datetime.combine(nov_datum, zeljena_ura)
      miza = 1
      izid = ''

      random.shuffle(zmagovalci)

      while len(zmagovalci) > 1:
          igralec1 = zmagovalci.pop()
          igralec2 = zmagovalci.pop()
          sodnik_tekme = random.choice(sodniki_up_ime)  

          t = tekma(
          cas=nov_cas,
          miza=miza,
          izid=izid,
          ime_turnirja=ime_turnirja,
          sodnik_tekme=sodnik_tekme,
          igralec1=igralec1,
          igralec2=igralec2, 
          krog = nov_krog
        )

          self.repo.dodaj_tekmo(t)

          nov_cas += timedelta(hours=1)
      return self.repo.dobi_tekmo_turnir(ime_turnirja)
    
    def ali_so_vsi_zmagovalci_vpisani(self, ime_turnirja, krog):
       stevilo1 = self.repo.ali_so_vsi_zmagovalci_vpisani(ime_turnirja, krog)
       return stevilo1
    
    def dobi_tekmo_krog(self, ime_turnirja: str, krog : int ):
       tekma = self.repo.dobi_tekmo_krog(ime_turnirja, krog)
       tekmacas = [cas_tekme.cas for cas_tekme in tekma]
       tekma_cas = tekmacas[0]
       return tekma_cas
    
    def dobi_tekmo_krog_je(self, ime_turnirja: str, krog: int):
     tekme = self.repo.dobi_tekmo_krog( ime_turnirja, krog)
     return tekme
    
    def ali_tekmo_krog_je(self, ime_turnirja: str, krog: int):
      if self.repo.dobi_tekmo_krog(ime_turnirja, krog):
         return True
      else:
         return False
      
   
         
        
   
       

        