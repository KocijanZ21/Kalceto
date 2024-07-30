"""
V tej datoteki definiramo vse podatkovne modele, ki jih bomo uporabljali v aplikaciji

"""

from datetime import date
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

# Pazi na vrstni red anotacij razredov!

@dataclass_json
@dataclass
class igralec:
    emso : str = field(default="")
    ime : str = field(default="")
    priimek : str = field(default="")
    spol : str = field(default="")
    drzava : str = field(default="")
    email : str = field(default="")
    rojstni_dan : str = field(default="")
    
@dataclass_json
@dataclass
class igralecDto:
    emso : str = field(default="")
    ime : str = field(default="")
    priimek : str = field(default="")
    spol : str = field(default="")
    drzava : str = field(default="")
    email : str = field(default="")
    rojstni_dan : str = field(default="")
    izid : str = field(default=0)

@dataclass_json
@dataclass
class sodnik:
    emso : str = field(default="")  
    ime : str = field(default="")
    priimek : str = field(default="")
   
@dataclass_json
@dataclass
class turnir:    
    id_turnirja : str = field(default="")
    kraj : str = field(default="")
    datum_pricetka : date=field(default=date.today())
    st_mest : int = field(default=0)
    zmagovalec : str = field(default="")

@dataclass_json
@dataclass
class tekma:    
    id_tekme : int = field(default=0)
    cas : str=field(default="")
    miza : int = field(default=0)
    izid : str = field(default=0)
    ime_turnirja : str = field(default=0)
    sodnik_tekme : str=field(default="")
    igralec1 : str=field(default="")
    igralec2 : str=field(default="")

@dataclass_json
@dataclass
class Uporabnik:
    username: str = field(default="")
    role: str = field(default="")
    password_hash: str = field(default="")
    last_login: str = field(default="")
    oseba : str = field(default="")
    
@dataclass_json
@dataclass
class UporabnikDto:
    username: str = field(default="")
    role: str = field(default="")
    oseba: str = field(default="")