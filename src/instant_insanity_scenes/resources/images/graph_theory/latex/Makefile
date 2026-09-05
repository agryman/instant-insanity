# Makefile to build PNG images from LaTeX .tex files using pdflatex + ghostscript

TEXFILES := $(wildcard *.tex)
PDFFILES := $(TEXFILES:.tex=.pdf)
PNGFILES := $(TEXFILES:.tex=.png)

# Default target
all: $(PNGFILES)

# Rule to build PDF from TEX
%.pdf: %.tex
	pdflatex -interaction=nonstopmode -halt-on-error $<

# Rule to convert PDF to PNG (720p via Ghostscript)
%.png: %.pdf
	gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -g840x400 -r144 -dPDFFitPage -dAlignToPixels=0 -dGridFitTT=0 -sOutputFile=$@ $<

# Clean up all generated files, except the PNG
mostlyclean:
	rm -f *.aux *.log *.synctex.gz *.pdf

# Clean up all generated files, including the PNG
clean: mostlyclean
	rm -f *.png
