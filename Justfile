install:
    mkdir -p out/
    @poetry install

fmt:
    @poetry run isort .
    @poetry run black .

mypy:
    @poetry run mypy *.py maze/*.py

run-all:
    @poetry run python tests.py
    @poetry run python main.py
    @poetry run python stats.py
    @poetry run python polar_grid.py
    @poetry run python mask.py
