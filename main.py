import sys
from time import perf_counter
from board import Board, solve_numberlink, is_board_solved, SolveStats


def main():
    # -----------------------------
    # Validar argumentos
    # -----------------------------
    if len(sys.argv) != 3:
        print("Uso:")
        print("   python main.py <archivo_tablero> <modo>")
        print("")
        print("Modos disponibles:")
        print("   resolver   -> resolver automáticamente el Numberlink")
        print("   jugar      -> jugar manualmente conectando símbolos")
        return

    archivo = sys.argv[1]
    modo = sys.argv[2].lower().strip()

    # -----------------------------
    # Cargar tablero
    # -----------------------------
    try:
        board = Board.from_file(archivo)
    except Exception as e:
        print(f"Error cargando tablero: {e}")
        return

    print("Bienvenido a Numberlink :)\n")
    print("Tablero inicial:\n")
    board.print_grid()
    print("")

    # -----------------------------
    # Modo resolver automático
    # -----------------------------
    if modo == "resolver":
        print("Intentando resolver automáticamente...\n")

        stats = SolveStats()
        t0 = perf_counter()
        solved = solve_numberlink(board, require_full_cover=True, stats=stats)
        t1 = perf_counter()
        elapsed = t1 - t0

        if solved:
            print("¡Tablero resuelto!\n")
            board.print_grid()
        else:
            print("No se encontró solución automática :(")

        print("\nResumen de ejecución:")
        print(f"  Tiempo: {elapsed:.6f} segundos")
        print(f"  Llamadas a backtrack: {stats.backtrack_calls}")
        print(f"  Caminos candidatos examinados: {stats.painted_paths}")
        print(f"  Chequeos BFS de alcanzabilidad: {stats.bfs_checks}")
        return


    # -----------------------------
    # Modo jugar manualmente
    # -----------------------------
    elif modo == "jugar":
        print("Modo manual: escribe el símbolo que quieres conectar.")
        print("Escribe 'x' para salir.\n")

        while True:
            comando = input("Símbolo a conectar: ").strip()

            # Salir
            if comando.lower() == "x":
                # Al salir, revisar si el tablero quedó resuelto
                if is_board_solved(board, require_full_cover=True):
                    print("\n¡Felicidades! Has resuelto el Numberlink.")
                else:
                    print("\nSaliendo del modo de juego. El tablero no está resuelto todavía.")
                print("\nEstado final del tablero:")
                board.print_grid()
                break

            # Interpretar el comando como símbolo
            simbolo = comando

            # Verificar que el símbolo exista en el tablero
            if simbolo not in board.connectors:
                print("Ese símbolo no existe en el tablero o ya está conectado.\n")
                continue

            conectado = board.play_symbol_path_by_coords(simbolo)
            print("")
            if conectado:
                print(f"¡Símbolo '{simbolo}' conectado!\n")
            else:
                print(f"No se conectó el símbolo '{simbolo}'.\n")

            # Después de cada intento, verificar si ya ganó
            if is_board_solved(board, require_full_cover=True):
                print("¡Felicidades! Has resuelto el Numberlink.")
                print("\nEstado final del tablero:")
                board.print_grid()
                break

        return

    else:
        print(f"Modo desconocido: {modo}")
        print("Modos válidos: resolver, jugar")
        return


if __name__ == "__main__":
    main()
