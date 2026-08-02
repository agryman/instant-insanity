from typing import Sequence

from manim import Mobject, tempconfig
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin, PAGE_HEIGHT
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene

# image subpackages
INTRODUCTION: str = "introduction"
GRAPH_THEORY: str = "graph_theory"
GRAPH_THEORY_LATEX: str = GRAPH_THEORY + ".latex"

class GraphTheoryScene2(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    def subscene_1_us_patent(self) -> None:
        if self.skip(self.subscene_1_us_patent):
            return

        # TO DO: move the US Patent to History
        # show the US Patent

        subpackages:str = GRAPH_THEORY

        image_filename:str = "us-patent.png"
        image_height: float = PAGE_HEIGHT
        image_voiceover:str = """
        Although it was released in 1967 by Parker Brothers, Instant Insanity had much earlier origins.
        """

        annotated_filename:str = "us-patent-annotated.png"
        annotated_voiceover:str = """
        A US patent for the puzzle was issued to Frederick Schossow in 1900.
        Instead of face colours, his puzzle used the playing
        card suit symbols clubs, diamonds, hearts, and spades.
        The puzzle might even have originated in some other country before 1900.
        """

        self.discuss_and_zoom_image(
            subpackages,
            image_filename,
            image_height,
            image_voiceover,
            [annotated_filename],
            [annotated_voiceover])

    def subscene_2_eureka_cover(self) -> None:
        if self.skip(self.subscene_2_eureka_cover):
            return

        # cite Eureka and show its cover
        image = self.get_image("eureka-cover.png", GRAPH_THEORY)
        discussion = """
        The ingenious use of graph theory to solve Instant Insanity
        was published in the April, 1947 issue of Eureka, the Archimedeans Journal.
        The Archimedeans is the Cambridge University Mathematical Society.
        """
        self.discuss_mobject(image, discussion)

    def subscene_2_eureka_page_1_toc(self) -> None:
        if self.skip(self.subscene_2_eureka_page_1_toc):
            return

        subpackages: str = GRAPH_THEORY
        image_filename: str = "eureka-page-1-toc.png"
        image_height: float = PAGE_HEIGHT
        image_voiceover: str = """
        This is the table of contents of Eureka, number 9, dated April 1947.
        """
        annotated_filename: str = "eureka-page-1-toc-annotated.png"
        annotated_voiceover: str = """
        The ingenious graph theory solution to the puzzle 
        was presented in the article "The Coloured Cubes Problem" by F. de Carteblanche on page 9.
        """
        self.discuss_and_zoom_image(
            subpackages,
            image_filename,
            image_height,
            image_voiceover,
            [annotated_filename],
            [annotated_voiceover]
        )

    def subscene_3_trinity_four(self) -> None:
        if self.skip(self.subscene_3_trinity_four):
            return

        # TO DO: move to History
        # see https://www.squaring.net/history_theory/brooks_smith_stone_tutte.html

        subpackages: str = GRAPH_THEORY
        image_height: float = PAGE_HEIGHT
        image_filename: str = "trinity-four-med.jpg"
        image_voiceover: str = """
        F. de Carteblanche was a pseudonym used by a group of Cambridge undergraduates
        known as the Trinity Four.
        They published recreational mathematical articles. 
        They also used the pseudonym Blanche Descartes.
        Rumour has it that Blanche Descartes was married to F. de Carteblanche.
        
        The group members were:
        """

        annotated_filenames: list[str] = [
            "trinity-four-med-leonard-brooks.jpg",
            "trinity-four-med-cedric-smith.jpg",
            "trinity-four-med-arthur-stone.jpg",
            "trinity-four-med-bill-tutte.jpg",
        ]
        annotated_voiceovers: list[str] = [
            "Leonard Brooks",
            "Cedric Smith",
            "Arthur Stone",
            """
            and Bill Tutt.
            Tutt became a legendary codebreaker at Bletchley Park during World War 2.
            After the war he moved to the University of Waterloo in Canada and
            became a highly influential graph theorist.
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

    def subscene_4_eureka_page_9(self) -> None:
        if self.skip(self.subscene_4_eureka_page_9):
            return

        image: Mobject = self.get_image("eureka-page-9-cropped.png", GRAPH_THEORY)
        discussion: str = """
        Let's look at the article.
        The puzzle was called the Tantalizer at that time and it used the colour orange instead of blue.
        Aside from those minor differences, it was the same as Instant Insanity.

        Carteblanche introduced a naming scheme for the cube faces for easy reference.
        These names are given in the table at the bottom of the page.
        We'll use this naming scheme too.

        Carteblache says he is not sure that his table matches the commercial version.
        His uncertainty is well founded since his table has two distinct solutions!
        Carteblanche probably just dreamed up the table as an example for the article.
        After viewing this video you'll know how to easily find both solutions.
        """
        self.discuss_mobject(image, discussion)

    def subscene_5_instant_insanity_table(self) -> None:
        if self.skip(self.subscene_5_instant_insanity_table):
            return

        # show the table for Instant Insanity
        image: Mobject = self.get_image("instant-insanity-table.png", GRAPH_THEORY_LATEX)
        discussion: str = """
        Here is the face colour table for Instant Insanity.
        Carteblache's face-naming scheme is based on imposing x y z axes on each cube
        The x axis points from back to front,
        the y axis points from left to right,
        and the z axis points from bottom to top.
        Each face is perpendicular to the axis given by the face name.
        Primes are added to the back, left, and bottom faces.
        Here front, back, right, left, top, and bottom refer to the positions of the faces in some arbitrary
        starting orientation. 
        When you rotate a cube the positions of its faces change but the labels go along for the ride.
        Similarly, the cube numbers 1, 2, 3, and 4 refer to the positions of the cubes in some arbitrary
        starting order and this order never changes.
        """
        self.discuss_mobject(image, discussion)

    def subscene_6_eureka_page_10(self) -> None:
        if self.skip(self.subscene_6_eureka_page_10):
            return

        image: Mobject = self.get_image("eureka-page-10-fig-1.png", GRAPH_THEORY)
        discussion: str = """
        The second page of the article explains the opposite-face graph
        and illustrates it in figure 1. The nodes represent
        the face colours. The edges represent pairs of opposite faces
        and are labelled by the number of the cube they belong to.
        Note that the unlabelled horizontal edge from W to O should have the label 3.
        Later, we'll explain how to use this graph for solving the puzzle.
        """
        self.discuss_mobject(image, discussion)

    def subscene_7_eureka_page_11(self) -> None:
        if self.skip(self.subscene_7_eureka_page_11):
            return

        image: Mobject = self.get_image("eureka-page-11-cropped.png", GRAPH_THEORY)
        discussion: str = """
        The final page of the article reiterates the claim that the
        solution is effectively unique and states that the chance of
        finding the solution by a random arrangement is one in forty-one thousand four hundred and seventy-two.
        This is another way of saying that there are forty-one thousand four hundred and seventy-two combinations.
        """
        self.discuss_mobject(image, discussion)

    def subscene_8_instant_insanity_box_front(self) -> None:
        if self.skip(self.subscene_8_instant_insanity_box_front):
            return

        image: Mobject = self.get_image("instant-insanity-box-front.png", INTRODUCTION)
        discussion: str = """
        The Carteblanche claim of forty-one thousand four hundred and seventy-two combinations
        is inconsistent with the claim on the Instant Insanity box
        which states there are eighty-two thousand nine hundred and forty-four combinations.
        The Instant Insanity claim is exactly twice the Carteblanche claim.
        Which number do you think is correct?
        We'll settle this question later.
        """
        self.discuss_mobject(image, discussion)

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        topic: Mobject
        image: Mobject
        discussion: str

        self.subscene_1_us_patent()
        self.subscene_2_eureka_cover()
        self.subscene_2_eureka_page_1_toc()
        self.subscene_3_trinity_four()
        self.subscene_4_eureka_page_9()
        self.subscene_5_instant_insanity_table()
        self.subscene_6_eureka_page_10()
        self.subscene_7_eureka_page_11()
        self.subscene_8_instant_insanity_box_front()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            # self.subscene_1_us_patent,
            # self.subscene_2_eureka_cover,
            # self.subscene_2_eureka_page_1_toc,
            self.subscene_3_trinity_four,
            # self.subscene_4_eureka_page_9,
            # self.subscene_5_instant_insanity_table,
            # self.subscene_6_eureka_page_10,
            # self.subscene_7_eureka_page_11,
            # self.subscene_8_instant_insanity_box_front,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene2()
        scene.render()
