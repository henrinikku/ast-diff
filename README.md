# ast-diff

[![codecov](https://codecov.io/gh/henrinikku/ast-diff/branch/main/graph/badge.svg?token=GAZWCV7WL8)](https://codecov.io/gh/henrinikku/ast-diff)

## Dokumentaatio

- [Määrittelydokumentti](docs/maarittelydokumentti.md)
- [Testausdokumentti](docs/testausdokumentti.md)

## Viikkoraportit

### Viikko 1

- [Määrittelydokumentti](docs/maarittelydokumentti.md)
- [Viikkoraportti 1](docs/viikko1.md)

### Viikko 2

- [Viikkoraportti 2](docs/viikko2.md)

### Viikko 3

- [Viikkoraportti 3](docs/viikko3.md)
- [Testausdokumentti](docs/testausdokumentti.md)

## Käyttöohjeet

Kaikki komennot suoritetaan projektin juurikansiossa.

### Vaatimukset

- Python 3.10.6
- poetry

### Asennus

```
poetry install
```

### Suoritus

```
poetry run astdiff <source> <target>
```

Missä `source` ja `target` ovat joko polkuja Python-tiedostoihin tai Python-koodinpätkiä.

### Testien suoritus

```
poetry run pytest
```

### Testikattavuuden mittaus

```
poetry run coverage run
```

### Testikattavuuden raportointi

```
poetry run coverage report
```

### Formatointi

```
poetry run black astdiff
```

### Linttaus

```
poetry run flake8
```
