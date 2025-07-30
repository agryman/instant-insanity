from manim import *

class SceneUpdaterExample(Scene):
    def construct(self):
        dot = Dot().set_color(BLUE)
        label = Text("Timer: 0.0", font_size=24).next_to(dot, UP)

        self.add(dot, label)

        self.elapsed_time = 0.0

        def update_timer(dt):
            """Updates the text label with the elapsed time."""
            self.elapsed_time += dt
            new_text = Text(f"Timer: {self.elapsed_time:.1f}", font_size=24)
            new_text.next_to(dot, UP)
            label.become(new_text)

        self.add_updater(update_timer)
        self.wait(5)
        self.remove_updater(update_timer)
        self.wait(1)

my_config: dict = {
    "background_color": BLACK,
    "preview": True
}

with tempconfig(my_config):
    scene = SceneUpdaterExample()
    scene.render()
