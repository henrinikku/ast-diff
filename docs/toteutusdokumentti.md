# Toteutusdokumentti

## Ohjelman toiminta

Ohjelman toiminnallisuus on yksinkertainen. Ohjelma tarjoaa yhden komennon, joka ottaa vastaan kaksi Python-tiedostoa tai -koodinpätkää ja tulostaa niiden erotuksen ns. edit scriptinä, eli listana operaatioita, joilla ensimmäistä tiedostoa kuvaavan syntaksipuun saa muutettua toista tiedostoa kuvaavaksi syntaksipuuksi.

## Algoritmin valinta

Syntaksipuiden diffausalgoritmit koostuvat usein kahdesta vaiheesta: samankaltaisten nodejen etsimisestä ja erotuksen generoinnista löydettyjen samankaltaisuuksien perusteella. Ensimmäinen vaihe on laskennallisesti haastava, eikä sen ratkaisemiseksi ole löydetty optimaalista järkevässä ajassa toimivaa algoritmia. Toinen vaihe on vähemmän haastava, ja Chawathen et al. kehittämä algoritmi [1] on todettu tähän tarkoitukseen optimaaliseksi, kun halutaan huomioida solmujen lisäys-, poisto-, päivitys- ja siirto-operaatiot. Tästä syystä puiden erottelualgoritmien kehittäjät vaikuttavat keskittyvän lähinnä matchaysalgoritmien paranteluun.

Projektissa oli alunperin tarkoitus käyttää Change Distilling-algoritmia [2], jonka aikavaativuus on O(n^2 \* log(n^2)), eli hieman alle O(n^3). Change Distilling-algoritmi tekee kuitenkin merkittäviä oletuksia siitä, millainen käsiteltävä syntaksipuu on. Algoritmi aloittaa matchien eli samankaltaisten solmujen etsimisen puun lehdistä, joiden samankaltaisuuden tunnistaminen perustuu pitkälti niiden merkkijonomuotoisten arvojen samankaltaisuuteen. Siispä jos puun lehdillä ei ole kuvaavaa merkkijonomuotoista arvoa (kuten ei usein ole), menee niiden matchays pieleen ja ongelmat moninkertaistuvat, kun tasoa ylempien solmujen matchays perustuu aina niiden lapsisolmujen samankaltaisuuteen.

Yllä mainitun ongelman takia päädyin lopulta toteuttamaan GumTree-algoritmin [3], jonka aikavaativuus on luokkaa O(n^2), eli se on Change Distilling-algoritmiin verrattuna paitsi vähemmän rajoittunut, myös huomattavasti nopeampi.

## Ohjelman rakenne

Korkealla tasolla ohjelman suoritus koostuu seuraavista vaiheista:

1. Syötteen parsiminen ja syntaksipuun muodostus.
2. Matchaavien solmujen löytäminen.
3. Edit scriptin generointi matchaavien solmujen perusteella.

Näistä vaiheista kaksi viimeistä toteuttavat itse erottelualgoritmin. Vaiheiden suorituksesta vastaa Differ-luokka, joka ottaa parametreina luokkien Matcher ja EditScriptGenerator toteutukset ja kutsuu niiden metodeja oikeassa järjestyksessä. Ajatuksena on, että ohjelmaa voisi halutessaan jatkaa lisäämällä siihen uusia toteutuksia eri vaiheille, joita voisi helposti yhdistellä ja vertailla. Ohjelmaa voisi myös helposti laajentaa tukemaan muitakin kieliä kuin Pythonia lisäämällä uusia `Parser`-toteutuksia.

### Syötteen parsiminen ja syntaksipuun muodostus

Syötteen parsimisen toteuttavat luokat perivät [`Parser`](../astdiff/parser/base.py)-luokan ja toteuttavat metodit syötteen parsimiseksi haluttuun muotoon (ks. [`Node`](../astdiff/ast/node.py)-luokka) jonkin ulkopuolisen kirjaston avulla. Tällä hetkellä käyttäjän on mahdollista valita parso-kirjaston ja Pythonin oletus AST-kirjaston väliltä.

