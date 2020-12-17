all: install dev

install:
	python3 -m pip install -r requirements.txt

install-dev: install
	python3 -m pip install -r requirements.dev.txt

format:
	black .
	isort .

static-test:
	black --check .
	isort --check --df .
	flake8
