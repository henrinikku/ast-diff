# Testausdokumentti

[![codecov](https://codecov.io/gh/henrinikku/ast-diff/branch/main/graph/badge.svg?token=GAZWCV7WL8)](https://codecov.io/gh/henrinikku/ast-diff)

## Miten testataan

Projektin automaattinen testaus perustuu kattaviin yksikkötesteihin. Kaikkiaan testejä on kolmenlaisia:

- Yksikkötestit
- Integraatiotestit
- Suorituskykytestit

Suurin osa testeistä on toteutettu `pytest`-kirjaston avulla, ja pari yksittäistä testiä Pythonin oletus `unittest`-kirjaston avulla. Pytest-runner kykenee tunnistamaan ja ajamaan kaikki testit.

## Yksikkötestit

Suurin osa projektin testeistä on yksikkötestejä, joita on kirjoitettu käytännössä kaikille luokille/metodeille erikseen pieniä poikkeuksia lukuunottamatta.

## Integraatiotestit

Projektin integraatiotestit eivät teknisesti eroa yksikkötesteistä, mutta ne testaavat ohjelmaa kokonaisuutena. Integraatiotestit on toteutettu Typer-kirjaston [1] tarjoaman `CliRunner` luokan avulla, joka mahdollistaa ohjelman komentorivikäyttöliittymän kutsumisen testien sisältä.

## Suorituskykytestit

Suorituskykytestien ajamiseen menee tällä hetkellä noin minuutti ja ne tulostavat seuraavanlaisen raportin:

```
-------------------------------------------------------------------------------------------------------------------------- benchmark: 8 tests --------------------------------------------------------------------------------------------------------------------------
Name (time in us)                                                 Min                        Max                       Mean                    StdDev                     Median                       IQR            Outliers         OPS            Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_anchor_matching_performance                             174.5360 (1.0)             441.1020 (1.0)             200.1294 (1.0)             32.1561 (1.0)             196.2310 (1.0)             20.6435 (1.0)           7;7  4,996.7664 (1.0)         100           1
test_container_matching_performance                          377.3760 (2.16)          1,358.7630 (3.08)            420.1764 (2.10)            99.7279 (3.10)            403.4510 (2.06)            33.5955 (1.63)          1;9  2,379.9529 (0.48)        100           1
test_metadata_calculation_performance_200_lines            5,226.7130 (29.95)         7,800.4580 (17.68)         5,556.5464 (27.76)          325.0989 (10.11)         5,479.3750 (27.92)          179.3325 (8.69)        16;16    179.9679 (0.04)        161           1
test_edit_script_generation_performance_200_lines         29,855.5120 (171.06)      339,507.4730 (769.68)       62,047.2950 (310.04)      97,495.5557 (>1000.0)      31,240.3880 (159.20)       2,583.9550 (125.17)        1;1     16.1167 (0.00)         10           1
test_gumtree_performance_200_lines                       101,009.7500 (578.73)      120,882.3090 (274.05)      107,155.5648 (535.43)       5,646.2623 (175.59)      106,225.7025 (541.33)       5,988.2220 (290.08)        2;1      9.3322 (0.00)         10           1
test_metadata_calculation_performance_2k_lines           111,638.8710 (639.63)      120,053.6120 (272.17)      115,527.7761 (577.27)       2,993.9139 (93.11)       115,452.7900 (588.35)       4,632.3800 (224.40)        3;0      8.6559 (0.00)          7           1
test_edit_script_generation_performance_2k_lines         395,380.2540 (>1000.0)     564,120.8890 (>1000.0)     453,600.4083 (>1000.0)     95,759.3002 (>1000.0)     401,300.0820 (>1000.0)    126,555.4763 (>1000.0)       1;0      2.2046 (0.00)          3           1
test_gumtree_performance_2k_lines                     21,684,961.6370 (>1000.0)  25,322,891.6610 (>1000.0)  23,446,486.2917 (>1000.0)  1,821,683.8087 (>1000.0)  23,331,605.5770 (>1000.0)  2,728,447.5180 (>1000.0)       1;0      0.0427 (0.00)          3           1
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

Suoritusajat on ilmoitettu raportissa mikrosekunteina, eli esimerkiksi GumTree-matchaysalgoritmin suorittamiseen kahdelle 2000 rivin Python-tiedostolle kuluu noin 19 sekuntia, mikä vastaa suurinpiirtein odotuksiani.

## Testisyötteet

Koska mahdollisia syntaksipuita on monenlaisia ja lopputulos riippuu paljon myös käytetystä parsintakirjastosta, useissa yksikkötesteissä käytetään syötteenä GumTree-paperissa [2] havainnollistavana esimerkkinä käytettyä, Java-kielen syntaksia kuvaavaa puuta. Lisäksi yksikkötesteissä käytetään syötteinä myös itse kirjoittamiani Python-koodinpätkiä. Itsetehdyt syötteet on täytynyt pitää melko pieninä, koska syntaksipuista tulee helposti melko suuria ja algoritmin toiminnan (ja siten odotetun lopputuloksen) järkeily on suhteellisen vaivalloista.

Suorituskykytestauksen syötteinä käytetään joidenkin Django-projektin [3] tiedostojen eri versioita.

Testeihin kovakoodattuja koodipätkiä lukuunottamatta kaikki testisyötteet löytyvät [tests/data](../tests/data/) -kansiosta.

## Testien suorittaminen

Yksikkö- ja integraatiotestit saa suoritettua ajamalla projektin juurikansiossa:

```
poetry run pytest
```

Suorituskykytestejä ei ajeta oletuksena, sillä niissä menee muita testejä huomattavasti enemmän aikaa. Suorituskykytestit saa suoritettua seuraavalla komennolla:

```
poetry run pytest --benchmark-only
```

## Testikattavuus

Testikattavuusraportti päivittyy automaattisesti codecov-palveluun, ja codecov-badge löytyy tämän dokumentin sekä README:n ylälaidasta.

Testien kattavuuden saa mitattua manuaalisesti ajamalla projektin juurikansiossa:

```
poetry run coverage run
```

Vastaavasti kattavuusraportin saa tulostettua ajamalla:

```
poetry run coverage report
```

Testikattavuus on raportin perusteella tällä hetkellä melko hyvällä tolalla:

```
Name                               Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------------------
astdiff/__init__.py                    0      0      0      0   100%
astdiff/ast/metadata.py               35      0     18      0   100%
astdiff/ast/node.py                   54      0     12      1    98%   58->exit
astdiff/ast/traversal.py              20      0      6      0   100%
astdiff/context.py                    75      3     24      2    95%   26, 103, 112
astdiff/differ.py                     27      0      0      0   100%
astdiff/editscript/__init__.py         5      0      2      0   100%
astdiff/editscript/ops.py             48      1     14      0    98%   24
astdiff/generator/__init__.py          0      0      0      0   100%
astdiff/generator/base.py              9      1      0      0    89%   18
astdiff/generator/factory.py           9      0      2      1    91%   22->exit
astdiff/generator/with_move.py        79      5     36      3    93%   134-138, 154->160, 157->154
astdiff/main.py                       25      1      2      1    93%   58
astdiff/matcher/__init__.py            0      0      0      0   100%
astdiff/matcher/base.py               14      1      0      0    93%   16
astdiff/matcher/factory.py            15      0      6      1    95%   26->exit
astdiff/matcher/gumtree.py           143      9     88      5    91%   126->exit, 131-142, 189-193, 226, 300-301
astdiff/matcher/gumtree_utils.py      33      1     10      0    93%   22
astdiff/parser/__init__.py             0      0      0      0   100%
astdiff/parser/base.py                36      2      6      0    95%   70, 78
astdiff/parser/builtin.py             23      0      6      0   100%
astdiff/parser/factory.py             13      0      4      1    94%   24->exit
astdiff/parser/parso.py               31      0     10      0   100%
astdiff/util.py                       49      0     20      0   100%
------------------------------------------------------------------------------
TOTAL                                743     24    266     15    95%
```

## Suorituskykytestauksen tuloksia

### Kopioimalla muodostetut syötteet

Ohjelman eri vaiheiden suorituskykyä testatessa kävi ilmi, että algoritmin ns. anchor matching (eli ensimmäinen) vaihe muodostaa merkittävän pullonkaulan syötteillä, joissa sama pitkähkö koodinpätkä toistuu monta kertaa peräkkäin. Tämä käy järkeen, sillä löytäessään useita keskenään isomorfisia alipuita algoritmi joutuu laskemaan kahden puun samankaltaisuutta mittaavan dice-kertoimen jokaiselle näiden puiden karteesisesta tulosta muodostuvalle parille selvittääkseen parhaan mahdollisen matchin. Dice-kertoimen laskeminen taas on suhteellisen kallis operaatio näin monta kertaa suoritettavaksi.

![runtime_no_dice_cache.png](img/runtime_no_dice_cache.png)

Onneksi Dice-kertoimen laskennan tulosten talletus ja uudelleenkäyttö ([249bc3de](https://github.com/henrinikku/ast-diff/commit/249bc3dea0200290f5b043aeb7fedb72285e4781)) eliminoi pullonkaulan täysin. Muutoksen myötä algoritmi toimii kymmeniä kertoja nopeammin mainitun kaltaisilla syötteillä.

![runtime_dice_cache.png](img/runtime_dice_cache.png)

### Käsin valitut syötteet

Anchor matching -vaihe vei odotetusten mukaisesti suurimman osan ajasta myös käsin valituilla Django-projektin [3] tiedostoilla testattaessa. Huom: alla syötteen koko merkitsee lähdetiedoston rivimäärän sijaan syntaksipuun solmujen lukumäärää.

![django-no-cache](img/runtime_django_source_no_cache.png)

Hieman yllättäen Dice-kertoimen cachetus paransi suorituskykyä jonkin verran myös tässä tapauksessa, vaikka tiedostoissa ei ole (ainakaan) tarkoituksella kovin paljoa toisteisuutta.

![django-cache](img/runtime_django_source.png)

## Viitteet

- [1] https://github.com/tiangolo/typer
- [2] https://hal.archives-ouvertes.fr/hal-01054552/document
- [3] https://github.com/django/django
