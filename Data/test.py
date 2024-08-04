from repository import Repo
from models import *


repo = Repo()

# Dobimo vse osebe
osebe = repo.dobi_prijave_turnir("End of summer tournament") 
#print(osebe)

up_ime_list = [oseba.up_ime for oseba in osebe]

#print(up_ime_list)

turn= repo.dobi_turnir()
#print(turn)

datum_list = [turnir1.datum_konca_prijav for turnir1 in turn]

#print(datum_list)

sodniki = repo.dobi_vse_sodnike()

emso_sodnikov = [sodni.emso for sodni in sodniki]

#print(emso_sodnikov)

sodniki_up = []
for st in emso_sodnikov:
    sodnik1 = repo.dobi_uporabnika_emso(st)
    sodniki_up.append(sodnik1)
sodniki_up    

up_ime_sodniki = [up_imena.username for up_imena in sodniki_up]

from datetime import datetime
from datetime import timedelta
import random
cas_tekme =  datetime.now()
new_time = cas_tekme.replace(hour=10, minute=0, second=0)
new_time += timedelta(minutes=30)
sodnik1 = random.choice(up_ime_sodniki) 
print(sodnik1)



    
