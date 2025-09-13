"""
This module performs a depth sort on a set of convex, planar polygons
in 3d space where depth is defined by a projection onto a 2d space.
"""
from typing import OrderedDict
import numpy as np
import networkx as nx
from shapely.geometry import Point, Polygon
from shapely.geometry.base import BaseGeometry

from instant_insanity.core.convex_planar_polygon import ConvexPlanarPolygon
from instant_insanity.core.projection import Projection
from instant_insanity.core.geometry_types import *

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

    def depth_sort(self, paths: PolygonIdToVertexPathMapping) -> SortedPolygonIdToVertexPathMapping:
        """
        This function performs a depth sort on a set of vertex paths that define
        convex, planar polygons.
        Each vertex path is identified by a PolygonID which are the keys of the input dict.
        The input vertex paths are given in model space.
        They are projected onto scene space and then depth-sorted.
        The result is returned as an OrderedDict.

        Args:
            paths: a dictionary that maps polygon ids to vertex paths that define convex, planar polygons.

        Returns:
            an ordered dictionary that maps polygon ids to projected and depth-sorted vertex paths.

        Raises:
            ValueError: if the input vertex paths do not define convex, planar polygons or cannot be depth-sorted.
        """
        # check that the input consists of convex, planar polygons
        polygon_id: PolygonId
        path: VertexPath
        convex_planar_polygons: dict[PolygonId, ConvexPlanarPolygon] = {
            polygon_id: ConvexPlanarPolygon(path)
            for polygon_id, path in paths.items()
        }
        # Note that we use ConvexPlanarPolygon to check that
        # each vertex path does in fact define a convex, planar polygon.
        # If not, then ConvexPlanarPolygon will raise an exception.

        # project each vertex path from model space to scene space
        projected_paths: PolygonIdToVertexPathMapping = {
            polygon_id: self.projection.project_points(path)
            for polygon_id, path in paths.items()
        }

        # depth-sort the polygons by performing a topological sort on the directed graph for
        # the binary relation on polygons: A is_behind B

        # initialize the graph by creating a node for each polygon id
        graph: nx.DiGraph = nx.DiGraph()
        polygon_ids: list[PolygonId] = list(paths.keys())
        graph.add_nodes_from(polygon_ids)

        # perform a pair-wise comparison of the projected polygons
        i: int
        polygon_id_i: PolygonId
        for i, polygon_id_i in enumerate(polygon_ids):
            path_i: VertexPath = projected_paths[polygon_id_i]
            polygon_i: Polygon = Polygon(path_i)

            j: int
            polygon_id_j: PolygonId
            for j, polygon_id_j in enumerate(polygon_ids):
                if j <= i:
                    continue
                path_j: np.ndarray = projected_paths[polygon_id_j]
                polygon_j: Polygon = Polygon(path_j)
                if not polygon_i.intersects(polygon_j):
                    continue

                # the projected polygons intersect so compute their intersection
                polygon_ij: BaseGeometry = polygon_i.intersection(polygon_j)

                # if they do not intersect in a Polygon we can ignore it
                if not isinstance(polygon_ij, Polygon):
                    continue

                # if the area is nearly zero we can ignore it
                area: float = polygon_ij.area
                if np.isclose(area, 0.0):
                    continue

                # get a representative point of the intersection
                point_ij: Point = polygon_ij.representative_point()
                x: float = point_ij.x
                y: float = point_ij.y

                t_i: float = self.projection.polygon_t(convex_planar_polygons[polygon_id_i], x, y)
                t_j: float = self.projection.polygon_t(convex_planar_polygons[polygon_id_j], x, y)
                if np.isclose(t_i, t_j):
                    raise ValueError(f'polygons {polygon_id_i} and {polygon_id_j} intersect in model space')
                if t_i < t_j:
                    graph.add_edge(polygon_id_i, polygon_id_j)
                else:
                    graph.add_edge(polygon_id_j, polygon_id_i)

        # we now have built the directed graph for is_behind so check if it's acyclic
        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError('the is_behind relation has cycles')

        sorted_ids: list[PolygonId] = list(nx.topological_sort(graph))

        sorted_paths: SortedPolygonIdToVertexPathMapping = OrderedDict()
        for polygon_id in sorted_ids:
            sorted_paths[polygon_id] = projected_paths[polygon_id]

        return sorted_paths
