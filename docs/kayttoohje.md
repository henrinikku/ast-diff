# Käyttöohje

Ohjelma tarjoaa yhden komennon, joka ottaa vastaan kaksi Python-tiedostoa ja tulostaa niitä kuvaavien syntaksipuiden väliset erot listana operaatioita (lisäys, poisto, päivitys ja siirto), joilla ensimmäistä tiedostoa kuvaavasta tiedostosta saadaan toista tiedostoa kuvaava syntaksipuu.

Kaikki komennot suoritetaan projektin juurikansiossa.

## Vaatimukset

- Python 3.10.6
- poetry

## Asennus

Jos haluat ainoastaan suorittaa ohjelman eikä ole tarvetta ajaa testejä tms, voit skipata dev-riippuvuudet lisäämällä komentoon `--no-dev`:

```
poetry install
```

Kehitystä varten on hyvä asentaa myös git hookit:

```
poetry run pre-commit install --install-hooks
```

## Suoritus

```
poetry run astdiff <source> <target>
```

Missä `source` ja `target` ovat joko polkuja Python-tiedostoihin tai Python-koodinpätkiä.

Kuvauksen asetuksista saa tulostettua ajamalla:

```
poetry run astdiff --help
```

```
Usage: astdiff [OPTIONS] SOURCE TARGET

 Prints an edit script which describes differences between syntax trees produced by source and target.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────╮
│ *    source      TEXT  [default: None] [required]                                                     │
│ *    target      TEXT  [default: None] [required]                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────╮
│ --parser-type                  [parso|builtin-ast]              [default: ParserType.BUILTIN_AST]     │
│ --matcher-type                 [gumtree|stub|change-distiller]  [default: MatcherType.GUMTREE]        │
│ --script-generator-type        [with-move]                      [default:                             │
│                                                                 EditScriptGeneratorType.WITH_MOVE]    │
│ --log-level                    INTEGER                          [default: 20]                         │
│ --install-completion                                            Install completion for the current    │
│                                                                 shell.                                │
│ --show-completion                                               Show completion for the current       │
│                                                                 shell, to copy it or customize the    │
│                                                                 installation.                         │
│ --help                                                          Show this message and exit.           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Testien suoritus

```
poetry run pytest
```

Suorituskykytestit saa suoritettua erillisellä flagilla:

```
poetry run pytest --benchmark-only
```

Ohjelman eri vaiheiden suoritusajasta saa piirrettyä kuvaajan ajamalla esim:

```
poetry run plotruntime --export-path docs/img/test.png
```

Kuvaajan piirtäminen vaatii kaleido-kirjaston, jonka asennuksessa saattaa olla ongelmia joillain käyttöjärjestelmillä. Toimii kuitenkin omalla MacBookillani ongemitta.

## Testikattavuuden mittaus

```
poetry run coverage run
```

## Testikattavuuden raportointi

```
poetry run coverage report
```

## Formatointi

```
poetry run black .
```

## Importien sorttaus

```
poetry run isort .
```

## Linttaus

```
poetry run flake8
```
