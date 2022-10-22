# Testausdokumentti

[![codecov](https://codecov.io/gh/henrinikku/ast-diff/branch/main/graph/badge.svg?token=GAZWCV7WL8)](https://codecov.io/gh/henrinikku/ast-diff)

### Miten testataan

Projektin testaus perustuu ainakin toistaiseksi kattaviin yksikkötesteihin. Lisäksi algoritmin eri vaiheiden suorituskykyä testataan mittaamalla niiden käyttämää aikaa suurilla syötteillä.

Koska mahdollisia syntaksipuita on monenlaisia ja lopputulos riippuu paljon myös käytetystä parsintakirjastosta, useissa testeissä käytetäänsyötteenä GumTree-paperissa [1] havainnollistavana esimerkkinä käytettyä puuta. Lisäksi syötteinä käytetään myös itse kirjoittamiani sekä Githubista kaivettuja Python-tiedostoja.

### Testien suorittaminen

Testit saa suoritettua ajamalla projektin juurikansiossa:

```
poetry run pytest
```

### Suorituskykytestit

Suorituskykytestejä ei ajeta oletuksena, sillä niissä menee muita testejä huomattavasti enemmän aikaa. Suorituskykytestit saa suoritettua seuraavalla komennolla:

```
poetry run pytest --benchmark-only
```

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

Suoritusajat on ilmoitettu raportissa mikrosekunteina, eli esimerkiksi GumTree-matchaysalgoritmin suorittamiseen kuluu 2000 rivin Python-tiedostoilla noin 19 sekuntia, mikä vastaa suurinpiirtein odotuksiani.

### Testikattavuus

Testikattavuusraportti päivittyy automaattisesti codecov-palveluun, ja codecov-badge löytyy tämän dokumentin sekä README:n ylälaidasta.

Testien kattavuuden saa mitattua manuaalisesti ajamalla projektin juurikansiossa:

```
poetry run coverage run
```

Vastaavasti kattavuusraportin saa tulostettua ajamalla:

```
poetry run coverage report
```

Yksikkötestien kattavuus on raportin perusteella tällä hetkellä melko hyvällä tolalla:

```
Name                          Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------
astdiff/__init__.py               0      0      0      0   100%
astdiff/ast.py                   26      0      4      0   100%
astdiff/context.py               48      1     10      0    98%   62
astdiff/differ.py                29      0      4      0   100%
astdiff/edit_script.py           19      0     10      0   100%
astdiff/gumtree.py              114      2     54      1    97%   71-72
astdiff/matcher.py               15      3      6      0    86%   22, 36, 56
astdiff/metadata.py              31      0     14      0   100%
astdiff/parse.py                 42      0     14      0   100%
astdiff/queue.py                 19      0      6      0   100%
astdiff/script_generator.py      15      1      8      0    96%   15
astdiff/traversal.py              9      0      4      0   100%
-------------------------------------------------------------------------
TOTAL                           367      7    134      1    98%
```

### Viitteet

- [1] https://hal.archives-ouvertes.fr/hal-01054552/document
