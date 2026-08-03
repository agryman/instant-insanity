from manim import tempconfig, Table, Text, BLACK, WHITE, BOLD, ManimColor
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.puzzle import (FaceColour, FaceLabel, INITIAL_FACE_LABEL_TO_PLANE, Puzzle,
                                          PuzzleCubeNumber, PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC)
from instant_insanity.mobjects.coloured_cube import MANIM_COLOUR_MAP
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.subscene import SubsceneMixin


class FaceColourTableDemo(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    def construct(self) -> None:
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)
        self.say("Here's the face colour table for Instant Insanity.")

        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        puzzle: Puzzle = Puzzle(puzzle_spec)

        # the table has one row per face label and one column per cube.
        face_colour_rows: list[list[FaceColour]] = [
            [puzzle.number_to_cube[cube_number].face_label_to_colour[face_label]
             for cube_number in PuzzleCubeNumber]
            for face_label in FaceLabel
        ]

        # each cell displays the initial letter of its face colour,
        # which is the inverse of FaceColour.from_initial.
        table: list[list[str]] = [
            [face_colour.name[0] for face_colour in face_colour_row]
            for face_colour_row in face_colour_rows
        ]
        row_labels: list[str] = [
            f'{face_label} ({INITIAL_FACE_LABEL_TO_PLANE[face_label]})'
            for face_label in FaceLabel
        ]
        col_labels: list[str] = [
            str(cube_number.value) for cube_number in PuzzleCubeNumber
        ]

        row_label_texts: list[Text] = [Text(row_label, color=BLACK, weight=BOLD) for row_label in row_labels]
        col_label_texts: list[Text] = [Text(col_label, color=BLACK, weight=BOLD) for col_label in col_labels]
        top_left_entry: Text = Text("Face/Cube", color=BLACK, weight=BOLD)

        face_colour_table: Table = Table(
            table,
            row_labels=row_label_texts,
            col_labels=col_label_texts,
            top_left_entry=top_left_entry,
            include_outer_lines=True,
            element_to_mobject=Text,
            element_to_mobject_config={
                "color": BLACK,
                "font": "sans-serif",
                "weight": BOLD,
                "fill_opacity": 1.0,
            },
            line_config={
                "stroke_color": BLACK,
            }
        )

        # colourize the data cells, leaving the white ones as is.
        # cell (i, j) of the data sits at table position (i + 2, j + 2)
        # because row 1 holds the column labels and column 1 holds the row labels.
        for i, face_colour_row in enumerate(face_colour_rows):
            for j, face_colour in enumerate(face_colour_row):
                if face_colour is FaceColour.WHITE:
                    continue
                cell_colour: ManimColor = MANIM_COLOUR_MAP[face_colour]
                face_colour_table.add_highlighted_cell((i + 2, j + 2), color=cell_colour, fill_opacity=1.0)
                face_colour_table.get_entries((i + 2, j + 2)).set_color(WHITE)

        # add the table background last so that it sits behind the highlighted cells.
        face_colour_table.add_background_rectangle(color=WHITE, opacity=1.0)
        face_colour_table.scale(0.5)
        self.add(face_colour_table)
        self.wait(5.0)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = FaceColourTableDemo()
        scene.render()
