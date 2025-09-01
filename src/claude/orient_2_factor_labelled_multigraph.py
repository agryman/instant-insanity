import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


def create_sample_labeled_multigraph():
    """Create a sample undirected labeled multigraph with 4 nodes, 4 edges, degree 2 for each node"""
    G = nx.MultiGraph()
    # Add edges with specific keys/labels
    G.add_edge(0, 1, key='edge_A')
    G.add_edge(1, 2, key='edge_B')
    G.add_edge(2, 3, key='edge_C')
    G.add_edge(3, 0, key='edge_D')
    return G


def create_labeled_multigraph_with_parallel_edges():
    """Create a labeled multigraph with parallel edges"""
    G = nx.MultiGraph()
    # Parallel edges with different labels
    G.add_edge(0, 1, key='edge_X')
    G.add_edge(0, 1, key='edge_Y')  # Parallel edge with different key
    G.add_edge(2, 3, key='edge_Z')
    G.add_edge(2, 3, key='edge_W')  # Parallel edge with different key
    return G


def create_labeled_multigraph_with_loops():
    """Create a labeled multigraph with self-loops"""
    G = nx.MultiGraph()
    # Self-loops with specific keys
    G.add_edge(0, 0, key='loop_A')  # Self-loop on node 0
    G.add_edge(1, 1, key='loop_B')  # Self-loop on node 1
    G.add_edge(2, 3, key='edge_M')
    G.add_edge(3, 2, key='edge_N')  # Creates parallel edge between 2 and 3
    return G


def orient_labeled_multigraph(G):
    """
    Orient an undirected labeled multigraph where each node has degree 2.
    Returns a directed labeled multigraph where each node has in-degree 1 and out-degree 1.
    Preserves all edge keys/labels exactly.
    """
    # Create directed multigraph
    D = nx.MultiDiGraph()
    D.add_nodes_from(G.nodes())

    # Keep track of which edges (by key) we've already oriented
    oriented_edges = set()

    # Find connected components
    components = list(nx.connected_components(G))

    for component in components:
        # Process each component separately
        remaining_nodes = set(component)

        while remaining_nodes:
            # Start from any remaining node
            start_node = next(iter(remaining_nodes))
            current_node = start_node

            # Traverse the component, orienting edges
            while current_node in remaining_nodes:
                remaining_nodes.discard(current_node)

                # Get all edges incident to current_node with their keys
                incident_edges = []
                for neighbor in G.neighbors(current_node):
                    edge_data = G.get_edge_data(current_node, neighbor)
                    for key, attributes in edge_data.items():
                        edge_tuple = (current_node, neighbor, key)
                        if key not in oriented_edges:
                            incident_edges.append((neighbor, key, attributes))

                # Process unoriented edges
                for neighbor, edge_key, edge_attrs in incident_edges:
                    if edge_key not in oriented_edges:
                        if current_node == neighbor:
                            # Self-loop: orient from node to itself
                            D.add_edge(current_node, current_node, key=edge_key, **edge_attrs)
                        else:
                            # Regular edge: orient from current to neighbor
                            D.add_edge(current_node, neighbor, key=edge_key, **edge_attrs)

                        oriented_edges.add(edge_key)

                        # Move to the neighbor for next iteration (if not self-loop and neighbor unprocessed)
                        if neighbor != current_node and neighbor in remaining_nodes:
                            current_node = neighbor
                            break
                else:
                    # No unoriented edges found, break the loop
                    break

    return D


def verify_orientation(D):
    """Verify that each node has in-degree 1 and out-degree 1"""
    print("Node degree verification:")
    all_valid = True
    for node in D.nodes():
        in_deg = D.in_degree(node)
        out_deg = D.out_degree(node)
        print(f"  Node {node}: in-degree = {in_deg}, out-degree = {out_deg}")
        if in_deg != 1 or out_deg != 1:
            all_valid = False
    return all_valid


