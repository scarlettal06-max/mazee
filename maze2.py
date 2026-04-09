import streamlit as st
import numpy as np
import collections
import re
import time

def solve_maze_bfs(maze, start, end):
    start_time = time.time()
    rows, cols = len(maze), len(maze[0])
    queue = collections.deque([(start, [start])])
    visited = set([start])

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == end:
            return path, time.time() - start_time

        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc

            if (0 <= nr < rows and 0 <= nc < cols and 
                maze[nr][nc] != 1 and 
                (nr, nc) not in visited):

                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

    return None, 0


# 🔥 SIDEBAR (como en tu imagen)
st.sidebar.title("OPCIONES DE LA APP")
st.sidebar.write("Carga el laberinto")
st.sidebar.caption("1=pared, 0=camino, 2=inicio, 3=final")

archivo = st.sidebar.file_uploader("Sube tu archivo .txt", type=["txt"])

algoritmo = st.sidebar.selectbox("Selecciona algoritmo", ["BFS"])

resolver = st.sidebar.button("Resolver Laberinto Cargado")


# 🔥 TÍTULO PRINCIPAL
st.title("Visualizador de Algoritmo de Búsqueda en Laberinto")


if archivo:
    content = archivo.read().decode("utf-8")
    lines = content.strip().split('\n')

    maze_data = []
    for line in lines:
        row = [int(d) for d in re.findall(r'\d', line)]
        if row:
            maze_data.append(row)

    maze = np.array(maze_data)

    # Buscar inicio y fin
    p2 = np.where(maze == 2)
    p3 = np.where(maze == 3)

    if p2[0].size > 0 and p3[0].size > 0:
        start = (p2[0][0], p2[1][0])
        end = (p3[0][0], p3[1][0])

        if resolver:
            path, tiempo = solve_maze_bfs(maze, start, end)

            if path:
                st.success(f"BFS resuelto en {tiempo:.6f} s | Pasos: {len(path)}")

                # 🔥 VISUAL TIPO CUADRITOS (como tu imagen)
                for r in range(maze.shape[0]):
                    fila = ""
                    for c in range(maze.shape[1]):
                        if (r, c) == start:
                            fila += "🚀"
                        elif (r, c) == end:
                            fila += "🏁"
                        elif (r, c) in path:
                            fila += "🔷"
                        elif maze[r, c] == 1:
                            fila += "⬛"
                        else:
                            fila += "⬜"
                    st.text(fila)
            else:
                st.error("No se encontró solución")
    else:
        st.warning("Debe existir un 2 (inicio) y un 3 (final)")
else:
    st.info("Carga un archivo para comenzar")
