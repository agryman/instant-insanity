from typing import Sequence, cast

from manim import tempconfig, Mobject, ORIGIN, FadeIn, FadeOut
from manim.typing import Point3D
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.puzzle import WINNING_MOVES_PUZZLE, Puzzle
from instant_insanity.mobjects.alice_bob_graphs import AliceBobGraph
from instant_insanity.mobjects.labelled_subgraph import LabelledSubgraphPair
from instant_insanity.mobjects.opposite_face_graph import EdgeToSubgraphMapping, OppositeFaceGraph
from instant_insanity.mobjects.toy_example_graph import mk_toy_example, NODE_TO_POINT
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene

GRAPH_THEORY_LATEX: str = "graph_theory.latex"

class GraphTheoryScene1(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    wm_graph: OppositeFaceGraph
    toy_graph: Mobject

    def subscene_1_the_opposite_face_graph(self) -> None:
        if self.skip(self.subscene_1_the_opposite_face_graph):
            return
        # the opposite-face graph
        topic = self.mk_topic("the opposite-face graph of Instant Insanity")
        discussion = """
        We are going to turn the Instant Insanity puzzle into a graph and use it to solve the puzzle.
        We refer to this graph as the opposite-face graph because it represents the pairs of opposite faces
        that occur in the cubes.
        """
        self.discuss_mobject(topic, discussion)

        discussion = """
        Here's the graph.
        Each dot represents one of the four face colours.
        Each line represents a pair of opposite faces in some cube.
        Each of the four cubes has three pairs of opposite faces so altogether the graph has twelve lines.
        This type of graph is called a labelled multigraph.
        We'll define those terms next.
        """
        self.discuss_mobject(self.wm_graph, discussion)

    def subscene_2_what_is_a_graph(self) -> None:
        if self.skip(self.subscene_2_what_is_a_graph):
            return

        # What is a graph?
        topic = self.mk_topic("What is a graph?")
        discussion = """
        Let's get started with some graph theory!
        We'll begin by establishing some terminology.
        Graph theory terminology can be confusing because
        mathematicians often give the same name to different things
        and different names to the same thing.
        """
        self.discuss_mobject(topic, discussion)

        # graphs of functions
        topic = self.mk_topic("graphs of functions")
        discussion = """
        In high school we learn that a graph is an x-y plot of some function or relation.
        """
        self.discuss_mobject(topic, discussion)

        # parabola graph
        image = self.get_image("parabola-graph.png", GRAPH_THEORY_LATEX)
        image.height = 6.0
        discussion = """
        For example, here's the graph of the function y equals x squared which produces a parabola.
        This kind of graph is not what graph theory is about.
        """
        self.discuss_mobject(image, discussion)

        # points, lines
        topic = self.mk_topic("points, lines")
        discussion = """
        Mathematicians also give the name graph to any collection of points
        connected by lines.
        """
        self.discuss_mobject(topic, discussion)

        # example simple graph
        discussion = """
        Here's a toy example graph. It has five points and four lines.
        This kind of graph is what graph theory is about.

        This kind of graph is used to represent relationships between pairs of objects.
        For example, the points might represent cities and the lines highways between them.
        """
        self.discuss_mobject(self.toy_graph, discussion)

    def subscene_3_simple_graphs(self) -> None:
        if self.skip(self.subscene_3_simple_graphs):
            return

        # simple graphs
        topic = self.mk_topic("simple graphs")
        discussion = """
        If no point is connected to itself and no two distinct points 
        are connected by more than one line
        then the graph is called a simple graph.
        """
        self.discuss_mobject(topic, discussion)

        # example simple graph
        discussion = """
        Here's the toy graph again.
        Note that each line in this graph connects two distinct points
        and every pair of distinct points is connected by at most one line.
        It is therefore a simple graph.
        """
        self.discuss_mobject(self.toy_graph, discussion)

    def subscene_4_alternate_terminology(self) -> None:
        if self.skip(self.subscene_4_alternate_terminology):
            return

        # graph = network
        topic = self.mk_topic("graph = network")
        discussion = """
        People sometimes use the name network instead of graph.
        The name used depends on the subject area.
        For example, social networks and neural networks are graphs.
        """
        self.discuss_mobject(topic, discussion)

        # point = dot = vertex = node
        topic = self.mk_topic("point = dot = vertex = node")
        discussion = """
        Some common alternate names for a point are dot, vertex, and node.
        """
        self.discuss_mobject(topic, discussion)

        # line = link = edge = arc
        topic = self.mk_topic("line = link = edge = arc")
        discussion = """
        Similarly, some common alternate names for a line are link, edge, and arc.
        """
        self.discuss_mobject(topic, discussion)

        # use graph, node, edge
        topic = self.mk_topic("graphs, nodes, edges")
        discussion = """
        From now on, we'll consistently use the names graph, node, and edge.
        """
        self.discuss_mobject(topic, discussion)

    def subscene_5_graph_layouts(self) -> None:
        if self.skip(self.subscene_5_graph_layouts):
            return

        # graph layout
        topic = self.mk_topic("graph layouts")
        discussion = """
        Two graphs are considered to mean the same thing 
        if they contain the same set of nodes
        and those nodes are connected in the same way.
        
        The positions of the nodes and the paths of the edges
        are not essential features of the graph - 
        they just define a particular layout of the graph. 
        """
        self.discuss_mobject(topic, discussion)

        self.play(FadeIn(self.toy_graph))
        self.say("""
        Here's our toy graph again.
        It has a clean layout.
        However, we can use a worse layout without
        changing the meaning of the graph.
        """)

        # Show animation of the toy graph with one node moving.
        # Move vertex D from its initial position.
        point_d_initial: Point3D = NODE_TO_POINT['D']

        # to the centre of triangle ABC
        point_d_final: Point3D = cast(Point3D, (NODE_TO_POINT['A'] + NODE_TO_POINT['B'] + NODE_TO_POINT['C']) / 3.0)

        # move_node_to mutates the graph, so Manim's animate builder can apply it to a
        # copy and interpolate the whole figure into the result.
        self.play(self.toy_graph.animate.move_node_to('D', point_d_final), run_time=2.0)

        self.say("""
        This new layout is worse because now two edges cross each other.
        """)

        self.play(self.toy_graph.animate.move_node_to('D', point_d_initial), run_time=2.0)
        self.play(FadeOut(self.toy_graph))

    def subscene_6_labelled_graphs(self) -> None:
        if self.skip(self.subscene_6_labelled_graphs):
            return

        # labelled graph
        topic = self.mk_topic("labelled graphs")
        discussion = """It is often useful to label the nodes and edges of a graph.
        A graph with labels is called a labelled graph."""
        self.discuss_mobject(topic, discussion)

        # example labelled graph
        discussion = """
        Here's our toy graph with labels added.
        The nodes are labelled A to E.
        The edges are labelled 1 to 4.
        """
        self.discuss_mobject(self.toy_graph, discussion)

        # labels in the opposite-face graph
        discussion = """
        Here's the opposite-face graph again.
        Its nodes are labelled by the face colours.
        Its edges are labelled by a combination of the cube number and axis name.
        We'll explain these labels in more detail later.
        """
        self.discuss_mobject(self.wm_graph, discussion)

    def subscene_7_multigraphs(self) -> None:
        if self.skip(self.subscene_7_multigraphs):
            return

        # multigraph
        topic = self.mk_topic("loops, parallel edges, multigraphs")
        discussion = """
        An edge that connects a node to itself is called a loop.
        Two edges that connect the same pair of distinct nodes are called parallel edges.
        A graph that contains loops or parallel edges is called a multigraph.
        """
        self.discuss_mobject(topic, discussion)

        # example multigraph
        # image = self.get_image("example-multigraph.png", GRAPH_THEORY_LATEX)
        discussion = """
        Here's our toy graph with two more edges.
        Edge 5 is a loop at node B.
        Edges 4 and 6 are parallel edges that connect nodes D and E.
        This toy graph is therefore not a simple graph - it is a multigraph.
        In fact, it is a labelled multigraph.
        """
        self.discuss_mobject(self.toy_graph, discussion)

        # opposite-face multigraph
        discussion = """
        Here's the opposite-face graph again.
        It contains loops and parallel edges.
        It is therefore a multigraph.
        In fact, it is a labelled multigraph.
        """
        self.discuss_mobject(self.wm_graph, discussion)

    def subscene_8_directed_graphs(self) -> None:
        if self.skip(self.subscene_8_directed_graphs):
            return
        # directed graphs
        topic = self.mk_topic("directed graphs")
        discussion = """
        Each edge of a graph represents a relationship between the pair of nodes it connects.
        """
        self.discuss_mobject(topic, discussion)

        discussion = """
        Some relationships are symmetric in the sense that they have no direction.
        For example, saying that Alice is a neighbour of Bob is the same as saying that Bob is a neighbour of Alice.
        In this case we represent the neighbour relationship by a plain, undirected edge.
        """
        neighbour_graph: AliceBobGraph = AliceBobGraph("neighbour", directed=False)
        self.discuss_mobject(neighbour_graph, discussion)

        likes_graph: AliceBobGraph = AliceBobGraph("likes", directed=True)
        discussion = """
        However, not all relationships are symmetric.
        For example, saying that Alice likes Bob is not the same as saying that Bob likes Alice.
        In this case we represent the likes relationship by a directed edge where the arrow points from the
        person doing the liking to the person who is liked.

        A graph in which the edges are directed is called a directed graph.
        """
        self.discuss_mobject(likes_graph, discussion)

        # example directed graph
        # image = self.get_image("example-directed-graph.png", GRAPH_THEORY_LATEX)
        discussion = """
        Here's our toy graph with directions added to its edges.
        It is therefore a directed graph.
        In fact, it is a directed labelled multigraph.
        """
        self.discuss_mobject(self.toy_graph, discussion)

        # opposite-face graph
        discussion = """
        Here's the opposite-face graph again.
        It's edges are not directed because they represent the symmetric relation
        of one face being opposite to another face.
        """
        self.discuss_mobject(self.wm_graph, discussion)

        puzzle: Puzzle = WINNING_MOVES_PUZZLE
        labelled_subgraph_pair = LabelledSubgraphPair(puzzle)
        labelled_subgraph_pair.add_solution_edges()

        labelled_subgraph_pair.add_to_scene(self)
        labelled_subgraph_pair.add_edge_directions(self)

        discussion = """
        However, we will encounter the following directed graphs in the solution of the puzzle.
        They represent the positions of pairs of opposite faces.
        For example, the edge labelled one ex in the front to back graph says that
        the green face of cube 1 is in front and its white face is in back.
         """
        self.say(discussion)

        discussion = """
        We've introduced enough graph theory concepts and terms for now.
        Let's go ahead and show how to use graph theory to solve the puzzle.
        """
        self.say(discussion)


    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        topic: Mobject
        image: Mobject
        discussion: str

        # create the full Winning Moves opposite-face graph
        full_subgraph: EdgeToSubgraphMapping = OppositeFaceGraph.mk_subgraph_for_flag(True)
        wm_graph: OppositeFaceGraph = OppositeFaceGraph(WINNING_MOVES_PUZZLE, ORIGIN)
        wm_graph.set_subgraph(full_subgraph)
        self.wm_graph = wm_graph

        self.subscene_1_the_opposite_face_graph()

        self.toy_graph = mk_toy_example(simple=True, labelled=False, directed=False)
        self.subscene_2_what_is_a_graph()
        self.subscene_3_simple_graphs()
        self.subscene_4_alternate_terminology()
        self.subscene_5_graph_layouts()

        self.toy_graph = mk_toy_example(simple=True, labelled=True, directed=False)
        self.subscene_6_labelled_graphs()

        self.toy_graph = mk_toy_example(simple=False, labelled=True, directed=False)
        self.subscene_7_multigraphs()

        self.toy_graph = mk_toy_example(simple=False, labelled=True, directed=True)
        self.subscene_8_directed_graphs()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            self.subscene_1_the_opposite_face_graph,
            self.subscene_2_what_is_a_graph,
            self.subscene_3_simple_graphs,
            self.subscene_4_alternate_terminology,
            self.subscene_5_graph_layouts,
            self.subscene_6_labelled_graphs,
            self.subscene_7_multigraphs,
            self.subscene_8_directed_graphs,
        ]

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene1()
        scene.render()
