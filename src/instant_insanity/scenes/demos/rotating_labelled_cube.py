import numpy as np

from manim import ThreeDScene, DEGREES, Cube, VGroup, Text, BLACK, WHITE, PI, UP, Group, Rotate

class RotatingLabelledCube(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=15 * DEGREES)

        cube = Cube(side_length=2, fill_opacity=0.6, stroke_color=WHITE)

        # Label specifications: (text, face normal, rotation axis)
        labels = [
            ("x",   [1, 0, 0], [0, 1, 0]),   # front
            ("x'", [-1, 0, 0], [0, 1, 0]),   # back
            ("y",   [0, 1, 0], [1, 0, 0]),   # right
            ("y'", [0, -1, 0], [1, 0, 0]),   # left
            ("z",   [0, 0, 1], [0, 1, 0]),   # top
            ("z'", [0, 0, -1], [0, 1, 0]),   # bottom
        ]

        label_mobs = VGroup()
        for text_str, direction, rot_axis in labels:
            label = Text(text_str, color=BLACK).scale(0.5)

            # Move to face center
            offset = 0.99 * np.array(direction)
            label.move_to(offset)

            # Align label plane to face plane
            # Default Text lies in XY plane, so rotate to match face
            label.rotate(angle=PI/2, axis=np.cross([0, 0, 1], direction))

            label_mobs.add(label)

        # Group cube and labels together
        cube_group = Group(cube, label_mobs)
        self.add(cube_group)

        self.play(Rotate(cube_group, angle=PI, axis=UP, run_time=4))
        self.wait()

if __name__ == "__main__":
    scene = RotatingLabelledCube()
    scene.render(preview=True)
