# Makefile to convert all AVIF files to PNG

# Find all AVIF files
AVIF_FILES := $(wildcard *.avif)

# Derive PNG output files
PNG_FILES := $(AVIF_FILES:.avif=.png)

# Default target
all: $(PNG_FILES)

# Rule to convert AVIF to PNG
%.png: %.avif
	avifdec $< $@

# Clean target to remove generated PNG files
.PHONY: clean
clean:
	rm -f $(PNG_FILES)
