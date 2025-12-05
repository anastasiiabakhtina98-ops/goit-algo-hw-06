import networkx as nx
from collections import deque

# === ГРАФ З ЗАВДАННЯ 1 ===
G = nx.DiGraph()

nodes = [
    "Берчені",
    "Кільце_Берчені",
    "Шлях_до_Шпеника",
    "Міст_Шпеника",
    "Шлях_до_Масарика",
    "Міст_Масарика",
    "Правий_берег_центр",
    "Площа_Петефі",
]
G.add_nodes_from(nodes)

edges = [
    ("Берчені", "Кільце_Берчені"),

    ("Кільце_Берчені", "Шлях_до_Шпеника"),
    ("Шлях_до_Шпеника", "Міст_Шпеника"),
    ("Міст_Шпеника", "Правий_берег_центр"),
    ("Правий_берег_центр", "Площа_Петефі"),

    ("Кільце_Берчені", "Шлях_до_Масарика"),
    ("Шлях_до_Масарика", "Міст_Масарика"),
    ("Міст_Масарика", "Правий_берег_центр"),
]
G.add_edges_from(edges)

start = "Берчені"
target = "Площа_Петефі"

# === DFS: пошук шляху ===
def dfs_path(graph, start, target):
    stack = [(start, [start])]
    visited = set()

    while stack:
        vertex, path = stack.pop()          # беремо останній елемент (глибина)
        if vertex == target:
            return path
        if vertex in visited:
            continue
        visited.add(vertex)
        for neigh in graph.neighbors(vertex):
            if neigh not in visited:
                stack.append((neigh, path + [neigh]))

    return None

#BFS: пошук найкоротшого шляху 
def bfs_path(graph, start, target):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        vertex, path = queue.popleft()      # беремо перший елемент (ширина)
        if vertex == target:
            return path
        if vertex in visited:
            continue
        visited.add(vertex)
        for neigh in graph.neighbors(vertex):
            if neigh not in visited:
                queue.append((neigh, path + [neigh]))

    return None

dfs_result = dfs_path(G, start, target)
bfs_result = bfs_path(G, start, target)

if dfs_result is None:
    print("DFS шлях не знайдено")
else:
    print("DFS шлях  :", " -> ".join(dfs_result))
    print("Довжина DFS:", len(dfs_result) - 1, "ребер")

if bfs_result is None:
    print("BFS шлях не знайдено")
else:
    print("BFS шлях  :", " -> ".join(bfs_result))
    print("Довжина BFS:", len(bfs_result) - 1, "ребер")


