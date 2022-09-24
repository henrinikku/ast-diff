# Viikkoraportti 3

## Työaika

Noin 15-20h. Lisäksi näin unta projektista.

## Mitä olen tehnyt tällä viikolla?

Luin pari aiheeseen liittyvää paperia ajetuksen kanssa. Tulin siihen tulokseen, että GumTree-algoritmi [1] on Change Distilling-algoritmia parempi vaihtoehto tähän projektiin kahdesta syystä: se on huomattavasti nopeampi (O(n^2)) ja tukee sekä yksityiskohtaisia että suurpiirteisiä syntaksipuita siinä missä Change Distilling-algoritmi menee pahasti pieleen jos puuta ei ole rakennettu siten, että kaikilla lehdillä on kuvaavat merkkijonomuotoiset arvot.

Päätettyäni vaihtaa algoritmia totesin myös, että parso-kirjasto sopii paremmin käyttötarkoitukseeni kuin pythonin ast. Tämä johtuu siitä, että Pythonin oletussyntaksipuilla on todella monen tyyppisiä nodeja, joista monet tarjoavat erilaisia kenttiä, kun taas parson tarjoamat puut sisältävät aina value-kentän, josta on helppo poimia talteen merkkijonomuotoinen arvo nodelle.

Lopulta toteutin GumTree algoritmin ensimmäisen osan, mikä näyttää toimivan hyvin.

## Miten ohjelma on edistynyt?

Hyvin, algoritmi on noin puoliksi valmis ja testaus tms. on edennyt hyvin.

## Mitä opin tällä viikolla / tänään?

GumTree-algoritmista ja erilaisista AST-kirjastoista paljon.

## Mikä jäi epäselväksi tai tuottanut vaikeuksia? Vastaa tähän kohtaan rehellisesti, koska saat tarvittaessa apua tämän kohdan perusteella.

Lisäsin tämän osan vasta muutaman minuutin deadlinen jälkeen, joten tätä ei tarvitse huomioida jos ei halua.

GumTree-algoritmin kehittäjät puhuvat paperissa isomorfisista puista, mutta eivät tarjoa isomorfismille mitään määritelmää. Vaikuttaa siltä, että he olettavat puiden isomorfismille määritelmän, jonka mukaan puut ovat keskenään isomorfiset tasan silloin kun ne ovat kaikin puolin samanlaiset. Tämä poikkeaa lähesulkoon jokaisesta googlaamalla vastaan tulleesta määritelmästä, mikä aiheutti hieman päänvaivaa.

## Mitä teen seuraavaksi?

Toteutan puuttuvan vaiheen algoritmista sekä viimeistelen edit scriptin generoinnin.

## Viitteet

- [1] https://hal.archives-ouvertes.fr/hal-01054552/document
