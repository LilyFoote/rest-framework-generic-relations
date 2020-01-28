SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make help    -- displays this help"
	@echo " make test    -- runs tests"
	@echo " make release -- pushes to pypi"

test:
	tox

release:
	rm -rf dist
	python setup.py sdist bdist_wheel
	twine upload dist/*
