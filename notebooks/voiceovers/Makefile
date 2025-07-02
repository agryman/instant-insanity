# Recursively find all .txt files, excluding .ipynb_checkpoints directories
TXT_FILES := $(shell find . -type d -name '.ipynb_checkpoints' -prune -false -o -type f -name '*.txt')
MP3_FILES := $(TXT_FILES:.txt=.mp3)
REQ_FILES := $(TXT_FILES:.txt=.request.json)
RESP_FILES := $(TXT_FILES:.txt=.response.json)

# Default target: generate all MP3s
all: $(MP3_FILES)

# Rule to generate .mp3 using speak.zsh
%.mp3: %.txt
	@echo "Synthesizing $< → $@"
	@./speak.zsh $(basename $<)

# Clean target: remove all generated output
clean: mostlyclean
	@echo "Removing MP3 files"
	@find . -type d -name '.ipynb_checkpoints' -prune -false -o -type f -name '*.mp3' -exec rm -f {} +

# Mostlyclean: remove request/response JSON files
mostlyclean:
	@echo "Removing request and response JSON files"
	@find . -type d -name '.ipynb_checkpoints' -prune -false -o -type f \( -name '*.request.json' -o -name '*.response.json' \) -exec rm -f {} +

.PHONY: all clean mostlyclean
