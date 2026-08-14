"""
This scene shows the closing credits.
"""
import numpy as np

from manim import tempconfig, VGroup, Text, LEFT, DOWN, BLACK, FadeIn
from manim.typing import Point3D
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

from gemini.audio import enrich_headset_audio
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.subscene import SubsceneMixin
from kwargs_xyz.logo import mk_logo

def mk_point(x: float, y: float, z: float = 0.0) -> Point3D:
    return np.array([x, y, z], dtype=np.float64)


class ClosingScene1(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    def construct(self):
        # self.set_speech_service(GCPTextToSpeechService())
        # RecorderService defaults transcription_model to "base", which pulls in
        # Whisper to recover word timings. None restores the SpeechService
        # default and skips transcription entirely.
        self.set_speech_service(RecorderService(transcription_model=None))
        self.add_grid(False)

        logo: VGroup = mk_logo(scale=1.0)
        logo.shift(LEFT * 4.0)
        self.play(FadeIn(logo))
        self.say("""
        This has been a quargs dot xyz production.
        """
        )

        # these are copies of the last three lines of the voiceover below
        credit_strs: list[str] = [
            'Written, animated, and narrated by Arthur Ryman',
            'Animation software provided by Manim Community',
            'Impetus and technical advice provided by Will Anielewicz'
        ]
        credit_str: str
        credit_lines: VGroup = VGroup(*[Text(credit_str, color=BLACK, font_size=24)
                                        for credit_str in credit_strs])
        credit_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        credit_lines.move_to(LEFT * 1.5, aligned_edge=LEFT)
        self.play(FadeIn(credit_lines))

        self.say("""
        Written, animated, and narrated by Arthur Ryman.
        
        Animation software provided by Mannim Community.
        
        Impetus and technical advice provided by Will ah-nyeh leh veetch .
        .
        """)

        # clean up hoarse voice
        enrich_headset_audio()


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = ClosingScene1()
        scene.render()

