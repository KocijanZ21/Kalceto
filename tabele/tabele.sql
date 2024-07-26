-- Active: 1708602955354@@baza.fmf.uni-lj.si@5432@sem2024_vanjak@public
GRANT ALL ON DATABASE sem2024_vanjak TO zivak WITH GRANT OPTION;
GRANT ALL ON DATABASE sem2024_vanjak TO zivak WITH GRANT OPTION;

GRANT ALL ON SCHEMA public TO zivak;
GRANT ALL ON SCHEMA public TO zivak;

GRANT CONNECT ON DATABASE sem2024_vanjak TO javnost;
GRANT USAGE ON SCHEMA public to javnost;

DROP TABLE IF EXISTS oseba;
DROP TABLE IF EXISTS igralec;
DROP TABLE IF EXISTS sodnik;
DROP TABLE IF EXISTS turnir;
DROP TABLE IF EXISTS tekma;

DROP TABLE IF EXISTS zaposlen;

CREATE TABLE oseba (
    emso TEXT PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,
    telefon TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    geslo TEXT NOT NULL UNIQUE
);

CREATE TABLE igralec (
    spol TEXT NOT NULL,
    drzava TEXT NOT NULL,
    rojstni_dan DATE NOT NULL DEFAULT now(),
    emso TEXT NOT NULL REFERENCES oseba(emso) PRIMARY KEY
);
CREATE TABLE sodnik (
    emso TEXT NOT NULL REFERENCES oseba(emso) PRIMARY KEY
);

CREATE TABLE turnir(
    id_turnirja SERIAL PRIMARY KEY,
    kraj TEXT NOT NULL,
    datum_pricetka DATE NOT NULL,
    st_mest INTEGER NOT NULL
);

CREATE TABLE tekma (
    id_tekme SERIAL PRIMARY KEY,
    cas TIMESTAMP NOT NULL,
    miza INTEGER NOT NULL,
    izid INTEGER NOT NULL,
    ime_turnirja INTEGER NOT NULL REFERENCES turnir(id_turnirja),
    sodnik TEXT NOT NULL REFERENCES sodnik(emso),
    igralec1 TEXT NOT NULL REFERENCES igralec(emso),
    igralec2 TEXT NOT NULL REFERENCES igralec(emso),
    CHECK (igralec1 <> igralec2)
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