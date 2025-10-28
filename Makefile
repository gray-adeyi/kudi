
default: setup

setup:
	uv sync
	uv run pre-commit install
test:
	uv run python -m unittest
