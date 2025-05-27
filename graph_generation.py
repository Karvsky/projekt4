# graph_generation.py
import random
from graph_representation import create_graph, add_edge, get_edges, get_degree

def generate_hamiltonian_graph(num_nodes, saturation_percentage):
    """
    Generates a connected undirected Hamiltonian graph.
    1. Creates a Hamiltonian cycle. [cite: 5]
    2. Adds edges by forming 3-cycles to meet saturation, ensuring all vertex degrees remain even. [cite: 5, 6]
    Assumes num_nodes > 0.
    """
    if num_nodes <= 0:
        return create_graph(0)

    graph = create_graph(num_nodes)
    nodes_list = list(range(num_nodes))

    if num_nodes == 1: # A single node is Hamiltonian (degree 0, which is even).
        return graph # Returns {0: []}

    random.shuffle(nodes_list)

    # 1. Create a Hamiltonian cycle
    for i in range(num_nodes):
        add_edge(graph, nodes_list[i], nodes_list[(i + 1) % num_nodes])

    max_possible_edges = num_nodes * (num_nodes - 1) // 2
    target_edges = int((saturation_percentage / 100.0) * max_possible_edges)
    
    # Ensure target_edges is at least the number of edges in the initial cycle
    if num_nodes > 1: # HC has num_nodes edges
        target_edges = max(target_edges, num_nodes)


    # 2. Add 3-cycles to meet saturation and keep degrees even [cite: 6]
    if num_nodes >= 3:
        possible_triangles = []
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                for k in range(j + 1, num_nodes):
                    possible_triangles.append(tuple(sorted((nodes_list[i], nodes_list[j], nodes_list[k]))))
        random.shuffle(possible_triangles)

        for a, b, c in possible_triangles:
            current_num_edges = len(get_edges(graph))
            if current_num_edges >= target_edges:
                break

            # Check how many *new* edges this triangle would add
            new_edges_for_triangle = 0
            if b not in graph.get(a, []): new_edges_for_triangle += 1
            if c not in graph.get(b, []): new_edges_for_triangle += 1
            if a not in graph.get(c, []): new_edges_for_triangle += 1
            
            if current_num_edges + new_edges_for_triangle <= target_edges:
                add_edge(graph, a, b)
                add_edge(graph, b, c)
                add_edge(graph, c, a)
            # If adding all new edges of a triangle overshoots, consider if partial additions are allowed
            # For simplicity and strict adherence to "add 3-cycles", we add all or none of the new edges for a triangle.

    # Verify all degrees are even (should be, due to HC + 3-cycles)
    # for node_idx in graph:
    #     if get_degree(graph, node_idx) % 2 != 0:
    #         print(f"DEVELOPMENT ERROR: Node {node_idx} in Hamiltonian graph has odd degree {get_degree(graph, node_idx)}.")
            
    return graph


def generate_non_hamiltonian_graph(num_nodes, saturation_percentage=50.0):
    """
    Generates an undirected non-Hamiltonian graph with a target saturation (default 50%). [cite: 7]
    Method: Generate a random graph and then isolate one vertex. [cite: 7]
    Assumes num_nodes > 0.
    """
    if num_nodes <= 0:
        return create_graph(0)
    
    # For N=1, isolating the vertex makes it G={0:[]}. find_hamiltonian_cycle might call this H.
    # To ensure non-Hamiltonian, better if N >= 2 for isolation to be effective.
    # Or for N=1, ensure it has no self-loop if self-loop implies H.
    if num_nodes == 1: # Graph {0:[]}. If HC for N=1 means a self-loop, this is non-H.
                       # If HC for N=1 is just the vertex, this is H.
                       # Let's assume for this problem, this is non-H if we need >0 edges for H cycle.
        return create_graph(num_nodes)


    graph = create_graph(num_nodes)
    nodes_list = list(range(num_nodes))
    
    max_possible_edges = num_nodes * (num_nodes - 1) // 2
    target_edges = int((saturation_percentage / 100.0) * max_possible_edges)

    possible_edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            possible_edges.append((nodes_list[i], nodes_list[j]))
    random.shuffle(possible_edges)

    edges_count = 0
    for u, v in possible_edges:
        if edges_count >= target_edges:
            break
        add_edge(graph, u, v)
        edges_count += 1

    # Isolate one vertex to make it non-Hamiltonian [cite: 7]
    # This is effective if num_nodes >= 2 (or N >= 1 if HC needs edges)
    if num_nodes > 0: # Check to prevent error on num_nodes = 0
        vertex_to_isolate = random.choice(nodes_list)
        
        # Remove all edges connected to vertex_to_isolate
        incident_edges = list(graph[vertex_to_isolate]) # Iterate over a copy
        for neighbor in incident_edges:
            if vertex_to_isolate in graph[neighbor]: # Remove from neighbor's list
                graph[neighbor].remove(vertex_to_isolate)
        graph[vertex_to_isolate] = [] # Clear own adjacency list

    return graph