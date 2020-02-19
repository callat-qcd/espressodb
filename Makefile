
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
