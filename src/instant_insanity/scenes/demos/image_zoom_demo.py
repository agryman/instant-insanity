"""
This module demonstrates how to zoom in on a rectangular region of an image.

An ImageMobject cannot be clipped, so instead of cutting the region out of the
image we cover everything else with a spotlight mask, namely a large rectangle
that has the region punched out of it. Fading the mask in makes the rest of the
image disappear. The mask and the image are then scaled up together, which keeps
the hole locked onto the same part of the image.
"""
from typing import Sequence

from manim import tempconfig
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin, PAGE_HEIGHT
from instant_insanity.mobjects.image import ImagesPath, EUREKA_SOURCE
from instant_insanity.scenes.subscene import Subscene, SubsceneMixin

GRAPH_THEORY: str = "graph_theory"
EUREKA_PAGE_1_TOC: str = "eureka-page-1-toc.png"
EUREKA_PAGE_1_TOC_ANNOTATED: str = "eureka-page-1-toc-annotated.png"

IMAGES_PATH: ImagesPath = ImagesPath()

class ImageZoomDemo(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    def get_playlist(self) -> Sequence[Subscene]:
        return ()

    def construct(self) -> None:
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        self.subscene_2_eureka_toc()

    def subscene_2_eureka_toc(self) -> None:
        if self.skip(self.subscene_2_eureka_toc):
            return

        subpackages: str = GRAPH_THEORY
        image_filename: str = EUREKA_PAGE_1_TOC
        image_source: str = EUREKA_SOURCE
        image_height: float = PAGE_HEIGHT
        image_voiceover: str = """
        This is the table of contents of Eureka, number 9, dated April 1947.
        """
        annotated_filename: str = EUREKA_PAGE_1_TOC_ANNOTATED
        annotated_voiceover: str = """
        The Coloured Cubes Problem by F. de Carteblanche is on page 9.
        """
        self.discuss_and_zoom_image(
            subpackages,
            (image_filename, image_source),
            image_height,
            image_voiceover,
            [annotated_filename],
            [annotated_voiceover])


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = ImageZoomDemo()
        scene.render()