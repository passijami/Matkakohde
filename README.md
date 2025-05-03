# Matkakohde

## Lopullinen sovellus (11.5.2025)
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen suosittelemiaan matkakohteita (kaupunkeja, maita tai muita kohteita). Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään matkakohteita sekä lisäämään kuvia.
- Käyttäjä näkee sovellukseen lisätyt matkakohteet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät suositukset.
- Käyttäjä pystyy etsimään eri matkakohteita hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä kohteita.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja omat suositukset sekä käyttäjän lisäämät matkakohteet.
- Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (kohde, sijainti ja arvostelu).
- Käyttäjä pystyy lisäämään muiden käyttäjien matkakohteita omalle "suosikit" -listalle. Nämä näkyvät käyttäjien profiilissa.
- Tietoturvallisuus on kunnossa ja vaadittavalla tasolla.

## Käynnistysohjeet

- Asenna flask

```
$ pip install flask
```

- Luo taulut tietokantaan

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

- Käynnistä sovellus

```
$ flask run
```
