![version](https://img.shields.io/badge/version-1.0.0-blue)

# Paws and Care (Unit Testing Demo)

Stdlib-only Python project. Singleton `ClinicDatabase`, `PetFactory` for Dog/Cat/Bird/Rabbit, plus unit tests.

## Setup

Requires Python 3.10+.

```bash
git clone <repo-url>
cd UnitTesting
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` is intentionally empty (no external deps).

## Run tests

```bash
python3 -m unittest discover -s tests -v
# or with venv active:
# python -m unittest discover -s tests -v
```

## Run CLI demo

```bash
python3 src/clinic/main.py
```

# License

MIT License — see [LICENSE](./LICENSE) for details.
