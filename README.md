# ast-diff

[![codecov](https://codecov.io/gh/henrinikku/ast-diff/branch/main/graph/badge.svg?token=GAZWCV7WL8)](https://codecov.io/gh/henrinikku/ast-diff)

## Dokumentaatio

- [Määrittelydokumentti](docs/maarittelydokumentti.md)
- [Toteutusdokumentti](docs/toteutusdokumentti.md)
- [Testausdokumentti](docs/testausdokumentti.md)
- [Käyttöohje](docs/kayttoohje.md)

## Viikkoraportit

### Viikko 1

- [Määrittelydokumentti](docs/maarittelydokumentti.md)
- [Viikkoraportti 1](docs/viikko1.md)

### Viikko 2

- [Viikkoraportti 2](docs/viikko2.md)

### Viikko 3

- [Viikkoraportti 3](docs/viikko3.md)
- [Testausdokumentti](docs/testausdokumentti.md)

### Viikko 4

- [Viikkoraportti 4](docs/viikko4.md)
- [Toteutusdokumentti](docs/toteutusdokumentti.md)

### Viikko 5

- [Viikkoraportti 5](docs/viikko5.md)

### Viikko 6

- [Viikkoraportti 6](docs/viikko6.md)

## Käyttöohjeet

Kaikki komennot suoritetaan projektin juurikansiossa.

### Vaatimukset

- Python 3.10.6
- poetry

### Asennus

Asenna riippuvuudet:

```
poetry install
```

Asenna git hookit:

```
poetry run pre-commit install --install-hooks
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
poetry run black .
```

### Importien sorttaus

```
poetry run isort .
```

### Linttaus

```
poetry run flake8
```
