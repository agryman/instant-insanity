from typing import Sequence

from manim import Mobject, tempconfig, Table, FadeIn, FadeOut
from manim_voiceover import VoiceoverScene, VoiceoverTracker

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.puzzle import WINNING_MOVES_PUZZLE, FaceLabel
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.face_colour_table import FaceColourTable
from instant_insanity.scenes.coordinate_grid import GridMixin
# from instant_insanity.mobjects.zoom_image import GRAPH_THEORY, INTRODUCTION
from instant_insanity.scenes.discussion import DiscussionMixin, PAGE_HEIGHT
from instant_insanity.mobjects.image import INTRODUCTION
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene


class GraphTheoryScene2(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):

    def subscene_5_instant_insanity_table(self) -> None:
        if self.skip(self.subscene_5_instant_insanity_table):
            return

        # show the table for Instant Insanity
        # image: Mobject = self.get_image("instant-insanity-table.png", GRAPH_THEORY_LATEX)
        face_colour_table: FaceColourTable = FaceColourTable(WINNING_MOVES_PUZZLE)
        table: Table = face_colour_table.table
        self.play(FadeIn(table))

        discussion: str

        discussion = """
        Here's the face colour table for our starting arrangement of Instant Insanity.
        We simply picked a random left-to-right order for the cubes and 
        a random orientation for each cube.
        The cube numbers 1, 2, 3, and 4 label the left-to-right positions of the cubes. 
        We never change this order.
        """
        self.say(discussion)

        discussion = """
        Since we are arranging the cubes in a left-to-right row,
        a solution must not repeat and colours on the front, back, top, and bottom sides.
        Let's check the table.
        """
        self.say(discussion)

        tracker: VoiceoverTracker
        # assert isinstance(self, VoiceoverScene)
        with self.voiceover(text="The front side has no repeated colours.") as tracker:
            face_colour_table.indicate_data_row(self, FaceLabel.X)
            voiceover_wait(self, tracker)

        with self.voiceover(text="Red is repeated on the back side.") as tracker:
            face_colour_table.indicate_data_row(self, FaceLabel.X_PRIME)

        with self.voiceover(text="The top side has no repeated colours.") as tracker:
            face_colour_table.indicate_data_row(self, FaceLabel.Z)

        with self.voiceover(text="Again, red is repeated on the bottom.") as tracker:
            face_colour_table.indicate_data_row(self, FaceLabel.Z_PRIME)

        discussion = """
        Therefore, unlike the table in the Carteblanche article, 
        our starting arrangement is not a solution.
        """
        self.say(discussion)

        # self.discuss_mobject(face_colour_table.table, discussion)
        self.play(FadeOut(table))

    def subscene_8_instant_insanity_box_front(self) -> None:
        if self.skip(self.subscene_8_instant_insanity_box_front):
            return

        subpackages: str = INTRODUCTION
        image_height: float = PAGE_HEIGHT
        image_filename: str = "instant-insanity-box-front.png"
        image_voiceover: str = """
        Here's the Instant Insanity box again..
        """

        annotated_filenames: list[str] = [
            "instant-insanity-box-front-greyscale-82944-wide.png",
        ]
        annotated_voiceovers: list[str] = [
            """
            It claims that there are eighty-two thousand nine hundred and forty-four combinations.
            """,
        ]

        self.discuss_and_zoom_image(
            subpackages,
            image_filename,
            image_height,
            image_voiceover,
            annotated_filenames,
            annotated_voiceovers
        )

        topic: Mobject = self.mk_topic(r"$82{,}944 = 2 \times 41{,}472$")
        discussion: str = """
        The Instant Insanity claim is exactly twice the Carteblanche claim.
    
        Next we'll show that the true number of essentially distinct combinations is
        in fact forty-one thousand four hundred and seventy-two as Carteblanche claimed.
        """
        self.discuss_mobject(topic, discussion)

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        topic: Mobject
        image: Mobject
        discussion: str

        self.subscene_5_instant_insanity_table()
        self.subscene_8_instant_insanity_box_front()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            self.subscene_5_instant_insanity_table,
            self.subscene_8_instant_insanity_box_front,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene2()
        scene.render()
