from manim import *
from instant_insanity.core.config import LINEN_CONFIG

def outline_with_n_points(m: VMobject, n: int = 300) -> VMobject:
    """Return a VMobject that traces `m`'s outline with `n` equally spaced points."""
    # Sample along arc-length parameterization (Manim’s proportion)
    ts = np.linspace(0.0, 1.0, n, endpoint=False)
    pts = np.array([m.point_from_proportion(float(t)) for t in ts])
    # Close the loop explicitly
    pts = np.vstack([pts, pts[0]])
    out = VMobject()
    out.set_points_as_corners(pts)
    return out

class SquareToCircleSmooth(Scene):
    def construct(self):
        # Original shapes (can be displayed as references if you want)
        square = Square(side_length=4).set_stroke(width=6)
        circle = Circle(radius=1).set_stroke(width=6)

        # Build resampled outlines with identical point counts
        n = 48
        src = outline_with_n_points(square, n).set_stroke(width=6)
        dst = outline_with_n_points(circle, n).set_stroke(width=6)

        src.set_color(GREEN)
        dst.set_color(RED)

        self.add(src)
        self.play(Transform(src, dst), run_time=2.5, rate_func=smooth)
        self.wait()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = SquareToCircleSmooth()
        scene.render()
