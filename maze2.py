import streamlit as st
import numpy as np
from collections import deque
import time

# 🔵 BFS
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


# 🟣 DFS
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


# 🎨 INTERFAZ
st.set_page_config(page_title="Laberintos", layout="wide")

st.sidebar.header("OPCIONES DE LA APP")

archivo = st.sidebar.file_uploader("Carga el laberinto (.txt)", type=["txt"])

metodo = st.sidebar.selectbox(
    "Selecciona algoritmo",
    ["BFS", "DFS en proceso"]
)

st.title("🧩 Solucionador de Laberintos")

if archivo:
    content = archivo.read().decode("utf-8")
    lines = content.strip().split('\n')

    maze_data = []

    try:
        for line in lines:
            line = line.strip()

            # 🔥 DETECCIÓN AUTOMÁTICA DE FORMATO
            if " " in line:
                row = [int(x) for x in line.split()]
            else:
                row = [int(x) for x in line]

            maze_data.append(row)

        maze_np = np.array(maze_data)

        # 🔍 DEBUG (para verificar lectura)
        st.write("Valores detectados:", np.unique(maze_np))

        # 🔍 Buscar inicio (2) y fin (3)
        start_positions = np.argwhere(maze_np == 2)
        end_positions = np.argwhere(maze_np == 3)

        st.write("Inicio encontrados:", len(start_positions))
        st.write("Finales encontrados:", len(end_positions))

        if len(start_positions) != 1 or len(end_positions) != 1:
            st.error("❌ Debe haber exactamente UN '2' (inicio) y UN '3' (meta).")
        else:
            start = tuple(start_positions[0])
            end = tuple(end_positions[0])

            st.subheader("📌 Laberinto cargado")
            st.write(maze_np)

            if st.button("Resolver Laberinto"):

                if metodo == "BFS":
                    ruta, tiempo = solve_maze_bfs(maze_np, start, end)

                elif metodo == "DFS en proceso":
                    with st.spinner("🔄 Ejecutando DFS..."):
                        ruta, tiempo = solve_maze_dfs(maze_np, start, end)

                if ruta:
                    nombre_metodo = "DFS" if metodo == "DFS en proceso" else "BFS"

                    st.success(f"✅ {nombre_metodo} resuelto en {tiempo:.6f} segundos | Pasos: {len(ruta)}")

                    # 🧱 Visualización
                    for r in range(maze_np.shape[0]):
                        fila = ""
                        for c in range(maze_np.shape[1]):
                            if (r, c) == start:
                                fila += "🚀"
                            elif (r, c) == end:
                                fila += "🏁"
                            elif (r, c) in ruta:
                                fila += "🔵" if nombre_metodo == "BFS" else "🟣"
                            elif maze_np[r, c] == 1:
                                fila += "⬛"
                            else:
                                fila += "⬜"
                        st.text(fila)
                else:
                    st.warning("⚠️ No hay ruta posible. El laberinto está bloqueado.")

    except:
        st.error("⚠️ Error al leer el archivo. Verifica el formato.")

else:
    st.info("📂 Sube un archivo .txt para comenzar")
