from manim import *

def mk_square(colour: ManimColor) -> Square:
    square: Square = Square(fill_color=colour, fill_opacity=1.0, stroke_color=BLACK, stroke_width=1.0)
    return square

class CubeScene(Scene):
    def construct(self):

        # add a grid of small dots
        dots = [Dot(point=(x * RIGHT + y * UP), color=GRAY, radius=0.02)
                for x in range(-5, 6) for y in range(-3, 4)]
        self.add(*dots)

        # add a red square
        red_square = mk_square(RED)
        self.add(red_square)

        blue_square = mk_square(BLUE)
        blue_square.shift(0.5 * RIGHT + 0.5 * UP)
        self.add(blue_square)

if __name__ == "__main__":
    scene = CubeScene()
    scene.render(preview=True)
