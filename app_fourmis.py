import flet as ft
import random
import math

def main(page: ft.Page):
    page.title = "Algorithme de Colonie de Fourmis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    nodes = []  # Liste des positions (x, y)

    # Champs de saisie
    nodes_field = ft.TextField(label="Nombre de nœuds", value="20", width=150)
    ants_field = ft.TextField(label="Nombre de fourmis", value="15", width=150)
    iterations_field = ft.TextField(label="Itérations", value="100", width=150)

    # Zone graphique
    graph_container = ft.Container(
        width=600,
        height=500,
        bgcolor="white",
        border=ft.border.all(2, "black")
    )

    status_text = ft.Text("Prêt", size=16, color="green")

    def calculer_distances():
        """Calcule la matrice des distances"""
        distances = []
        for i in range(len(nodes)):
            row = []
            for j in range(len(nodes)):
                if i == j:
                    row.append(0.0)
                else:
                    dx = nodes[i][0] - nodes[j][0]
                    dy = nodes[i][1] - nodes[j][1]
                    row.append(math.sqrt(dx * dx + dy * dy))
            distances.append(row)
        return distances

    def dessiner_graphe():
        shapes = []
        for i, (x, y) in enumerate(nodes):
            cercle = ft.Container(
                width=20,
                height=20,
                bgcolor="green",
                border_radius=10,
                left=x - 10,
                top=y - 10,
                content=ft.Text(str(i), size=10, color="white"),
                alignment=ft.Alignment(0, 0)
            )
            shapes.append(cercle)

        graph_container.content = ft.Stack(
            controls=shapes,
            width=600,
            height=500
        )
        page.update()

    def generer_nodes():
        nonlocal nodes
        try:
            num_nodes = int(nodes_field.value)
        except ValueError:
            num_nodes = 20

        nodes = []
        for _ in range(num_nodes):
            x = random.uniform(50, 550)
            y = random.uniform(50, 450)
            nodes.append((x, y))

        distances = calculer_distances()
        print(f"{len(nodes)} nœuds générés")
        if len(nodes) > 1:
            print(f"Distance entre nœud 0 et 1 : {distances[0][1]:.2f}")

        dessiner_graphe()

    btn_generer = ft.ElevatedButton(
        "Générer le Graphe",
        on_click=lambda e: generer_nodes()
    )

    page.add(
        ft.Column([
            ft.Text("Paramètres de l'algorithme", size=20),
            ft.Row([nodes_field, ants_field, iterations_field]),
            btn_generer,
            ft.Divider(),
            status_text,
            graph_container
        ])
    )

    # Graphe initial
    generer_nodes()



if __name__ == "__main__":
    ft.app(target=main)
