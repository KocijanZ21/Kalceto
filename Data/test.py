from repository import Repo
from models import *
from datetime import datetime, date, time
from datetime import timedelta

repo = Repo()

# Dobimo vse osebe
osebe = repo.dobi_prijave_turnir("End of summer tournament") 
#print(osebe)

prejsni_datum = repo.dobi_tekmo_turnir('End of summer tournament')




tekma2 = repo.dobi_tekmo_turnir("End of summer tournament")


zmagovalci = [zmag.izid for zmag in tekma2]
#ali = all(row[1] != '' for row in zmagovalci)


krog1 = 2

ali = repo.ali_so_vsi_zmagovalci_vpisani("End of summer tournament", krog1)
print(ali)
tekma_krog = repo.dobi_tekmo_krog(krog1)

zmagovalec = repo.dobi_zmagovalca_turnirja("End of summer tournament")
print(zmagovalec)














    
