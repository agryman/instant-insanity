from typing import Sequence

from manim import tempconfig
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin, PAGE_HEIGHT
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene

GRAPH_THEORY: str = "graph_theory"

class HistoryScene1(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    def subscene_1_us_patent(self) -> None:
        if self.skip(self.subscene_1_us_patent):
            return

        # show the US Patent

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
            
            The puzzle might have originated elsewhere before 1900.
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

    def subscene_2_trinity_four(self) -> None:
        if self.skip(self.subscene_2_trinity_four):
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
            "Leonard Brooks, the L in Blanche",
            "Arthur Stone, the A in Blanche",
            "Cedric Smith, the C in Blanche",
            """
            and Bill Tutt, the B in Blanche.
            Tutt became a legendary codebreaker at Bletchley Park during World War 2.
            After the war he moved to Canada and, after many years at the 
            University of Toronto, he helped establish 
            the Department of Combinatorics and Optimization in 
            the Faculty of Mathematics 
            at the University of Waterloo
            He became a highly influential graph theorist.
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

        self.subscene_1_us_patent()
        self.subscene_2_trinity_four()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            # self.subscene_1_us_patent,
            # self.subscene_2_trinity_four,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = HistoryScene1()
        scene.render()
