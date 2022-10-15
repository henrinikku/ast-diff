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

Suorituskykytestejä ei ajeta oletuksena, sillä niissä menee muita testejä huomattavasti enemmän aikaa. Suorituskykytestit saa mukaan suoritukseen ajamalla projektin juurikansiossa:

```
poetry run pytest --benchmark-enable
```

Suorituskykytestien ajamiseen menee tällä hetkellä noin minuutti ja ne tulostavat seuraavanlaisen raportin:

```
----------------------------------------------------------------------------------------------------------------------- benchmark: 6 tests -----------------------------------------------------------------------------------------------------------------------
Name (time in us)                                               Min                        Max                       Mean                  StdDev                     Median                     IQR            Outliers         OPS            Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_anchor_matching_performance                           135.2260 (1.0)             345.9340 (1.0)             161.6103 (1.0)           38.3543 (1.0)             144.8470 (1.0)           22.3225 (1.0)         13;13  6,187.7241 (1.0)         100           1
test_container_matching_performance                        166.7480 (1.23)            501.0390 (1.45)            198.4191 (1.23)          48.3660 (1.26)            177.5845 (1.23)          42.6445 (1.91)         11;7  5,039.8361 (0.81)        100           1
test_metadata_calculation_performance_200_lines          8,496.2260 (62.83)        10,834.4010 (31.32)         9,460.9116 (58.54)        573.2413 (14.95)         9,422.4980 (65.05)        875.7950 (39.23)        35;0    105.6981 (0.02)         94           1
test_gumtree_performance_200_lines                     105,485.7390 (780.07)      116,118.1680 (335.67)      107,249.5536 (663.63)     3,178.4628 (82.87)       106,303.4555 (733.90)       817.2210 (36.61)         1;1      9.3240 (0.00)         10           1
test_metadata_calculation_performance_2k_lines         153,856.2900 (>1000.0)     157,717.1800 (455.92)      155,740.1863 (963.68)     1,398.1399 (36.45)       156,134.3180 (>1000.0)    2,204.3630 (98.75)         3;0      6.4210 (0.00)          7           1
test_gumtree_performance_2k_lines                   18,876,470.9840 (>1000.0)  19,142,180.2440 (>1000.0)  19,010,944.0247 (>1000.0)  132,884.1995 (>1000.0)  19,014,180.8460 (>1000.0)  199,281.9450 (>1000.0)       1;0      0.0526 (0.00)          3           1
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
