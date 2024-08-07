# Kalceto

Aplikacija je namenjena vsem navdušenim igralcem namiznega nogometa. Prvi korak k uporabi aplikacije je registracija. Uporabnik se na začetku registrira kot igralec ali kot sodnik. V primeru, da se prijavi kot igralec si v nadaljevanju lahko izbere prihajajoči turnir. Ko so zapolnjena vsa mesta, se naredi naključni izbor dvojic. V aplikaciji lahko potem vsak prijavljeni igralec pogleda razpored tekem, časovnico in kraj tekme, na kateri mizi bo igral, kdo bo sodnik in kdo bo njegov nasprotnik. Po koncu tekme sodnik vpiše izid. Po zaključku prvega kroga program oblikuje nove dvojice. 

**KRATKA NAVODILA ZA UPORABO**

Uporabnik na začetku izbere ali želi na turnirjih sodelovati kot sodnik ali kot igralec. Glede na izbiro se potem vpogled v spletno stran nekoliko loči. 

**SODNIK**

Ko se oseba registrira kot sodnik, se njegovi podatki shranijo v bazo. Tako kot igralci imajo možnost pregleda nad turnirji in tekmami. Če se na turnir prijavi dovolj igralcev, se naredijo tekme, iz baze pa se naključno izbere enega sodnika za vsako tekmo. Vsi sodniki imajo ob vpogledu tekem na voljo tudi vpis zmagovalca. Po koncu tekme sodnik izbere ime zmagovalca in pritisne gumb shrani. Ko vsi sodniki vpišejo zmagovalce tekem prvega kroga se na dnu pojavi gumb 'Začni nov krog', ko se pritisne gumb se generirajo nove tekme in začne se drugi krog turnirja. Ko se odigra zadnja tekma, bo gumb 'Začni nov krog' ostal na dnu strani, vendar ta ne bo generiral novih tekem, ampak bo uporabnika preusmeril na stran, kjer si bo lahko ogledal zmagovalca turnirja. 

**IGRALEC**

Ko se oseba registrira kot igralec, se tudi njegovi podatki shranijo v bazo. Potem ko se prijavi, pride na domačo stran, kjer so zapisani vsi njegovi podatki. Tam lahko pod zavihkom turnirji pregleda vse razpisane turnirje in se na njih tudi prijavi, če so prijave še odprte. Rok za prijavo je do 10 dni pred začetkom turnirja. Ob preteku roka ali zapolnjenemu turnirju se pojavi sporočilo, da so prijave zaprte. Ko je število mest polno, se generirajo tekme. Tam so objavljeni vsi potrebni podatki, torej kdaj je tekma, katera miza, ime sodnika, imena igralcev in po koncu tekme tudi zmagovalec. Igralec za razliko od sodnika vidi samo razpisane tekme, torej ne more vpisati izida ali začeti novega kroga. Na strani kjer so razpisane tekme je zgoraj desno tudi zavihek zmagovalec, ki igralca pelje na stran kjer so razpisani turnirji in lahko pogleda ali je ta že znan. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KocijanZ21/Kalceto.git/main?urlpath=proxy%2F8080)

![alt text](https://github.com/KocijanZ21/Kalceto/blob/main/diagram.png?raw=true)
