# Makefile — assemble per-part videos with embedded, time-shifted subtitles.
#
# Strategy (Option A): embed each scene's .srt into its .mp4 as a soft mov_text
# subtitle track, then concatenate the subtitled scenes with the ffmpeg concat
# demuxer. Because the subtitles travel inside each mp4, ffmpeg time-shifts them
# using real video packet timestamps, so captions stay aligned with no drift and
# no manual duration bookkeeping.
#
# Usage:
#   make                # build the default PART (part_1_introduction)
#   make PART=part_2_x  # build a different part (add its SCENES list below)
#   make clean          # remove generated intermediates and outputs

FFMPEG  ?= ffmpeg
QUALITY ?= 720p30
PART    ?= part_1_introduction

SCENES_DIR := src/instant_insanity/scenes/$(PART)
MEDIA      := $(SCENES_DIR)/media/videos/$(QUALITY)

# Ordered list of scene class names. The order here IS the playback order.
SCENES := IntroductionScene1 IntroductionScene2

SUBBED      := $(addprefix $(MEDIA)/,$(addsuffix .sub.mp4,$(SCENES)))
CONCAT_LIST := $(MEDIA)/concat.txt
FINAL_MP4   := $(MEDIA)/$(PART).mp4
FINAL_SRT   := $(MEDIA)/$(PART).srt

.PHONY: all clean
all: $(FINAL_SRT)

# 1. Embed each scene's srt into its mp4 as a soft mov_text subtitle track.
#    Video and audio are copied bit-for-bit; only the subtitles are converted.
$(MEDIA)/%.sub.mp4: $(MEDIA)/%.mp4 $(MEDIA)/%.srt
	$(FFMPEG) -y -i $(word 1,$^) -i $(word 2,$^) -c copy -c:s mov_text $@

# 2. Build the concat list in playback order. Paths are basenames because the
#    concat demuxer resolves them relative to the list file's directory.
$(CONCAT_LIST): $(SUBBED)
	@rm -f $@
	@$(foreach s,$(SCENES),printf "file '%s'\n" "$(s).sub.mp4" >> $@;)

# 3. Concatenate the subtitled scenes into one video (lossless stream copy).
#    -map 0 forces ALL streams through; without it ffmpeg's default stream
#    selection drops the subtitle track during concat.
$(FINAL_MP4): $(CONCAT_LIST)
	$(FFMPEG) -y -f concat -safe 0 -i $< -map 0 -c copy $@

# 4. Extract the combined, time-shifted subtitles as a standalone .srt for
#    YouTube upload. (Optional: YouTube can also read the embedded track.)
$(FINAL_SRT): $(FINAL_MP4)
	$(FFMPEG) -y -i $< -map 0:s:0 $@

clean:
	rm -f $(SUBBED) $(CONCAT_LIST) $(FINAL_MP4) $(FINAL_SRT)