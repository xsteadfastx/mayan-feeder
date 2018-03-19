.PHONY: clean env test

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -rf .tox
	pipenv --rm

env:
	pipenv install --python 3.6.4 --dev

test:
	pipenv run tox
