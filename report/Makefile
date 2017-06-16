

define bibtex_pdf
	pdflatex $(1).tex
	bibtex $(1).aux
	pdflatex $(1).tex
	pdflatex $(1).tex
endef

all: pdf-report

pdf-report:
	pdflatex main.tex
	pdflatex main.tex
	evince main.pdf &



#report:
	#$(call bibtex_pdf,report)
	#evince report.pdf &


