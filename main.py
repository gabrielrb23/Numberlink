import sys
from board import Board, solve_numberlink


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
        if solve_numberlink(board, require_full_cover=True):
            print("¡Tablero resuelto!\n")
            board.print_grid()
        else:
            print("No se encontró solución automática :(")
        return

    # -----------------------------
    # Modo jugar manualmente
    # -----------------------------
    elif modo == "jugar":
        print("Modo manual: escribe el símbolo que quieres conectar.")
        print("Escribe 'x' para salir.\n")

        while True:
            simbolo = input("Símbolo a conectar: ").strip()
            if simbolo.lower() == "x":
                print("Saliendo del modo de juego.")
                break

            if simbolo not in board.connectors:
                print("Ese símbolo no existe o ya está conectado.\n")
                continue

            conectado = board.play_symbol_path_by_coords(simbolo)
            print("")
            if conectado:
                print(f"¡Símbolo '{simbolo}' conectado!\n")
            else:
                print(f"No se conectó el símbolo '{simbolo}'.\n")

        print("Estado final del tablero:")
        board.print_grid()
        return

    else:
        print(f"Modo desconocido: {modo}")
        print("Modos válidos: resolver, jugar")
        return


if __name__ == "__main__":
    main()
