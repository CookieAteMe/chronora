PYTHON ?= python3

install:
	./install.sh

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(PYTHON) -m compileall chronora tests
