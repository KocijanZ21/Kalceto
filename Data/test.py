from repository import Repo
from models import *
from datetime import datetime, date, time
from datetime import timedelta

repo = Repo()

# Dobimo vse osebe
osebe = repo.dobi_prijave_turnir("End of summer tournament") 
#print(osebe)

en_turnir = repo.dobi_turnir_en("End of summer tournament")


datum_turnirja = [datum.datum_pricetka for datum in en_turnir]
print(datum_turnirja)


zelena_ura = time(10, 0)
cas_tekme = datetime.combine(datum_turnirja[0], zelena_ura)


tekma2 = repo.dobi_tekmo_turnir("End of summer tournament")











    
