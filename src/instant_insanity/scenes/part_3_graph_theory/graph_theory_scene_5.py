"""
This module animates the conversion of the subgraphs into a solution of the puzzle.
The scene starts with the two subgraphs on the bottom half the of the frame and nothing
in the top half. The state of the scene is determined by the puzzle and the solution number.
"""
from typing import Sequence

from manim import tempconfig, DOWN, BLACK, Text, Indicate, AnimationGroup, OUT
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.cube_rotations import VisibleCubeTexts
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import Puzzle, WINNING_MOVES_PUZZLE, PuzzleCubeNumber, AxisLabel
from instant_insanity.mobjects.labelled_subgraph import LabelledSubgraphPair
from instant_insanity.mobjects.puzzle_face_labeller import PuzzleFaceLabeller
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, DEFAULT_BUFF
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin, INDICATE_SCALE_FACTOR, INDICATE_TEXT_COLOUR
from instant_insanity.scenes.part_3_graph_theory.graph_theory_scene_3 import GraphTheoryScene3
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene


class GraphTheoryScene5(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    """
    This scene shows how to convert the subgraph pair into puzzle solutions.
    """
    puzzle: Puzzle
    labelled_subgraph_pair: LabelledSubgraphPair
    puzzle_face_labeller: PuzzleFaceLabeller
    puzzle3d: Puzzle3D
    initial_gap: float
    min_gap: float

    def indicate_face_label(self, cube: PuzzleCubeNumber, plane: FacePlane) -> None:
        face_label: Text = self.puzzle_face_labeller.get_face_label(cube, plane)
        self.play(Indicate(face_label, scale_factor=INDICATE_SCALE_FACTOR, color=INDICATE_TEXT_COLOUR))

    def indicate_edge_label(self, plane: FacePlane, cube: PuzzleCubeNumber, axis: AxisLabel) -> None:
        edge_label: Text = self.labelled_subgraph_pair.get_edge_label(plane, cube, axis)
        self.play(Indicate(edge_label, scale_factor=INDICATE_SCALE_FACTOR, color=INDICATE_TEXT_COLOUR))

    def subscene_1_introduction(self) -> None:
        if self.skip(self.subscene_1_introduction):
            return

        voiceover: str = """
        Now we'll show how to convert these subgraphs 
        into the solution of the puzzle.
        """
        self.say(voiceover)

    def subscene_2_show_puzzle(self) -> None:
        if self.skip(self.subscene_2_show_puzzle):
            return

        voiceover: str = """
        The cubes are currently in their starting orientations.
        """
        self.say(voiceover)

    def subscene_3_describe_face_labels(self) -> None:
        if self.skip(self.subscene_3_describe_face_labels):
            return

        visible_planes: list[FacePlane] = [FacePlane.FRONT, FacePlane.RIGHT, FacePlane.TOP]

        plane_to_voiceover: dict[FacePlane, str] = {
            FacePlane.FRONT: "In this arrangement, each cube has face ex on the front side,",
            FacePlane.RIGHT: "face wy on the right side,",
            FacePlane.TOP: "and face zed on the top side.",
        }

        cube_to_visible_texts: dict[PuzzleCubeNumber, VisibleCubeTexts] = (
            self.puzzle_face_labeller.cube_to_visible_texts
        )

        plane: FacePlane
        n: PuzzleCubeNumber
        plane_to_texts: dict[FacePlane, list[Text]] = {
            plane: [
                cube_to_visible_texts[n].get_label(plane)
                for n in PuzzleCubeNumber
            ]
            for plane in visible_planes
        }

        for plane in visible_planes:
            voiceover: str = plane_to_voiceover[plane]
            texts: list[Text] = plane_to_texts[plane]
            text: Text
            indicate_texts: AnimationGroup = AnimationGroup(
                *[Indicate(text, scale_factor=INDICATE_SCALE_FACTOR, color=INDICATE_TEXT_COLOUR) for text in texts],
                lag_ratio=0.15
            )
            self.say(voiceover)
            self.play(indicate_texts, runtime=2.0)

    def subscene_4_discuss_matching(self) -> None:
        if self.skip(self.subscene_4_discuss_matching):
            return

        voiceover: str
        voiceover = """
        We need to match each cube to the orientations given in the subgraphs.
        We'll match the front-back then the top-bottom.
        """
        self.say(voiceover)

    def subscene_4_discuss_front_cube_1(self) -> None:
        if self.skip(self.subscene_4_discuss_front_cube_1):
            return

        voiceover: str
        voiceover = """
        Let's get started on the front-back subgraph. 
        """
        self.say(voiceover)
        self.labelled_subgraph_pair.indicate_label(self, FacePlane.FRONT)

        voiceover = """
        Look at edge 1 ex which connects green to white.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.FRONT, PuzzleCubeNumber.ONE, AxisLabel.X)

        voiceover = """
        We need face ex, which is green, on the front
        but it's already there so we don't need to rotate it.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.ONE, FacePlane.FRONT)

    def subscene_4_discuss_front_cube_2(self) -> None:
        if self.skip(self.subscene_4_discuss_front_cube_2):
            return

        voiceover: str
        voiceover = """
        Next consider edge 2 ex which connects red to green.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.FRONT, PuzzleCubeNumber.TWO, AxisLabel.X)

        voiceover = """
        We need face ex, which is red, on the front
        but it's already there so we don't need to rotate it.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.TWO, FacePlane.FRONT)

    def subscene_4_discuss_front_cube_3(self) -> None:
        if self.skip(self.subscene_4_discuss_front_cube_2):
            return

        voiceover: str = """
        Now look at edge 3 wy which connects white to blue.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.FRONT, PuzzleCubeNumber.THREE, AxisLabel.Y)

        voiceover: str = """
        We need face wy, which is white, on the front but it's 
        currently on the right so we need to rotate it.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.THREE, FacePlane.RIGHT)

    def subscene_4_discuss_front_cube_4(self) -> None:
        if self.skip(self.subscene_4_discuss_front_cube_4):
            return

        voiceover: str
        voiceover= """
        Wrapping up the front-back subgraph, 
        look at edge 4 ex which connects blue to red.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.FRONT, PuzzleCubeNumber.FOUR, AxisLabel.X)

        voiceover = """
        We need face ex, which is blue, on the front but it's 
        already there so we don't need to rotate it.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.FOUR, FacePlane.FRONT)

        voiceover = """
        We have now completed matching the front and back sides to the front-back subgraph.
        From now on, we'll only rotate the cubes about the front-back axis 
        so that we don't change their front and back faces.

        At this point we're halfway to the solution.
        It remains to match the top and bottom sides to the top-bottom subgraph.
        Let's get started.
        """
        self.say(voiceover)

        self.labelled_subgraph_pair.indicate_label(self, FacePlane.TOP)

    def subscene_5_discuss_top_cube_1(self) -> None:
        if self.skip(self.subscene_5_discuss_top_cube_1):
            return

        voiceover: str

        voiceover = """
        Look at edge 1 wy which connects blue to red.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.TOP, PuzzleCubeNumber.ONE, AxisLabel.Y)

        voiceover = """
        We need face wy, which is blue, on the top side but it's currently on the right so we need to rotate it.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.ONE, FacePlane.RIGHT)

    def subscene_5_discuss_top_cube_2(self) -> None:
        if self.skip(self.subscene_5_discuss_top_cube_2):
            return

        voiceover: str
        voiceover = """
        Now, look at edge 2 zed which connects green to white.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.TOP, PuzzleCubeNumber.TWO, AxisLabel.Z)

        voiceover = """
        We need face zed, which is white, on the bottom side but it's currently on the top so we need to rotate it.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.TWO, FacePlane.TOP)

    def subscene_5_discuss_top_cube_3(self) -> None:
        if self.skip(self.subscene_5_discuss_top_cube_3):
            return

        voiceover: str
        voiceover = """
        Next, look at edge 3 zed which connects red to green.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.TOP, PuzzleCubeNumber.THREE, AxisLabel.Z)

        voiceover = """
        We need face zed, which is green, on the bottom side but it's currently on the top so we need to rotate it.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.THREE, FacePlane.TOP)

    def subscene_5_discuss_top_cube_4(self) -> None:
        if self.skip(self.subscene_5_discuss_top_cube_4):
            return

        voiceover: str
        voiceover = """
        Finally, look at edge 4 zed which connects white to blue.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.TOP, PuzzleCubeNumber.FOUR, AxisLabel.Z)

        voiceover = """
        We need face zed, which is blue, on the bottom side but it's currently on the top so we need to rotate it.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.FOUR, FacePlane.TOP)

    def subscene_6_conclusion(self) -> None:
        if self.skip(self.subscene_6_conclusion):
            return

        voiceover: str

        voiceover = """
        We've oriented all the cubes to match the subgraphs.
        Let's roll the cubes to confirm that we have solved the puzzle.
        """
        self.say(voiceover)
        self.puzzle_face_labeller.roll_puzzle()

        voiceover = """
        We have successfully converted the subgraphs into the solution.
        
        You now know some graph theory and how to use it to solve Instant Insanity!
        This concludes the mathematical portion of the video.
        Stay tuned for a brief history of the puzzle and Carteblanche.
        """
        self.say(voiceover)

    def construct(self):
        # self.set_speech_service(GCPTextToSpeechService())
        self.set_speech_service(RecorderService(transcription_model=None))
        self.add_grid(False)

        # recreate the final content of the previous scene
        puzzle: Puzzle =  WINNING_MOVES_PUZZLE
        self.puzzle = puzzle

        labelled_subgraph_pair: LabelledSubgraphPair = LabelledSubgraphPair(puzzle)
        self.labelled_subgraph_pair = labelled_subgraph_pair

        labelled_subgraph_pair.add_to_scene(self)
        labelled_subgraph_pair.add_solution_edges()
        labelled_subgraph_pair.add_edge_directions(self)

        # create and display the 3D puzzle
        projection: Projection = mk_standard_orthographic_projection()
        puzzle3d: Puzzle3D = GraphTheoryScene3.mk_puzzle3d(puzzle, projection)
        self.puzzle3d = puzzle3d
        self.add(puzzle3d)

        initial_gap: float = puzzle3d.get_cube_gap()
        self.initial_gap = initial_gap

        min_gap: float = DEFAULT_BUFF
        self.min_gap = min_gap

        # add the cube visible face labels
        puzzle_face_labeller: PuzzleFaceLabeller = PuzzleFaceLabeller(self, puzzle3d)
        self.puzzle_face_labeller = puzzle_face_labeller
        puzzle_face_labeller.update_puzzle_texts()

        self.subscene_1_introduction()
        self.subscene_2_show_puzzle()
        self.subscene_3_describe_face_labels()
        self.subscene_4_discuss_matching()
        self.subscene_4_discuss_front_cube_1()
        self.subscene_4_discuss_front_cube_2()

        self.subscene_4_discuss_front_cube_3()
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.THREE, DOWN)

        self.subscene_4_discuss_front_cube_4()

        self.subscene_5_discuss_top_cube_1()
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.ONE, OUT)

        self.subscene_5_discuss_top_cube_2()
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.TWO, OUT)
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.TWO, OUT)

        self.subscene_5_discuss_top_cube_3()
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.THREE, OUT)
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.THREE, OUT)

        self.subscene_5_discuss_top_cube_4()
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.FOUR, OUT)
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.FOUR, OUT)

        self.subscene_6_conclusion()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            self.subscene_1_introduction,
            self.subscene_2_show_puzzle,
            self.subscene_3_describe_face_labels,
            self.subscene_4_discuss_matching,
            self.subscene_4_discuss_front_cube_1,
            self.subscene_4_discuss_front_cube_2,
            self.subscene_4_discuss_front_cube_3,
            self.subscene_4_discuss_front_cube_4,
            self.subscene_5_discuss_top_cube_1,
            self.subscene_5_discuss_top_cube_2,
            self.subscene_5_discuss_top_cube_3,
            self.subscene_5_discuss_top_cube_4,
            self.subscene_6_conclusion,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene5()
        scene.render()
