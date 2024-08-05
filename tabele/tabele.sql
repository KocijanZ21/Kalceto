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
DROP TABLE IF EXISTS prijave_turnir;


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
    priimek TEXT NOT NULL,
    spol TEXT NOT NULL,
    drzava TEXT NOT NULL,
    email TEXT NOT NULL,
    rojstni_dan DATE NOT NULL DEFAULT now()
);

CREATE TABLE turnir(
    id_turnirja TEXT PRIMARY KEY,
    kraj TEXT NOT NULL,
    datum_pricetka DATE NOT NULL,
    datum_konca_prijav DATE NOT NULL,
    st_mest INTEGER NOT NULL,
    zmagovalec TEXT NOT NULL
);

CREATE TABLE prijave_turnir(
    kateri_turnir TEXT NOT NULL REFERENCES turnir(id_turnirja),
    up_ime TEXT NOT NULL REFERENCES uporabniki(username)
)

CREATE TABLE tekma (
    id_tekme SERIAL PRIMARY KEY,
    cas TIMESTAMP NOT NULL ,
    miza INTEGER NOT NULL ,
    izid TEXT NOT NULL,
    ime_turnirja TEXT NOT NULL REFERENCES turnir(id_turnirja),
    sodnik_tekme TEXT NOT NULL REFERENCES uporabniki(username),
    igralec1 TEXT NOT NULL REFERENCES uporabniki(username),
    igralec2 TEXT NOT NULL REFERENCES uporabniki(username),
    krog INTEGER NOT NULL
);
create table uporabniki (
    username TEXT PRIMARY KEY UNIQUE,
    role TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    last_login TEXT NOT NULL,
    emso TEXT NOT NULL
);
INSERT INTO turnir(id_turnirja, kraj, datum_pricetka, datum_konca_prijav, st_mest, zmagovalec) VALUES ('End of summer tournament', 'Ljubljana', '25.8.2024', '15.8.2024', '16', '');

INSERT INTO turnir(id_turnirja, kraj, datum_pricetka, datum_konca_prijav, st_mest, zmagovalec) VALUES ('End of winter tournament', 'Ljubljana', '25.12.2024', '15.12.2024', '16', '');

INSERT INTO turnir(id_turnirja, kraj, datum_pricetka, datum_konca_prijav, st_mest, zmagovalec) VALUES ('Fall tournament', 'Celje', '30.9.2024', '20.12.2024', '16', '');
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