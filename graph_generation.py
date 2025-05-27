# Plik: graph_generation.py
import random
from graph_representation import create_graph, add_edge, get_edges

def generate_hamiltonian_graph(num_nodes, saturation_percentage):
    """
    Generuje graf z cyklem Hamiltona oraz z dokładnym nasyceniem 30% lub 70%.
    """
    if saturation_percentage not in (30, 70):
        raise ValueError("Saturacja musi być dokładnie 30 lub 70.")

    if num_nodes <= 0:
        return create_graph(0)

    graph = create_graph(num_nodes)
    nodes = list(range(num_nodes))

    # Tworzymy bazowy cykl Hamiltona
    for i in range(num_nodes):
        add_edge(graph, nodes[i], nodes[(i + 1) % num_nodes])

    # Oblicz docelową liczbę krawędzi
    max_edges = num_nodes * (num_nodes - 1) // 2
    target_edges = (saturation_percentage * max_edges) // 100
    current_edges = len(get_edges(graph))

    # Dodaj losowe krawędzie, aż osiągniemy dokładne nasycenie
    possible_pairs = [(u, v) for u in nodes for v in nodes if u < v]
    random.shuffle(possible_pairs)
    for u, v in possible_pairs:
        if current_edges >= target_edges:
            break
        if v not in graph[u]:
            add_edge(graph, u, v)
            current_edges += 1

    return graph

def generate_non_hamiltonian_graph(num_nodes, saturation_percentage):
    """
    Generuje graf bez cyklu Hamiltona (z izolowanym wierzchołkiem) oraz
    z dokładnym nasyceniem 30% lub 70%.
    """
    if saturation_percentage not in (30, 70):
        raise ValueError("Saturacja musi być dokładnie 30 lub 70.")

    if num_nodes <= 0:
        return create_graph(0)

    graph = create_graph(num_nodes)
    nodes = list(range(num_nodes))
    isolated = nodes[0]

    # Oblicz docelową liczbę krawędzi
    max_edges = num_nodes * (num_nodes - 1) // 2
    target_edges = (saturation_percentage * max_edges) // 100
    current_edges = 0

    possible_pairs = [
        (u, v)
        for u in nodes if u != isolated
        for v in nodes if v != isolated and u < v
    ]
    random.shuffle(possible_pairs)
    for u, v in possible_pairs:
        if current_edges >= target_edges:
            break
        add_edge(graph, u, v)
        current_edges += 1

    return graph
