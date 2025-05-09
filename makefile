include common.mk

API_DIR = server
DB_DIR = data
SEC_DIR = security
REQ_DIR = .

PYTHONPATH = $(shell pwd)
PYTESTFLAGS = -vv --verbose --cov-branch --cov-report term-missing --tb=short -W ignore::FutureWarning

FORCE:

prod: all_tests github

github: FORCE
	- git commit -a
	git push origin main

all_tests: FORCE
	PYTHONPATH=$(PYTHONPATH) $(MAKE) -C $(API_DIR) tests
	PYTHONPATH=$(PYTHONPATH) $(MAKE) -C $(SEC_DIR) tests
	PYTHONPATH=$(PYTHONPATH) $(MAKE) -C $(DB_DIR) tests

dev_env: FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt
	@echo "You should set PYTHONPATH to: "
	@echo $(shell pwd)

docs: FORCE
	cd $(API_DIR); make docs
