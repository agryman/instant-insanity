"""
This module animates the conversion of the subgraphs into a solution of the puzzle.
The scene starts with the two subgraphs on the bottom half the of the frame and nothing
in the top half. The state of the scene is determined by the puzzle and the solution number.
Recall that Carteblanche's puzzle has two solutions.
"""
from typing import cast, Sequence

from manim import Scene, tempconfig, LEFT, DOWN, RIGHT, Tex, BLACK, FadeIn, PI
from manim.typing import Point3D, Vector3D
from manim_voiceover import VoiceoverScene

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DSetCubeGapAnimorph, Puzzle3DCubeRotationAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import Puzzle, WINNING_MOVES_PUZZLE, PuzzleCubeNumber, AxisLabel, PuzzleSpec, \
    WINNING_MOVES_PUZZLE_SPEC
from instant_insanity.mobjects import labelled_subgraph
from instant_insanity.mobjects.labelled_subgraph import LabelledSubgraph, LabelledSubgraphPair
from instant_insanity.mobjects.puzzle_face_labeller import PuzzleFaceLabeller
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping, mk_edge_directions
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, DEFAULT_BUFF
from instant_insanity.mobjects.stealth_tip import CubeEdgeTip
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.helpers import morph_and_checkpoint
from instant_insanity.scenes.part_3_graph_theory.graph_theory_scene_3 import GraphTheoryScene3
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene


class GraphTheoryScene5(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    """
    This scene shows how to convert the subgraph pair into puzzle solutions.
    """
    puzzle: Puzzle
    start_centre: Point3D
    end_centre: Point3D

    def subscene_1_introduction(self) -> None:
        if self.skip(self.subscene_1_introduction):
            return

        voiceover: str = """
        The final step of the process is to convert these subgraphs
        into cube orientations which, by construction, will solve the puzzle.
        """
        self.say(voiceover)

    def subscene_2_show_puzzle(self) -> None:
        if self.skip(self.subscene_2_show_puzzle):
            return

        voiceover: str = """
        Here's the puzzle with its cubes in their starting positions.
        Recall that this arrangement is not a solution.
        Let's rotate it to show that two sides repeat red.
        """
        self.say(voiceover)

    def subscene_3_describe_face_labels(self) -> None:
        if self.skip(self.subscene_3_describe_face_labels):
            return

        voiceover:str = """
        The starting position for each cube has 
        the face labelled x on the front,
        y on the right, and z on the top.
        """
        self.say(voiceover)

    def subscene_4_discuss_cube_1(self) -> None:
        if self.skip(self.subscene_4_discuss_cube_1):
            return

        voiceover: str = """
        We need to rotate each cube to match the subgraphs.
        We'll match the front-back subgraph first and 
        then match the top-bottom subgraph.
        For each subgraph, we'll match one cube at a time.

        Let's start with cube 1 in the front-back subgraph. 
        Look for the edge labelled 1x which connects green to white.
        The starting position for each cube has its face labelled x
        facing front. Therefore, the starting position of cube 1
        already matches the front-back subgraph. No further rotation is needed.
        """
        self.say(voiceover)

    def subscene_5_discuss_cube_2(self) -> None:
        if self.skip(self.subscene_5_discuss_cube_2):
            return

        voiceover: str = """
        Next consider cube 2. It's front-back edge is labelled 2x which
        also matches its starting position. Therefore, no further rotation is needed.
        """
        self.say(voiceover)

    def subscene_6_discuss_cube_3(self) -> None:
        if self.skip(self.subscene_5_discuss_cube_2):
            return

        voiceover: str = """
        Now look at cube 3. It's front-back edge is labelled 3y so we
        need to rotate the right face into the front position.
        """
        self.say(voiceover)

    def subscene_7_discuss_cube_4(self) -> None:
        if self.skip(self.subscene_7_discuss_cube_4):
            return

        voiceover: str = """
        Wrapping up the front-back subgraph, we see that the cube 4 edge
        is labelled 4x, which is its starting position. No rotation is needed.

        At this point we have half of a solution since no colour is repeated
        on the front and back sides.
        """
        self.say(voiceover)

    def subscene_8_discuss_top_bottom_subgraph(self) -> None:
        if self.skip(self.subscene_8_discuss_top_bottom_subgraph):
            return

        voiceover: str = """
        Now let's work on the top-bottom subgraph. 
        The edge for cube 1 is labelled 1y.
        Rotate the right face to the top.
        """
        self.say(voiceover)

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        # recreate the final content of the previous scene
        puzzle: Puzzle =  WINNING_MOVES_PUZZLE
        labelled_subgraph_pair: LabelledSubgraphPair = LabelledSubgraphPair(puzzle)
        labelled_subgraph_pair.add_to_scene(self)
        labelled_subgraph_pair.add_solution_edges()
        labelled_subgraph_pair.add_edge_directions(self)

        self.subscene_1_introduction()

        # create and display the 3D puzzle
        self.wait(0.5)
        projection: Projection = mk_standard_orthographic_projection()
        puzzle3d: Puzzle3D = GraphTheoryScene3.mk_puzzle3d(puzzle, projection)
        self.add(puzzle3d)

        # add the cube visible face labels
        puzzle_face_labeller: PuzzleFaceLabeller = PuzzleFaceLabeller(self, puzzle3d)
        puzzle_face_labeller.update_puzzle_texts()
        self.wait(0.5)

        self.subscene_2_show_puzzle()

        initial_gap: float = puzzle3d.get_cube_gap()

        puzzle_face_labeller.remove_puzzle_texts()

        # contract the puzzle
        min_gap: float = DEFAULT_BUFF
        contract_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(puzzle3d, min_gap)
        morph_and_checkpoint(self, contract_animorph)

        # rotate the puzzle
        rotation: Vector3D = cast(Vector3D, RIGHT * PI / 2.0)
        rotation_animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(puzzle3d, rotation)
        for _ in range(4):
            morph_and_checkpoint(self, rotation_animorph)

        # expand the puzzle
        expand_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(puzzle3d, initial_gap)
        morph_and_checkpoint(self, expand_animorph)

        puzzle_face_labeller.update_puzzle_texts()

        self.subscene_3_describe_face_labels()

        self.subscene_4_discuss_cube_1()

        self.subscene_5_discuss_cube_2()

        self.subscene_6_discuss_cube_3()

        # TO DO: rotate cube 3 90 degrees about the DOWN axis.

        self.subscene_7_discuss_cube_4()

        # TO DO: rotate the puzzle twice by 180 degrees, pausing.

        self.subscene_8_discuss_top_bottom_subgraph()

        # TO DO: rotate cube 1 by 90 degrees about OUT

        # TO DO: discuss top-bottom cubes 2, 3, 4 then rotate all to confirm

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            self.subscene_1_introduction,
        ]

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene5()
        scene.render()
