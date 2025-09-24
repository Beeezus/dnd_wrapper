# Open5e Minimal Client

A tiny, typed Python wrapper for a few Open5e endpoints I actually use at the table.

While hunting for “open APIs,” I noticed many popular services already have solid community wrappers (think Hunter or Meteo). So I dug into a less-hyped API from my hobby Open5e and built the most frequent request structure I, as a DM, would reach for when crafting a game: quick filters for **spells**, **monsters**, and **magic items**, with sane timeouts/retries and no pagination or other fuss.

---

## Features

- Minimal, synchronous client on top of `httpx`
- Explicit allow-lists for filters (unknown/`None` are dropped)
- Tiny API: `spells()`, `monsters()`, `magic_items()`
- Typed and mypy-friendly

---

## Install 

1) Install Python with pyenv
```bash
pyenv install 3.11.8
pyenv local 3.11.8
```

2) Create a virtual environment and install dependencies
```bash
python -m venv venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Basic usage
```python
from src.wrapper import Open5e

client = Open5e()

# Spells by exact name
spells = client.spells(name='Fireball')

# Monsters by partial name + type + size
monsters = client.monsters(name__icontains='gob', type='fiend', size='L')

# Magic items by rarity and attunement
items = client.magic_items(rarity='legendary', requires_attunement=True)

```


## Allowed filters

Unknown keys and None values are removed before the request is made.

**Spells**:
name, classes__name__in, level, level__range, range, range__range,
school__name, school__name__in, duration, duration__in,
concentration, verbal, somatic, material, material_consumed, casting_time

**Monsters**:
name, name__icontains, desc, desc__icontains, cr, cr__range,
hit_points, armor_class, type, type__contains, size

**Magic items**:
name, name__icontains, desc, desc__contains, type,
type__contains, rarity, requires_attunement


## Tests
**mypy**
```bash
(venv) ➜  dnd_wrapper git:(main) mypy src
Success: no issues found in 2 source files
```

**flake8**
```bash 
(venv) ➜  dnd_wrapper git:(main) ✗ flake8 src -v
flake8.checker            MainProcess   1050 INFO     Making checkers
flake8.main.application   MainProcess   1946 INFO     Finished running
flake8.main.application   MainProcess   1946 INFO     Reporting errors
flake8.main.application   MainProcess   1946 INFO     Found a total of 15 violations and reported 0
```
