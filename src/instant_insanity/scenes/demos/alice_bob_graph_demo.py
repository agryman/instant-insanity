from manim import Scene, tempconfig, UP, DOWN

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.mobjects.alice_bob_graphs import AliceBobGraph


class AliceBobGraphDemo(Scene):
    def construct(self) -> None:
        neighbour_graph: AliceBobGraph = AliceBobGraph("neighbour", directed=False)
        neighbour_graph.move_to(UP)
        self.add(neighbour_graph)

        likes_graph: AliceBobGraph = AliceBobGraph("likes", directed=True)
        likes_graph.move_to(DOWN)
        self.add(likes_graph)

        self.wait(3.0)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = AliceBobGraphDemo()
        scene.render()
