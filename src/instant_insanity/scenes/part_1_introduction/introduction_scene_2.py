from typing import cast, Sequence

from manim import tempconfig, PI, DOWN, RIGHT, Mobject, FadeIn, ORIGIN, FadeOut, Table, UP, LEFT, Text, Indicate, \
    BLACK
from manim.typing import Vector3D
from manim_voiceover import VoiceoverScene

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DCubeRotationAnimorph, Puzzle3DSetCubeGapAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, PuzzleCubeNumber, WINNING_MOVES_PUZZLE, \
    Puzzle, AxisLabel
from instant_insanity.mobjects.face_colour_table import FaceColourTable
from instant_insanity.mobjects.image import INTRODUCTION
from instant_insanity.mobjects.opposite_face_graph import EdgeToSubgraphMapping, OppositeFaceGraph
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, mk_standard_puzzle3d, DEFAULT_BUFF
from instant_insanity.mobjects.puzzle_face_labeller import PuzzleFaceLabeller
# from instant_insanity.scenes import discussion
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin, PAGE_HEIGHT
from instant_insanity.scenes.helpers import morph_and_checkpoint
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene

ROTATION_RUNTIME: float = 0.5
ROTATION_WAIT_TIME: float = 0.1


class IntroductionScene2(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    """
    This scene shows the puzzle cubes and explains the goal of the puzzle.
    It leads into the graph theory scenes.
    """

    puzzle: Puzzle
    puzzle3d: Puzzle3D
    initial_gap: float
    min_gap: float
    puzzle_face_labeller: PuzzleFaceLabeller
    face_colour_table: FaceColourTable

    def subscene_1_describe_puzzle(self):
        if self.skip(self.subscene_1_describe_puzzle):
            return

        voiceover: str

        voiceover = """
        The Instant Insanity puzzle consists of four cubes whose faces are coloured 
        red, white, blue, or green.
        """
        self.say(voiceover)

    def subscene_2_describe_goal(self):
        if self.skip(self.subscene_2_describe_goal):
            return

        voiceover: str

        voiceover = """
        The puzzle challenges us to arrange the cubes in a row so that 
        each side contains all four colours.
        
        Let's see if this arrangement is a solution.
        """
        self.say(voiceover)

        # set the cube gap
        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.min_gap)
        morph_and_checkpoint(self, gap_animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        voiceover = """
        The front side looks good.
        """
        self.say(voiceover)

        right_rotation: Vector3D = cast(Vector3D, RIGHT * PI / 2.0)
        right_rotation_animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, right_rotation)
        morph_and_checkpoint(self, right_rotation_animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        voiceover = """
        So does the top side.
        """
        self.say(voiceover)

        morph_and_checkpoint(self, right_rotation_animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        voiceover = """
        The back side repeats red so this arrangement is not a solution.
        """
        self.say(voiceover)

        morph_and_checkpoint(self, right_rotation_animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        voiceover = """
        The bottom side also repeats red.
        Only two of the four sides satisfy the goal.
        """
        self.say(voiceover)

        morph_and_checkpoint(self, right_rotation_animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.initial_gap)
        morph_and_checkpoint(self, gap_animorph)

        voiceover = """
        This arrangement is not a solution so
        we have to rotate individual cubes until we get four colours on each side.
        
        How hard could that be?
        """
        self.say(voiceover)

    def subscene_3_instant_insanity_box_front(self) -> None:
        if self.skip(self.subscene_3_instant_insanity_box_front):
            return

        subpackages: str = INTRODUCTION
        image_height: float = PAGE_HEIGHT
        image_filename: str = "instant-insanity-box-front.png"
        image_voiceover: str = """
        Here's the Instant Insanity box.
        """

        annotated_filenames: list[str] = [
            "instant-insanity-box-front-greyscale-82944-wide.png",
        ]
        annotated_voiceovers: list[str] = [
            """
            It claims there are eighty-two thousand nine hundred
            and forty-four combinations so we can't possibly try every one of them.
            We need a more intelligent search strategy.
            """,
        ]

        self.remove(self.puzzle3d)
        self.discuss_and_zoom_image(
            subpackages,
            image_filename,
            image_height,
            image_voiceover,
            annotated_filenames,
            annotated_voiceovers
        )
        self.add(self.puzzle3d)

    def subscene_4_lead_into_graph_theory(self):
        if self.skip(self.subscene_4_lead_into_graph_theory):
            return

        voiceover: str
        # set the cube gap
        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.initial_gap)
        morph_and_checkpoint(self, gap_animorph)

        voiceover = """
        One day a math professor visited Arthur's high school and 
        gave an introductory lecture on graph theory.
        He ended the talk by showing an ingenious graph-theoretic method for solving Instant Insanity.
        We'll describe that method in this video.
        """
        self.say(voiceover)

        voiceover = """
        We start by assigning labels to all the cube faces so we can refer to them more easily.
        """
        self.say(voiceover)

        # show the labels
        self.puzzle_face_labeller.update_puzzle_texts()
        voiceover = """
        We've assigned the lowercase letters ex, wy, and zed to the front, right, and top faces.
        These letters correspond to the axes of a 3-dimensional coordinate system centered on each cube.
        The following table summarizes the labelling scheme.
        """
        self.say(voiceover)

        # TODO: shift the puzzle up
        # hide the labels
        self.puzzle_face_labeller.remove_puzzle_texts()
        # self.remove(self.puzzle3d)
        puzzle3d: Puzzle3D = self.puzzle3d
        self.play(puzzle3d.animate.shift(UP * 2))

        # show the table
        table: Table = self.face_colour_table.table
        table.scale(0.4)
        table.shift(DOWN * 1.5)
        self.play(FadeIn(table))

        voiceover = """
        We've assigned the numbers one through four to the cubes going from left to right.
        We've also assigned primed letters to the faces opposite the visible faces.
        For example, the back face of each cube is labelled ex prime since it is opposite the front face.
        """
        self.say(voiceover)

        # hide the table
        # self.play(FadeOut(self.face_colour_table.table))
        self.play(table.animate.shift(LEFT * 3.0))

        # create the full Winning Moves opposite-face graph
        full_subgraph: EdgeToSubgraphMapping = OppositeFaceGraph.mk_subgraph_for_flag(True)
        wm_graph: OppositeFaceGraph = OppositeFaceGraph(WINNING_MOVES_PUZZLE, ORIGIN)
        wm_graph.set_subgraph(full_subgraph)

        wm_graph.shift(RIGHT * 3.0 + DOWN * 1.5)
        self.play(FadeIn(wm_graph))
        voiceover = """
        Here's the graph that represents the puzzle.
        We call it the opposite-face graph.
        """
        self.say(voiceover)

        voiceover = """
        A graph is a set of nodes connected by edges.
        Each node represents one of the four face colours.
        Each edge represents a pair of opposite faces and connects their colours.
        The edges are labelled with the cube number and the face axis letter which is an uppercase ex, wy, or zed.
        For example, look at the edge labelled 1 ex.
        """
        self.say(voiceover)

        # Indicate edge 1X
        edge_label_1x: Text = wm_graph.get_edge_label(PuzzleCubeNumber.ONE, AxisLabel.X)
        self.play(Indicate(edge_label_1x, scale_factor=1.5, color=BLACK))

        voiceover = """
        This edge represents the ex axis pair of faces in cube 1.
        One face of this pair is green and the other is white.
        
        There are four cubes and each cube has three pairs of opposite faces so
        altogether there are twelve edges in the graph.

        If you enjoy solving puzzles, and are curious about graph theory, then this video is for you.
        """
        self.say(voiceover)
        self.play(FadeOut(wm_graph), FadeOut(table))
        self.remove(puzzle3d)

        topic: Mobject = self.mk_topic("Instant Insanity - A Puzzling Introduction to Graph Theory")
        discussion = """        
        Welcome to: Instant Insanity - A Puzzling Introduction to Graph Theory!
        """
        self.discuss_mobject(topic, discussion)

        self.add(self.puzzle3d)
        self.wait()

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        # create and display the 3D puzzle
        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        puzzle: Puzzle = WINNING_MOVES_PUZZLE
        projection: Projection = mk_standard_orthographic_projection()

        self.puzzle = puzzle
        self.puzzle3d = mk_standard_puzzle3d(puzzle_spec, projection, centre=True)
        self.initial_gap = self.puzzle3d.get_cube_gap()
        self.min_gap = DEFAULT_BUFF
        self.add(self.puzzle3d)

        self.face_colour_table = FaceColourTable(puzzle)
        self.puzzle_face_labeller = PuzzleFaceLabeller(self, self.puzzle3d)

        self.subscene_1_describe_puzzle()
        self.subscene_2_describe_goal()
        self.subscene_3_instant_insanity_box_front()
        self.subscene_4_lead_into_graph_theory()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            # self.subscene_1_describe_puzzle,
            # self.subscene_2_describe_goal,
            # self.subscene_3_instant_insanity_box_front,
            self.subscene_4_lead_into_graph_theory,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = IntroductionScene2()
        scene.render()
