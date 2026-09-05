"""A no-op speech service for dry-run renders.

Rendering a :class:`~manim_voiceover.voiceover_scene.VoiceoverScene` normally
requires either a network round trip to a TTS API or a live microphone take.
Neither is wanted while iterating on the visuals, so ``DryRunService`` stands in
for a real speech service: it synthesises silence instead of speech.

It cannot literally do nothing. ``VoiceoverScene.add_voiceover_text`` passes the
generated file to ``Scene.add_sound``, and ``VoiceoverTracker`` reads its length
with ``mutagen.mp3.MP3``, so a real MP3 has to exist on disk. This service
writes a silent one whose length is estimated from the word count, which keeps
the animation timing close to what the finished voiceover will produce.

Bookmarks are not supported: no ``word_boundaries`` are emitted, so
``VoiceoverScene.wait_until_bookmark`` will raise.
"""

from pathlib import Path
from typing import Any, Optional

from manim import MathTex, Text, UP, Write, tempconfig, BLACK
from manim_voiceover import VoiceoverScene, VoiceoverTracker
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService
from pydub import AudioSegment

from instant_insanity_core.voiceovers.voiceover import voiceover_wait
from kwargs_xyz_core.config import PREVIEW_CONFIG

# Speaking rate of a typical narrator, in words per minute.
DEFAULT_WORDS_PER_MINUTE: float = 150.0

# Length given to a voiceover whose estimate falls below it, in seconds.
DEFAULT_MIN_DURATION: float = 0.5

# Sample rate of the generated silence, in hertz.
SILENCE_FRAME_RATE: int = 44100


class DryRunService(SpeechService):
    """Speech service that generates silence instead of speech.

    Use it in place of a real service to render a scene without calling a TTS
    API or recording a take::

        self.set_speech_service(DryRunService())
    """

    words_per_minute: float
    min_duration: float

    def __init__(
        self,
        words_per_minute: float = DEFAULT_WORDS_PER_MINUTE,
        min_duration: float = DEFAULT_MIN_DURATION,
        **kwargs: Any
    ) -> None:
        """
        Args:
            words_per_minute: The assumed speaking rate used to estimate how
                long each voiceover would take to speak.
            min_duration: The minimum length in seconds of a generated audio
                file. Short texts are padded up to this length.
            **kwargs: Additional arguments passed to SpeechService.

        Raises:
            ValueError: If words_per_minute or min_duration is not positive.
        """
        if words_per_minute <= 0.0:
            raise ValueError(f'words_per_minute must be positive: {words_per_minute}')
        if min_duration <= 0.0:
            raise ValueError(f'min_duration must be positive: {min_duration}')

        super().__init__(**kwargs)

        self.words_per_minute = words_per_minute
        self.min_duration = min_duration

    def estimate_duration(self, text: str) -> float:
        """Estimates how long it would take to speak the given text.

        Args:
            text: The text that would be spoken, without bookmarks.

        Returns:
            The estimated duration in seconds, at least min_duration.
        """
        word_count: int = len(text.split())
        duration: float = 60.0 * word_count / self.words_per_minute

        return max(duration, self.min_duration)

    def generate_from_text(
        self,
        text: str,
        cache_dir: Optional[str] = None,
        path: Optional[str] = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Writes a silent MP3 whose length approximates the spoken text.

        Args:
            text: The text that would be spoken, possibly containing bookmarks.
            cache_dir: The directory to write the audio file to. Defaults to
                the cache directory of this service.
            path: The file name to write within cache_dir. Defaults to a name
                derived from the text.
            **kwargs: Additional arguments, ignored.

        Returns:
            The cache entry for this voiceover, as documented by SpeechService.
        """
        if cache_dir is None:
            cache_dir = self.cache_dir

        input_text: str = remove_bookmarks(text)
        duration: float = round(self.estimate_duration(input_text), 3)
        input_data: dict[str, Any] = {
            'input_text': input_text,
            'duration': duration,
            'service': 'dry_run'
        }

        cached_result: Optional[dict[str, Any]] = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        audio_path: str = path if path is not None else self.get_audio_basename(input_data) + '.mp3'

        silence: AudioSegment = AudioSegment.silent(
            duration=int(round(1000.0 * duration)),
            frame_rate=SILENCE_FRAME_RATE
        )
        silence.export(str(Path(cache_dir) / audio_path), format='mp3')

        json_dict: dict[str, Any] = {
            'input_text': text,
            'input_data': input_data,
            'original_audio': audio_path
        }

        return json_dict

    def __str__(self) -> str:
        return f'DryRunService(words_per_minute={self.words_per_minute})'


class DryRunServiceDemo(VoiceoverScene):
    """Demo scene that renders two voiceover blocks with no speech."""

    def construct(self) -> None:
        self.set_speech_service(DryRunService())

        title: Text = Text('Hello from Manim!', font_size=48, color=BLACK)

        tracker: VoiceoverTracker
        with self.voiceover(text="Welcome to this mathematics explanation video!") as tracker:
            self.play(Write(title), run_time=tracker.duration)
            voiceover_wait(self, tracker)

        with self.voiceover(text="Let's explore some interesting mathematical concepts together.") as tracker:
            self.play(title.animate.shift(UP * 2))
            formula: MathTex = MathTex(r'e^{i\pi} + 1 = 0', color=BLACK)
            self.play(Write(formula))
            voiceover_wait(self, tracker)


if __name__ == '__main__':
    with tempconfig(PREVIEW_CONFIG):
        scene: DryRunServiceDemo = DryRunServiceDemo()
        scene.render()
