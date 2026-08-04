from manim import (tempconfig, Table, Text, BLACK, WHITE, BOLD, ManimColor, VMobject, VGroup, NORMAL,
                   Indicate, AnimationGroup)
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.core.puzzle import (FaceColour, FaceLabel, INITIAL_FACE_LABEL_TO_PLANE, Puzzle,
                                          PuzzleCubeNumber, PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, WINNING_MOVES_PUZZLE)
from instant_insanity.mobjects.coloured_cube import MANIM_COLOUR_MAP
from instant_insanity.mobjects.face_colour_table import mk_text, FaceColourTable
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.subscene import SubsceneMixin


class FaceColourTableDemo(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    def construct(self) -> None:
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        puzzle: Puzzle = WINNING_MOVES_PUZZLE
        face_color_table: FaceColourTable = FaceColourTable(puzzle)
        table: Table = face_color_table.table
        self.add(table)
        self.say("Here's the face colour table for Instant Insanity.")

        voiceover: str = 'Each row gives the colours of one face across the four cubes.'
        with self.voiceover(text=voiceover) as tracker:
            for face_label in FaceLabel:
                face_color_table.indicate_data_row(self, face_label)
            voiceover_wait(self, tracker)

        self.wait(2.0)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = FaceColourTableDemo()
        scene.render()
