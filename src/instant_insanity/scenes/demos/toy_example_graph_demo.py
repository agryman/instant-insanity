"""
This module demonstrates the toy example graph made by
instant_insanity.mobjects.toy_example.

The undirected scene reproduces
resources/images/graph_theory/latex/example-multigraph.png and the directed scene
reproduces example-directed-graph.png.
"""
from typing import cast

from manim import Scene, tempconfig
from manim.typing import Point3D

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.mobjects.toy_example_graph import ToyExampleGraph, mk_toy_example, tikz_point, NODE_TO_POINT


class ToyExampleGraphDemo(Scene):
    def construct(self) -> None:
        toy_example: ToyExampleGraph = ToyExampleGraph(simple=True, labelled=False, directed=False)
        self.add(toy_example)
        self.wait(1.0)

        # move vertex D from its initial position
        point_d_initial: Point3D = NODE_TO_POINT['D']

        # to the centre of triangle ABC
        point_d_final: Point3D = cast(Point3D, (NODE_TO_POINT['A'] + NODE_TO_POINT['B'] + NODE_TO_POINT['C']) / 3.0)

        # move_node_to mutates the graph, so Manim's animate builder can apply it to a
        # copy and interpolate the whole figure into the result.
        self.play(toy_example.animate.move_node_to('D', point_d_final), run_time=2.0)
        self.wait(1.0)

        self.play(toy_example.animate.move_node_to('D', point_d_initial), run_time=2.0)
        self.wait(1.0)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = ToyExampleGraphDemo()
        scene.render()
