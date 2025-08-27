import networkx as nx
import matplotlib.pyplot as plt


def create_sample_graph():
    """Create a sample undirected graph with 4 nodes, 4 edges, degree 2 for each node"""
    G = nx.Graph()
    # Create a 4-cycle: 0-1-2-3-0
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
    return G


def orient_graph(G):
    """
    Orient an undirected graph where each node has degree 2.
    Returns a directed graph where each node has in-degree 1 and out-degree 1.
    """
    # Create directed graph
    D = nx.DiGraph()
    D.add_nodes_from(G.nodes())

    # Find connected components (each will be a cycle)
    components = list(nx.connected_components(G))

    for component in components:
        # Convert component to subgraph
        subgraph = G.subgraph(component)

        # Find a cycle in this component
        cycle = nx.find_cycle(subgraph)

        # Orient the cycle - add directed edges following the cycle order
        for u, v in cycle:
            if not D.has_edge(u, v) and not D.has_edge(v, u):
                D.add_edge(u, v)

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


def visualize_graphs(G, D):
    """Visualize both the original undirected graph and the oriented directed graph"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Position nodes in a circle for better visualization
    pos = nx.circular_layout(G)

    # Draw original undirected graph
    nx.draw(G, pos, ax=ax1, with_labels=True, node_color='lightblue',
            node_size=500, font_size=16, font_weight='bold')
    ax1.set_title("Original Undirected Graph\n(4 nodes, 4 edges, degree 2 each)")

    # Draw oriented directed graph
    nx.draw(D, pos, ax=ax2, with_labels=True, node_color='lightcoral',
            node_size=500, font_size=16, font_weight='bold',
            arrows=True, arrowsize=20, arrowstyle='->')
    ax2.set_title("Oriented Directed Graph\n(in-degree 1, out-degree 1 each)")

    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    # Create sample graph
    G = create_sample_graph()

    print("Original undirected graph:")
    print(f"Nodes: {list(G.nodes())}")
    print(f"Edges: {list(G.edges())}")
    print(f"Degrees: {dict(G.degree())}")

    # Orient the graph
    D = orient_graph(G)

    print("\nOriented directed graph:")
    print(f"Directed edges: {list(D.edges())}")

    # Verify the orientation
    print("\nVerification:")
    is_valid = verify_orientation(D)
    print(f"Valid orientation (all nodes have in-degree=1, out-degree=1): {is_valid}")

    # Visualize
    visualize_graphs(G, D)


# Alternative example: two disconnected 2-cycles
def create_two_cycles_graph():
    """Create a graph with two disconnected 2-cycles (4 nodes, 4 edges total)"""
    G = nx.Graph()
    # Two 2-cycles: (0-1-0) and (2-3-2)
    G.add_edges_from([(0, 1), (1, 0), (2, 3), (3, 2)])  # This creates multi-edges
    # Actually, let's create it properly:
    G = nx.MultiGraph()
    G.add_edges_from([(0, 1), (0, 1), (2, 3), (2, 3)])  # Two edges between each pair
    return G


print("\n" + "=" * 50)
print("Alternative example with MultiGraph (two 2-cycles):")

# Note: The above MultiGraph approach works but is unusual.
# Let's show a more typical example with a single 4-cycle:
G_cycle4 = nx.cycle_graph(4)  # Creates nodes 0,1,2,3 in a cycle
print(f"4-cycle graph - Nodes: {list(G_cycle4.nodes())}")
print(f"4-cycle graph - Edges: {list(G_cycle4.edges())}")
print(f"4-cycle graph - Degrees: {dict(G_cycle4.degree())}")

D_cycle4 = orient_graph(G_cycle4)
print(f"Oriented 4-cycle - Directed edges: {list(D_cycle4.edges())}")
verify_orientation(D_cycle4)
