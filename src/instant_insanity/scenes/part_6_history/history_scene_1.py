from typing import Sequence

from manim import tempconfig
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.mobjects.image import GRAPH_THEORY
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin, PAGE_HEIGHT
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene


class HistoryScene1(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    def subscene_10_us_patent(self) -> None:
        if self.skip(self.subscene_10_us_patent):
            return

        # show the US Patent
        # https://patents.google.com/patent/US646463A/en

        subpackages:str = GRAPH_THEORY

        image_filename:str = "us-patent.png"
        image_height: float = PAGE_HEIGHT
        image_voiceover:str = """
        Although it was released in 1967 by Parker Brothers, Instant Insanity had much earlier origins.
        """

        annotated_filenames: list[str] = ["us-patent-annotated.png"]
        annotated_voiceovers: list[str] = [
            """
            A US patent for the puzzle was issued to Frederick Schossow in 1900.
            Instead of face colours, his puzzle used the symbols for the suits in a deck of playing cards.
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

    def subscene_20_eureka_cover(self) -> None:
        if self.skip(self.subscene_20_eureka_cover):
            return

        # https://archim.soc.srcf.net/publications/

        # cite Eureka and show its cover
        image = self.get_image("eureka-cover.png", GRAPH_THEORY)
        discussion = """
        The ingenious use of graph theory to solve Instant Insanity
        was published in April, 1947 in Eureka, the journal
        of the Cambridge University Mathematical Society.
        """
        self.discuss_mobject(image, discussion)

    def subscene_21_eureka_page_1_toc(self) -> None:
        if self.skip(self.subscene_21_eureka_page_1_toc):
            return

        subpackages: str = GRAPH_THEORY
        image_filename: str = "eureka-page-1-toc.png"
        image_height: float = PAGE_HEIGHT
        image_voiceover: str = """
        Here's the table of contents of issue number 9.
        """
        annotated_filenames: list[str] = [
            "eureka-page-1-toc-annotated.png",
        ]
        annotated_voiceovers: list[str] = [
            """
            The solution is given in the article titled
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

    def subscene_22_eureka_page_9(self) -> None:
        if self.skip(self.subscene_22_eureka_page_9):
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
            Another minor difference is that Carteblanche asks us to stack the cubes in a vertical pile
            but we prefer to arrange them in a horizontal row.
            """,
            """
            Here's the face colour table for Carteblanche's puzzle.
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

    def subscene_23_eureka_page_10(self) -> None:
        if self.skip(self.subscene_23_eureka_page_10):
            return

        subpackages: str = GRAPH_THEORY
        image_height: float = PAGE_HEIGHT
        image_filename: str = "eureka-page-10.png"
        image_voiceover: str = """
        The second page of the article explains how to convert the puzzle
        into an opposite-face graph and how to use the graph to solve the puzzle.
        The graph is shown in Figure 1.
        """

        annotated_filenames: list[str] = [
            "eureka-page-10-fig-1.png",
        ]
        annotated_voiceovers: list[str] = [
            """
            Note that the unlabelled horizontal edge from W to O comes from cube 3.
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

    def subscene_24_eureka_page_11(self) -> None:
        if self.skip(self.subscene_24_eureka_page_11):
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

    def subscene_30_trinity_four(self) -> None:
        if self.skip(self.subscene_30_trinity_four):
            return

        # image obtained from https://www.squaring.net/history_theory/brooks_smith_stone_tutte.html

        subpackages: str = GRAPH_THEORY
        image_height: float = PAGE_HEIGHT
        image_filename: str = "trinity-four-med.jpg"
        image_voiceover: str = """
        F. de Carteblanche was a collaborative pseudonym used by a group of Cambridge undergraduates
        known as the Trinity Four.
        They published recreational mathematical articles. 
        They also published under the pseudonym Blanche Descartes.
        The fictional backstory was that Blanche Descartes and F. de Carteblanche were married to each other.

        The Trinity Four members were:
        """

        annotated_filenames: list[str] = [
            "trinity-four-med-leonard-brooks.jpg",
            "trinity-four-med-arthur-stone.jpg",
            "trinity-four-med-cedric-smith.jpg",
            "trinity-four-med-bill-tutte.jpg",
        ]
        annotated_voiceovers: list[str] = [
            "Leonard Brooks",
            "Arthur Stone",
            "Cedric Smith",
            """
            and Bill Tutt.
            
            Bill, Leonard, Arthur, and Cedric were the B, L, A, and C in Blanche.
            
            Tutt became a legendary codebreaker at Bletchley Park during World War 2
            where he cracked the Lorenz cipher.
            After the war he moved to Canada and, after spending many years at the 
            University of Toronto, he helped establish 
            the Department of Combinatorics and Optimization in 
            the Faculty of Mathematics 
            at the University of Waterloo
            He was a highly influential graph theorist.
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

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        self.subscene_10_us_patent()

        self.subscene_20_eureka_cover()
        self.subscene_21_eureka_page_1_toc()
        self.subscene_22_eureka_page_9()
        self.subscene_23_eureka_page_10()
        self.subscene_24_eureka_page_11()

        self.subscene_30_trinity_four()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            # self.subscene_10_us_patent,
            # self.subscene_20_eureka_cover,
            # self.subscene_21_eureka_page_1_toc,
            # self.subscene_22_eureka_page_9,
            # self.subscene_23_eureka_page_10,
            # self.subscene_24_eureka_page_11,
            # self.subscene_30_trinity_four,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = HistoryScene1()
        scene.render()
