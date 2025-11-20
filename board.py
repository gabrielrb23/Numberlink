from dataclasses import dataclass
from typing import List, Dict, Tuple, Set
from collections import deque

Position = Tuple[int, int]


@dataclass
class Board:
    grid: List[List[str]]
    rows: int
    cols: int
    connectors: Dict[str, List[Position]]

    # Carga y visualización
    @classmethod
    def from_file(cls, path: str) -> "Board":
        """
        Formato del archivo:
        - Primera línea: 'filas columnas'
        - Luego 'filas' líneas con caracteres (letra/dígito o espacio).
        """
        with open(path, "r", encoding="utf-8") as f:
            header = f.readline()
            if not header:
                raise ValueError("Archivo vacío")
            parts = header.split()
            if len(parts) != 2:
                raise ValueError("Primera línea debe tener: filas columnas")
            rows, cols = map(int, parts)

            grid: List[List[str]] = [[" "] * cols for _ in range(rows)]
            connectors: Dict[str, List[Position]] = {}

            for i in range(rows):
                line = f.readline()
                if not line:
                    line = ""
                line = line.rstrip("\n")

                # Ajustar longitud de la línea al número de columnas
                if len(line) < cols:
                    line = line + " " * (cols - len(line))
                elif len(line) > cols:
                    line = line[:cols]

                for j, ch in enumerate(line):
                    grid[i][j] = ch
                    if ch != " ":
                        connectors.setdefault(ch, []).append((i, j))

        # Validar que cada conector aparece exactamente 2 veces
        for ch, pos_list in connectors.items():
            if len(pos_list) != 2:
                raise ValueError(
                    f"El conector '{ch}' aparece {len(pos_list)} veces (debe aparecer 2)."
                )

        return cls(grid=grid, rows=rows, cols=cols, connectors=connectors)

    def print_grid(self) -> None:
        
        # índices de columnas
        col_indices = "    " + "".join(f"  {j} " for j in range(self.cols))
        print(col_indices)

        horizontal = "   +" + "---+" * self.cols

        for i, row in enumerate(self.grid):
            print(horizontal)
            cells = ""
            for c in row:
                cells += ("   |" if c == " " else f" {c} |")
            print(f"{i:2d} |{cells}")
        print(horizontal)

    # Juego manual
    def play_symbol_path_by_coords(self, symbol: str) -> bool:
        """
        Permite al usuario conectar un símbolo escribiendo coordenadas
        'fila,columna' paso a paso.
        Devuelve True si se conectó correctamente el par, False en caso contrario.
        """
        if symbol not in self.connectors:
            print(f"El símbolo '{symbol}' ya está conectado o no existe.")
            return False

        pos1, pos2 = self.connectors[symbol]
        current = pos1
        target = pos2

        # Mantener rastro para poder deshacer si el usuario cancela
        painted: List[Position] = []

        paso = 1
        print(f"\nVas a conectar el símbolo '{symbol}'.")
        print(f"Punto de inicio: {pos1}, punto objetivo: {target}.")
        print("En cada paso escribe una coordenada 'fila,columna'. Ej: 2,3")
        print("Las celdas deben ser vecinas (arriba/abajo/izquierda/derecha).")
        print("Escribe 'x' para cancelar este símbolo.\n")

        while True:
            self.print_grid()
            print(f"Posición actual: {current}, objetivo: {target}")
            entrada = input(
                f"Paso {paso} - fila,columna (o 'x' para cancelar): "
            ).strip().lower()

            if entrada == "x":
                print("Camino cancelado. Deshaciendo lo dibujado...")
                for r, c in painted:
                    self.grid[r][c] = " "
                return False

            try:
                fila_str, col_str = entrada.split(",")
                nr = int(fila_str.strip())
                nc = int(col_str.strip())
            except Exception:
                print("Formato inválido. Usa algo como: 2,3")
                continue

            if not (0 <= nr < self.rows and 0 <= nc < self.cols):
                print("Coordenadas fuera del tablero.")
                continue

            r, c = current
            # Debe ser vecino en 4-direcciones
            if abs(nr - r) + abs(nc - c) != 1:
                print("La celda debe ser vecina (arriba/abajo/izquierda/derecha).")
                continue

            cell = self.grid[nr][nc]

            # llegamos al objetivo?
            if (nr, nc) == target:
                print("Has llegado al otro extremo del símbolo.")
                # registrar conexión definitiva
                self.connectors.pop(symbol, None)
                return True

            # celda vacía? -> pintar
            if cell == " ":
                self.grid[nr][nc] = symbol
                current = (nr, nc)
                painted.append(current)
                paso += 1
                continue

            # celda ocupada?
            print(
                f"No puedes pasar por ({nr}, {nc}), está ocupado por '{cell}'."
            )


