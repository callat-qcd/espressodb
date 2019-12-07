paper | paper.pdf: paper.md paper.bib
	pandoc -t latex -o paper.pdf --bibliography paper.bib paper.md

tex: paper.md paper.bib
	cp paper.md paper.tex.md
	sed -i.bak 's/\[@Kurth_2018]/\\cite{Kurth_2018}/' paper.tex.md
	sed -i.bak 's/\[@Joubert:2018:AOE:3291656.3291732]/\\cite{Joubert:2018:AOE:3291656.3291732}/' paper.tex.md
	sed -i.bak 's/\[@Berkowitz:2018gqe]/\\cite{Berkowitz:2018gqe}/' paper.tex.md
	sed -i.bak 's/\[@incite:2019; @incite:2020]/\\cite{incite:2019,incite:2020}/' paper.tex.md
	sed -i.bak 's/\[@Nicholson:2018mwc; @Chang:2018uxx]/\\cite{Nicholson:2018mwc,Chang:2018uxx}/' paper.tex.md
	sed -i.bak 's/\[@Berkowitz:2017vcp]/\\cite{Berkowitz:2017vcp}/' paper.tex.md
	sed -i.bak 's/\[@Berkowitz:2018gqe; @Berkowitz:2017xna]/\\cite{Berkowitz:2018gqe,Berkowitz:2017xna}/' paper.tex.md
	sed -i.bak 's/# References//' paper.tex.md
	pandoc -t latex -o doc-src/arXiv/paper_body.tex paper.tex.md
	sed -i.bak 's:doc-src/_static/lattedb-example.png:lattedb-example.png:' doc-src/arXiv/paper_body.tex
	rm doc-src/arXiv/paper_body.tex.bak
	cp doc-src/_static/lattedb-example.png doc-src/arXiv/
	cp paper.bib doc-src/arXiv/
	rm paper.tex.md paper.tex.md.bak


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
