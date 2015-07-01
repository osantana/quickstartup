.PHONY: clean-pyc clean-build

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete

test:
	./manage.py test

test-all:
	tox

coverage:
	coverage run --source quickstartup manage.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

release: clean
	git tag `python setup.py -q version`
	git push origin `python setup.py -q version`
	python setup.py sdist upload

APPS = core \
       accounts \
       website \
       contacts

messages:
	for app in $(APPS); do \
		(cd quickstartup/$$app && echo "\n-- Processing $$app..." && django-admin.py makemessages); \
	done

compile:
	for app in $(APPS); do \
		(cd quickstartup/$$app && echo "\n-- Processing $$app..." && django-admin.py compilemessages); \
	done