Tämä vaihe on ohjelman toimivuuden kannalta pakollinen, mutta en toteuttanut parsimista itse (eikä se ollut alunperinkään tarkoitus), joten en huomioi parsimisen aikavaativuutta ohjelman aikavaativuusanalyysissa. Suorituskykytestauksen yhteydessä kävi kuitenkin ilmi, että parsimiseen kuluu merkittävä osuus ohjelman kokonaissuoritusajasta. Syötteistä riippuen parsinta vie tyypillisesti joko eniten tai toisiksi eniten suoritusaikaa.

### Matchaavien solmujen löytäminen

Solmujen matchayksen toteuttavat luokat perivät [`Matcher`](../astdiff/matcher/base.py)-luokan ja toteuttavat metodin matchaavien solmujen joukon löytämiseksi. Tällä hetkellä käyttäjän on mahdollista valita kolmen eri toteutuksen väliltä:

1. [`gumtree`](../astdiff/matcher/gumtree.py) (oletus)
2. [`stub`](../astdiff/matcher/base.py) (ei matchaa mitään nodeja)
3. [`change-distiller`](../astdiff/matcher/base.py) (ei toteutettu ja heittää virheen, jätin esimerkiksi siitä miten ohjelmaa voisi helposti laajentaa)

`GumTreeMatcher`-luokan toteuttaman algoritmin aikavaativuus on luokkaa O(n^2). Kuten GumTree-paperin [3] kohdassa 3.3 sanotaan, algoritmi käy pahimmassa tapauksessa läpi useamman solmun karteesisen tulon pariin kertaan, ja karteesisen tulon "sisällä" suoritettavien kalliimpien operaatioiden suorituksen vaativuutta on rajoitettu vakiomuuttujilla ja tulosten uudelleenkäytöllä.

### Edit scriptin generointi

Edit scriptin generoinnin toteuttavat luokat perivät [`EditScriptGenerator`](../astdiff/generator/base.py)-luokan ja toteuttavat metodin erotuksen generoimiseksi ennalta lasketun matchaavien solmujen joukon perusteella. Tällä hetkellä toteutettuna on Chawathen vuonna 1996 kehittämä algoritmi [1] ([`WithMoveEditScriptGenerator`](../astdiff/generator/with_move.py)), jonka käyttöä myös GumTree-paperissa [3] suositellaan.

Algoritmin aikavaativuus on luokkaa O(n^2), mikä johtuu jälleen siitä, että algoritmi käy pahimmassa tapauksessa läpi alipuiden karteesisen tulon. Sama aikavaativuus tuodaan ilmi sekä GumTree-paperissa että Chawathen alkuperäisessä paperissa.

## Aikavaativuus

Algoritmin kummankin vaiheen aikavaativuus on luokkaa O(n^2), joten algoritmin aikavaativuus on sama.

## Parannusehdotukset

Jos ohjelmaa haluaisi jatkaa, ilmeinen seuraava askel olisi toteuttaa jokin tekstimuotoinen tai graafinen esitystapa löydetyille eroille. Edit scriptin koko kasvaa nopeasti liian suureksi paljaalla silmällä mukavasti luettavaksi.

Ohjelmaan voisi myös lisätä useita toteutuksia eri vaiheille, jolloin eri algoritmien vertailu ja yhdistely onnistuisi helposti. Myös eri ohjelmointikieliä voisi tukea ottamalla käyttöön uusia parsintakirjastoja.

## Viitteet

- [1] https://dl.acm.org/doi/pdf/10.1145/235968.233366
- [2] http://serg.aau.at/pub/MartinPinzger/Publications/Fluri2007-changedistiller.pdf
- [3] https://hal.archives-ouvertes.fr/hal-01054552/document
- [4] https://docs.python.org/3/library/ast.html
