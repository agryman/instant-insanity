from manim import *


class MobjectUpdaterExample(Scene):
    def construct(self):
        square = Square()
        square.set_color(RED)
        square.move_to(LEFT * 3)

        def move_right(mobj, dt):
            """Moves the mobject steadily to the right."""
            mobj.shift(RIGHT * dt)

        square.add_updater(move_right)
        self.add(square)
        self.wait(4)  # square moves for 4 seconds
        square.remove_updater(move_right)
        self.wait(1)


my_config: dict = {
    "background_color": WHITE,
    "preview": True
}

with tempconfig(my_config):
    scene = MobjectUpdaterExample()
    scene.render()
