# hamiltonian_cycle.py

def _find_hamiltonian_cycle_recursive(graph, num_total_nodes, current_node, path_list, visited_nodes_map, first_node_in_path):
    path_list.append(current_node)
    visited_nodes_map[current_node] = True

    if len(path_list) == num_total_nodes:
        # All nodes visited, check if it can return to the start (first_node_in_path)
        if first_node_in_path in graph.get(current_node, []): # Neighbors of current_node
            return True # Cycle found
        else:
            # Cannot close cycle from this path, backtrack
            visited_nodes_map[path_list.pop()] = False
            return False

    # Try neighbors of current_node
    # Sort neighbors for deterministic behavior (optional, but good for testing)
    sorted_neighbors = sorted(graph.get(current_node, []))

    for neighbor in sorted_neighbors:
        if not visited_nodes_map.get(neighbor, False): # Check if neighbor is visited
            if _find_hamiltonian_cycle_recursive(graph, num_total_nodes, neighbor, path_list, visited_nodes_map, first_node_in_path):
                return True # Cycle found in deeper recursion

    # No Hamiltonian cycle found from current_node with current path, backtrack
    visited_nodes_map[path_list.pop()] = False
    return False


def find_hamiltonian_cycle(graph):
    """
    Finds a Hamiltonian cycle in the graph using backtracking.
    Returns the cycle as a list of vertices (e.g., [0, 1, 2, 0]), or None.
    """
    num_graph_nodes = len(graph) # Number of nodes defined in the graph structure
    
    if num_graph_nodes == 0:
        return None # Or [] for empty path/cycle

    # Standard definitions often require N>=3 for a Hamiltonian cycle.
    # For N=1, a cycle could be [v0, v0] if self-loops are edges, or just [v0].
    # For N=2, v0-v1, cycle is [v0, v1, v0].
    # The problem implies N > 10 for Hamiltonian generation, so finder will mostly see larger graphs.

    if num_graph_nodes == 1:
        node = list(graph.keys())[0]
        # A single node can be a cycle [node, node] if it has a self-loop,
        # or just [node] by convention. Let's return [node, node] if self-loop, else None.
        if node in graph.get(node, []): # Check for self-loop
             return [node, node]
        # If we adopt the convention that a single node is a cycle: return [node]
        # However, to be consistent with "cycle path format", and backtracking logic,
        # a cycle needs to "return". If no self-loop, the general algo below will return None.
        # Let's stick to the general algorithm's findings.
        # The recursive function should correctly determine this.

    path = []
    # visited_nodes_map: Using dict for visited status in case node IDs are not 0 to N-1 contiguous.
    # graph_representation.py uses 0 to N-1 nodes.
    visited = {node: False for node in graph.keys()} 
    
    # Try starting from each node. If a HC exists, it can be found from any start.
    # For simplicity and to match problem spec (N>10), we can start from a fixed node (e.g., smallest ID).
    # Nodes are assumed to be integers.
    
    # Sort nodes to ensure a deterministic starting point if graph keys are not ordered.
    # (Python dicts are ordered from 3.7+, but explicit sort is safer).
    potential_start_nodes = sorted(list(graph.keys()))
    
    if not potential_start_nodes: # Should be caught by num_graph_nodes == 0
        return None

    start_node = potential_start_nodes[0] # Pick the first node as a starting point.

    # Call the recursive helper
    if _find_hamiltonian_cycle_recursive(graph, num_graph_nodes, start_node, path, visited, start_node):
        return path + [path[0]] # Close the cycle by appending the start node
    else:
        return None