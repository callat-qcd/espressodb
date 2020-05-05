

.PHONY: tgz
tgz: arXiv.tgz

.PHONY: pdf
pdf: arXiv.pdf

paper_body.tex: ../../paper.md
	cp ../../paper.md paper.tex.md
	sed -i.bak 's/\[@Kurth_2018]/\\cite{Kurth_2018}/' paper.tex.md
	sed -i.bak 's/\[@Joubert:2018:AOE:3291656.3291732]/\\cite{Joubert:2018:AOE:3291656.3291732}/' paper.tex.md
	sed -i.bak 's/\[@8665785]/\\cite{8665785}/' paper.tex.md
	sed -i.bak 's/\[@incite:2019; @incite:2020]/\\cite{incite:2019,incite:2020}/' paper.tex.md
	sed -i.bak 's/\[@Nicholson:2018mwc; @Chang:2018uxx]/\\cite{Nicholson:2018mwc,Chang:2018uxx}/' paper.tex.md
	sed -i.bak 's/\[@Berkowitz:2017vcp]/\\cite{Berkowitz:2017vcp}/' paper.tex.md
	sed -i.bak 's/\[@8665785; @Berkowitz:2017xna]/\\cite{8665785,Berkowitz:2017xna}/' paper.tex.md
	sed -i.bak 's/\[@10.1093\/nar\/gkt328]/\\cite{10.1093\/nar\/gkt328}/' paper.tex.md
	sed -i.bak 's/# References//' paper.tex.md
	pandoc -t latex -o paper_body.tex paper.tex.md
	sed -i.bak 's:doc-src/_static/lattedb-example.png:lattedb-example.png:' paper_body.tex
	$(RM) paper.tex.md paper.tex.md.bak paper_body.tex.bak

lattedb-example.png:
	cp ../_static/lattedb-example.png .

OBJECTS = arXiv.tex paper_body.tex use-case.tex lattedb-example.png joss-logo.png

arXiv.tgz: arXiv.pdf $(OBJECTS) arXiv.bbl
	tar -czf arXiv.tgz $(OBJECTS) arXiv.bbl

arXiv.pdf: $(OBJECTS) paper.bib
	pdflatex arXiv.tex && bibtex arXiv && pdflatex arXiv.tex && pdflatex arXiv.tex

.PHONY: clean
clean:
	$(RM) lattedb-example.png
	$(RM) paper_body.tex
	$(RM) arXiv.tgz
	$(RM) arXiv.pdf
	$(RM) arXiv.aux
	$(RM) arXiv.bbl
	$(RM) arXiv.blg
	$(RM) arXiv.log
	$(RM) arXiv.out
	$(RM) arXiv.synctex.gz
	$(RM) paper.tex.md
	$(RM) paper.tex.md.bak
	$(RM) paper_body.tex.bak
