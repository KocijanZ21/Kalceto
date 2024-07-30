-- Active: 1708602955354@@baza.fmf.uni-lj.si@5432@sem2024_vanjak@public
GRANT ALL ON DATABASE sem2024_vanjak TO zivak WITH GRANT OPTION;
GRANT ALL ON DATABASE sem2024_vanjak TO zivak WITH GRANT OPTION;

GRANT ALL ON SCHEMA public TO zivak;
GRANT ALL ON SCHEMA public TO zivak;

GRANT CONNECT ON DATABASE sem2024_vanjak TO javnost;
GRANT USAGE ON SCHEMA public to javnost;

DROP TABLE IF EXISTS uporabniki;
DROP TABLE IF EXISTS igralec;
DROP TABLE IF EXISTS sodnik;
DROP TABLE IF EXISTS turnir;
DROP TABLE IF EXISTS tekma;

CREATE TABLE igralec (
    emso TEXT PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,
    spol TEXT NOT NULL,
    drzava TEXT NOT NULL,
    email TEXT NOT NULL,
    rojstni_dan DATE NOT NULL DEFAULT now()
);
CREATE TABLE sodnik (
    emso TEXT PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL
);

CREATE TABLE turnir(
    id_turnirja TEXT PRIMARY KEY,
    kraj TEXT NOT NULL,
    datum_pricetka DATE NOT NULL,
    st_mest INTEGER NOT NULL,
    zmagovalec TEXT NOT NULL
);

CREATE TABLE tekma (
    id_tekme SERIAL PRIMARY KEY,
    cas TIMESTAMP NOT NULL ,
    miza INTEGER NOT NULL ,
    izid TEXT NOT NULL,
    ime_turnirja INTEGER NOT NULL,
    sodnik_tekme TEXT NOT NULL REFERENCES sodnik(emso),
    igralec1 TEXT NOT NULL REFERENCES igralec(emso),
    igralec2 TEXT NOT NULL REFERENCES igralec(emso),
    CHECK (igralec1 <> igralec2)
);
create table uporabniki (
    username TEXT PRIMARY KEY,
    role TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    last_login TEXT NOT NULL,
    oseba TEXT NOT NULL
);

GRANT ALL ON ALL TABLES IN SCHEMA public TO zivak;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO zivak;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;
GRANT UPDATE ON ALL TABLES IN SCHEMA public TO javnost;
GRANT DELETE ON ALL TABLES IN SCHEMA public TO javnost;
GRANT INSERT ON ALL TABLES IN SCHEMA public TO javnost;

GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO javnost;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO javnost;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO javnost;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO javnost;