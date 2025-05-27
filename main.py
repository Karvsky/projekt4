import time # Make sure time is imported if it was implicitly used by removed argparse/other parts in the original prompt's main.py
from graph_representation import print_graph_representation, get_edges, get_all_degrees # Added get_edges, get_all_degrees based on their use later
from graph_generation import generate_hamiltonian_graph, generate_non_hamiltonian_graph
from eulerian_cycle import find_eulerian_cycle
from hamiltonian_cycle import find_hamiltonian_cycle
from benchmark import run_benchmarks

def get_int_input(prompt_message, error_message="Invalid input. Please enter a whole number."):
    """Continuously prompts user for an integer until valid input is given."""
    while True:
        try:
            value = int(input(prompt_message))
            return value
        except ValueError:
            print(error_message)

def get_float_input(prompt_message, error_message="Invalid input. Please enter a number."):
    """Continuously prompts user for a float until valid input is given."""
    while True:
        try:
            value = float(input(prompt_message))
            return value
        except ValueError:
            print(error_message)

def main_interactive():
    """Runs the graph algorithm program with an interactive menu."""
    while True:
        print("\n--- Graph Algorithms Menu ---")
        print("1. Generate Hamiltonian graph and find cycles")
        print("2. Generate Non-Hamiltonian graph and find cycles")
        print("3. Run performance benchmarks")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            print("\n--- Generate Hamiltonian Graph ---")
            num_nodes = -1
            while num_nodes <= 0:
                num_nodes = get_int_input("Enter the number of nodes (must be a positive integer): ")
                if num_nodes <= 0:
                    print("Number of nodes must be a positive integer.")
            
            if num_nodes <= 10: # Based on "Ilość wierzchołków większa niż 10"
                 print(f"Warning: For 'hamilton' mode, project specification suggests nodes > 10 (got {num_nodes}).")

            saturation = -1.0
            while not (0 < saturation <= 100):
                saturation = get_float_input("Enter graph saturation percentage (e.g., 30 or 70, must be > 0 and <= 100): ") #
                if not (0 < saturation <= 100):
                    print("Saturation must be between 0 and 100 (exclusive of 0).")
            
            if saturation not in [30.0, 70.0]: #
                print(f"Warning: Project specification suggests 30% or 70% saturation for Hamiltonian graphs (got {saturation}%).")

            print(f"\nGenerating Hamiltonian graph: {num_nodes} nodes, {saturation}% saturation...")
            graph = generate_hamiltonian_graph(num_nodes, saturation)
            graph_type_str = f"Generated Hamiltonian Graph (N={num_nodes}, Sat={saturation}%)"
            is_expected_hamiltonian = True
            process_graph_and_find_cycles(graph, graph_type_str, is_expected_hamiltonian, 'hamilton')

        elif choice == '2':
            print("\n--- Generate Non-Hamiltonian Graph ---")
            num_nodes = -1
            while num_nodes <= 0:
                num_nodes = get_int_input("Enter the number of nodes (must be a positive integer): ")
                if num_nodes <= 0:
                    print("Number of nodes must be a positive integer.")
            
            fixed_saturation_non_h = 50.0 #
            print(f"Note: Saturation for non-Hamiltonian mode is fixed at {fixed_saturation_non_h}%.")
            
            print(f"\nGenerating Non-Hamiltonian graph: {num_nodes} nodes, {fixed_saturation_non_h}% saturation...")
            graph = generate_non_hamiltonian_graph(num_nodes, fixed_saturation_non_h)
            graph_type_str = f"Generated Non-Hamiltonian Graph (N={num_nodes}, Sat={fixed_saturation_non_h}%)"
            is_expected_hamiltonian = False
            process_graph_and_find_cycles(graph, graph_type_str, is_expected_hamiltonian, 'non-hamilton')

        elif choice == '3':
            print("\n--- Running Benchmarks ---") #
            run_benchmarks()

        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def process_graph_and_find_cycles(graph, graph_type_str, is_expected_hamiltonian, mode_name):
    """Helper function to process a generated graph and find cycles."""
    if graph is not None:
        print_graph_representation(graph, graph_type_str)

        # 2. Find Eulerian cycle
        print("\n--- Finding Eulerian Cycle ---")
        euler_cycle = find_eulerian_cycle(graph)
        if euler_cycle:
            # Check if it's just a single node (convention for edgeless graphs)
            if len(euler_cycle) == 1 and not get_edges(graph):
                 print(f"Eulerian Cycle: Conventionally, for a graph with node(s) but no edges, the 'cycle' is {euler_cycle}.")
            elif len(euler_cycle) > 20: # Truncate long cycles for printing
                print(f"Eulerian Cycle found: {euler_cycle[:10]}... (length: {len(euler_cycle)}) ...{euler_cycle[-10:]}")
            else:
                print(f"Eulerian Cycle found: {euler_cycle}")
        else:
            print("No Eulerian Cycle found.")
            # Could add more diagnostics here: check degrees, connectivity.
            degrees = get_all_degrees(graph) # Assumes get_all_degrees is available
            odd_degree_nodes = [node for node, deg in degrees.items() if deg % 2 != 0]
            if odd_degree_nodes:
                print(f"  Reason hint: Found nodes with odd degrees: {odd_degree_nodes[:5]}{'...' if len(odd_degree_nodes)>5 else ''}")

        # 3. Find Hamiltonian cycle (backtracking)
        print("\n--- Finding Hamiltonian Cycle (using backtracking) ---")
        start_hc_time = time.perf_counter()
        hamilton_cycle = find_hamiltonian_cycle(graph)
        end_hc_time = time.perf_counter()
        print(f"  (Search time: {end_hc_time - start_hc_time:.4f} seconds)")

        if hamilton_cycle:
            if len(hamilton_cycle) > 20:
                 print(f"Hamiltonian Cycle found: {hamilton_cycle[:10]}... (length: {len(hamilton_cycle)}) ...{hamilton_cycle[-10:]}")
            else:
                print(f"Hamiltonian Cycle found: {hamilton_cycle}")
            if mode_name == 'non-hamilton' and not is_expected_hamiltonian: # Corrected condition
                print("  Alert: Hamiltonian cycle found in a graph expected to be non-Hamiltonian!")
        else:
            print("No Hamiltonian Cycle found.")
            if mode_name == 'hamilton' and is_expected_hamiltonian: # Corrected condition
                 print("  Alert: No Hamiltonian cycle found in a graph generated to be Hamiltonian!")
    else:
        # This case should ideally be caught by input validation earlier
        print("Error: Graph could not be generated.")


if __name__ == "__main__":
    # main() # Old command-line based main
    main_interactive()