from manim import *

from instant_insanity.core.config import LINEN_CONFIG


def add_coordinate_grid(scene: Scene) -> None:
    fw = 12 #config.frame_width
    fh = 6 #config.frame_height

    plane = NumberPlane(
        x_range=(-fw / 2, fw / 2, 1),  # integers every 1 scene unit
        y_range=(-fh / 2, fh / 2, 1),
        x_length=fw,  # fill full scene width
        y_length=fh,  # fill full scene height
        faded_line_ratio=0,  # only primary grid lines
        background_line_style={"stroke_color": GREY_B, "stroke_width": 1},
        axis_config={"stroke_color": BLACK, "stroke_width": 2, "include_tip": False},
    )

    # Change axis number colors to black
    plane.x_axis.add_numbers()
    plane.y_axis.add_numbers()
    plane.x_axis.numbers.set_color(BLACK)
    plane.y_axis.numbers.set_color(BLACK)

    origin = Dot(ORIGIN, radius=DEFAULT_DOT_RADIUS * 0.75, color=BLACK)
    x_label = MathTex('x', font_size=24, color=BLACK).next_to(plane.x_axis.get_end(), UP, buff=0.1)
    y_label = MathTex('y', font_size=24, color=BLACK).next_to(plane.y_axis.get_end(), LEFT, buff=0.1)

    scene.add(plane, origin, x_label, y_label)


class SceneCoordinateGrid(Scene):
    def construct(self):
        add_coordinate_grid(self)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = SceneCoordinateGrid()
        scene.render()
