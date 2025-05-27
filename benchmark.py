# benchmark.py
import time
import matplotlib.pyplot as plt
from graph_generation import generate_hamiltonian_graph, generate_non_hamiltonian_graph
from eulerian_cycle import find_eulerian_cycle
from hamiltonian_cycle import find_hamiltonian_cycle
# from graph_representation import print_graph_representation # For debugging

def run_benchmarks():
    """
    Runs benchmarks for Eulerian and Hamiltonian cycle algorithms and generates plots.
    Follows specifications from section 4 of the project description.
    """
    print("Running benchmarks...\n")

    # Part 1: Hamiltonian graphs, Euler and Hamilton cycle times [cite: 3]
    # Nodes > 10 for generated Hamiltonian graphs. [cite: 7]
    # Saturations: 30% and 70%. [cite: 4]
    node_counts_h_graphs = [11, 12, 13, 14, 15, 16] # Example N values, adjust as needed. Max 15-16 for HC.
    saturations_h_graphs = [30.0, 70.0]

    results_euler = {sat: {'n': [], 'time': []} for sat in saturations_h_graphs}
    results_hamilton_on_h = {sat: {'n': [], 'time': []} for sat in saturations_h_graphs}

    print("Benchmarking on Hamiltonian Graphs:")
    for n_val in node_counts_h_graphs:
        for sat_val in saturations_h_graphs:
            print(f"  N={n_val}, Saturation={sat_val}%")
            # For robust results, one might average over multiple graph instances.
            # Here, one instance per (n, sat) pair for simplicity.
            graph_h = generate_hamiltonian_graph(n_val, sat_val)

            # Time Eulerian cycle detection
            start_t = time.perf_counter()
            find_eulerian_cycle(graph_h)
            end_t = time.perf_counter()
            results_euler[sat_val]['n'].append(n_val)
            results_euler[sat_val]['time'].append(end_t - start_t)

            # Time Hamiltonian cycle detection
            start_t = time.perf_counter()
            find_hamiltonian_cycle(graph_h)
            end_t = time.perf_counter()
            results_hamilton_on_h[sat_val]['n'].append(n_val)
            results_hamilton_on_h[sat_val]['time'].append(end_t - start_t)

    # Plotting for Hamiltonian graphs (t=f(n) for Euler, t=f(n) for Hamilton)
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    for sat_val in saturations_h_graphs:
        ax1.plot(results_euler[sat_val]['n'], results_euler[sat_val]['time'], marker='o', linestyle='-', label=f'Saturation {sat_val}%')
    ax1.set_xlabel("Number of Nodes (n)")
    ax1.set_ylabel("Time (seconds)")
    ax1.set_title("Eulerian Cycle Detection Time (on Hamiltonian Graphs)")
    ax1.legend()
    ax1.grid(True)

    for sat_val in saturations_h_graphs:
        ax2.plot(results_hamilton_on_h[sat_val]['n'], results_hamilton_on_h[sat_val]['time'], marker='o', linestyle='-', label=f'Saturation {sat_val}%')
    ax2.set_xlabel("Number of Nodes (n)")
    ax2.set_ylabel("Time (seconds)")
    ax2.set_title("Hamiltonian Cycle Detection Time (on Hamiltonian Graphs)")
    ax2.legend()
    ax2.grid(True)
    
    fig1.suptitle("Performance on Generated Hamiltonian Graphs")
    fig1.tight_layout(rect=[0, 0, 1, 0.96]) # Adjust layout to make space for suptitle
    plt.savefig("benchmark_hamiltonian_graphs.png")
    print("\nPlot saved: benchmark_hamiltonian_graphs.png")

    # Part 2: Non-Hamiltonian graphs, Hamilton cycle time [cite: 7]
    # N is small (e.g., 20-30), Saturation 50%. [cite: 7]
    node_counts_non_h_graphs = [10, 12, 14, 16, 18, 20] # Example N values up to ~20.
    saturation_non_h = 50.0
    results_hamilton_on_non_h = {'n': [], 'time': []}

    print("\nBenchmarking on Non-Hamiltonian Graphs (Hamiltonian Cycle Detection):")
    for n_val in node_counts_non_h_graphs:
        print(f"  N={n_val}, Saturation={saturation_non_h}% (Non-Hamiltonian)")
        graph_non_h = generate_non_hamiltonian_graph(n_val, saturation_non_h)
        
        start_t = time.perf_counter()
        find_hamiltonian_cycle(graph_non_h) # Expected to be None
        end_t = time.perf_counter()
        results_hamilton_on_non_h['n'].append(n_val)
        results_hamilton_on_non_h['time'].append(end_t - start_t)

    # Plotting for non-Hamiltonian graphs (t=f(n) for Hamilton)
    plt.figure(figsize=(8, 6))
    plt.plot(results_hamilton_on_non_h['n'], results_hamilton_on_non_h['time'], marker='o', linestyle='-', label=f'Saturation {saturation_non_h}%')
    plt.xlabel("Number of Nodes (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Hamiltonian Cycle Detection Time (on Non-Hamiltonian Graphs)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("benchmark_non_hamiltonian_graphs.png")
    print("Plot saved: benchmark_non_hamiltonian_graphs.png")
    
    print("\n--- Benchmarks Complete ---")
    # plt.show() # Uncomment to display plots interactively after saving