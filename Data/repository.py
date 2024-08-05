"""
V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.

"""
import os
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
from typing import List
#import auth_public as auth
import Data.auth_public as auth

from Data.models import igralec, sodnik, turnir, prijave_turnir, tekma, Uporabnik


# Preberemo port za bazo iz okoljskih spremenljivk
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)


class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def dobi_turnir(self) -> List[turnir]:
        self.cur.execute(""" 
            SELECT id_turnirja, kraj, datum_pricetka, datum_konca_prijav, st_mest, zmagovalec 
            FROM turnir
        """)
        t = [turnir.from_dict(t) for t in self.cur.fetchall()]
        return t
    
    def dobi_turnir_en(self, id_turnirja: str) -> List[turnir]:
        self.cur.execute(""" 
            SELECT id_turnirja, kraj, datum_pricetka, datum_konca_prijav, st_mest, zmagovalec 
            FROM turnir
            Where id_turnirja = %s
        """, (id_turnirja,))
        t_en = [turnir.from_dict(t_en) for t_en in self.cur.fetchall()]
        return t_en
    
    def posodobi_zmagovalca_turnirja(self, id_turnirja, zmagovalec):
        self.cur.execute("""
            UPDATE turnir
            SET zmagovalec = %s
            WHERE id_turnirja = %s
        """, (zmagovalec, id_turnirja))
        self.conn.commit()


    def dodaj_turnir(self, t : turnir):
        self.cur.execute("""
            INSERT into turnir(id_turnirja, kraj, datum_pricetka, datum_konca_prijav, st_mest, zmagovalec)
            VALUES(%s, %s, %s, %s, %s, %s)
        """, (t.id_turnirja,t.kraj, t.datum_pricetka,t.datum_konca_prijav, t.st_mest, t.zmagovalec))
        self.conn.commit()
     
    def odstrani_turnir(self, id_turnirja : str):
        self.cur.execute("""
            DELETE from turnir
            WHERE id_turnirja = %s
        """, (id_turnirja,))
        self.conn.commit()
    
    def dobi_prijave_turnir(self, kateri_turnir: str) -> prijave_turnir:
        self.cur.execute(""" 
            SELECT kateri_turnir, up_ime
            FROM prijave_turnir
            WHERE kateri_turnir = %s
        """,(kateri_turnir,))
        pri = [prijave_turnir.from_dict(pri) for pri in self.cur.fetchall()]
        return pri
    
    
    def dobi_prijave_turnir_oseba(self, kateri_turnir: str, up_ime : str) -> prijave_turnir:
        self.cur.execute(""" 
            SELECT kateri_turnir, up_ime
            FROM prijave_turnir
            WHERE kateri_turnir = %s and up_ime = %s
        """,(kateri_turnir, up_ime,))
        pri = [prijave_turnir.from_dict(pri) for pri in self.cur.fetchall()]
        return pri
    
    def sestej_prijave_turnir(self, kateri_turnir: str ) -> prijave_turnir:
        self.cur.execute("""
            SELECT COUNT(up_ime)
            FROM prijave_turnir
            WHERE kateri_turnir = %s
            """, (kateri_turnir,))
        return self.cur.fetchone()
    
    def dodaj_prijavo_turnir(self, p : prijave_turnir):
        self.cur.execute("""
            INSERT into prijave_turnir(kateri_turnir, up_ime)
            VALUES(%s, %s)
        """, (p.kateri_turnir, p.up_ime))
        self.conn.commit()

    def odstrani_prijavo_turnir(self, up_ime : str):
        self.cur.execute("""
            DELETE from prijave_turnir
            WHERE up_ime = %s
        """, (up_ime,))
        self.conn.commit()
  
    def dodaj_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            INSERT into uporabniki(username, role, password_hash, last_login, emso)
            VALUES (%s, %s, %s, %s, %s)
            """, (uporabnik.username,uporabnik.role, uporabnik.password_hash, uporabnik.last_login, uporabnik.emso))
        self.conn.commit()


    def dobi_uporabnika(self, username:str) -> Uporabnik:
        self.cur.execute("""
            SELECT username, role, password_hash, last_login, emso
            FROM uporabniki
            WHERE username = %s
        """, (username,))
         
        u = Uporabnik.from_dict(self.cur.fetchone())
        return u 
    
    def dobi_uporabnika_emso(self, emso:str) -> Uporabnik:
        self.cur.execute("""
            SELECT username
            FROM uporabniki
            WHERE emso = %s
        """, (emso,))
         
        up = Uporabnik.from_dict(self.cur.fetchone())
        return up 
    
    def posodobi_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            Update uporabniki set last_login = %s where username = %s
            """, (uporabnik.last_login,uporabnik.username))
        self.conn.commit()

    
    def dodaj_igralca(self, ig : igralec):
        self.cur.execute("""
            INSERT into igralec(emso, ime, priimek, spol, drzava, email, rojstni_dan)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        """, (ig.emso, ig.ime, ig.priimek, ig.spol, ig.drzava, ig.email, ig.rojstni_dan))
        self.conn.commit()

    def dobi_igralca(self, emso : str) -> igralec:
        self.cur.execute("""
            SELECT emso, ime, priimek, spol, drzava, email, rojstni_dan FROM igralec
            WHERE emso = %s
        """, (emso,))

        ig = igralec.from_dict(self.cur.fetchone())
        return ig
    
    def odstrani_igralca(self, emso : str):
        self.cur.execute("""
            DELETE from igralec
            WHERE emso = %s
        """, (emso,))
        self.conn.commit()

    def dobi_sodnika(self, emso : str) -> sodnik:
        self.cur.execute("""
            SELECT emso, ime, priimek, spol, drzava, email, rojstni_dan FROM sodnik
            WHERE emso = %s
        """, (emso,))

        s = sodnik.from_dict(self.cur.fetchone())
        return s
    
    def dobi_vse_sodnike(self) -> List[sodnik]:
        self.cur.execute("""
            SELECT emso, ime, priimek, spol, drzava, email, rojstni_dan FROM sodnik
        """)

        sod = [sodnik.from_dict(sod) for sod in self.cur.fetchall()]
        return sod
    
    def dodaj_sodnika(self, s : sodnik):
        self.cur.execute("""
            INSERT into sodnik(emso, ime, priimek, spol, drzava, email, rojstni_dan)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        """, (s.emso, s.ime, s.priimek, s.spol, s.drzava, s.email, s.rojstni_dan))
        self.conn.commit()
        
    def odstrani_sodnika(self, emso : str):
        self.cur.execute("""
            DELETE from sodnik
            WHERE emso = %s
        """, (emso,))
        self.conn.commit()
    
    def dobi_tekmo(self) -> List[tekma]:
        self.cur.execute("""
            SELECT id_tekme, cas, miza, izid, ime_turnirja, sodnik_tekme, igralec1, igralec2, krog
            FROM tekma
        """)
        te = [tekma.from_dict(t) for t in self.cur.fetchall()]
        return te
    
    def dobi_tekmo_turnir(self, ime_turnirja : str ) -> List[tekma]:
        self.cur.execute("""
            SELECT id_tekme, cas, miza, izid, ime_turnirja, sodnik_tekme, igralec1, igralec2, krog
            FROM tekma
            WHERE ime_turnirja = %s
        """, (ime_turnirja,)) 
        ime = [tekma.from_dict(ime) for ime in self.cur.fetchall()]
        return ime
    
    def dobi_tekmo_krog(self, krog : int ) -> List[tekma]:
        self.cur.execute("""
            SELECT id_tekme, cas, miza, izid, ime_turnirja, sodnik_tekme, igralec1, igralec2, krog
            FROM tekma
            WHERE krog = %s
        """, (krog,)) 
        ime_krog = [tekma.from_dict(ime_krog) for ime_krog in self.cur.fetchall()]
        return ime_krog
    
    def dodaj_tekmo(self, tek : tekma):
        self.cur.execute("""
            INSERT into tekma(cas, miza, izid, ime_turnirja, sodnik_tekme, igralec1, igralec2, krog )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """, (tek.cas, tek.miza, tek.izid, tek.ime_turnirja, tek.sodnik_tekme, tek.igralec1, tek.igralec2, tek.krog))
        self.conn.commit()

    def odstrani_tekmo(self, id_tekme):
        self.cur.execute("""
            DELETE from tekma
            WHERE id = %s
        """, (id_tekme,))
        self.conn.commit()

    def posodobi_izid_tekme(self, id_tekme, izid):
        self.cur.execute("""
            UPDATE tekma
            SET izid = %s
            WHERE id_tekme = %s
        """, (izid, id_tekme))
        self.conn.commit()

    def dobi_trenutni_krog(self, ime_turnirja):
        self.cur.execute("""
            SELECT  krog
            FROM tekma
            WHERE ime_turnirja = %s
            Order by cas desc
        """, (ime_turnirja,)) 
        zadnji = [tekma.from_dict(zadnji) for zadnji in self.cur.fetchall()]
        trenutni_krog= [kr.krog for kr in zadnji]
        return trenutni_krog[0]
    
    def dobi_zmagovalci(self, ime_turnirja, krog):
        self.cur.execute("""
            SELECT izid 
            FROM tekma
            WHERE ime_turnirja = %s AND krog = %s
        """, (ime_turnirja,krog,)) 
        zmag = [tekma.from_dict(zmag) for zmag in self.cur.fetchall()]
        return zmag
    
    def ali_so_vsi_zmagovalci_vpisani(self, ime_turnirja, krog):
        self.cur.execute("""
            SELECT COUNT(izid) 
            FROM tekma
            WHERE ime_turnirja = %s AND krog = %s AND izid = ''
        """, (ime_turnirja,krog,)) 
        stevilo = self.cur.fetchone()
        return stevilo[0]





       
    
      
    
