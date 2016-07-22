# -*- coding: utf-8; mode: makefile-gmake -*-

include utils/makefile.include
include utils/makefile.sphinx

PHONY   =
PYTHON ?= python3
PYLINT ?= pylint3

all: clean docs build pylint

PHONY += help
help:
	@echo  '  clean		- Remove most generated files'
	@echo  '  pylint	- run pylint *linting*'
	@echo  '  test		- run nose test'
	@echo  '  build		- build packages'
	@echo  '  docs		- build documentation'
	@echo  '  help-rqmts 	- info about build requirements'
	@echo  ''
	@echo  '  make V=0|1 [targets] 0 => quiet build (default), 1 => verbose build'
	@echo  '  make V=2   [targets] 2 => give reason for rebuild of target'
	@echo  '  make PYTHON=python2 use special python interpreter'

PHONY += help-rqmts
help-rqmts: msg-sphinx-builder

quiet_cmd_clean = CLEAN  $@
      cmd_clean = \
	rm -rf build tests/build ;\
	find . -name '*.pyc' -exec rm -f {} +      ;\
	find . -name '*.pyo' -exec rm -f {} +      ;\
	find . -name __pycache__ -exec rm -rf {} + ;\
	find . -name '*.orig' -exec rm -f {} +     ;\
	find . -name '*.rej' -exec rm -f {} +      ;\
	find . -name '*~' -exec rm -f {} +         ;\
	find . -name '*.bak' -exec rm -f {} +      ;\

quiet_cmd_build  = BUILD  $@
      cmd_build  = $(PYTHON) setup.py build

quiet_cmd_pylint = LINT   $@
      cmd_pylint = $(PYLINT) --rcfile utils/pylintrc fspath

quiet_cmd_test   = TEST   $@
      cmd_test   = cd tests; $(PYTHON) run.py -I py35 -d -m '^[tT]est' $(TEST)

quiet_cmd_doc    = LINT   $@
      cmd_pylint = $(PYLINT) --rcfile utils/pylintrc fspath

PHONY += clean
clean: docs-clean
	$(call cmd,clean)

PHONY += docs
docs:  sphinx-builder
	$(call cmd,sphinx,html,docs,docs,html)

PHONY += docs-clean
docs-clean:
	$(call cmd,sphinx_clean)

PHONY += build
build:
	$(call cmd,build)

PHONY += pylint
pylint:
	$(call cmd,pylint)

PHONY += test
test:
	$(call cmd,test)

.PHONY: $(PHONY)

