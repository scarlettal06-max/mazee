import streamlit as st
import numpy as np
from collections import deque
import time

# =========================
# 🔵 BFS
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
# 🟣 DFS
# =========================
def solve_maze_dfs(maze, start, end):
    start_time = time.time()
    stack = [(start, [start])]
    visited = {start}

    while stack:
        (r, c), path = stack.pop()

        if (r, c) == end:
            return path, (time.time() - start_time)

        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append(((nr, nc), path + [(nr, nc)]))

    return None, 0


# =========================
# 🎨 CONFIG UI
# =========================
st.set_page_config(page_title="Laberintos", layout="wide")

st.sidebar.header("🛠 OPCIONES")

archivo = st.sidebar.file_uploader("Cargar archivo (.txt)", type=["txt"])

metodo = st.sidebar.selectbox(
    "Selecciona algoritmo",
    ["BFS", "DFS"]
)

st.title("🧩 Solucionador de Laberintos")

# =========================
# 📂 PROCESAMIENTO
# =========================
if archivo:
    content = archivo.read().decode("utf-8")
    lines = content.strip().split('\n')

    maze_data = []

    try:
        for line in lines:
            line = line.strip()

            # 🔥 Detecta formato automático
            if " " in line:
                row = [int(x) for x in line.split()]
            else:
                row = [int(x) for x in line]

            maze_data.append(row)

        maze_np = np.array(maze_data)

        # 🔍 Buscar inicio y fin
        start_positions = np.argwhere(maze_np == 2)
        end_positions = np.argwhere(maze_np == 3)

        if len(start_positions) != 1 or len(end_positions) != 1:
            st.error("❌ Debe haber exactamente UN '2' (inicio) y UN '3' (meta).")
        else:
            start = tuple(start_positions[0])
            end = tuple(end_positions[0])

            if st.button("🚀 Resolver Laberinto"):

                # =========================
                # 🚀 EJECUCIÓN
                # =========================
                with st.spinner(f"Resolviendo con {metodo}..."):
                    if metodo == "BFS":
                        ruta, tiempo = solve_maze_bfs(maze_np, start, end)
                    else:
                        ruta, tiempo = solve_maze_dfs(maze_np, start, end)

                # =========================
                # 📊 RESULTADO
                # =========================
                if ruta:
                    st.success(f"✅ {metodo} completado en {tiempo:.6f}s | Pasos: {len(ruta)}")

                    # =========================
                    # 🎮 VISUALIZACIÓN LIMPIA
                    # =========================
                    laberinto = ""

                    for r in range(maze_np.shape[0]):
                        for c in range(maze_np.shape[1]):
                            if (r, c) == start:
                                laberinto += "🚀 "
                            elif (r, c) == end:
                                laberinto += "🏁 "
                            elif (r, c) in ruta:
                                laberinto += "🔵 " if metodo == "BFS" else "🟣 "
                            elif maze_np[r, c] == 1:
                                laberinto += "⬛ "
                            else:
                                laberinto += "⬜ "
                        laberinto += "\n"

                    # 🔥 render perfecto alineado
                    st.markdown(f"```\n{laberinto}\n```")

                else:
                    st.warning("⚠️ No hay ruta posible. El laberinto está bloqueado.")

    except:
        st.error("⚠️ Error al leer el archivo. Verifica que solo tenga números.")
else:
    st.info("📂 Sube un archivo .txt para comenzar")
