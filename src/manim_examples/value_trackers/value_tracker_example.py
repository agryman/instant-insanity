from manim import *

class ValueTrackerExample(Scene):
    def construct(self):
        number_line = NumberLine(include_numbers=True)
        pointer = Vector(DOWN)
        label = MathTex("x").add_updater(lambda m: m.next_to(pointer, UP))

        tracker = ValueTracker(0)
        pointer.add_updater(
            lambda m: m.next_to(
                        number_line.n2p(tracker.get_value()),
                        UP
                    )
        )
        self.add(number_line, pointer,label)
        duration:float = 2.0
        self.wait(duration)

        tracker += 1.5 # value = 1.5
        self.wait(duration)

        tracker -= 4 # value = -2.5
        self.wait(duration)

        self.play(tracker.animate.set_value(5), run_time=7.5) # delta value = 7.5, value -> 5.0
        self.wait(duration)

        self.play(tracker.animate.set_value(3), run_time=2.0) # delta value = -2.0, value -> 3.0
        self.wait(duration)

        self.play(tracker.animate.increment_value(-2), run_time=2.0) # delta value = -2.0, value -> 1.0
        self.wait(duration)

my_config: dict = {
    "background_color": BLACK,
    "preview": True
}

with tempconfig(my_config):
    scene = ValueTrackerExample()
    scene.render()
