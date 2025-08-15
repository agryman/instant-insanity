from typing import Dict, Iterable, List, Sequence, Tuple

import math
from manim import (
    Arrow,
    Scene,
    Text,
    VGroup,
    Rectangle,
    FadeIn,
    tempconfig,
)

# ---------------------------------------------------------------------------
# Edit these to define your graph
# ---------------------------------------------------------------------------

NODE_LABELS: Sequence[str] = (
    'parse',
    'tokenize',
    'analyze',
    'optimize',
    'generate IR',
    'emit code',
)

EDGE_LIST: Sequence[Tuple[str, str]] = (
    ('parse', 'analyze'),
    ('tokenize', 'parse'),
    ('analyze', 'optimize'),
    ('analyze', 'generate IR'),
    ('optimize', 'generate IR'),
    ('generate IR', 'emit code'),
)

# Optional local default if you don't already have a project-wide LINEN_CONFIG.
LINEN_CONFIG = {
    'preview': True,
    'quality': 'low_quality',
    'disable_caching': True,
}

# ---------------------------------------------------------------------------
# Layout + building utilities
# ---------------------------------------------------------------------------

def topological_layers(
    nodes: Iterable[str],
    edges: Iterable[Tuple[str, str]],
) -> List[List[str]]:
    """Compute left-to-right topological layers for a DAG.

    Nodes are grouped into layers so that all edges go from a layer i to a layer j > i.
    Raises a ValueError if a cycle is detected or an edge references an unknown node.

    Args:
        nodes: Unique node labels.
        edges: Directed edges as (u, v) pairs, u -> v.

    Returns:
        A list of layers; each layer is a list of node labels.

    """
    node_list = list(dict.fromkeys(nodes))  # stable uniqueness, preserves order
    index = {n: i for i, n in enumerate(node_list)}

    # Validate edges
    for u, v in edges:
        if u not in index or v not in index:
            raise ValueError(f'Edge references unknown node: {(u, v)}')

    # Build indegree and adjacency
    indeg = {n: 0 for n in node_list}
    adj: Dict[str, List[str]] = {n: [] for n in node_list}
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    # Kahn with level propagation (longest distance from any source)
    from collections import deque

    q = deque([n for n in node_list if indeg[n] == 0])
    level = {n: 0 for n in node_list}
    processed = 0

    while q:
        u = q.popleft()
        processed += 1
        for v in adj[u]:
            level[v] = max(level[v], level[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if processed != len(node_list):
        raise ValueError('Graph contains a cycle; a DAG is required.')

    # Pack into layers by level, preserving original relative order per layer
    max_level = max(level.values()) if level else 0
    layers: List[List[str]] = [[] for _ in range(max_level + 1)]
    for n in node_list:
        layers[level[n]].append(n)
    return layers


def make_node(label: str, font_size: int = 28, pad_x: float = 0.35, pad_y: float = 0.25) -> VGroup:
    """Create a labeled rectangular node.

    Args:
        label: The text to display inside the rectangle.
        font_size: Manim font size for the text.
        pad_x: Horizontal padding around the text (scene units).
        pad_y: Vertical padding around the text (scene units).

    Returns:
        A VGroup containing [Rectangle, Text] centered at the origin.

    """
    txt = Text(label, font_size=font_size)
    rect = Rectangle(width=txt.width + 2 * pad_x, height=txt.height + 2 * pad_y)
    node = VGroup(rect, txt)
    txt.move_to(rect.get_center())
    return node


def layout_nodes_by_layers(
    layers: List[List[str]],
    h_spacing: float = 3.5,
    v_spacing: float = 1.7,
) -> Dict[str, VGroup]:
    """Create and position rectangle+text nodes given layered labels.

    Args:
        layers: Node labels organized into left-to-right layers.
        h_spacing: Horizontal spacing between consecutive layers.
        v_spacing: Vertical spacing between nodes in the same layer.

    Returns:
        Mapping from node label to its VGroup (already positioned).

    """
    placed: Dict[str, VGroup] = {}
    for lx, layer in enumerate(layers):
        # Center nodes in this layer vertically around y=0
        n = len(layer)
        if n == 0:
            continue
        total_height = (n - 1) * v_spacing
        y_top = total_height / 2.0
        x = lx * h_spacing
        for i, label in enumerate(layer):
            node = make_node(label)
            y = y_top - i * v_spacing
            node.move_to((x, y, 0))
            placed[label] = node
    # Shift left so the whole graph is centered horizontally
    if layers:
        width = (len(layers) - 1) * h_spacing
        x_shift = -width / 2.0
        for node in placed.values():
            node.shift((x_shift, 0, 0))
    return placed


def build_edge_arrows(
    edges: Iterable[Tuple[str, str]],
    nodes: Dict[str, VGroup],
    buff: float = 0.25,
    tip_ratio: float = 0.06,
) -> VGroup:
    """Build arrow mobjects for each directed edge.

    Args:
        edges: Directed edges as (u, v) pairs.
        nodes: Mapping from node label to its placed VGroup.
        buff: Offset from the node centers along the line to avoid overlapping rectangles.
        tip_ratio: Arrow tip size relative to the arrow length.

    Returns:
        A VGroup containing all arrows.

    """
    arrows = VGroup()
    for u, v in edges:
        src = nodes[u]
        dst = nodes[v]
        start = src.get_center()
        end = dst.get_center()

        # If start==end (shouldn't happen in DAG), nudge to avoid zero-length arrow.
        if (end[0] == start[0]) and (end[1] == start[1]):
            end = end + (0.001, 0.0, 0.0)

        arr = Arrow(
            start=start,
            end=end,
            buff=buff,
            max_tip_length_to_length_ratio=tip_ratio,
            stroke_width=2.5,
        )
        arrows.add(arr)
    return arrows


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------

class DisplayDAG(Scene):
    """Display a directed acyclic graph with rectangular text nodes and arrows.

    The graph is laid out left-to-right by topological layers computed from EDGE_LIST.
    To adapt for your own data, edit NODE_LABELS and EDGE_LIST above.

    """

    def construct(self) -> None:
        """Build and render the DAG."""
        layers = topological_layers(NODE_LABELS, EDGE_LIST)
        node_map = layout_nodes_by_layers(layers)

        # Group nodes for layering/z-index control
        nodes_group = VGroup(*node_map.values())

        arrows = build_edge_arrows(EDGE_LIST, node_map, buff=0.28, tip_ratio=0.065)

        # Draw edges behind nodes
        self.add(arrows)
        self.add(nodes_group)

        # Optional entrance
        self.play(FadeIn(nodes_group, lag_ratio=0.05, run_time=1.0))

        # Keep final frame
        self.wait(0.5)


if __name__ == '__main__':
    # If you already define LINEN_CONFIG elsewhere in your project, you can
    # remove the fallback above and import/use your own config here.
    with tempconfig(LINEN_CONFIG):
        scene = DisplayDAG()
        scene.render()