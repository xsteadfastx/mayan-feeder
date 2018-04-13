.PHONY: clean env test update

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -rf .tox
	pipenv --rm

env:
	pipenv install --python 3.6.5 --dev

test:
	pipenv run tox -r

update:
	pipenv update --dev
	@grep mayan-feeder Pipfile.lock > /dev/null && pipenv uninstall mayan_feeder || exit 0
