import random
from graph_representation import create_graph, add_edge, get_edges, get_degree

def generate_hamiltonian_graph(num_nodes, saturation_percentage):
    """
    POPRAWIONA wersja generacji grafu hamiltonowskiego.
    Naprawia błędy w dodawaniu trójkątów i kontroli nasycenia.
    """
    if num_nodes <= 0:
        return create_graph(0)

    graph = create_graph(num_nodes)
    nodes_list = list(range(num_nodes))

    if num_nodes == 1:
        return graph  # {0: []} - pojedynczy wierzchołek

    # Wymieszaj wierzchołki dla losowości
    random.shuffle(nodes_list)

    # 1. Stwórz cykl Hamiltona
    for i in range(num_nodes):
        add_edge(graph, nodes_list[i], nodes_list[(i + 1) % num_nodes])

    max_possible_edges = num_nodes * (num_nodes - 1) // 2
    target_edges = int((saturation_percentage / 100.0) * max_possible_edges)
    
    # Upewnij się, że target_edges >= liczba krawędzi w cyklu Hamiltona
    target_edges = max(target_edges, num_nodes)

    print(f"DEBUG: Cykl Hamilton ma {num_nodes} krawędzi, cel: {target_edges}")

    # 2. POPRAWKA: Dodawaj krawędzie pojedynczo, kontrolując nasycenie
    if num_nodes >= 3:
        # Wszystkie możliwe krawędzie (oprócz już istniejących)
        all_possible_edges = []
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                u, v = nodes_list[i], nodes_list[j]
                if v not in graph.get(u, []):  # Krawędź jeszcze nie istnieje
                    all_possible_edges.append((u, v))
        
        random.shuffle(all_possible_edges)
        
        # Dodawaj krawędzie do osiągnięcia celu, priorytetowo jako części trójkątów
        current_edges = len(get_edges(graph))
        
        while current_edges < target_edges and all_possible_edges:
            edge_to_add = all_possible_edges.pop(0)
            u, v = edge_to_add
            
            # Sprawdź czy dodanie tej krawędzi nie psuje parzystości stopni
            degree_u_before = get_degree(graph, u)
            degree_v_before = get_degree(graph, v)
            
            # Dodaj krawędź tymczasowo
            add_edge(graph, u, v)
            current_edges += 1
            
            # Sprawdź parzystość po dodaniu
            degree_u_after = get_degree(graph, u)
            degree_v_after = get_degree(graph, v)
            
            # Jeśli jeden z wierzchołków ma teraz nieparzysty stopień,
            # spróbuj znaleźć inną krawędź do dodania żeby to naprawić
            if (degree_u_after % 2 != 0 or degree_v_after % 2 != 0) and current_edges < target_edges:
                # Znajdź wierzchołki z nieparzystymi stopniami
                odd_degree_nodes = []
                if degree_u_after % 2 != 0:
                    odd_degree_nodes.append(u)
                if degree_v_after % 2 != 0:
                    odd_degree_nodes.append(v)
                
                # Spróbuj znaleźć krawędź która naprawi parzystość
                fix_found = False
                for i, (x, y) in enumerate(all_possible_edges):
                    if current_edges >= target_edges:
                        break
                        
                    if x in odd_degree_nodes or y in odd_degree_nodes:
                        # Ta krawędź może pomóc naprawić parzystość
                        add_edge(graph, x, y)
                        current_edges += 1
                        all_possible_edges.pop(i)
                        fix_found = True
                        break
                
                if not fix_found and current_edges < target_edges:
                    # Dodaj jeszcze jedną losową krawędź jeśli dostępna
                    if all_possible_edges and current_edges < target_edges:
                        x, y = all_possible_edges.pop(0)
                        add_edge(graph, x, y)
                        current_edges += 1

    # Weryfikacja końcowa
    final_degrees = {node: get_degree(graph, node) for node in graph}
    odd_degrees = [node for node, deg in final_degrees.items() if deg % 2 != 0]
    
    if odd_degrees:
        print(f"WARNING: Graf ma wierzchołki z nieparzystymi stopniami: {odd_degrees}")
        print(f"Stopnie: {final_degrees}")
    
    final_edges = len(get_edges(graph))
    print(f"DEBUG: Graf końcowy ma {final_edges} krawędzi (cel: {target_edges})")
    
    return graph

def generate_non_hamiltonian_graph(num_nodes, saturation_percentage=50.0):
    """
    POPRAWIONA wersja generacji grafu nie-hamiltonowskiego.
    Zapewnia że graf rzeczywiście nie ma cyklu Hamiltona.
    """
    if num_nodes <= 0:
        return create_graph(0)
    
    if num_nodes == 1:
        return create_graph(num_nodes)  # Pojedynczy wierzchołek
    
    if num_nodes == 2:
        # Dla 2 wierzchołków, graf bez krawędzi nie ma cyklu Hamiltona
        return create_graph(num_nodes)

    graph = create_graph(num_nodes)
    nodes_list = list(range(num_nodes))
    
    max_possible_edges = num_nodes * (num_nodes - 1) // 2
    target_edges = int((saturation_percentage / 100.0) * max_possible_edges)

    # STRATEGIA 1: Stwórz graf z izolowanym wierzchołkiem
    if num_nodes >= 3:
        # Wybierz losowy wierzchołek do izolacji
        isolated_vertex = random.choice(nodes_list)
        remaining_vertices = [v for v in nodes_list if v != isolated_vertex]
        
        print(f"DEBUG: Izolujemy wierzchołek {isolated_vertex}")
        
        # Oblicz ile krawędzi może być między pozostałymi wierzchołkami
        remaining_count = len(remaining_vertices)
        max_edges_remaining = remaining_count * (remaining_count - 1) // 2
        
        # Dostosuj target_edges do pomniejszonego grafu
        adjusted_target = min(target_edges, max_edges_remaining)
        
        # Generuj losowe krawędzie między pozostałymi wierzchołkami
        possible_edges = []
        for i in range(len(remaining_vertices)):
            for j in range(i + 1, len(remaining_vertices)):
                possible_edges.append((remaining_vertices[i], remaining_vertices[j]))
        
        random.shuffle(possible_edges)
        
        # Dodaj krawędzie do osiągnięcia celu
        edges_added = 0
        for u, v in possible_edges:
            if edges_added >= adjusted_target:
                break
            add_edge(graph, u, v)
            edges_added += 1
        
        # Wierzchołek isolated_vertex pozostaje bez krawędzi (stopień 0)
    
    # Weryfikacja że graf nie ma cyklu Hamiltona
    # (izolowany wierzchołek gwarantuje brak cyklu Hamiltona)
    degrees = {node: get_degree(graph, node) for node in graph}
    isolated_nodes = [node for node, deg in degrees.items() if deg == 0]
    
    print(f"DEBUG: Graf nie-hamiltonowski ma {len(get_edges(graph))} krawędzi")
    print(f"DEBUG: Wierzchołki izolowane: {isolated_nodes}")
    
    return graph