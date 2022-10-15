# Toteutusdokumentti

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

- [1] https://docs.python.org/3/library/ast.html
- [2] http://serg.aau.at/pub/MartinPinzger/Publications/Fluri2007-changedistiller.pdf
- [3] https://hal.archives-ouvertes.fr/hal-01054552/document
