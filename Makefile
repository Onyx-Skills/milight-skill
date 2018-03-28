ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VIRTUALENV_ROOT=$(HOME)/.virtualenvs/onyx
PYTHON=python

babel:
	pybabel extract -F babel.cfg -o translations/messages.pot .

# run:
# $ LANG=en make addlang
addlang:
	pybabel init -i translations/messages.pot -d translations -l $(LANG)

compilelang:
	pybabel compile -d translations

updlang:
	pybabel update -i translations/messages.pot -d translations
