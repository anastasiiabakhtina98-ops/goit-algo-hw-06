import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Створюємо зважений спрямований граф
G = nx.DiGraph()

# Вузли: умовні транспортні точки
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

# Ребра з вагами (відстань у км)
weighted_edges = [
    # Від Берчені до розвилки (2 км)
    ("Берчені", "Кільце_Берчені", 2.0),
    
    # Шлях 1: через міст на вул. Шпеника (швидший, але довший підйом)
    ("Кільце_Берчені", "Шлях_до_Шпеника", 1.5),
    ("Шлях_до_Шпеника", "Міст_Шпеника", 1.2),
    ("Міст_Шпеника", "Правий_берег_центр", 0.8),
    ("Правий_берег_центр", "Площа_Петефі", 1.0),
    
    # Шлях 2: через міст на вул. Масарика (довший, але рівний)
    ("Кільце_Берчені", "Шлях_до_Масарика", 2.0),
    ("Шлях_до_Масарика", "Міст_Масарика", 1.8),
    ("Міст_Масарика", "Правий_берег_центр", 1.2),
]

# Додаємо ребра з вагами
for u, v, weight in weighted_edges:
    G.add_edge(u, v, weight=weight)

print(f"Кількість вузлів: {G.number_of_nodes()}")
print(f"Кількість ребер: {G.number_of_edges()}")

# Алгоритм Дейкстри
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0
    
    predecessors = {node: None for node in graph.nodes()}
    pq = [(0, start)]
    
    while pq:
        current_distance, current_vertex = heapq.heappop(pq)
        
        if current_distance > distances[current_vertex]:
            continue
            
        for neighbor, data in graph[current_vertex].items():
            weight = data['weight']
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex  
                heapq.heappush(pq, (distance, neighbor))
    
    return distances, predecessors

def get_path(predecessors, end):
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    return path[::-1]  # Реверсуємо шлях

# Знаходимо найкоротші шляхи від кожної вершини до всіх інших
all_shortest_paths = {}
print("\n" + "="*80)
print("НАЙКОРОТШІ ШЛЯХИ МІЖ УСІМА ВЕРШИНАМИ (алгоритм Дейкстри)")
print("="*80)

for start_node in nodes:
    distances, predecessors = dijkstra(G, start_node)
    all_shortest_paths[start_node] = (distances, predecessors)
    
    print(f"\nВід {start_node}:")
    print("-" * 50)
    for node in nodes:
        if distances[node] != float('inf'):
            path = get_path(predecessors, node)
            print(f"  -> {node}: {distances[node]:.1f} км (шлях: {' -> '.join(path)})")
        else:
            print(f"  -> {node}: недоступно")

# від Берчені до Площа_Петефі
print("\n" + "="*80)
print("НАЙКОРОТШИЙ ШЛЯХ ВІД БЕРЧЕНІ ДО ПЛОЩІ ПЕТЕФІ")
print("="*80)
distances_bercheni, predecessors_bercheni = all_shortest_paths["Берчені"]
path_to_petofi = get_path(predecessors_bercheni, "Площа_Петефі")
total_distance = distances_bercheni["Площа_Петефі"]

print(f"Шлях: {' -> '.join(path_to_petofi)}")
print(f"Загальна відстань: {total_distance:.1f} км")
print(f"Деталі маршруту:")
for i in range(len(path_to_petofi)-1):
    u, v = path_to_petofi[i], path_to_petofi[i+1]
    weight = G[u][v]['weight']
    print(f"  {u} -> {v}: {weight:.1f} км")

# Візуалізація
plt.figure(figsize=(14, 8))
pos = {
    "Берчені": (-3, 0),
    "Кільце_Берчені": (-1.5, 0),
    "Шлях_до_Шпеника": (0, 1),
    "Міст_Шпеника": (1.5, 1),
    "Шлях_до_Масарика": (0, -1),
    "Міст_Масарика": (1.5, -1),
    "Правий_берег_центр": (3, 0),
    "Площа_Петефі": (4.5, 0),
}

# Малюємо граф з вагами
nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=4500)
nx.draw_networkx_edges(G, pos, edge_color="gray", width=2, arrows=True, arrowstyle="-|>", 
                      connectionstyle="arc3,rad=0")

# Додаємо ваги на ребра
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.1f}" for k,v in edge_labels.items()})

nx.draw_networkx_labels(G, pos, font_size=7, font_weight="bold")

# Виділяємо найкоротший шлях червоним
path_edges = list(nx.utils.pairwise(path_to_petofi))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=3, 
                      arrows=True, arrowstyle="-|>", connectionstyle="arc3,rad=0")

plt.title("Найкоротший шлях від Берчені до Площі Петефі (червоним)\n"
          f"Загальна відстань: {total_distance:.1f} км", fontsize=12)
plt.axis("off")
plt.tight_layout()
plt.savefig("deykstra_uzhhorod_route.png", dpi=300, bbox_inches="tight")
plt.show()


