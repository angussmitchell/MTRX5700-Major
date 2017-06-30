

define bibtex_pdf
	pdflatex -shell-escape $(1).tex
	bibtex $(1).aux
	pdflatex -shell-escape $(1).tex
	pdflatex -shell-escape $(1).tex
endef

all: pdf-report

pdf-report:
	pdflatex -shell-escape main.tex
	pdflatex -shell-escape main.tex
	evince main.pdf &



#report:
	#$(call bibtex_pdf,report)
	#evince report.pdf &


