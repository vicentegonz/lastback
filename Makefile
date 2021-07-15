POETRY_VERSION = 1.1.5

# Env stuff
.PHONY: get-poetry
get-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - --version $(POETRY_VERSION)

.PHONY: build-env
build-env:
	python3 -m venv .venv
	poetry run pip install --upgrade pip
	poetry run poetry install

# Passive linters
.PHONY: black
black:
	poetry run black backend manage.py --check

.PHONY: flake8
flake8:
	poetry run flake8 backend manage.py

.PHONY: isort
isort:
	poetry run isort backend manage.py --profile=black --check

.PHONY: pylint
pylint:
	poetry run pylint backend manage.py

# Aggresive linters
.PHONY: black!
black!:
	poetry run black backend manage.py

.PHONY: isort!
isort!:
	poetry run isort backend manage.py --profile=black

# Helpers
.PHONY: migrate!
migrate!:
	docker-compose run web python manage.py migrate

.PHONY: seeds!
seeds!:
	docker-compose run web python manage.py loaddata $(shell find | grep '^\.\/backend\/.*\/fixtures/.*' | rev | cut -d'/' -f1 | rev | tr '\n' ' ')
