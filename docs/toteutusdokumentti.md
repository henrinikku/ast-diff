# Toteutusdokumentti

## Algoritmin valinta

Syntaksipuiden diffausalgoritmit koostuvat käytännössä aina kahdesta vaiheesta: samankaltaisten nodejen etsimisestä ja erotuksen generoinnista löydettyjen samankaltaisuuksien perusteella. Ensimmäinen vaihe on hyvin haastava, eikä sen ratkaisemiseksi ole löydetty optimaalista järkevässä ajassa toimivaa algoritmia. Toinen vaihe on vähemmän haastava, ja Chawathen et al. kehittämä algoritmi [1] on todettu tähän tarkoitukseen optimaaliseksi tapauksessa, jossa halutaan huomioida solmujen lisäys-, poisto-, päivitys- ja siirto-operaatiot. Tästä syystä puiden erottelualgoritmien kehittäjät vaikuttavat keskittyvän lähinnä matchaysalgoritmien paranteluun.

Projektissa oli alunperin tarkoitus käyttää Change Distilling-algoritmia [2], jonka aikavaativuus on O(n^2 \* log(n^2)), eli hieman alle O(n^3). Change Distilling-algoritmi tekee kuitenkin merkittäviä oletuksia siitä, millainen käsiteltävä syntaksipuu on. Algoritmi aloittaa matchien eli samankaltaisten solmujen etsimisen puun lehdistä, joiden samankaltaisuuden tunnistaminen perustuu pitkälti niiden merkkijonomuotoisten arvojen samankaltaisuuteen. Siispä jos puun lehdillä ei ole kuvaavaa merkkijonomuotoista arvoa (kuten ei usein ole), menee niiden matchays pieleen ja ongelmat moninkertaistuvat, kun tasoa ylempien solmujen matchays perustuu aina niiden oksien samankaltaisuuteen.

Yllä mainitun ongelman takia päädyin lopulta toteuttamaan GumTree-algoritmin [3], jonka aikavaativuus on luokkaa O(n^2), eli se on Change Distilling-algoritmiin verrattuna paitsi vähemmän rajoittuneempi, myös huomattavasti nopeampi.

## Ohjelman rakenne

Korkealla tasolla ohjelman suoritus koostuu seuraavista vaiheista:

1. Syötteen parsiminen ja syntaksipuun muodostus.
2. Matchaavien solmujen löytäminen.
3. Edit scriptin generointi matchaavien solmujen perusteella.

Näistä vaiheista kaksi viimeistä toteuttavat erottelualgoritmin, jonka toteutuksesta vastaavat luokat Matcher ja EditScriptGenerator. Vaiheiden suorituksesta vastaa Differ-luokka, joka ottaa parametreina luokkien Matcher ja EditScriptGenerator toteutukset ja kutsuu niiden metodeja oikeassa järjestyksessä. Ajatuksena on, että ohjelmaa voisi halutessaan jatkaa lisäämällä siihen uusia toteutuksia eri vaiheille, joita voisi helposti yhdistellä ja vertailla.

### Syötteen parsiminen ja syntaksipuun muodostus

TODO

### Matchaavien solmujen löytäminen

TODO

### Edit scriptin generointi

TODO

## Aikavaativuus

TODO

## Parannusehdotukset

TODO

## Viitteet

- [1] https://dl.acm.org/doi/pdf/10.1145/235968.233366
- [2] http://serg.aau.at/pub/MartinPinzger/Publications/Fluri2007-changedistiller.pdf
- [3] https://hal.archives-ouvertes.fr/hal-01054552/document
- [4] https://docs.python.org/3/library/ast.html
