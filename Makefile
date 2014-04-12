SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make help    -- displays this help"
	@echo " make test    -- runs tests"
	@echo " make release -- pushes to pypi"

test:
	python manage.py test

release:
	python setup.py sdist bdist_wheel
	twine upload dist/*
