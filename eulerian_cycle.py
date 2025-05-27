# eulerian_cycle.py
import copy
from graph_representation import get_degree, get_nodes, get_edges

def _is_connected_for_euler(graph_orig, num_total_nodes):
    """
    Checks if all vertices with degree > 0 are connected in the graph.
    Uses BFS starting from the first node found with degree > 0.
    """
    graph = copy.deepcopy(graph_orig) # Operate on a copy if modifications were planned, but not needed for BFS
    
    nodes_with_edges = [node for node in graph if get_degree(graph, node) > 0]

    if not nodes_with_edges: # No edges in the graph
        return True # Considered connected for Euler purposes (vacuously true)

    # Perform BFS to check connectivity of the subgraph induced by nodes_with_edges
    q = []
    visited_bfs = set()
    
    # Start BFS from the first node that has edges
    start_node_for_bfs = nodes_with_edges[0]
    q.append(start_node_for_bfs)
    visited_bfs.add(start_node_for_bfs)

    head = 0
    while head < len(q):
        u = q[head]
        head += 1
        for v_neighbor in graph.get(u, []):
            # Only consider neighbors that are part of the 'nodes_with_edges' group
            if v_neighbor in nodes_with_edges and v_neighbor not in visited_bfs:
                visited_bfs.add(v_neighbor)
                q.append(v_neighbor)
                
    return len(visited_bfs) == len(nodes_with_edges)


def find_eulerian_cycle(graph_orig):
    """
    Finds an Eulerian cycle using Hierholzer's algorithm.
    Returns the cycle as a list of vertices, or None if no cycle exists.
    """
    if not graph_orig: # Empty graph
        return [] 

    num_nodes = len(graph_orig)
    # Work on a copy for edge removal
    graph = copy.deepcopy(graph_orig)

    # Condition 1: All vertices must have even degree.
    for node in graph: # Iterate over actual nodes present
        if get_degree(graph, node) % 2 != 0:
            # print(f"Info: Node {node} has odd degree {get_degree(graph, node)}. Not Eulerian.")
            return None

    # Condition 2: All vertices with non-zero degree belong to the same connected component.
    # Use original graph for this check as 'graph' will be modified.
    if not _is_connected_for_euler(graph_orig, num_nodes):
        # print("Info: Graph (nodes with edges) is not connected. Not Eulerian.")
        return None

    # Find a starting node: must have degree > 0 if there are edges.
    start_node = -1
    # Iterate over sorted keys for deterministic behavior if multiple choices
    sorted_nodes = sorted(graph.keys())

    for node_val in sorted_nodes:
        if get_degree(graph, node_val) > 0:
            start_node = node_val
            break
    
    if start_node == -1: # Graph has nodes but no edges
        if num_nodes > 0: return [sorted_nodes[0]] # Convention: path is the first node.
        return [] # Or empty list if truly no nodes.

    tour = []
    curr_path_stack = [start_node]
    
    while curr_path_stack:
        u = curr_path_stack[-1]
        if graph.get(u): # If u has any adjacent edges left
            # Take an arbitrary unvisited edge (u,v)
            v = graph[u].pop(0) # Remove edge u-v from u's list
            graph[v].remove(u)   # Remove edge v-u from v's list
            curr_path_stack.append(v) # Add v to current path
        else:
            # No more edges from u, backtrack and add u to the tour
            tour.append(curr_path_stack.pop())
            
    final_tour = tour[::-1] # Reverse to get the correct order

    # Validate: Tour should start and end at the same node if it's a cycle and used edges.
    if len(final_tour) > 1 and final_tour[0] != final_tour[-1]:
        # This shouldn't happen with Hierholzer's if preconditions are met.
        # print("Error: Tour is not a cycle (does not start and end at the same vertex).")
        return None # Or handle as an Eulerian path if that was the goal

    # Validate that all edges were used. Hierholzer's should ensure this.
    # If any node in the copied 'graph' still has edges, something is wrong or graph was disconnected.
    if any(graph[node] for node in graph): # Check if any adjacency list is non-empty
         # print("Error: Not all edges were covered by the tour.")
         return None

    return final_tour