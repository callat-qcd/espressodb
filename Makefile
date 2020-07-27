
.PHONY: paper
paper: paper.pdf

paper.pdf: paper.md paper.bib
	pandoc -t latex -o paper.pdf --bibliography paper.bib paper.md

.PHONY: arxiv
arxiv:
	make -C doc-src/arXiv

.PHONY: clean
clean:
	rm paper.pdf

.PHONY: docs
docs:
	make -C doc-src html

.PHONY: test
test:
	make -C example/ test
	make -C tests/ test

VERSION:=$(shell python setup.py --version)

version:
	@echo $(VERSION)

create-dist: test
	python -m pip install --upgrade setuptools wheel twine
	python setup.py sdist bdist_wheel

pypi-test-upload: create-dist
	@echo "---------------------------------------------------------"
	@echo "Start uploading djang-gvar version ${VERSION} to testpypi"
	@echo "---------------------------------------------------------"
	python -m twine upload --repository testpypi dist/espressodb-${VERSION}*

pypi-main-upload: pypi-test-upload
	@echo"---------------------------------------------------------"
	@echo "Start uploading djang-gvar version ${VERSION} to mainpypi"
	@echo"---------------------------------------------------------"
	python -m twine upload dist/espressodb-${VERSION}*
