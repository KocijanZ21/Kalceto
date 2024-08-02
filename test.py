import psycopg2

conn = psycopg2.connect("dbname=sem2024_vanjak host=baza.fmf.uni-lj.si user=javnost password=javnogeslo")
cur = conn.cursor()

# Preveri client_encoding
cur.execute("SHOW client_encoding;")
print(cur.fetchone())

# Vnesi šumnike in preveri, če deluje
cur.execute("INSERT INTO uporabniki(username, role, password_hash, last_login, emso) VALUES ('čšž', 'sodnik', 'vanja', '12', '23');")
conn.commit()

cur.execute("SELECT * FROM uporabniki;")
print(cur.fetchone())
