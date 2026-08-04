from typing import Sequence

from manim import Mobject, tempconfig, Table, FadeIn, FadeOut
from manim_voiceover import VoiceoverScene, VoiceoverTracker

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.puzzle import WINNING_MOVES_PUZZLE, FaceLabel
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.face_colour_table import FaceColourTable
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin, PAGE_HEIGHT
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene

# image subpackages
INTRODUCTION: str = "introduction"
GRAPH_THEORY: str = "graph_theory"
GRAPH_THEORY_LATEX: str = GRAPH_THEORY + ".latex"

class GraphTheoryScene2(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    def subscene_2_eureka_cover(self) -> None:
        if self.skip(self.subscene_2_eureka_cover):
            return

        # cite Eureka and show its cover
        image = self.get_image("eureka-cover.png", GRAPH_THEORY)
        discussion = """
        The ingenious use of graph theory to solve Instant Insanity
        was published in the April, 1947 issue of Eureka, the journal
        of the Cambridge University Mathematical Society.
        """
        self.discuss_mobject(image, discussion)

    def subscene_2_eureka_page_1_toc(self) -> None:
        if self.skip(self.subscene_2_eureka_page_1_toc):
            return

        subpackages: str = GRAPH_THEORY
        image_filename: str = "eureka-page-1-toc.png"
        image_height: float = PAGE_HEIGHT
        image_voiceover: str = """
        Here's the table of contents of Eureka, number 9, dated April 1947.
        """
        annotated_filenames: list[str] = [
            "eureka-page-1-toc-annotated.png",
        ]
        annotated_voiceovers: list[str] = [
            """
            The solution is given in 
            "The Coloured Cubes Problem" by F. de Carteblanche on page 9.
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

    def subscene_4_eureka_page_9(self) -> None:
        if self.skip(self.subscene_4_eureka_page_9):
            return

        subpackages: str = GRAPH_THEORY
        image_height: float = PAGE_HEIGHT
        image_filename: str = "eureka-page-9.png"
        image_voiceover: str = """
        Let's look at the article.
        """

        annotated_filenames: list[str] = [
            "eureka-page-9-the-article.png",
            "eureka-page-9-naming-scheme.png",
        ]
        annotated_voiceovers: list[str] = [
            """
            The puzzle was called the Tantalizer at that time and it used the colour orange instead of blue.            
            Aside from those minor differences, it was the same as Instant Insanity.
            Another irrelevant difference is that Carteblanche asks us to stack the cubes in a vertical pile
            but we prefer to line them up in a horizontal row.
            """,
            """
            Carteblanche introduced a naming scheme for the cube faces to make referring to them easy.
            These names are given in the table at the bottom of the page.
            We'll use this naming scheme too.
            
            Note that no colour is repeated in the table rows for the front, back, right, and left faces
            so this arrangement of the cubes makes a vertical pile that solves the puzzle.
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

    def subscene_6_eureka_page_10(self) -> None:
        if self.skip(self.subscene_6_eureka_page_10):
            return

        subpackages: str = GRAPH_THEORY
        image_height: float = PAGE_HEIGHT
        image_filename: str = "eureka-page-10.png"
        image_voiceover: str = """
        The second page of the article explains how to convert the puzzle
        into a graph and how to use it to solve the puzzle.
        The graph is shown in Figure 1.
        """

        annotated_filenames: list[str] = [
            "eureka-page-10-fig-1.png",
        ]
        annotated_voiceovers: list[str] = [
            """
            The nodes of the graph represent the face colours and 
            are labelled G, R, O, and W.
            Its edges represent pairs of opposite faces and 
            are labelled by the number of the cube they belong to.
            Each edge connects the colours that occur in a pair of opposite faces.
            There are four cubes and three pairs of opposite faces in each cube
            so the graph has twelve edges.
            
            Note that the unlabelled horizontal edge from W to O should have the label 3.
    
            Later, we'll explain how to use this graph for solving the puzzle.
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

    def subscene_7_eureka_page_11(self) -> None:
        if self.skip(self.subscene_7_eureka_page_11):
            return

        subpackages: str = GRAPH_THEORY
        image_height: float = PAGE_HEIGHT
        image_filename: str = "eureka-page-11.png"
        image_voiceover: str = """
        The final page of the article contains a noteworthy statement.
        """

        annotated_filenames: list[str] = [
            "eureka-page-11-greyscale-41472.png",
        ]
        annotated_voiceovers: list[str] = [
            """
            The article claims that the chance that a random arrangement
            of the cubes solves the puzzle is one in forty-one thousand four hundred
            and seventy two, making it only half as difficult as the Instant Insanity box claims.
            """
        ]

        self.discuss_and_zoom_image(
            subpackages,
            image_filename,
            image_height,
            image_voiceover,
            annotated_filenames,
            annotated_voiceovers
        )

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

        self.subscene_2_eureka_cover()
        self.subscene_2_eureka_page_1_toc()
        self.subscene_4_eureka_page_9()
        self.subscene_5_instant_insanity_table()
        self.subscene_6_eureka_page_10()
        self.subscene_7_eureka_page_11()
        self.subscene_8_instant_insanity_box_front()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            # self.subscene_2_eureka_cover,
            # self.subscene_2_eureka_page_1_toc,
            # self.subscene_4_eureka_page_9,
            self.subscene_5_instant_insanity_table,
            # self.subscene_6_eureka_page_10,
            # self.subscene_7_eureka_page_11,
            # self.subscene_8_instant_insanity_box_front,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene2()
        scene.render()
