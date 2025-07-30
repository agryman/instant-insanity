"""
This module performs a depth sort on a set of convex, planar polygons
in 3d space where depth is defined by a projection onto a 2d space.
"""
import numpy as np
import networkx as nx
from shapely.geometry import Point, Polygon
from shapely.geometry.base import BaseGeometry

from instant_insanity.core.convex_planar_polygon import ConvexPlanarPolygon
from instant_insanity.core.projection import Projection


class DepthSort:
    """
    This class performs a depth sort on a set of convex, planar polygons based
    on a projection onto a 2d space.

    The projection p maps a 3d point (x, y, z) to the point (x', y', t).
    The coordinates (x', y') define the projected point in 2d space.
    The coordinate t defines the depth of the projected point with
    t increasing towards the viewpoint of the projection.

    Given a planar 3d polygon A, we can invert the projection (x', y') to find the
    parameter t.

    If the 2d projections of 3d polygons A and B have a nonempty intersection in 2d space,
    then we can choose any point p = (x', y') in their nonempty intersection.
    We then invert the projection to find the parameters t_A and t_B.

    Now assume that polygons A and B do not intersect in 3d space.
    This implies that t_A is not equal to t_B.
    If t_A < t_B then A is behind B in the drawing order.
    Conversely, if t_B < t_A then B is behind A in the drawing order.

    Suppose we have arranged all the polygons in a list P such whenever
    P[i] is behind P[j] then i < j.
    We can draw the scene in the order defined by the list to achieve the correct appearance.
    This is called the Painter's Algorithm.

    The spatial geometry of a polygon is defined by its vertex list.
    However, a polygon may have other attributes, such as fill colour.
    For generality, we'll assume that the bookkeeping for the nongeometric attributes
    of a polygon is handled elsewhere. We'll only assume that each polygon is
    uniquely identified by a string identifier. The input to the sort function will
    therefore be a dictionary that maps identifiers to vertex lists. The output
    will include a list of identifiers in proper depth-sort order.

    The depth-sort algorithm requires that we project the 3d vertices onto 2d space.
    These projected vertices will be what we actually render. Therefore, in order to
    avoid unnecessary recomputation of the projections, the algorithm with also return
    a dictionary of the projected polygons.


    Attributes:
        projection: the projection map

    """
    projection: Projection

    def __init__(self, projection: Projection):
        self.projection = projection

    def depth_sort(self, polygons: dict[str, np.ndarray]) -> tuple[list[str], dict[str, np.ndarray]]:
        """
        This function performs a depth sort on a set of convex, planar polygons
        Args:
            polygons: a dictionary that maps identifiers to convex, planar polygons

        Returns:
            a tuple containing:
                the depth-sorted list of polygon identifiers, and
                a dictionary of the 2d projections of the 3d polygons
        """

        # check that the input consists of convex, planar polygons
        name: str
        vertices: np.ndarray
        convex_planar_polygons: dict[str, ConvexPlanarPolygon] = {
            name: ConvexPlanarPolygon(vertices)
            for name, vertices in polygons.items()
        }

        # project each 3d polygon onto 2d space
        projected_polygons: dict[str, np.ndarray] = {
            name: self.projection.project_points(vertices)
            for name, vertices in polygons.items()
        }

        # depth-sort the polygons by performing a topological sort on the directed graph for
        # the binary relation on polygons: A is_behind B

        # initialize the graph by creating a node for each polygon
        graph: nx.DiGraph = nx.DiGraph()
        names: list[str] = list(polygons.keys())
        graph.add_nodes_from(names)

        # perform a pair-wise comparison of the projected polygons
        i: int
        name_i: str
        for i, name_i in enumerate(names):
            vertices_i: np.ndarray = projected_polygons[name_i]
            polygon_i: Polygon = Polygon(vertices_i)
            j: int
            name_j: str
            for j, name_j in enumerate(names):
                if j <= i:
                    continue
                vertices_j: np.ndarray = projected_polygons[name_j]
                polygon_j: Polygon = Polygon(vertices_j)
                if not polygon_i.intersects(polygon_j):
                    continue

                # the projected polygons intersect so compute the intersection
                polygon_ij: BaseGeometry = polygon_i.intersection(polygon_j)

                # if they do not intersect in a Polygon we can ignore it
                if not isinstance(polygon_ij, Polygon):
                    continue

                # get a representative point of the intersection
                point_ij: Point = polygon_ij.representative_point()
                x: float = point_ij.x
                y: float = point_ij.y

                t_i: float = self.projection.polygon_t(convex_planar_polygons[name_i], x, y)
                t_j: float = self.projection.polygon_t(convex_planar_polygons[name_j], x, y)
                if np.isclose(t_i, t_j):
                    raise ValueError(f'polygons {name_i} and {name_j} intersect in model space')
                if t_i < t_j:
                    graph.add_edge(name_i, name_j)
                else:
                    graph.add_edge(name_j, name_i)

        # we now have built the directed graph for is_behind so check if it's acyclic
        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError('the is_behind relation has cycles')

        sorted_names: list[str] = list(nx.topological_sort(graph))

        return sorted_names, projected_polygons
