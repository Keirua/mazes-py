install:
    mkdir -p out/
    @poetry install

fmt:
    @poetry run isort .
    @poetry run black .

mypy:
    @poetry run mypy *.py maze/*.py

test:
    @poetry run python tests.py

run-all:
    @poetry run python tests.py
    @poetry run python main.py
    @poetry run python stats.py
    @poetry run python polar_grid.py
    @poetry run python mask.py
    @poetry run python main_triangle_rect.py
    @poetry run python main_triangle_triangle.py
