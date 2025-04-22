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
	gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -g1280x720 -r144 -dPDFFitPage -dAlignToPixels=0 -dGridFitTT=0 -sOutputFile=$@ $<

# Clean up all temporary TeXShop generated files
clean:
	rm -f *.aux *.log *.synctex.gz
