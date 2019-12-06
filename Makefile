paper | paper.pdf: paper.md paper.bib
	pandoc -t latex -o paper.pdf --bibliography paper.bib paper.md

tex: paper.md paper.bib
	pandoc -t latex -o arXiv/paper_body.tex --bibliography paper.bib paper.md
	sed -i.bak 's:doc-src/_static/lattedb-example.png:lattedb-example.png:' arXiv/paper_body.tex
	rm arXiv/paper_body.tex.bak
	cp doc-src/_static/lattedb-example.png arXiv/


.PHONY: clean
clean:
	rm paper.pdf

.PHONY: test
test: test_my_project test_m2m

.PHONY: test_my_project
test_my_project:
	cd example/my_project && pytest

.PHONY: test_m2m
test_m2m:
	cd example/espressodb_tests && pytest