def print_labeled_multigraph_info(G, name="Graph"):
    """Print detailed information about a labeled multigraph"""
    print(f"\n{name}:")
    print(f"  Nodes: {list(G.nodes())}")

    print("  Edges with keys:")
    for u, v, key in G.edges(keys=True):
        edge_data = G.get_edge_data(u, v, key)
        if u == v:
            print(f"    {u} -> {v} (key: '{key}') [self-loop]")
        else:
            print(f"    {u} -- {v} (key: '{key}')")

    print(f"  Node degrees: {dict(G.degree())}")


def verify_edge_preservation(G_original, D_oriented):
    """Verify that all edge keys are preserved in the orientation"""
    original_keys = set(key for u, v, key in G_original.edges(keys=True))
    oriented_keys = set(key for u, v, key in D_oriented.edges(keys=True))

    print(f"\nEdge key preservation check:")
    print(f"  Original keys: {sorted(original_keys)}")
    print(f"  Oriented keys: {sorted(oriented_keys)}")
    print(f"  Keys preserved: {original_keys == oriented_keys}")

    return original_keys == oriented_keys


def visualize_labeled_multigraphs(G, D):
    """Visualize both graphs with edge labels"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Position nodes
    pos = nx.spring_layout(G, seed=42)

    # Draw original undirected multigraph
    nx.draw(G, pos, ax=ax1, with_labels=True, node_color='lightblue',
            node_size=800, font_size=14, font_weight='bold',
            edge_color='gray', width=2)

    # Add edge labels for original graph
    edge_labels_G = {(u, v): key for u, v, key in G.edges(keys=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels_G, ax=ax1, font_size=10)
    ax1.set_title("Original Undirected Labeled MultiGraph")

    # Draw oriented directed multigraph
    nx.draw(D, pos, ax=ax2, with_labels=True, node_color='lightcoral',
            node_size=800, font_size=14, font_weight='bold',
            arrows=True, arrowsize=20, arrowstyle='->',
            edge_color='red', width=2)

    # Add edge labels for directed graph
    edge_labels_D = {(u, v): key for u, v, key in D.edges(keys=True)}
    nx.draw_networkx_edge_labels(D, pos, edge_labels_D, ax=ax2, font_size=10)
    ax2.set_title("Oriented Directed Labeled MultiGraph")

    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("LABELED MULTIGRAPH ORIENTATION EXAMPLES")
    print("=" * 70)

    # Example 1: Simple 4-cycle with labeled edges
    print("\nExample 1: Simple 4-cycle with labeled edges")
    G1 = create_sample_labeled_multigraph()
    print_labeled_multigraph_info(G1, "Original Labeled MultiGraph")

    D1 = orient_labeled_multigraph(G1)
    print_labeled_multigraph_info(D1, "Oriented Labeled MultiDiGraph")

    verify_orientation(D1)
    verify_edge_preservation(G1, D1)

    # Example 2: Labeled multigraph with parallel edges
    print("\n" + "=" * 60)
    print("\nExample 2: Labeled MultiGraph with parallel edges")
    G2 = create_labeled_multigraph_with_parallel_edges()
    print_labeled_multigraph_info(G2, "Original Labeled MultiGraph")

    D2 = orient_labeled_multigraph(G2)
    print_labeled_multigraph_info(D2, "Oriented Labeled MultiDiGraph")

    verify_orientation(D2)
    verify_edge_preservation(G2, D2)

    # Example 3: Labeled multigraph with self-loops
    print("\n" + "=" * 60)
    print("\nExample 3: Labeled MultiGraph with self-loops")
    G3 = create_labeled_multigraph_with_loops()
    print_labeled_multigraph_info(G3, "Original Labeled MultiGraph")

    D3 = orient_labeled_multigraph(G3)
    print_labeled_multigraph_info(D3, "Oriented Labeled MultiDiGraph")

    verify_orientation(D3)
    verify_edge_preservation(G3, D3)

    # Visualize one example
    print("\nVisualizing Example 1...")
    visualize_labeled_multigraphs(G1, D1)