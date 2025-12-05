import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()  # напрямлений граф, бо нас цікавить напрямок руху

# Вузли: умовні транспортні точки
nodes = [
    "Берчені",
    "Кільце_Берчені",          # умовне кільце/перехрестя біля Берчені
    "Шлях_до_Шпеника",
    "Міст_Шпеника",
    "Шлях_до_Масарика",
    "Міст_Масарика",
    "Правий_берег_центр",      # правий берег ближче до центру
    "Площа_Петефі",            # ціль
]

G.add_nodes_from(nodes)

# Ребра: можливі напрямки руху (дуже спрощена схема)
edges = [
    # Від Берчені до розвилки
    ("Берчені", "Кільце_Берчені"),

    # Шлях 1: через міст на вул. Шпеника
    ("Кільце_Берчені", "Шлях_до_Шпеника"),
    ("Шлях_до_Шпеника", "Міст_Шпеника"),
    ("Міст_Шпеника", "Правий_берег_центр"),
    ("Правий_берег_центр", "Площа_Петефі"),

    # Шлях 2: через міст на вул. Масарика
    ("Кільце_Берчені", "Шлях_до_Масарика"),
    ("Шлях_до_Масарика", "Міст_Масарика"),
    ("Міст_Масарика", "Правий_берег_центр"),
]

G.add_edges_from(edges)

# Аналіз
print("Кількість вузлів:", G.number_of_nodes())
print("Кількість доріг (ребер):", G.number_of_edges())

degrees = dict(G.degree()) # type: ignore
print("\nСтупені вузлів:")
for node, d in degrees.items():
    print(f"  {node}: {d}")

# Шляхи від Берчені до Петефі
print("\nУсі прості шляхи від Берчені до Площа_Петефі:")
for path in nx.all_simple_paths(G, source="Берчені", target="Площа_Петефі"):
    print("  -> ".join(path))

# Візуалізація
plt.figure(figsize=(12, 7))
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

nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=4500)
nx.draw_networkx_edges(G, pos, edge_color="gray", width=2, arrows=True, arrowstyle="-|>")
nx.draw_networkx_labels(G, pos, font_size=6, font_weight="bold")

# виділяємо мости
nx.draw_networkx_nodes(
    G, pos,
    nodelist=["Міст_Шпеника", "Міст_Масарика"],
    node_color="red",
    node_size=4500,
)

plt.title("Маршрути з вул. Берчені до пл. Петефі через мости Шпеника та Масарика")
plt.axis("off")
plt.tight_layout()
plt.savefig("uzhhorod_route_bercheni_petefi.png", dpi=300, bbox_inches="tight")
plt.show()