#  SOLVER AUTOMÁTICO
# Conseguir todas las posiciones vecinas de una celda
def _neighbors(board: "Board", pos: Position):
    r, c = pos
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < board.rows and 0 <= nc < board.cols:
            yield (nr, nc)

# Distancia Manhattan
def _manhattan(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# BFS rápido para comprobar si aún hay algún camino para un par
def _reachable(board: "Board", start: Position, goal: Position, symbol: str) -> bool:
    q = deque([start])
    visited: Set[Position] = {start}

    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            return True

        for nr, nc in _neighbors(board, (r, c)):
            if (nr, nc) in visited:
                continue

            ch = board.grid[nr][nc]

            # Podemos pasar por espacios vacíos o por el propio símbolo (start/goal)
            if (nr, nc) != goal and ch != " ":
                continue

            visited.add((nr, nc))
            q.append((nr, nc))

    return False

# Comprobar si con los caminos ya dibujados, todos los pares siguen teniendo al menos un camino posible
def _all_remaining_pairs_reachable(board: "Board", symbols: List[str], idx: int) -> bool:
    """
    Comprueba que, con los caminos ya dibujados, todos los pares desde idx
    hacia adelante siguen teniendo al menos un camino posible.
    """
    for k in range(idx, len(symbols)):
        s = symbols[k]
        pos1, pos2 = board.connectors[s]
        if not _reachable(board, pos1, pos2, s):
            return False
    return True


# DFS con heurística tipo Dijkstra/A* para generar caminos
def _generate_paths_for_pair(
    board: "Board",
    symbol: str,
    start: Position,
    goal: Position,
    max_paths: int = 10000,
) -> List[List[Position]]:
    """
    Genera hasta max_paths caminos simples desde start hasta goal.
    Usa una heurística de distancia Manhattan al objetivo.
    """
    paths: List[List[Position]] = []

    def dfs(current: Position, path: List[Position], visited: Set[Position]):
        if len(paths) >= max_paths:
            return

        if current == goal:
            paths.append(list(path))
            return

        neighs = list(_neighbors(board, current))
        # Ordenamos por distancia al objetivo (heurística tipo A*)
        neighs.sort(key=lambda p: _manhattan(p, goal))

        for nxt in neighs:
            if nxt in visited:
                continue

            r, c = nxt
            ch = board.grid[r][c]

            # Podemos ir a:
            #  - el goal (tiene el mismo símbolo)
            #  - celdas vacías
            if nxt != goal:
                if ch != " ":
                    continue

            visited.add(nxt)
            path.append(nxt)
            dfs(nxt, path, visited)
            path.pop()
            visited.remove(nxt)

    dfs(start, [start], {start})
    return paths


# Backtracking global sobre los símbolos
def solve_numberlink(board: "Board", require_full_cover: bool = True) -> bool:
    """
    Resuelve el Numberlink del tablero dado:
    - Conecta cada par de símbolos con un camino simple (sin cruces).
    - Si require_full_cover=True, exige que no queden espacios vacíos.

    Devuelve True si encuentra solución (el tablero queda modificado con la solución).
    """
    # Ordenar símbolos por distancia Manhattan entre sus extremos (heurística)
    symbols = sorted(
        board.connectors.keys(),
        key=lambda s: _manhattan(*board.connectors[s]),
    )

    def backtrack(idx: int) -> bool:
        # Ya conectamos todos los pares?
        if idx == len(symbols):
            if not require_full_cover:
                return True
            # Verificar que no queden espacios vacíos
            for r in range(board.rows):
                for c in range(board.cols):
                    if board.grid[r][c] == " ":
                        return False
            return True

        symbol = symbols[idx]
        start, goal = board.connectors[symbol]

        # Generar caminos candidatos para este par
        candidate_paths = _generate_paths_for_pair(board, symbol, start, goal)

        for path in candidate_paths:
            painted: List[Position] = []
            ok = True

            # Pintar el camino (excepto extremos)
            for (r, c) in path:
                if (r, c) == start or (r, c) == goal:
                    continue

                if board.grid[r][c] != " ":
                    ok = False
                    break

                board.grid[r][c] = symbol
                painted.append((r, c))

            if not ok:
                # Deshacer y seguir con otro camino
                for (r, c) in painted:
                    board.grid[r][c] = " "
                continue

            # Chequeo rápido: ¿los pares restantes siguen siendo alcanzables?
            if _all_remaining_pairs_reachable(board, symbols, idx + 1):
                if backtrack(idx + 1):
                    return True

            # Si llegamos aquí es que este camino no llevó a solución -> deshacer
            for (r, c) in painted:
                board.grid[r][c] = " "

        # Ningún camino para este símbolo dio solución -> backtracking
        return False

    return backtrack(0)
