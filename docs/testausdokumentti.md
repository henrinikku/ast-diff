# Testausdokumentti

[![codecov](https://codecov.io/gh/henrinikku/ast-diff/branch/main/graph/badge.svg?token=GAZWCV7WL8)](https://codecov.io/gh/henrinikku/ast-diff)

### Miten testataan

Projektin testaus perustuu ainakin toistaiseksi kattaviin yksikkötesteihin. Suorituskykyä mittaavia testejä en ole toteuttanut vielä, mutta haluaisin lisätä ne jossain vaiheessa. Saatan myös lisätä myöhemmin integraatiotestejä käyttöliittymän testaamiseksi. Mikäli pisteiden saamiseen vaaditaan tietyn tyyppisten testien lisäämistä, lisään tarvittavat testit.

### Testien suorittaminen

Testit saa suoritettua ajamalla projektin juurikansiossa:

```
poetry run pytest
```

### Testien kattavuuden mittaaminen

Testien kattavuuden saa mitattua ajamalla projektin juurikansiossa:

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
