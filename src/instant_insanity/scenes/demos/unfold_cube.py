
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.puzzle import WINNING_MOVES_PUZZLE_SPEC
from instant_insanity.mobjects.coloured_cube import ColouredCube

from manim import (
    ThreeDScene, Rotate, config,
    UP, LEFT, RIGHT, PI, DEGREES,
    WHITE, Square
)
from manim.typing import Point3D

config.background_color = WHITE  # must be set before scene instantiation

class UnfoldCubeToNet(ThreeDScene):
    def construct(self):

        self.set_camera_orientation(phi=-15 * DEGREES, theta=-90 * DEGREES, gamma=0 * DEGREES)

        cube: ColouredCube = ColouredCube(side_length=1.0, cube_spec=WINNING_MOVES_PUZZLE_SPEC[0])
        cube.shift(3 * LEFT)

        # Function to sort faces based on distance to camera
        def sort_faces(cube: ColouredCube) -> ColouredCube:
            cam_pos: Point3D = self.camera.frame_center
            return cube.sort_faces(cam_pos)

        # Add an updater to re-sort the faces each frame
        cube.add_updater(sort_faces)
        self.add(cube)

        # Add labels to the cube faces - this is commented out as it does not work correctly
        # labels = add_face_labels(cube)
        # self.add(labels)

        delay: float = 1.0
        self.wait(delay)

        top: Square = cube.face_square[FacePlane.TOP]
        bottom: Square = cube.face_square[FacePlane.BOTTOM]
        front: Square = cube.face_square[FacePlane.FRONT]
        back: Square = cube.face_square[FacePlane.BACK]
        left: Square = cube.face_square[FacePlane.LEFT]
        right: Square = cube.face_square[FacePlane.RIGHT]

        # Animate unfolding into T-net
        self.play(Rotate(top, angle=PI / 2, axis=RIGHT, about_point=front.get_top()), run_time=delay)
        self.play(Rotate(bottom, angle=-PI / 2, axis=RIGHT, about_point=front.get_bottom()),
            Rotate(back, angle=-PI / 2, axis=RIGHT, about_point=front.get_bottom()), run_time=delay)
        self.play(Rotate(back, angle=-PI / 2, axis=RIGHT, about_point=bottom.get_bottom()), run_time=delay)
        self.play(Rotate(left, angle=PI / 2, axis=UP, about_point=front.get_left()), run_time=delay)
        self.play(Rotate(right, angle=-PI / 2, axis=UP, about_point=front.get_right()), run_time=delay)

        # Clean up: remove updater after animation
        cube.remove_updater(sort_faces)

        self.wait(delay)


# For running the scene directly
if __name__ == "__main__":
    scene = UnfoldCubeToNet()
    scene.render(preview=True)
