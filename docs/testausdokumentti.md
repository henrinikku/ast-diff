# Testausdokumentti

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
coverage run -m pytest
```

Vastaavasti kattavuusraportin saa tulostettua ajamalla:

```
coverage report --omit="tests/*"
```

Yksikkötestien kattavuus on raportin perusteella tällä hetkellä melko hyvällä tolalla:

```
Name                          Stmts   Miss  Cover
-------------------------------------------------
astdiff/__init__.py               0      0   100%
astdiff/ast.py                   26      0   100%
astdiff/context.py               48      1    98%
astdiff/differ.py                30      0   100%
astdiff/edit_script.py           19      0   100%
astdiff/gumtree.py              130      2    98%
astdiff/matcher.py               15      3    80%
astdiff/metadata.py              30      0   100%
astdiff/parse.py                 43      0   100%
astdiff/script_generator.py      15      1    93%
astdiff/traversal.py              9      0   100%
-------------------------------------------------
TOTAL                           365      7    98%
```
