format:
	python -m black .
	python -m isort .

quicktest:
	python -m black --check .
	python -m isort --check .
	python -m pflake8 .
	python -m mypy --strict

pytest:
	python -m pytest --cov=. --cov-fail-under=100 --cov-report=term --durations=3 --cache-clear

test: quicktest pytest

builddocs: flavor = markdown
builddocs:
	sphinx-build -b ${flavor} sphinx_config docs

servedocs:
	sphinx-autobuild -b html sphinx_config docs

build-dist:
	# Remove old dist files, if present.
	rm dist/* || true
	# Build the sdist so we can build the wheel
	python -m build --sdist --no-isolation
	# Reproducible wheel build by setting SOURCE_DATE_EPOCH
	# https://github.com/kushaldas/asaman/blob/ae82002dccb1ab7a97e3bb543d0e09c397c402b1/asaman/__init__.py#L18
	SOURCE_DATE_EPOCH=1309379017 python -m build --no-isolation
	# Let twine validate the sdist and wheel
	python -m twine check --strict dist/*

publish: build-dist
	python -m twine upload dist/*
