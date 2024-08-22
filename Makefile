.PHONY: format lint clean

clean:
	rm -rf build dist .eggs *.egg-info
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

format:
	isort . --skip .venv --skip-glob "*.ipynb"
	black . --exclude ".venv|.*\.ipynb"

lint: clean
	mypy . --exclude ".venv|.*\.ipynb"
	black . --check --exclude ".venv|.*\.ipynb"
	isort . --check-only --skip .venv --skip-glob "*.ipynb"
	flake8 . --exclude ".venv,*.ipynb"