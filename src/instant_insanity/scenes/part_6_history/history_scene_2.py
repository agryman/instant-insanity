from typing import Sequence

from manim import tempconfig
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.mobjects.image import UW_TUTTE_SOURCE, UW_HONSBERGER_SOURCE
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene

SUBPACKAGES: str = "history"
IMAGE_HEIGHT: float = 8.0


class HistoryScene2(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    def subscene_1_uw_tutte(self) -> None:
        if self.skip(self.subscene_1_uw_tutte):
            return

        image_filename: str = "uw-tutte.png"
        image_source: str = UW_TUTTE_SOURCE
        image_voiceover: str = """
        Tutt became a legendary codebreaker at Bletchley Park during World War II
        where he cracked the Lorenz cipher.
        Here is how a BBC documentary introduces him:
        
        "This is a British mathematician called Bill Tutt. 
        You won't have heard of him but in 1943 he pulled off 
        what many believe was the greatest intellectual feat of World War II."
        
        After the war Tutt moved to Canada and
        spent many years at the University of Toronto.
        In 1962 he helped establish 
        the Department of Combinatorics and Optimization in 
        the Faculty of Mathematics 
        at the University of Waterloo where he remained 
        until his death in 2002.
        He was a highly influential graph theorist.
        """
        self.discuss_and_zoom_image(
            SUBPACKAGES,
            (image_filename, image_source),
            IMAGE_HEIGHT,
            image_voiceover,
        )

    def subscene_2_uw_honsberger(self) -> None:
        if self.skip(self.subscene_2_uw_honsberger):
            return

        image_filename: str = "uw-honsberger.png"
        image_source: str = UW_HONSBERGER_SOURCE
        image_voiceover: str = """
        Honsberger was the Head of the Mathematics Department at
        Northview Heights from 1958 to 1963.
        He left teaching to obtain an advanced degree
        at the University of Waterloo and in 1967 became a professor there
        in the Department of Combinatorics and Optimization.
        
        Honsberger and Tutt were colleagues for many years.
        Like Tutt, Honsberger wrote many recreational mathematics articles.
        
        It seems inevitable that Tutt would have shown Honsberger 
        his graphical solution to Instant Insanity. 
        Honsberger then visited Northview Heights and retold the story 
        as the impressive conclusion of his graph theory lecture. 
        Your narrator was there. 
        By watching this video you have become the latest link in an 
        oral tradition that has spanned decades.
        """
        self.discuss_and_zoom_image(
            SUBPACKAGES,
            (image_filename, image_source),
            IMAGE_HEIGHT,
            image_voiceover,
        )

    def construct(self):
        # self.set_speech_service(GCPTextToSpeechService())
        self.set_speech_service(RecorderService(transcription_model=None))
        self.subscene_1_uw_tutte()
        self.subscene_2_uw_honsberger()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            self.subscene_1_uw_tutte,
            self.subscene_2_uw_honsberger,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = HistoryScene2()
        scene.render()
