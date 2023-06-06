# ast-diff

Diff Python files using the [Gumtree](https://hal.science/hal-01054552/PDF/main.pdf) algoritm.

## Usage
Takes two parameters, source and target. Each parameter can be either python code or a path to a python file.

### Python
```
python3 -m astdiff "print('123')" "print()"
```

### Docker
```
docker run henrinikku/astdiff "print('123')" "print()"
```
