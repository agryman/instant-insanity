from manim import (
    ThreeDScene, config,
    OUT, IN, UP, DOWN, LEFT, RIGHT, DEGREES,
    WHITE, BLACK, Line3D, FadeIn,
    Text, tempconfig, RendererType, UL,
    ThreeDCamera
)
from manim.typing import Point3D

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.puzzle import WINNING_MOVES_PUZZLE_SPEC, CARTEBLANCHE_PUZZLE_SPEC
from instant_insanity.scenes.coloured_cube import ColouredCube, FACE_NORMAL, OPPOSITE_FACES

config.background_color = WHITE  # must be set before scene instantiation
RENDERER_TYPE: RendererType = RendererType.OPENGL


class ExplodeCube(ThreeDScene):
    def construct(self):

        renderer_str = f"renderer: {config.renderer.value}"
        renderer_text = Text(renderer_str, font_size=24, color=BLACK)
        self.add_fixed_in_frame_mobjects(renderer_text)
        renderer_text.to_corner(UL)
        self.set_camera_orientation(phi=-15 * DEGREES, theta=-90 * DEGREES, gamma=0 * DEGREES)

        # cube = ColouredCube(side_length=1.0, cube_spec=WINNING_MOVES_PUZZLE[0])
        cube = ColouredCube(side_length=1.0)
        cube.shift(3 * LEFT)

        # Function to sort faces based on distance to camera
        def sort_faces(cube: ColouredCube) -> ColouredCube:
            cam_pos: Point3D = self.camera.frame_center
            return cube.sort_faces(cam_pos)

        # Add an updater to re-sort the faces each frame
        # if RENDERER_TYPE == RendererType.CAIRO:
        #     cube.add_updater(sort_faces)
        
        # self.add(cube)
        
        delay = 1.0
        # self.wait(delay)

        # # Animate the cube exploding
        # self.play(*[
        #     cube.face_square[face].animate.shift(normal)
        #     for face, normal in FACE_NORMAL.items()
        # ], run_time=delay)

        # self.wait(delay)

        # # Clean up: remove updater after animation
        # if RENDERER_TYPE == RendererType.CAIRO:
        #     cube.remove_updater(sort_faces)

        # Fade-in the lines connecting the cube faces

        lines: list[Line3D] = [Line3D(
            cube.face_square[face1].get_center(),
            cube.face_square[face2].get_center(),
            color=BLACK
        ) for face1, face2 in OPPOSITE_FACES]
    
        for line in lines:
            self.play(FadeIn(line), run_time=delay)

        self.wait(delay)


# For running the scene directly
# if __name__ == "__main__":
#     scene = ExplodeCube()
#     scene.render(preview=True)

# For running the scene directly
if __name__ == "__main__":
    with tempconfig({
        "renderer": RENDERER_TYPE
    }):
        scene = ExplodeCube()
        scene.render(preview=True)
