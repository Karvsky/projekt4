from graph_representation import print_graph_representation
from graph_generation import generate_hamiltonian_graph, generate_non_hamiltonian_graph
from eulerian_cycle import find_eulerian_cycle
from benchmark import run_benchmarks

def get_int_input(prompt, error_msg="Niepoprawna wartość. Podaj liczbę całkowitą."):
    """Pobiera liczbę całkowitą od użytkownika, z walidacją."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(error_msg)

if __name__ == "__main__":
    while True:
        print("Wybierz opcję:")
        print("1. Generuj graf z cyklem Hamiltona")
        print("2. Generuj graf bez cyklu Hamiltona")
        print("3. Znajdź cykl Eulera")
        print("4. Uruchom benchmarki")
        print("5. Wyjście")
        choice = get_int_input("Twój wybór: ")

        if choice == 1:
            n = get_int_input("Podaj liczbę wierzchołków: ")
            while True:
                sat = get_int_input("Wybierz nasycenie (30 lub 70): ")
                if sat in (30, 70):
                    break
                print("Niepoprawne nasycenie. Wybierz 30 lub 70.")
            graph = generate_hamiltonian_graph(n, sat)
            print_graph_representation(graph)

        elif choice == 2:
            n = get_int_input("Podaj liczbę wierzchołków: ")
            while True:
                sat = get_int_input("Wybierz nasycenie (30 lub 70): ")
                if sat in (30, 70):
                    break
                print("Niepoprawne nasycenie. Wybierz 30 lub 70.")
            graph = generate_non_hamiltonian_graph(n, sat)
            print_graph_representation(graph)

        elif choice == 3:
            n = get_int_input("Podaj liczbę wierzchołków: ")
            # Dla przykładu generujemy graf Hamiltona o nasyceniu 70%:
            graph = generate_hamiltonian_graph(n, 70)
            cycle = find_eulerian_cycle(graph)
            if cycle:
                print(f"Cykl Eulera: {cycle}")
            else:
                print("Brak cyklu Eulera.")

        elif choice == 4:
            run_benchmarks()

        elif choice == 5:
            print("Koniec programu.")
            break

        else:
            print("Nieznana opcja, spróbuj ponownie.")
