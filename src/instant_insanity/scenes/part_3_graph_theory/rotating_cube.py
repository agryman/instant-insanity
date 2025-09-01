from manim import (ThreeDScene, ThreeDAxes, Cube, PURE_RED, PURE_BLUE, PURE_GREEN,
                   WHITE, YELLOW, PURPLE, BLACK, DEGREES, RIGHT, LEFT, UP, DOWN, IN, OUT,
                   PI, Rotate)


#config.background_color = WHITE  # must be set before scene instantiation

class RotatingCube(ThreeDScene):
    def add_axes(self):
        # Create axes

        axes = ThreeDAxes(x_range=[0, 1, 1])

        x_label = axes.get_x_axis_label('x')
        y_label = axes.get_y_axis_label('y')
        z_label = axes.get_z_axis_label('z')

        self.add(axes, x_label, y_label, z_label)

    def construct(self):

        self.add_axes()

        # Create a cube
        #cube = Cube(side_length=2, fill_opacity=0.5, fill_color=BLUE)
        cube = Cube(side_length=2)
        self.add(cube)

        # Get the individual faces from cube.submobjects
        # Face order: +Z, -Z, +Y, -Y, +X, -X
        # Corresponds to: front, back, top, bottom, right, left
        face_colors = {
            0: PURE_RED,    # -Z: bottom
            1: WHITE,       # +Z: top
            2: PURE_BLUE,   # -X: back
            3: PURE_GREEN,  # +X: front
            4: YELLOW,      # +Y: right
            5: PURPLE,      # -Y: left
        }

        for i, face in enumerate(cube.submobjects):
            face.set_fill(color=face_colors[i], opacity=1.0)
            face.set_stroke(BLACK, width=2)

        # Set the initial camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=15 * DEGREES)
        #self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        #self.set_camera_orientation(phi=30 * DEGREES, theta=15 * DEGREES)
        #self.set_camera_orientation(phi=90 * DEGREES, theta=0 * DEGREES)

        # Animate the rotation of the cube
        rotation_axes = [RIGHT, LEFT, UP, DOWN, OUT, IN]
        quarter_turn = PI / 2
        for rotation_axis in rotation_axes:
            for _ in range(4):
                self.play(Rotate(cube, angle=quarter_turn, axis=rotation_axis, run_time=2))

        # Hold the final frame
        self.wait(1)


if __name__ == "__main__":
    scene = RotatingCube()
    scene.render(preview=True)

