import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


def create_sample_multigraph():
    """Create a sample undirected multigraph with 4 nodes, 4 edges, degree 2 for each node"""
    G = nx.MultiGraph()
    # Example 1: Simple 4-cycle
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
    return G


def create_multigraph_with_parallel_edges():
    """Create a multigraph with parallel edges"""
    G = nx.MultiGraph()
    # Two parallel edges between nodes 0 and 1, and between nodes 2 and 3
    G.add_edge(0, 1)  # First edge between 0 and 1
    G.add_edge(0, 1)  # Second parallel edge between 0 and 1
    G.add_edge(2, 3)  # First edge between 2 and 3
    G.add_edge(2, 3)  # Second parallel edge between 2 and 3
    return G


def create_multigraph_with_loops():
    """Create a multigraph with self-loops"""
    G = nx.MultiGraph()
    # Self-loops count as degree 2 each
    G.add_edge(0, 0)  # Self-loop on node 0 (contributes degree 2)
    G.add_edge(1, 1)  # Self-loop on node 1 (contributes degree 2)
    G.add_edge(2, 3)  # Regular edge
    G.add_edge(3, 2)  # This creates a second edge between 2 and 3
    return G


def orient_multigraph(G):
    """
    Orient an undirected multigraph where each node has degree 2.
    Returns a directed multigraph where each node has in-degree 1 and out-degree 1.
    Handles parallel edges and self-loops.
    """
    # Create directed multigraph
    D = nx.MultiDiGraph()
    D.add_nodes_from(G.nodes())

    # Keep track of which edges we've already oriented
    oriented_edges = set()

    # Find connected components (each will form cycles, possibly with parallel edges)
    components = list(nx.connected_components(G))

    for component in components:
        # Get subgraph for this component
        subgraph = G.subgraph(component)

        # Handle each node in the component
        remaining_nodes = set(component)

        while remaining_nodes:
            # Start from any remaining node
            start_node = next(iter(remaining_nodes))
            current_node = start_node

            # Trace a path/cycle starting from this node
            while current_node in remaining_nodes:
                remaining_nodes.discard(current_node)

                # Find neighbors of current node that haven't been fully processed
                neighbors = list(G.neighbors(current_node))

                # Handle self-loops first (they're special)
                if current_node in neighbors:
                    # Count self-loops
                    self_loop_count = G.number_of_edges(current_node, current_node)
                    for i in range(self_loop_count):
                        edge_key = (current_node, current_node, i)
                        if edge_key not in oriented_edges:
                            D.add_edge(current_node, current_node)
                            oriented_edges.add(edge_key)
                    # Remove self from neighbors list for further processing
                    neighbors = [n for n in neighbors if n != current_node]

                # Process connections to other nodes
                unprocessed_neighbors = [n for n in neighbors if n in remaining_nodes or
                                         any((current_node, n, k) not in oriented_edges
                                             for k in range(G.number_of_edges(current_node, n)))]

                if unprocessed_neighbors:
                    # Pick the first unprocessed neighbor
                    next_node = unprocessed_neighbors[0]

                    # Add one directed edge from current to next
                    edge_count = G.number_of_edges(current_node, next_node)
                    for k in range(edge_count):
                        edge_key_1 = (current_node, next_node, k)
                        edge_key_2 = (next_node, current_node, k)

                        if edge_key_1 not in oriented_edges and edge_key_2 not in oriented_edges:
                            D.add_edge(current_node, next_node)
                            oriented_edges.add(edge_key_1)
                            oriented_edges.add(edge_key_2)
                            break

                    current_node = next_node
                else:
                    break

    return D


def verify_orientation(D):
    """Verify that each node has in-degree 1 and out-degree 1"""
    for node in D.nodes():
        in_deg = D.in_degree(node)
        out_deg = D.out_degree(node)
        print(f"Node {node}: in-degree = {in_deg}, out-degree = {out_deg}")
        if in_deg != 1 or out_deg != 1:
            return False
    return True


def visualize_multigraphs(G, D):
    """Visualize both the original undirected multigraph and the oriented directed multigraph"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Position nodes for better visualization
    pos = nx.spring_layout(G, seed=42)

    # Draw original undirected multigraph
    nx.draw(G, pos, ax=ax1, with_labels=True, node_color='lightblue',
            node_size=700, font_size=16, font_weight='bold',
            edge_color='gray', width=2)
    ax1.set_title("Original Undirected MultiGraph")

    # Draw oriented directed multigraph
    nx.draw(D, pos, ax=ax2, with_labels=True, node_color='lightcoral',
            node_size=700, font_size=16, font_weight='bold',
            arrows=True, arrowsize=20, arrowstyle='->',
            edge_color='red', width=2)
    ax2.set_title("Oriented Directed MultiGraph")

    plt.tight_layout()
    plt.show()


def print_multigraph_info(G, name="Graph"):
    """Print detailed information about a multigraph"""
    print(f"\n{name}:")
    print(f"Nodes: {list(G.nodes())}")
    print(f"Edges with keys: {list(G.edges(keys=True))}")
    print(f"Degrees: {dict(G.degree())}")

    # Print parallel edges and self-loops info
    for u, v in G.edges():
        if u <= v:  # Avoid duplicates in undirected case
            edge_count = G.number_of_edges(u, v)
            if edge_count > 1:
                print(f"  Parallel edges between {u} and {v}: {edge_count}")
            if u == v:
                print(f"  Self-loop on node {u}")


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("MULTIGRAPH ORIENTATION EXAMPLES")
    print("=" * 60)

    # Example 1: Simple 4-cycle
    print("\nExample 1: Simple 4-cycle")
    G1 = create_sample_multigraph()
    print_multigraph_info(G1, "Original MultiGraph")

    D1 = orient_multigraph(G1)
    print_multigraph_info(D1, "Oriented MultiDiGraph")

    print("\nVerification:")
    is_valid = verify_orientation(D1)
    print(f"Valid orientation: {is_valid}")

    # Example 2: Multigraph with parallel edges
    print("\n" + "=" * 50)
    print("\nExample 2: MultiGraph with parallel edges")
    G2 = create_multigraph_with_parallel_edges()
    print_multigraph_info(G2, "Original MultiGraph")

    D2 = orient_multigraph(G2)
    print_multigraph_info(D2, "Oriented MultiDiGraph")

    print("\nVerification:")
    is_valid = verify_orientation(D2)
    print(f"Valid orientation: {is_valid}")

    # Example 3: Multigraph with self-loops
    print("\n" + "=" * 50)
    print("\nExample 3: MultiGraph with self-loops")
    G3 = create_multigraph_with_loops()
    print_multigraph_info(G3, "Original MultiGraph")

    D3 = orient_multigraph(G3)
    print_multigraph_info(D3, "Oriented MultiDiGraph")

    print("\nVerification:")
    is_valid = verify_orientation(D3)
    print(f"Valid orientation: {is_valid}")

    # Visualize one of the examples
    visualize_multigraphs(G1, D1)
