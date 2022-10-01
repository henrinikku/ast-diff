# Toteutusdokumentti

### Ohjelman rakenne

Korkealla tasolla algoritmin suoritus koostuu kahdesta vaiheesta:

1. Matchaavien solmujen löytäminen.
2. Edit scriptin generointi matchaavien solmujen perusteella.

Näitä vaiheita edustavat luokat Matcher ja EditScriptGenerator, ja vaiheiden suorituksesta vastaa Differ-luokka, joka ottaa parametreina luokkien Matcher ja EditScriptGenerator toteutukset.

TODO
