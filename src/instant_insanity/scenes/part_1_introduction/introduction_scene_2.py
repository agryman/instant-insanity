from pathlib import Path

from manim import Tex, BLACK, tempconfig
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.scenes.part_1_introduction.introduction_scene_1 import IMAGE_PATH

voiceover_text_1: str = """
The Instant Insanity puzzle consists of four cubes whose faces are coloured either red, white, blue, or green.
The goal of the puzzle is to arrange the cubes in a row so that no colour is
repeated along each of the four sides.
"""

voiceover_text_2: str = """
As its name suggests, Instant Insanity is very challenging to solve simply by trial and error
because there is a huge number of possible ways to arrange the cubes.
The Winning Moves box claims that there are eighty-two thousand nine hundred and forty-four combinations.

The surprising and delightful thing about Instant Insanity is that you can solve it very quickly 
using an elegant method based on some simple concepts from the branch of mathematics known as graph theory.
"""

voiceover_text_3: str = """
One day in 1968, a university professor visited Arthur's high school and gave a guest lecture on graph theory.
He finished the lecture by showing how to apply graph theory to quickly solve Instant Insanity.
Arthur was very impressed by this demonstration of the power of graph theory and 
often used it for thinking about technical problems later in his career.
"""

voiceover_text_4: str = """
Fast forward to the present where we now have a wealth of excellent math videos on YouTube.
Several of them explain the solution to Instant Insanity but, in Arthur's opinion,
none of them fully exploit the potential of animation to clarify the concepts.
It occurred to Arthur that a compelling animation of the graph theory solution to Instant Insanity
might resonate with the current generation of young math enthusiasts
and perhaps inspire them to explore the subject further.

This video explains the Instant Insanity puzzle and its graph theory solution without 
assuming any prior knowledge of the subject.
If you enjoy solving puzzles, and know some high school mathematics, then this video is for you.
"""

class IntroductionScene2(VoiceoverScene):
    def construct(self):
        image_path = Path(IMAGE_PATH).expanduser()
        self.set_speech_service(GCPTextToSpeechService())

        # Define the path to images
        hello: Tex = Tex("Hello, world.", color=BLACK, font_size=72)

        with self.voiceover(text=voiceover_text_1) as tracker:
            self.add(hello)
            self.wait(1)
            self.remove(hello)

        with self.voiceover(text=voiceover_text_2) as tracker:
            self.add(hello)
            self.wait(1)
            self.remove(hello)

        with self.voiceover(text=voiceover_text_3) as tracker:
            self.add(hello)
            self.wait(1)
            self.remove(hello)

        with self.voiceover(text=voiceover_text_4) as tracker:
            self.add(hello)
            self.wait(1)
            self.remove(hello)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = IntroductionScene2()
        scene.render()
