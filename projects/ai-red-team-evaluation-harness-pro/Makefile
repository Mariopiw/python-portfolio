setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check .

run:
	python -m harness.cli

baseline:
	python -m harness.cli --update-baseline
