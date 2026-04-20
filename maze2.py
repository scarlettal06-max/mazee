import streamlit as st
import numpy as np
from collections import deque
import time
import heapq

# =========================
# 🔵 BFS (SIN CAMBIOS)
# =========================
def solve_maze_bfs(maze, start, end):
    start_time = time.time()
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == end:
            return path, (time.time() - start_time)

        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))

    return None, 0


# =========================
# 🟣 DFS (SOLO ORDEN CAMBIADO)
# =========================
def solve_maze_dfs(maze, start, end):
    start_time = time.time()
    stack = [(start, [start])]

    while stack:
        (r, c), path = stack.pop()

        if (r, c) == end:
            return path, (time.time() - start_time)

        # 🔥 CAMBIO AQUÍ
        for dr, dc in [(1,0),(0,-1),(0,1),(-1,0)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in path:
                    stack.append(((nr, nc), path + [(nr, nc)]))

    return None, 0


# =========================
# 🟢 A* (CONFIGURADO)
# =========================
def heuristic(a, b):
    # Distancia Manhattan: |x1 - x2| + |y1 - y2|
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_maze_astar(maze, start, end):
    start_time = time.time()

    # open_set guarda: (f_cost, counter, current_node, path, g_cost)
    open_set = []
    # g_cost es la distancia real recorrida desde el inicio
    heapq.heappush(open_set, (0, 0, start, [start], 0))

    visited = {} # Guardamos el g_cost mínimo para cada nodo
    
    # 🔥 PESO DINÁMICO: 
    # Un peso de 1.0 es A* estándar (óptimo).
    # Un peso > 1.0 (ej. 2.0 o 5.0) hace que sea "ambicioso" y tome rutas distintas.
    WEIGHT = 2.5 

    counter = 0

    while open_set:
        f, _, current, path, g = heapq.heappop(open_set)

        if current == end:
            return path, (time.time() - start_time)

        if current in visited and visited[current] <= g:
            continue
        
        visited[current] = g
        r, c = current

        for dr, dc in [(-1,0),(0,-1),(1,0),(0,1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1:
                    new_g = g + 1
                    h = heuristic(neighbor, end)
                    
                    # f(n) = g(n) + w * h(n)
                    f_cost = new_g + (WEIGHT * h)

                    counter += 1
                    heapq.heappush(
                        open_set,
                        (f_cost, counter, neighbor, path + [neighbor], new_g)
                    )

    return None, 0
# =========================
# 🎨 CONFIG UI (IGUAL)
# =========================
st.set_page_config(page_title="Laberintos", layout="wide")

st.sidebar.header("🛠 OPCIONES")
archivo = st.sidebar.file_uploader("Cargar archivo (.txt)", type=["txt"])

metodo = st.sidebar.selectbox(
    "Selecciona algoritmo",
    ["BFS", "DFS", "A*"]
)

st.title("🧩 Solucionador de Laberintos")

# =========================
# 📂 PROCESAMIENTO (IGUAL)
# =========================
if archivo:
    content = archivo.read().decode("utf-8")
    lines = content.strip().split('\n')

    maze_data = []

    try:
        for line in lines:
            line = line.strip()

            if " " in line:
                row = [int(x) for x in line.split()]
            else:
                row = [int(x) for x in line]

            maze_data.append(row)

        maze_np = np.array(maze_data)

        start_positions = np.argwhere(maze_np == 2)
        end_positions = np.argwhere(maze_np == 3)

        if len(start_positions) != 1 or len(end_positions) != 1:
            st.error("❌ Debe haber exactamente UN '2' y UN '3'")
        else:
            start = tuple(start_positions[0])
            end = tuple(end_positions[0])

            if st.button("🚀 Resolver Laberinto"):

                with st.spinner(f"Resolviendo con {metodo}..."):
                    if metodo == "BFS":
                        ruta, tiempo = solve_maze_bfs(maze_np, start, end)
                    elif metodo == "DFS":
                        ruta, tiempo = solve_maze_dfs(maze_np, start, end)
                    else:
                        ruta, tiempo = solve_maze_astar(maze_np, start, end)

                if ruta:
                    st.success(f"✅ {metodo} | Tiempo: {tiempo:.6f}s | Pasos: {len(ruta)}")

                    laberinto = ""

                    for r in range(maze_np.shape[0]):
                        for c in range(maze_np.shape[1]):
                            if (r, c) == start:
                                laberinto += "🚀 "
                            elif (r, c) == end:
                                laberinto += "🏁 "
                            elif (r, c) in ruta:
                                if metodo == "BFS":
                                    laberinto += "🔵 "
                                elif metodo == "DFS":
                                    laberinto += "🟣 "
                                else:
                                    laberinto += "🟢 "
                            elif maze_np[r, c] == 1:
                                laberinto += "⬛ "
                            else:
                                laberinto += "⬜ "
                        laberinto += "\n"

                    st.text(laberinto)

                else:
                    st.warning("⚠️ No hay ruta posible.")

    except:
        st.error("⚠️ Error al leer el archivo.")
else:
    st.info("📂 Sube un archivo .txt")
