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
    
    def sestej_prijave_turnir(self,kateri_turnir: str) -> prijave_turnir:
       st_prijavljenih = self.repo.sestej_prijave_turnir(kateri_turnir)[0]
       return st_prijavljenih