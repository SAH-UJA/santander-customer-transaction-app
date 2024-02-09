# Makefile

.PHONY: install test clean

install:
    poetry install

test:
    poetry run pytest

clean:
    rm -rf __pycache__ .pytest_cache

