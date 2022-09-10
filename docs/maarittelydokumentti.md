# Määrittelydokumentti

## Ohjelmointikieli

Teen projektin Pythonilla. Voin vertaisarvioida Pythonilla, Javalla, C++:lla, C#:lla sekä JS/TS:lla tehtyjä projekteja.

## Ongelma

Tavoitteenani on luoda ohjelma, joka ottaa syötteenä kaksi Python-tiedostoa ja löytää niiden väliset rakenteelliset erot. Esimerkiksi poikkeavat muuttujat ja luokkamäärittelyt ovat rakenteellisia eroja, mutta ylimääräiset sulkeet ja rivinvaihdot eivät ole.

Ideaalitilanteessa ohjelma esittäisi eroavaisuudet nätisti esimerkiksi värikoodaamalla poistetut, lisätyt ja muokatut kohdat. Jos tällaisen tulostuksen toteutukseen ei jää aikaa, minimivaatimuksena ohjelma tulostaa ns. edit scriptin, eli listan muutoksista (Add, Update, Remove, Move), joilla ensimmäistä tiedostoa kuvaava syntaksipuu saadaan vastaamaan toista tiedostoa kuvaavaa syntaksipuuta.

## Tietorakenteet ja algoritmit

Keskeisin tietorakenne, jota vasten operoidaan läpi ohjelman suorituksen on Pythonin syntaksia kuvaava abstrakti syntaksipuu (AST) [1]. Käytän Pythonin AST-oletuskirjastoa annettujen tiedostojen parsimiseen. En siis keskity tässä projektissa Python-kieliopin parsimiseen, vaan tuloksena syntyvien puiden välisten eroavaisuuksien löytämiseen.

Aion toteuttaa Change Distilling-algoritmin [2] syntaksipuiden eroavuuksien löytämiseen. Syy valintaan on, että se vaikuttaa olevan yksi tunnetuimmista tähän tarkoitukseen sopivista algoritmeista, minkä takia siihen liittyviä resursseja on saatavilla kohtuullisesti. Se on käsittääkseni myös suhteellisen tehokas ja vaikuttaa haastavuudeltaan tälle kurssille sopivalta. Mainittakoon vielä, että vaikka algoritmi pyrkii löytämään mahdollisimman pienen edit scriptin, ei ole takeita siitä että tuloksena syntyvä edit script on pienin mahdollinen.

Syntaksipuiden lisäksi toteutukseen tarvitaan varmasti ainakin hajautustauluja ja listoja, sekä mahdollisesti myös kekoja. En ole vielä lukenut Change Distilling-paperia ajatuksella alusta loppuun, joten en ole varma toteutuksen yksityiskohdista.

## Laskennallinen vaativuus

Ongelma on laskennallisesti haastava. Change Distilling-algoritmin aikavaativuus on O(n^2 \* log(n^2)), missä n on puiden solmujen lukumäärä. On siis selvää, että algoritmi ei sovellu todella suurten tiedostojen rakenteelliseen vertailuun. Mikäli algoritmi osoittautuu epäsopivaksi käyttötarkoitukseen, käytän sen tilalla jotain muuta vastaavaa algoritmia, jonka aikavaativuus on korkeintaan O(n^3).

Jostain syystä Change-Distilling paperissa ei käsitellä algoritmin tilavaativuutta juurikaan. Asetan siis tavoittelemakseni tilavaativuudeksi saman O(n^2 \* log(n^2)). Todennäköisesti kuitenkin vähemmällä selvitään.

## Opinto-ohjelma

Tietojenkäsittelytieteen kandidaatti (TKT).

## Kieli

Teen muut tarvittavat dokumentaatiot ja ohjelmakoodin englanniksi.

## Viitteet

- [1] https://docs.python.org/3/library/ast.html
- [2] http://serg.aau.at/pub/MartinPinzger/Publications/Fluri2007-changedistiller.pdf
