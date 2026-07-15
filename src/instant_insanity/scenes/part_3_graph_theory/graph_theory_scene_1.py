from manim import tempconfig, Mobject, Tex, BLACK, FadeIn, FadeOut, ORIGIN
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.puzzle import WINNING_MOVES_PUZZLE
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.image import ImagesPath
from instant_insanity.mobjects.opposite_face_graph import EdgeToSubgraphMapping, OppositeFaceGraph
from instant_insanity.scenes.coordinate_grid import GridMixin


class GraphTheoryScene1(GridMixin, VoiceoverScene):
    images_path: ImagesPath = ImagesPath()
    subpackages: str = "graph_theory.latex"

    def get_image(self, filename: str, height: float = 6.0) -> Mobject:
        image: Mobject = self.images_path.get_image(self.subpackages, filename)
        image.height = height

        return image

    def say(self, text: str) -> None:
        """
        Says text in the scene.
        Args:
            text: The text to say.
        """
        with self.voiceover(text=text) as tracker:
            voiceover_wait(self, tracker)

    def discuss_mobject(self, mobject: Mobject, discussion: str) -> None:
        self.play(FadeIn(mobject))
        self.say(discussion)
        self.play(FadeOut(mobject))

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        topic: Mobject
        image: Mobject
        discussion: str

        # the opposite-face graph
        topic = Tex("the opposite-face graph of Instant Insanity", font_size=48, color=BLACK)
        discussion = """
        Our goal is to represent the Instant Insanity puzzle as a graph and use it to solve the puzzle.
        We refer to this graph as the opposite-face graph for reasons which will become apparent.
        """
        self.discuss_mobject(topic, discussion)

        # create the full Winning Moves opposite-face graph
        full_subgraph: EdgeToSubgraphMapping = OppositeFaceGraph.mk_subgraph_for_flag(True)
        wm_graph: OppositeFaceGraph = OppositeFaceGraph(WINNING_MOVES_PUZZLE, ORIGIN)
        wm_graph.set_subgraph(full_subgraph)
        discussion = """
        Here's the opposite-face graph of the Instant Insanity puzzle.
        Its points represent the four face colours.
        Its lines represent pairs of opposite faces.
        Each of the four cubes has three pairs of opposite faces so the graph has twelve lines.
        This type of graph is called a labelled multigraph.
        We'll define those terms, and some others, next.
        """
        self.discuss_mobject(wm_graph, discussion)

        # What is a graph?
        topic = Tex("What is a graph?", font_size=48, color=BLACK)
        discussion = """
        Let's get started with some graph theory!
        We'll begin by establishing some terminology.
        Mathematicians often give the same name to different things
        and different names to the same thing.
        This holds for the name graph.
        It is used for two different things.
        """
        self.discuss_mobject(topic, discussion)

        # graphs of functions
        topic = Tex("graphs of functions", font_size=48, color=BLACK)
        discussion = """
        In high school we learn that a graph is an x-y plot of some function or relation.
        """
        self.discuss_mobject(topic, discussion)

        # parabola graph
        image = self.get_image("parabola-graph.png")
        image.height = 6.0
        discussion = """
        For example, here's the graph of the function y equals x squared which produces a parabola.
        This kind of graph is not the subject of graph theory.
        """
        self.discuss_mobject(image, discussion)

        # points, lines
        topic = Tex("points, lines", font_size=48, color=BLACK)
        discussion = """
        Mathematicians also give the name graph to any collection of points
        interconnected by lines.
        Every line must begin on some point and must end on some point.
            
        This type of graph is used to represent pairwise relationships between objects.
        We represent each object by a point and each pairwise relationship between objects by a line
        that interconnects the corresponding points.
        """
        self.discuss_mobject(topic, discussion)

        # example simple graph
        toy_graph = self.get_image("example-simple-graph.png")
        discussion = """
        Here's a toy example graph. It has five points and four lines.
        This kind of graph is the subject of graph theory, and the topic of this video.
        """
        self.discuss_mobject(toy_graph, discussion)

        # simple graphs
        topic = Tex("simple graphs", font_size=48, color=BLACK)
        discussion = """
        If no line connects a point to itself and there is at most one line connecting any two
        distinct points then the graph is called a simple graph.
        """
        self.discuss_mobject(topic, discussion)

        # example simple graph
        discussion = """
        Here's the toy graph again.
        Note that each line in this graph connects two distinct points
        and every pair of distinct points is connected by at most one line.
        It is therefore a simple graph.
        """
        self.discuss_mobject(toy_graph, discussion)

        # graph = network
        topic = Tex("graph = network", font_size=48, color=BLACK)
        discussion = """
        Mathematicians sometimes use the name network instead of graph.
        The preferred name depends on the historical development of the subject matter being studied.
        """
        self.discuss_mobject(topic, discussion)

        # point = dot = vertex = node
        topic = Tex("point = dot = vertex = node", font_size=48, color=BLACK)
        discussion = """
        Mathematicians may also give different names to points.
        Some common alternate names for a point are dot, vertex, and node.
        """
        self.discuss_mobject(topic, discussion)

        # line = link = edge = arc
        topic = Tex("line = link = edge = arc", font_size=48, color=BLACK)
        discussion = """
        Similarly, some common alternate names for a line are link, edge, and arc.
        """
        self.discuss_mobject(topic, discussion)

        # use graph, node, edge
        topic = Tex("graphs, nodes, edges", font_size=48, color=BLACK)
        discussion = """
        From now on, we'll consistently use the names graph, node, and edge.
        """
        self.discuss_mobject(topic, discussion)

        # graph layout
        topic = Tex("graph layouts", font_size=48, color=BLACK)
        discussion = """
        Two graphs are considered to be essentially the same if they contain the same number of nodes
        and those nodes are interconnected in the same way. 
        The positions of the nodes and the paths of the edges
        are not essential features of the graph - 
        they just define a particular layout of the graph. 
        We can lay out any graph in many ways. 
        We seek layouts that make the structure of the graph easier to understand.
        """
        self.discuss_mobject(topic, discussion)

        # example crossover graph
        image = self.get_image("example-crossover-graph.png")
        discussion = """
        Here is another layout of our toy graph. 
        This layout is less clear because two of its edges cross each other.
        """
        self.discuss_mobject(image, discussion)

        # this is a natural break point for the scene

        # labelled graph
        topic = Tex("labelled graphs", font_size=48, color=BLACK)
        discussion = """It is often useful to associate data with the nodes and edges of a graph.
        A graph with associated data is called a labelled graph."""
        self.discuss_mobject(topic, discussion)

        # example labelled graph
        image = self.get_image("example-labelled-graph.png")
        discussion = """
        Here's our toy graph with labels added.
        The nodes are labelled A, B, C, D, and E.
        The edges are labelled 1, 2, 3, and 4.
        """
        self.discuss_mobject(image, discussion)

        # labels in the opposite-face graph
        discussion = """
        Here's the opposite-face graph again.
        Its nodes are labelled by the face colours.
        Its edges are labelled by a combination of the cube number and axis name of the face pair.
        We'll explain this in more detail later.
        """
        self.discuss_mobject(wm_graph, discussion)

        # multigraph
        topic = Tex("loops, parallel edges, multigraphs", font_size=48, color=BLACK)
        discussion = """
        An edge that connects a node to itself is called a loop.
        Two edges that connect the same pair of distinct nodes are called parallel edges.
        A graph that contains loops or parallel edges is called a multigraph.
        """
        self.discuss_mobject(topic, discussion)

        # example multigraph
        image = self.get_image("example-multigraph.png")
        discussion = """
        Here's our toy graph with two more edges.
        Edge 5 is a loop at node B.
        Edges 4 and 6 are parallel edges that connect nodes D and E.
        This toy graph is therefore not a simple graph - it is a multigraph.
        In fact, it is a labelled multigraph.
        """
        self.discuss_mobject(image, discussion)

        # opposite-face multigraph
        discussion = """
        Here's the opposite-face graph again.
        It contains loops and parallel edges.
        It is therefore a multigraph.
        In fact, it is a labelled multigraph.
        """
        self.discuss_mobject(wm_graph, discussion)

        # directed graphs
        topic = Tex("directed graphs", font_size=48, color=BLACK)
        discussion = """
        Each edge of a graph represents a relationship between the pair of nodes it interconnects.
        
        Some relationships are symmetric in the sense that they have no direction.
        For example, saying that Alice is a neighbour of Bob is the same as saying that Bob is a neighbour of Alice.
        In this case we can represent the neighbour relationship by a plain, undirected line.

        However, most relationships are not symmetric.
        For example, saying that Alice likes Bob is not the same as saying that Bob likes Alice.
        In this case we can represent the likes relationship by a directed line where the arrow points from the
        person doing the liking to the person who is liked.
        
        A graph in which the edges are directed is called a directed graph.
        """
        self.discuss_mobject(topic, discussion)

        # example directed graph
        image = self.get_image("example-directed-graph.png")
        discussion = """
        Here's our toy graph with directions added to its edges.
        It is therefore a directed graph.
        In fact, it is a directed labelled multigraph.
        """
        self.discuss_mobject(image, discussion)

        # TODO: maybe show the rock-paper-scissors(-lizard-spock) directed graph

        # opposite-face graph
        discussion = """
        Here's the opposite-face graph again.
        It's edges are not directed.
        However, we will encounter directed graphs in the solution of the puzzle.
        We've introduced enough graph theory concepts and terms for now.
        Let's proceed with showing how to use graph theory to solve the puzzle.
        """
        self.discuss_mobject(wm_graph, discussion)

        # TODO: move the discussion of node degrees to where it is used. We'll define subgraphs there too.
        # in-degree, out-degree, total degree
        # topic = Tex("in-degree, out-degree, total degree", font_size=48, color=BLACK)
        # discussion = """
        # We often need to talk about the number of edges that enter or exit a node.
        # This number is called the total degree of the node, or simply its degree.
        # In a directed graph, the number of edges that exit a node is called its out-degree
        # and the number of edges that enter a node is called its in-degree.
        # The sum of the in-degree and the out-degree equals the total degree.
        # """
        # self.discuss_mobject(topic, discussion)

        # example-degree-table.png
        # image = self.get_image("example-degree-table.png")
        # discussion = """
        # We can summarize the degree information in a table with one row for each node.
        # Here's the degree table for our example directed graph.
        # """
        # self.discuss_mobject(image, discussion)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene1()
        scene.render()
