install:
    mkdir -p out/
    @poetry install

fmt:
    @poetry run isort .
    @poetry run black .

mypy:
    @poetry run mypy .
