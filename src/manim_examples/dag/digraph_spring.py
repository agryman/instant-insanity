from enum import StrEnum, auto
from manim import *
from instant_insanity.core.config import PREVIEW_CONFIG

class Var(StrEnum):
    puzzle = auto()
    cube_number = auto()
    graph = auto()
    cube_spec = auto()
    viewpoint = auto()
    projection = auto()
    cube = auto()
    axis_label = auto()
    cube_axis = auto()
    start = auto()
    end = auto()
    first = auto()
    second = auto()
    first_name = auto()
    second_name = auto()



edges: list[tuple[Var, Var]] = [
    (Var.graph, Var.puzzle),
    (Var.cube_spec, Var.puzzle),
    (Var.cube_spec, Var.cube_number),
    (Var.cube, Var.cube_spec),
    (Var.projection, Var.viewpoint),
    (Var.cube, Var.projection),
    (Var.cube_axis, Var.axis_label),
    (Var.cube_axis, Var.cube_number),
]

class DiGraphSpring(Scene):
    def construct(self):
        nodes = list(Var)
        g = DiGraph(nodes, edges, layout='spring')
        self.add(g)
        self.wait(4)

if __name__ == "__main__":
    with tempconfig(PREVIEW_CONFIG):
        scene = DiGraphSpring()
        scene.render()
