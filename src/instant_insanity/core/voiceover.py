from manim_voiceover import VoiceoverScene, VoiceoverTracker

# Minimum time in seconds that each voiceover block stays on screen.
DEFAULT_MIN_VOICEOVER_DURATION: float = 1.0

def voiceover_wait(
        scene: VoiceoverScene,
        tracker: VoiceoverTracker,
        min_duration: float= DEFAULT_MIN_VOICEOVER_DURATION
) -> None:
    """
    This function waits for the minimum duration before exiting a voiceover block.

    Args:
        scene: The voiceover scene that contains the voiceover block.
        tracker: The voiceover tracker for the voiceover block.
        min_duration: The minimum duration to wait for in the voiceover block.
    """

    elapsed: float = tracker.duration - tracker.get_remaining_duration()
    scene.safe_wait(min_duration - elapsed)
