TEMPFILE := $(shell mktemp -u)


.PHONY: install
install:
	python3 setup.py install

.PHONY: uninstall
uninstall:
	python3 setup.py install --record ${TEMPFILE} && \
		cat ${TEMPFILE} | xargs rm -rf && \
		rm -f ${TEMPFILE}

.PHONY: devenv
devenv:
	@echo "Installing latest development requirements"
	pipenv install --dev

coala-venv:
	@echo ">>> Preparing virtual environment for coala"
	@# We need to run coala in a virtual env due to dependency issues
	virtualenv -p python3 venv-coala
	. venv-coala/bin/activate && pip install -r coala_requirements.txt

.PHONY: clean
clean:
	find . -name '*.pyc' -or -name '__pycache__' -or -name '*.py.orig' | xargs rm -rf
	rm -rf venv venv-coala coverage.xml
	rm -rf dist githubcap.egg-info build docs/

.PHONY: pytest
pytest:
	@echo ">>> Executing testsuite"
	python3 -m pytest -s --cov=./githubcap -vvl --timeout=2 test/

.PHONY: pylint
pylint:
	@echo ">>> Running pylint"
	pylint githubcap

.PHONY: coala
coala: coala-venv
	@echo ">>> Running coala"
	. venv-coala/bin/activate && coala --non-interactive

.PHONY: pydocstyle
pydocstyle:
	@echo ">>> Running pydocstyle"
	pydocstyle githubcap

.PHONY: check
check: pytest pylint pydocstyle coala

.PHONY: api
api:
	@sphinx-apidoc -e -o docs.source/githubcap/doc/ githubcap -f

.PHONY: doc
doc: api
	@make -f Makefile.docs html
	@echo "Documentation available at 'docs/index.html'"

.PHONY: docs html test
docs: doc
html: doc
test: check
