import flet as ft
import random
import math
import threading
from algofourmis import AntColony

def main(page: ft.Page):
    page.title = "Algorithme de Colonie de Fourmis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    nodes = []  # Liste des positions (x, y)
    distances = []
    pheromones = []
    best_path = []
    iteration = 0
    running = False
    stop_event = threading.Event()

    # Champs de saisie
    nodes_field = ft.TextField(label="Nombre de nœuds", value="20", width=150)
    ants_field = ft.TextField(label="Nombre de fourmis", value="15", width=150)
    iterations_field = ft.TextField(label="Itérations", value="100", width=150)
    best_field = ft.TextField(label="Meilleures fourmis", value="3", width=150)
    decay_field = ft.TextField(label="Décay", value="0.95", width=150)
    alpha_field = ft.TextField(label="Alpha", value="1", width=150)
    beta_field = ft.TextField(label="Beta", value="2", width=150)

    status_text = ft.Text("Prêt", size=16, color="green")
    iteration_text = ft.Text("Itération: 0", size=16)
    pheromone_text = ft.Text("Phéromones moyennes: ", size=14)
    path_text = ft.Text("Meilleur chemin: ", size=14)

    graph_container = ft.Container(
        width=600,
        height=500,
        bgcolor="white",
        border=ft.border.all(2, "black")
    )
    def calculer_distances():
        dists = []
        for i in range(len(nodes)):
            row = []
            for j in range(len(nodes)):
                if i == j:
                    row.append(0)
                else:
                    dx = nodes[i][0] - nodes[j][0]
                    dy = nodes[i][1] - nodes[j][1]
                    row.append(math.sqrt(dx*dx + dy*dy))
            dists.append(row)
        return dists

    def create_line(x1, y1, x2, y2, color, thickness):
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)
        return ft.Container(
            width=length,
            height=thickness,
            bgcolor=color,
            left=x1,
            top=y1 - thickness/2,
            rotate=ft.Rotate(angle=angle, alignment=ft.alignment.Alignment(-1,0))
        )

    def dessiner_graphe():
        shapes = []

        if pheromones:
            max_pheromone = max(max(row) for row in pheromones)
            for i in range(len(nodes)):
                for j in range(i+1, len(nodes)):
                    if pheromones[i][j] > 0.1:
                        opacity = min(1, pheromones[i][j]/max_pheromone)
                        thickness = max(1, (pheromones[i][j]/max_pheromone)*3)
                        shapes.append(create_line(nodes[i][0], nodes[i][1],
                                                  nodes[j][0], nodes[j][1],
                                                  ft.Colors.with_opacity(opacity, ft.Colors.BLUE),
                                                  thickness))
        if best_path:
            for i in range(len(best_path)-1):
                start, end = best_path[i], best_path[i+1]
                if start < len(nodes) and end < len(nodes):
                    shapes.append(create_line(nodes[start][0], nodes[start][1],
                                              nodes[end][0], nodes[end][1],
                                              "red", 3))
        for idx, (x, y) in enumerate(nodes):
            shapes.append(ft.Container(
                width=20, height=20, bgcolor="green",
                border_radius=10, left=x-10, top=y-10,
                content=ft.Text(str(idx), size=10, color="white"),
                alignment=ft.alignment.Alignment(0,0)
            ))
        graph_container.content = ft.Stack(controls=shapes, width=600, height=500)
        page.update()

    def generer_nodes(e=None):
        nonlocal nodes, distances, pheromones
        try:
            num_nodes = int(nodes_field.value)
        except ValueError:
            num_nodes = 20
        nodes = [(random.uniform(50,550), random.uniform(50,450)) for _ in range(num_nodes)]
        distances = calculer_distances()
        pheromones = [[1.0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        dessiner_graphe()

    def update_callback(iter_num, current_best_path, current_pheromones):
        nonlocal iteration, best_path, pheromones
        iteration = iter_num
        best_path = current_best_path if current_best_path else []
        pheromones = current_pheromones

        async def update_ui():
            iteration_text.value = f"Itération: {iteration}"
            if current_best_path:
                path_text.value = f"Meilleur chemin: {best_path} (longueur: {current_best_path[1]:.2f})"
            avg = sum(sum(row) for row in pheromones)/(len(nodes)**2)
            pheromone_text.value = f"Phéromones moyennes: {avg:.4f}"
            dessiner_graphe()
        page.run_task(update_ui)

    def start_algorithm(e):
        nonlocal running
        if running or not distances:
            return
        running = True
        stop_event.clear()
        start_btn.disabled = True
        stop_btn.disabled = False
        status_text.value = "En cours d'exécution..."
        status_text.color = "orange"
        page.update()

        def run_ants():
            try:
                colony = AntColony(
                    distances,
                    int(ants_field.value),
                    int(best_field.value),
                    int(iterations_field.value),
                    float(decay_field.value),
                    float(alpha_field.value),
                    float(beta_field.value)
                )
            except ValueError:
                colony = AntColony(distances, 15, 3, 100, 0.95,1,2)
            colony.run(update_callback, stop_event)
            async def finalize():
                nonlocal running
                running = False
                start_btn.disabled = False
                stop_btn.disabled = True
                status_text.value = "Terminé"
                status_text.color = "green"
                page.update()
            page.run_task(finalize)
        threading.Thread(target=run_ants, daemon=True).start()

    start_btn = ft.Button("Démarrer", on_click=start_algorithm)
    stop_btn = ft.Button("Stop", disabled=True, on_click=lambda e: stop_event.set())
    btn_generer = ft.Button("Générer le Graphe", on_click=generer_nodes)

    page.add(ft.Column([
        ft.Text("Paramètres de l'algorithme", size=20),
        ft.Row([nodes_field, ants_field, iterations_field]),
        ft.Row([best_field, decay_field, alpha_field, beta_field]),
        ft.Row([btn_generer, start_btn, stop_btn]),
        ft.Divider(),
        status_text,
        iteration_text,
        pheromone_text,
        path_text,
        graph_container
    ]))

    generer_nodes()  # Graphe initial

if __name__ == "__main__":
    ft.app(target=main)
