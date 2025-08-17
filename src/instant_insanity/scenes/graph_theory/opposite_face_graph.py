from manim import tempconfig, Scene, ORIGIN, LEFT, RIGHT, FadeIn

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.puzzle import (WINNING_MOVES_PUZZLE, CARTEBLANCHE_PUZZLE)
from instant_insanity.mobjects.opposite_face_graph import EdgeToSubgraphMapping, OppositeFaceGraph


class OppositeFaceGraphs(Scene):
    def construct(self):
        # add_coordinate_grid(self)

        full_subgraph: EdgeToSubgraphMapping = OppositeFaceGraph.mk_subgraph_for_flag(True)

        cb_graph: OppositeFaceGraph = OppositeFaceGraph(CARTEBLANCHE_PUZZLE, ORIGIN + 3 * LEFT)
        cb_graph.set_subgraph(full_subgraph)
        self.add(cb_graph)
        self.play(FadeIn(cb_graph))

        wm_graph: OppositeFaceGraph = OppositeFaceGraph(WINNING_MOVES_PUZZLE, ORIGIN + 3 * RIGHT)
        wm_graph.set_subgraph(full_subgraph)
        self.add(wm_graph)
        self.play(FadeIn(wm_graph))

        self.wait()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = OppositeFaceGraphs()
        scene.render()
