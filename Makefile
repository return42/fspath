# -*- coding: utf-8; mode: makefile-gmake -*-

include utils/makefile.include
include utils/makefile.python
include utils/makefile.sphinx
include utils/makefile.0

GIT_URL   = git@github.com:return42/fspath.git
PYOBJECTS = fspath
DOC       = docs
API_DOC   = $(DOC)/fspath-api
SLIDES    = docs/slides

all: clean pylint pytest build docs

PHONY += help help-min help-all

help: help-min
	@echo  ''
	@echo  'to get more help:  make help-all'

help-min:
	@echo  '  docs      - build documentation'
	@echo  '  docs-live - autobuild HTML documentation while editing'
	@echo  '  clean     - remove most generated files'
	@echo  '  rqmts	    - info about build requirements'
	@echo  ''
	@echo  '  test  - run *tox* test'
	@echo  '  install   - developer install (./local)'
	@echo  '  uninstall - uninstall (./local)'

	$(Q)$(MAKE) -e -s make-help

help-all: help-min
	@echo  ''
	$(Q)$(MAKE) -e -s docs-help
	@echo  ''
	$(Q)$(MAKE) -e -s python-help


PHONY += install
install: pyenvinstall

PHONY += uninstall
uninstall: pyenvuninstall

PHONY += $(API_DOC) docs docs-live
docs: $(API_DOC) slides
	@$(PY_ENV_BIN)/pip install $(PIP_VERBOSE) -e .
	$(call cmd,sphinx,html,docs,docs)

docs-live: pyenvinstall $(API_DOC)
	$(call cmd,sphinx_autobuild,html,$(DOCS_FOLDER),$(DOCS_FOLDER))

$(API_DOC): pyenvinstall $(PY_ENV)
	$(PY_ENV_BIN)/sphinx-apidoc --separate --maxdepth=1 -o $(API_DOC) fspath
	rm -f $(API_DOC)/modules.rst

PHONY += slides
slides: pyenvinstall
	$(call cmd,sphinx,html,$(SLIDES),$(SLIDES),slides)

PHONY += clean
clean: pyclean docs-clean
	@rm -rf ./$(API_DOC)
	$(call cmd,common_clean)

PHONY += rqmts
rqmts: msg-python-exe msg-pip-exe

PHONY += test
test: pytest

.PHONY: $(PHONY)

