# ast-diff

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
poetry run <source> <target>
```

Missä `source` ja `target` ovat joko polkuja Python-tiedostoihin tai Python-koodinpätkiä.

### Testien suoritus

```
poetry run pytest
```

### Koodin formatointi

```
poetry run black astdiff
```

### Koodin linttaus

```
poetry run flake8
```
