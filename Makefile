# -*- coding: utf-8; mode: makefile-gmake -*-

include utils/makefile.include
include utils/makefile.python
include utils/makefile.sphinx

GIT_URL   = https://github.com/return42/fspath.git
PYOBJECTS = fspath
DOC = docs
API_DOC = $(DOC)/fspath-api
SLIDES    = docs/slides

all: clean pylint pytest build docs

PHONY += help
help:
	@echo  '  docs	- build documentation'
	@echo  '  clean	- remove most generated files'
	@echo  '  rqmts	- info about build requirements'
	@echo  ''
	@echo  '  test  - run *tox* test'
	@echo  '  install   - developer install'
	@echo  '  uninstall - developer uninstall'
	@$(MAKE) -s -f utils/makefile.include make-help
	@echo  ''
	@$(MAKE) -s -f utils/makefile.python python-help
	@echo  ''
	@$(MAKE) -s -f utils/makefile.sphinx docs-help

PHONY += test
test: pytest

PHONY += install
install: pyinstall

PHONY += uninstall
uninstall: pyuninstall

PHONY += docs
docs:  sphinx-doc $(API_DOC) slides
	@$(PY_ENV_BIN)/pip install $(PIP_VERBOSE) -e .
	$(call cmd,sphinx,html,docs,docs)

$(API_DOC): $(PY_ENV)
	$(PY_ENV_BIN)/sphinx-apidoc --separate --maxdepth=1 -o $(API_DOC) fspath
	rm -f $(API_DOC)/modules.rst

PHONY += slides
slides:  sphinx-doc
	$(call cmd,sphinx,html,$(SLIDES),$(SLIDES),slides)

PHONY += clean
clean: pyclean docs-clean
	$(call cmd,common_clean)
	rm -rf $(API_DOC)

PHONY += help-rqmts
rqmts: msg-sphinx-doc msg-pylint-exe msg-pip-exe

.PHONY: $(PHONY)

