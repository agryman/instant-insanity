# Makefile — assemble the finished video from per-part videos, with embedded,
# time-shifted subtitles.
#
# Strategy: embed each scene's .srt into its .mp4 as a soft mov_text subtitle
# track, concatenate the subtitled scenes into a per-part mp4, then concatenate
# the parts into the final video. Because the subtitles travel inside each mp4,
# ffmpeg time-shifts them using real video packet timestamps, so captions stay
# aligned with no drift and no manual duration bookkeeping. Every concat is a
# lossless stream copy.
#
# The media/ directories are owned by Manim and are only ever READ here. Every
# intermediate lands in build-output/. output/ holds the two artifacts that get
# uploaded: the video and its subtitle file.
#
#   src/.../<part>/media/videos/720p30/Scene.mp4 + .srt   (Manim, read-only)
#       -> build-output/<part>/Scene.sub.mp4    (subtitles embedded)
#       -> build-output/<part>/concat.txt       (playback order)
#       -> build-output/<part>.mp4              (scenes concatenated)
#       -> output/instant-insanity.mp4          (parts concatenated)
#       -> output/instant-insanity.srt          (subtitles, extracted)
#
# Usage:
#   make                 # build both artifacts in output/
#   make output          # same
#   make build-output/part-3.mp4   # build a single part
#   make subtitles       # just output/instant-insanity.srt
#   make clean           # remove generated intermediates and outputs

FFMPEG  ?= ffmpeg
QUALITY ?= 720p30

SCENES_ROOT := src/instant_insanity/scenes
# Named build-output/ rather than build/ to stay clear of the directory Python
# packaging tools use.
BUILD_DIR   := build-output
OUTPUT_DIR  := output

# Ordered list of parts. The order here IS the playback order.
# PARTS := part-1 part-3
PARTS := part-1

# Source scene directory for each part.
PART_DIR_part-1 := part_1_introduction
PART_DIR_part-3 := part_3_graph_theory

# Ordered list of scene class names per part. The order here IS the playback
# order. These are listed explicitly rather than globbed because a media
# directory may also hold demo, experimental, or superseded renders.
SCENES_part-1 := IntroductionScene1 \
                 IntroductionScene2

SCENES_part-3 := GraphTheoryScene1 \
                 GraphTheoryScene2 \
                 GraphTheoryScene3 \
                 GraphTheoryScene4 \
                 GraphTheoryScene5

PART_MP4S   := $(addprefix $(BUILD_DIR)/,$(addsuffix .mp4,$(PARTS)))
PARTS_LIST  := $(BUILD_DIR)/parts-concat.txt
OUTPUT_MP4  := $(OUTPUT_DIR)/instant-insanity.mp4
OUTPUT_SRT  := $(OUTPUT_DIR)/instant-insanity.srt

# `output` is also a directory name, so it must be phony or make would treat
# the existing directory as an up-to-date target.
.PHONY: all output subtitles clean
all: output
output: $(OUTPUT_MP4) $(OUTPUT_SRT)
subtitles: $(OUTPUT_SRT)

# Per-part rules, generated once per entry in PARTS.
#
# Subtitled scenes are written to build-output/<part>/ rather than beside their
# sources, so nothing is ever added to the Manim-managed media directory. A
# static pattern rule is needed (rather than one generic `%.sub.mp4` rule)
# because the target and its prerequisites live in different directories.
#
# Concat lists use basenames because the concat demuxer resolves paths relative
# to the list file's own directory — which is where the .sub.mp4 files are.
# Each list is rewritten by the recipe that produces it, so it can never go
# stale relative to the SCENES_* variables.
#
# -map 0 forces ALL streams through; without it ffmpeg's default stream
# selection drops the subtitle track during concat.
define PART_rules
MEDIA_$(1)  := $$(SCENES_ROOT)/$$(PART_DIR_$(1))/media/videos/$$(QUALITY)
STAGE_$(1)  := $$(BUILD_DIR)/$(1)
SUBBED_$(1) := $$(addprefix $$(STAGE_$(1))/,$$(addsuffix .sub.mp4,$$(SCENES_$(1))))
LIST_$(1)   := $$(STAGE_$(1))/concat.txt

$$(SUBBED_$(1)): $$(STAGE_$(1))/%.sub.mp4: $$(MEDIA_$(1))/%.mp4 $$(MEDIA_$(1))/%.srt
	@mkdir -p $$(@D)
	$$(FFMPEG) -y -i $$(word 1,$$^) -i $$(word 2,$$^) -c copy -c:s mov_text $$@

$$(LIST_$(1)): $$(SUBBED_$(1))
	@mkdir -p $$(@D)
	@rm -f $$@
	@$$(foreach s,$$(SCENES_$(1)),printf "file '%s'\n" "$$(s).sub.mp4" >> $$@;)

$$(BUILD_DIR)/$(1).mp4: $$(LIST_$(1))
	$$(FFMPEG) -y -f concat -safe 0 -i $$< -map 0 -c copy $$@
endef

$(foreach p,$(PARTS),$(eval $(call PART_rules,$(p))))

# Concatenate the parts into the final video. Rebuilds whenever any part is
# newer than it.
$(OUTPUT_MP4): $(PART_MP4S)
	@mkdir -p $(OUTPUT_DIR)
	@rm -f $(PARTS_LIST)
	@$(foreach p,$(PARTS),printf "file '%s'\n" "$(p).mp4" >> $(PARTS_LIST);)
	$(FFMPEG) -y -f concat -safe 0 -i $(PARTS_LIST) -map 0 -c copy $@

# Extract the combined, time-shifted subtitles as a standalone .srt. YouTube
# ignores the embedded mov_text track, so this file is a delivered artifact in
# its own right: upload it via Studio > Subtitles alongside the video.
$(OUTPUT_SRT): $(OUTPUT_MP4)
	$(FFMPEG) -y -i $< -map 0:s:0 $@

# Everything under build-output/ is generated, as are both delivered artifacts.
clean:
	rm -rf $(BUILD_DIR)
	rm -f $(OUTPUT_MP4) $(OUTPUT_SRT)
