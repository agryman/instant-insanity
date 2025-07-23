"""
This scene creates a cube from a set of 2d polygons.
The polygons are projections of the 3d faces of the cube.
The polygons are ordered from back to the front.
"""

from manim import *
from manim.typing import Vector3D

from instant_insanity.core.cube import FaceName
from instant_insanity.core.puzzle import FaceColour, PuzzleCube
from instant_insanity.manim_scenes.coloured_cube import MANIM_COLOUR_MAP, TEST_PUZZLE_CUBE_SPEC

def mk_face(vertex_list: list[Vector3D], colour: ParsableManimColor) -> Polygon:
    """
    Make a cube face from its vertex list.
    """
    return Polygon(*vertex_list, fill_color=colour, fill_opacity=1.0, stroke_color=BLACK, stroke_width=1.0)


class CubeFromPolygons(Scene):
    def construct(self):

        # create a puzzle cube spec that has a different colour for each face
        puzzle_cube: PuzzleCube = PuzzleCube(TEST_PUZZLE_CUBE_SPEC)
        face_colour: dict[FaceName, FaceColour] = puzzle_cube.faces

        # define the vertices of the standard cube
        v1: Vector3D = LEFT + DOWN + OUT
        v2: Vector3D = RIGHT + DOWN + OUT
        v3: Vector3D = RIGHT + UP + OUT
        v4: Vector3D = LEFT + UP + OUT
        v5: Vector3D = LEFT + DOWN + IN
        v6: Vector3D = RIGHT + DOWN + IN
        v7: Vector3D = RIGHT + UP + IN
        v8: Vector3D = LEFT + UP + IN

        # define the faces of the standard cube
        # list the vertices in counterclockwise order

        # create the front face
        front_vertices: list[Vector3D] = [v1, v2, v3, v4]
        front_colour: ManimColor = MANIM_COLOUR_MAP[face_colour[FaceName.FRONT]]
        front_face = mk_face(front_vertices, front_colour)

        # create the back face
        back_vertices: list[Vector3D] = [v8, v7, v6, v5]
        back_colour: ManimColor = MANIM_COLOUR_MAP[face_colour[FaceName.BACK]]
        back_face: Polygon = mk_face(back_vertices, back_colour)
        back_face.shift(RIGHT + 0.5 * UP)

        self.add(front_face, back_face)

my_config: dict = {
    "background_color": WHITE,
    "preview": True
}

with tempconfig(my_config):
    scene = CubeFromPolygons()
    scene.render()
