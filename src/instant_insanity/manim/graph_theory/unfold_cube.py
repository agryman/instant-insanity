from typing import Self

import numpy as np

from manim import *
from manim.typing import Point3D

config.background_color = WHITE  # must be set before scene instantiation

class UnfoldingCube(VGroup):
    front: Square
    back: Square
    right: Square
    left: Square
    top: Square
    bottom: Square

    def __init__(
        self,
        side_length: float = 2,
        **kwargs,
    ) -> None:
        self.side_length = side_length
        super().__init__(
            **kwargs,
        )

    def generate_points(self) -> None:
        """
        Creates the sides of the :class:`UnfoldingCube`.

        This method gets called by the __init__ method of Mobject.
        """

        # Create front face
        self.front = Square(side_length=self.side_length, shade_in_3d=True)
        self.front = self.front.shift(OUT * self.side_length / 2)

        # Create and position other faces relative to the front
        self.back = self.front.copy().rotate(PI, axis=UP, about_point=ORIGIN)

        self.top = self.front.copy().rotate(PI / 2, axis=LEFT, about_point=ORIGIN)
        self.bottom = self.front.copy().rotate(PI / 2, axis=RIGHT, about_point=ORIGIN)

        self.left = self.front.copy().rotate(PI / 2, axis=DOWN, about_point=ORIGIN)
        self.right = self.front.copy().rotate(PI / 2, axis=UP, about_point=ORIGIN)

        self.add(self.front, self.back, self.top, self.bottom, self.left, self.right)


    init_points = generate_points

    def init_colors(self, propagate_colors: bool = True) -> Self:

        """
        Initialize the colours of the cube.

        This method gets called by the __init__ method of Mobject.
        """

        face_colours = [
            (self.front, PURE_RED),
            (self.back, PURE_BLUE),
            (self.top, YELLOW),
            (self.bottom, PURPLE),
            (self.left, PURE_GREEN),
            (self.right, ORANGE)
        ]

        opacity = 1.0
        stroke_color = BLACK
        stroke_width = 1.0

        for face, colour in face_colours:
            face.set_fill(colour, opacity=opacity).set_stroke(color=stroke_color, width=stroke_width)

        return self


class UnfoldCubeToNet(ThreeDScene):
    def construct(self):

        #self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        #self.set_camera_orientation(phi=0 * DEGREES, theta=0 * DEGREES)
        #self.set_camera_orientation(phi=-30 * DEGREES, theta=-15 * DEGREES, gamma=-15 * DEGREES)
        #self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES) # straight on correctly oriented
        self.set_camera_orientation(phi=-15 * DEGREES, theta=-90 * DEGREES, gamma=0 * DEGREES)

        cube = UnfoldingCube(side_length=1.0)
        cube.shift(3 * LEFT)

        # Function to sort faces based on distance to camera
        def sort_faces(cube: UnfoldingCube) -> UnfoldingCube:
            cam_pos: Point3D = self.camera.frame_center
            face: Square
            for face in cube:
                dist = np.linalg.norm(face.get_center() - cam_pos)
                face.z_index = -dist  # closer → higher z_index
            cube.submobjects.sort(key=lambda mob: mob.z_index)
            return cube

        # Add an updater to re-sort the faces each frame
        cube.add_updater(sort_faces)
        self.add(cube)

        delay = 1.0
        self.wait(delay)

        # Animate unfolding into T-net
        self.play(Rotate(cube.top, angle=PI / 2, axis=RIGHT, about_point=cube.front.get_top()), run_time=delay)
        self.play(Rotate(cube.bottom, angle=-PI / 2, axis=RIGHT, about_point=cube.front.get_bottom()),
            Rotate(cube.back, angle=-PI / 2, axis=RIGHT, about_point=cube.front.get_bottom()), run_time=delay)
        self.play(Rotate(cube.back, angle=-PI / 2, axis=RIGHT, about_point=cube.bottom.get_bottom()), run_time=delay)
        self.play(Rotate(cube.left, angle=PI / 2, axis=UP, about_point=cube.front.get_left()), run_time=delay)
        self.play(Rotate(cube.right, angle=-PI / 2, axis=UP, about_point=cube.front.get_right()), run_time=delay)

        # Clean up: remove updater after animation
        cube.remove_updater(sort_faces)

        self.wait(delay)


# For running in PyCharm
if __name__ == "__main__":
    scene = UnfoldCubeToNet()
    scene.render(preview=True)