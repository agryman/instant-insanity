from manim import *

class SmallAxesInCorner3D(ThreeDScene):
    def construct(self):
        # Create a small 3D coordinate system with x, y, z in [0, 1]
        axes = ThreeDAxes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            z_range=[0, 1, 0.2],
            x_length=2,
            y_length=2,
            z_length=2,
        )

        # Position the axes in the bottom-left corner of the screen
        axes.shift(LEFT * 5 + DOWN * 3)

        # Optional: add labels for the axes
        labels = axes.get_axis_labels(x_label="x", y_label="y", z_label="z")

        # Set the camera orientation
        #self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.set_camera_orientation(phi=75 * DEGREES, theta=15 * DEGREES)

        self.add(axes, labels)
        self.wait()


if __name__ == "__main__":
    scene = SmallAxesInCorner3D()
    scene.render(preview=True)
