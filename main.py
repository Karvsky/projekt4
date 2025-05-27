# main.py
import argparse
from graph_representation import print_graph_representation
from graph_generation import generate_hamiltonian_graph, generate_non_hamiltonian_graph
from eulerian_cycle import find_eulerian_cycle
from hamiltonian_cycle import find_hamiltonian_cycle
from benchmark import run_benchmarks # Import the benchmark function

def main():
    parser = argparse.ArgumentParser(
        description="Project 4: Graph Algorithms - Eulerian and Hamiltonian Cycles. ",
        formatter_class=argparse.RawTextHelpFormatter # For better help text formatting
    )
    
    # Using a subparser for modes might be cleaner if more modes are added later.
    # For now, a single positional argument for mode.
    parser.add_argument(
        'mode',
        choices=['hamilton', 'non-hamilton', 'benchmark'], # Simplified mode names
        help=(
            "Operating mode:\n"
            "  hamilton      : Generate a Hamiltonian graph and find cycles. [cite: 3]\n"
            "  non-hamilton  : Generate a non-Hamiltonian graph and find cycles. [cite: 7]\n"
            "  benchmark     : Run performance benchmarks for cycle detection algorithms. [cite: 3]"
        )
    )
    parser.add_argument(
        '--nodes',
        type=int,
        help="Number of nodes (required for 'hamilton' and 'non-hamilton' modes)."
    )
    parser.add_argument(
        '--saturation',
        type=float, # Percentage
        help="Graph saturation percentage (required for 'hamilton' mode, e.g., 30 or 70). [cite: 4]"
    )

    args = parser.parse_args()

    if args.mode == 'benchmark':
        run_benchmarks()
        return

    # Validate common arguments for graph generation modes
    if args.nodes is None:
        parser.error(f"Mode '{args.mode}' requires the --nodes argument.")
    if args.nodes <= 0:
        parser.error("--nodes must be a positive integer.")

    graph = None
    graph_type_str = ""
    is_expected_hamiltonian = False

    if args.mode == 'hamilton':
        if args.saturation is None:
            parser.error("Mode 'hamilton' requires the --saturation argument.")
        if not (0 < args.saturation <= 100):
             parser.error("--saturation must be between 0 and 100.")
        if args.nodes <= 10: # Based on "Ilość wierzchołków większa niż 10" [cite: 7]
             print(f"Warning: For 'hamilton' mode, project specification suggests nodes > 10 (got {args.nodes}). [cite: 7]")
        # As per instructions, saturation for Hamiltonian should be 30% or 70% [cite: 4]
        if args.saturation not in [30.0, 70.0]:
            print(f"Warning: Project specification suggests 30% or 70% saturation for Hamiltonian graphs (got {args.saturation}%). [cite: 4]")

        print(f"\nGenerating Hamiltonian graph: {args.nodes} nodes, {args.saturation}% saturation...")
        graph = generate_hamiltonian_graph(args.nodes, args.saturation)
        graph_type_str = f"Generated Hamiltonian Graph (N={args.nodes}, Sat={args.saturation}%)"
        is_expected_hamiltonian = True
    
    elif args.mode == 'non-hamilton':
        # Saturation is fixed at 50% for non-Hamiltonian mode as per spec [cite: 7]
        fixed_saturation_non_h = 50.0
        if args.saturation is not None:
            print(f"Warning: Saturation for 'non-hamilton' mode is fixed at {fixed_saturation_non_h}%. Input --saturation ignored.")
        
        print(f"\nGenerating Non-Hamiltonian graph: {args.nodes} nodes, {fixed_saturation_non_h}% saturation...")
        graph = generate_non_hamiltonian_graph(args.nodes, fixed_saturation_non_h)
        graph_type_str = f"Generated Non-Hamiltonian Graph (N={args.nodes}, Sat={fixed_saturation_non_h}%)"
        is_expected_hamiltonian = False


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
            degrees = get_all_degrees(graph)
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
            if args.mode == 'non-hamilton' and is_expected_hamiltonian == False:
                print("  Alert: Hamiltonian cycle found in a graph expected to be non-Hamiltonian!")
        else:
            print("No Hamiltonian Cycle found.")
            if args.mode == 'hamilton' and is_expected_hamiltonian == True:
                 print("  Alert: No Hamiltonian cycle found in a graph generated to be Hamiltonian!")
    else:
        # This case should ideally be caught by argument parsing errors earlier
        if args.mode not in ['benchmark']:
             print("Error: Graph could not be generated with the provided arguments.")

if __name__ == "__main__":
    main()