from pathlib import Path

from manim import Tex, BLACK, tempconfig, FadeIn
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import Puzzle, PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, mk_standard_puzzle3d
from instant_insanity.scenes.coordinate_grid import GridMixin

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

This video introduces graph theory and shows how to use it to solve Instant Insanity.
If you enjoy puzzles, and know some high school mathematics, then this video is for you.
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
"""

class IntroductionScene2(GridMixin, VoiceoverScene):
    """
    This scene shows the puzzle cubes and explains the goal of the puzzle.
    """
    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(True)

        # create and display the 3D puzzle
        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        projection: Projection = mk_standard_orthographic_projection()
        puzzle3d: Puzzle3D = mk_standard_puzzle3d(puzzle_spec, projection, centre=True)
        self.add(puzzle3d)
        self.wait()

        placeholder: Tex
        voiceover_text: str

        voiceover_text = """
        The Instant Insanity puzzle consists of four cubes whose faces are coloured red, white, blue, or green.
        """

        # rotate the whole puzzle along the horizontal axis
        # do a series of quarter-turn rotations, pausing after each one

        # start with one cube

        # rotate each cube along its vertical axis
        # do a series of quarter-turn rotations, pausing after each one

        # placeholder = Tex("Show the cubes and rotate them.", color=BLACK, font_size=72)
        # self.add(placeholder)
        with self.voiceover(text=voiceover_text) as tracker:
            self.wait(3)
        # self.remove(placeholder)



        placeholder = Tex("Show the solution and rotate it.", color=BLACK, font_size=72)
        voiceover_text = """
        The goal of the puzzle is to arrange the cubes in a row so that no colour is
        repeated along each of the four sides.
        """
        self.add(placeholder)
        with self.voiceover(text=voiceover_text) as tracker:
            self.wait(3)
        self.remove(placeholder)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = IntroductionScene2()
        scene.render()
