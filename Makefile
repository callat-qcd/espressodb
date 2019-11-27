paper.pdf: paper.md paper.bib
	pandoc -t latex -o paper.pdf --bibliography paper.bib paper.md

.PHONY: clean
clean:
	rm paper.pdf

.PHONY: test
test:
	cd example/my_project && pytest
	cd example/espressodb_tests && pytest
