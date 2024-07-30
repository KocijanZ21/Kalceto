"""
V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.

"""
import os
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
from typing import List
#import auth_public as auth
import Data.auth_public as auth

from Data.models import igralec, sodnik, turnir, tekma, Uporabnik


# Preberemo port za bazo iz okoljskih spremenljivk
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)


class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def dobi_turnir(self) -> List[turnir]:
        self.cur.execute(""" 
            SELECT id_turnirja, kraj, datum_pricetka, st_mest, zmagovalec 
            FROM turnir
            Order by cas desc
        """)
        t = [turnir.from_dict(t) for t in self.cur.fetchall()]
        return t

    def dodaj_turnir(self, t : turnir):
        self.cur.execute("""
            INSERT into turnir(id_turnirja, kraj, datum_pricetka, st_mest, zmagovalec)
            VALUES(%s, %s, %s, %s, %s)
        """, (t.id_turnirja,t.kraj, t.datum_pricetka, t.st_mest, t.zmagovalec))
        self.conn.commit()
     
    def odstrani_turnir(self, id_turnirja : str):
        self.cur.execute("""
            DELETE from turnir
            WHERE id_turnirja = %s
        """, (id_turnirja,))
        self.conn.commit()
    
  
    def dodaj_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            INSERT into uporabniki(username, role, password_hash, last_login, oseba)
            VALUES (%s, %s, %s, %s, %s)
            """, (uporabnik.username,uporabnik.role, uporabnik.password_hash, uporabnik.last_login, uporabnik.oseba))
        self.conn.commit()


    def dobi_uporabnika(self, username:str) -> Uporabnik:
        self.cur.execute("""
            SELECT username, role, password_hash, last_login, oseba
            FROM uporabniki
            WHERE username = %s
        """, (username,))
         
        u = Uporabnik.from_dict(self.cur.fetchone())
        return u
    
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
            SELECT emso, ime, priimek, spol drzava, email, rojstni_dan FROM igralec
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
            SELECT emso, ime FROM sodnik
            WHERE emso = %s
        """, (emso,))

        s = sodnik.from_dict(self.cur.fetchone())
        return s
    
    def dodaj_sodnika(self, s : sodnik):
        self.cur.execute("""
            INSERT into sodnik(emso, ime, priimek)
            VALUES(%s, %s, %s)
        """, (s.emso, s.ime, s.priimek))
        self.conn.commit()
        
    def odstrani_sodnika(self, emso : str):
        self.cur.execute("""
            DELETE from sodnik
            WHERE emso = %s
        """, (emso,))
        self.conn.commit()
    
    def dobi_tekmo(self) -> List[tekma]:
        self.cur.execute("""
            SELECT id_tekme, cas, miza, izid, ime_turnirja, sodnik_tekme, igralec1, igralec2 
            FROM tekma
        """)
        te = [tekma.from_dict(t) for t in self.cur.fetchall()]
        return te
    
    def dobi_tekmo_turnir(self, ime_turnirja : str ) -> List[tekma]:
        self.cur.execute("""
            SELECT id_tekme, izid, ime_turnirja, sodnik_tekme, igralec1, igralec2
            FROM tekma
            WHERE ime_turnirja = %s
        """, (ime_turnirja,)) 
        ime = tekma.from_dict(self.cur.fetchone())
        return ime
    
    def dodaj_tekmo(self, tek : tekma):
        self.cur.execute("""
            INSERT into tekma(cas, miza, izid, ime_turnirja, sodnik_tekme, igralec1, igralec2 )
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        """, (tek.cas, tek.miza, tek.izid, tek.ime_turnirja, tek.sodnik_tekme, tek.igralec1, tek.igralec2))
        self.conn.commit()

    def odstrani_tekmo(self, id_tekme):
        self.cur.execute("""
            DELETE from tekma
            WHERE id = %s
        """, (id_tekme,))
        self.conn.commit()