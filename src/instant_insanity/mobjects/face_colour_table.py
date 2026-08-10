"""
This class defines the face colour table for a puzzle.
It uses the Manim Table class.
The entries of the table are computed from a puzzle spec.
Each data row of the table can be briefly indicated using the Indicate animation.
"""
from manim import VMobject, BLACK, NORMAL, Text, Table, BOLD, ManimColor, WHITE, Scene, VGroup, AnimationGroup, Indicate

from instant_insanity.core.puzzle import Puzzle, FaceColour, PuzzleCubeNumber, FaceLabel, INITIAL_FACE_LABEL_TO_PLANE
from instant_insanity.mobjects.coloured_cube import MANIM_COLOUR_MAP


def mk_text(
        text: float |int | str | VMobject,
        color=BLACK,
        font = "sans-serif",
        weight = NORMAL,
        fill_opacity = 1.0,
) -> VMobject:
    return Text(str(text), color=color, font=font, weight=weight, fill_opacity=fill_opacity)

class FaceColourTable:

    puzzle: Puzzle
    table: Table

    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle

        # the table has one row per face label and one column per cube.
        face_colour_rows: list[list[FaceColour]] = [
            [puzzle.number_to_cube[cube_number].face_label_to_colour[face_label]
             for cube_number in PuzzleCubeNumber]
            for face_label in FaceLabel
        ]

        # each cell displays the initial letter of its face colour,
        # which is the inverse of FaceColour.from_initial.
        table_data: list[list[str]] = [
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

        row_label_texts: list[VMobject] = [mk_text(row_label) for row_label in row_labels]
        col_label_texts: list[VMobject] = [mk_text(col_label) for col_label in col_labels]
        top_left_entry: VMobject = mk_text("Face/Cube", weight=BOLD)

        table: Table = Table(
            table_data,
            row_labels=row_label_texts,
            col_labels=col_label_texts,
            top_left_entry=top_left_entry,
            include_outer_lines=False,
            element_to_mobject=mk_text,
            element_to_mobject_config={
                "weight": BOLD,
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
                cell_colour: ManimColor = MANIM_COLOUR_MAP[face_colour]
                table.add_highlighted_cell((i + 2, j + 2), color=cell_colour, fill_opacity=1.0)
                if face_colour is FaceColour.WHITE:
                    continue
                table.get_entries((i + 2, j + 2)).set_color(WHITE)

        self.table = table

    def indicate_data_row(
            self, scene: Scene,
            face_label: FaceLabel,
            scale_factor: float = 1.5,
            run_time: float = 2.0
    ) -> None:
        """
        Indicate the table data row for the face label
        Args:
            scene: The scene that contains the face table.
            face_label: The face label of the data row to indicate.
            scale_factor: The scale factor applied to the indicated data row.
            run_time: The run time in seconds.
        """
        # get_rows() returns the column label row at index 0, so the data rows start
        # at index 1.
        data_rows: VGroup = self.table.get_rows()[1:]

        # each row holds its row label followed by its four cells.
        data_row: VGroup
        row_face_label: FaceLabel
        for row_face_label, data_row in zip(FaceLabel, data_rows):
            if row_face_label == face_label:
                mobject: VMobject
                # indicate each mobject separately rather than the row as a whole, so that
                # each one expands about its own centre. indicating the row would copy and
                # scale it as a single mobject, which expands it about the centre of the row
                # and pulls the cells apart. AnimationGroup defaults to lag_ratio=0, so all
                # of the indications in a row play together.
                scene.play(
                    AnimationGroup(
                        *[
                            # indicate each mobject in its own colour so that only its size changes.
                            Indicate(mobject, color=mobject.get_color(), scale_factor=scale_factor)
                            for mobject in data_row
                        ]
                    ), run_time=run_time
                )
