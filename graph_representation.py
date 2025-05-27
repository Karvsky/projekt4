# graph_representation.py

def create_graph(num_nodes):
    """Initializes an empty graph with a given number of nodes (0 to num_nodes-1)."""
    return {i: [] for i in range(num_nodes)}

def add_edge(graph, u, v, directed=False):
    """Adds an undirected edge between u and v. Avoids duplicate edges."""
    if u not in graph: graph[u] = []
    if v not in graph: graph[v] = []

    if v not in graph[u]:
        graph[u].append(v)
    if not directed:
        if u not in graph[v]:
            graph[v].append(u)

def get_nodes(graph):
    """Returns a list of nodes in the graph."""
    return list(graph.keys())

def get_edges(graph, directed=False):
    """Returns a list of unique edges in the graph."""
    edges = set()
    for u in graph:
        for v in graph[u]:
            if directed:
                edges.add((u, v))
            else:
                # For undirected, store as (min(u,v), max(u,v)) to avoid duplicates like (0,1) and (1,0)
                edge = tuple(sorted((u, v)))
                edges.add(edge)
    return list(edges)

def get_degree(graph, node):
    """Returns the degree of a node."""
    return len(graph.get(node, []))

def get_all_degrees(graph):
    """Returns a dictionary of node degrees."""
    return {node: len(adj_list) for node, adj_list in graph.items()}

def print_graph_representation(graph, representation_name="Adjacency List"):
    """Prints the graph in the chosen representation."""
    print(f"\nGraph Representation ({representation_name}):")
    if not graph:
        if 0 not in graph and len(graph.keys()) == 0 : # Truly empty graph
             print("Graph is empty (no nodes).")
             return
        # Potentially graph with nodes but no edges, or just specific nodes listed
        
    # Handle graph with nodes but potentially no edges correctly
    sorted_nodes = sorted(graph.keys())
    if not sorted_nodes and representation_name != "Adjacency List": # Check if it was meant to have nodes
        pass # Let it print based on graph content

    for node in sorted_nodes:
        neighbors = graph.get(node, [])
        print(f"{node}: {sorted(neighbors)}")
        
    num_graph_nodes = len(graph) # Number of entries in the adjacency list dictionary
    num_edges = len(get_edges(graph)) # Counts unique edges

    print(f"Number of nodes defined in representation: {num_graph_nodes}")
    print(f"Number of unique edges: {num_edges}")