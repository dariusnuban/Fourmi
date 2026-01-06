# TP - Créer une Application de Visualisation d'Algorithme de Colonie de Fourmis

## Objectif du TP

À la fin de cette séance, vous aurez créé votre propre application interactive qui visualise l'algorithme de colonie de fourmis pour résoudre le problème du voyageur de commerce (TSP - Traveling Salesman Problem).

## Prérequis

- Python 3.7 ou supérieur installé
- Un éditeur de code (VS Code, PyCharm, ou autre)
- Connaissances de base en Python (boucles, fonctions, listes)

## Installation

Ouvrez un terminal et installez Flet :

```bash
pip install flet
```

---

## Partie 1 : Comprendre le Problème

### Le Problème du Voyageur de Commerce

Imaginez un livreur qui doit visiter plusieurs villes et revenir à son point de départ. Comment trouver le chemin le plus court qui passe par toutes les villes une seule fois ?

### L'Algorithme de Colonie de Fourmis

Les fourmis réelles trouvent le chemin le plus court vers la nourriture en déposant des phéromones. Plus un chemin est emprunté, plus il contient de phéromones, ce qui attire d'autres fourmis. Les chemins courts sont parcourus plus rapidement, accumulant plus de phéromones.

**Principe de l'algorithme :**
1. Plusieurs "fourmis virtuelles" explorent des chemins aléatoires
2. Chaque fourmi dépose des phéromones sur son chemin
3. Les phéromones s'évaporent avec le temps (decay)
4. Les fourmis sont attirées par les chemins avec plus de phéromones
5. Progressivement, le meilleur chemin émerge

---

## Partie 2 : Créer l'Interface de Base

### Étape 1 : Structure de base avec Flet

**Objectif :** Créer une fenêtre avec un titre et un bouton de test.

**Ce que vous devez faire :**
1. Créez un fichier `app_fourmis.py`
2. Importez Flet : `import flet as ft`
3. Créez une fonction `main(page: ft.Page)` qui prend une page en paramètre
4. Configurez le titre de la page, le thème clair et un padding de 20
5. Ajoutez un titre "Visualisation de l'Algorithme" et un bouton "Cliquez-moi"
6. Utilisez `page.add()` avec un `ft.Column()` pour organiser les éléments
7. À la fin du fichier, lancez l'application avec `ft.app(target=main)`

<details>
<summary>💡 Besoin d'aide ?</summary>

**Indices :**
- Pour configurer la page : `page.title = "..."`, `page.theme_mode = ft.ThemeMode.LIGHT`, `page.padding = 20`
- Pour créer un texte : `ft.Text("votre texte", size=24, weight="bold")`
- Pour créer un bouton : `ft.ElevatedButton("texte", on_click=lambda e: print("test"))`
- Pour organiser verticalement : `ft.Column([element1, element2])`

</details>

<details>
<summary>🔴 Solution complète</summary>

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Algorithme de Colonie de Fourmis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Ajoutons un titre et un bouton
    titre = ft.Text("Visualisation de l'Algorithme", size=24)
    bouton_test = ft.Button("Cliquez-moi", on_click=lambda e: print("Bouton cliqué!"))
    
    page.add(
        ft.Column([
            titre,
            bouton_test
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)
```

</details>

**Testez votre application :**
```bash
python app_fourmis.py
```

Vous devriez voir une fenêtre avec votre titre et votre bouton !

---

### Étape 2 : Ajouter des champs de paramètres

**Objectif :** Créer des champs pour configurer l'algorithme et une zone pour afficher le graphe.

**Ce que vous devez faire :**
1. Créez trois champs de saisie (`ft.TextField`) pour :
   - Nombre de nœuds (valeur par défaut : "20")
   - Nombre de fourmis (valeur par défaut : "15")
   - Nombre d'itérations (valeur par défaut : "100")
   - Chaque champ doit avoir une largeur de 150
2. Créez une zone graphique (`ft.Container`) :
   - Largeur : 600, hauteur : 500
   - Fond bleu clair (`bgcolor="lightblue"`)
   - Bordure bleue de 2px
3. Ajoutez un texte de statut "Prêt à démarrer" en vert
4. Organisez tout avec un `ft.Column` contenant :
   - Un titre "Paramètres de l'algorithme"
   - Une ligne (`ft.Row`) avec les trois champs
   - Un séparateur (`ft.Divider()`)
   - Le texte de statut
   - La zone graphique

<details>
<summary>💡 Besoin d'aide ?</summary>

**Indices :**
- TextField : `ft.TextField(label="...", value="...", width=150)`
- Container : `ft.Container(width=600, height=500, bgcolor="lightblue", border=ft.border.all(2, "blue"))`
- Text coloré : `ft.Text("...", size=16, color="green")`
- Row pour aligner horizontalement : `ft.Row([champ1, champ2, champ3])`

</details>

<details>
<summary>🔴 Solution complète</summary>

```python
def main(page: ft.Page):
    page.title = "Algorithme de Colonie de Fourmis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Champs de saisie pour les paramètres
    nodes_field = ft.TextField(label="Nombre de nœuds", value="20", width=150)
    ants_field = ft.TextField(label="Nombre de fourmis", value="15", width=150)
    iterations_field = ft.TextField(label="Itérations", value="100", width=150)
    
    # Zone pour afficher le graphe
    graph_container = ft.Container(
        width=600,
        height=500,
        bgcolor="lightblue",
        border=ft.border.all(2, "blue")
    )
    
    # Textes d'information
    status_text = ft.Text("Prêt à démarrer", size=16, color="green")
    
    page.add(
        ft.Column([
            ft.Text("Paramètres de l'algorithme", size=20, weight="bold"),
            ft.Row([nodes_field, ants_field, iterations_field]),
            ft.Divider(),
            status_text,
            graph_container
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)
```

</details>

**Testez votre application** : vous devriez voir les champs de saisie et une zone bleue pour le graphe.

---

## Partie 3 : Générer et Afficher le Graphe

### Étape 3 : Créer des nœuds aléatoires

**Objectif :** Générer des positions aléatoires pour les villes et les afficher comme des cercles verts numérotés.

**Ce que vous devez faire :**

1. **Ajoutez les imports nécessaires** :
   - `import random` pour générer des positions aléatoires
   - `import math` pour les calculs de distance

2. **Créez une variable globale** `nodes = []` pour stocker les positions (x, y) des nœuds

3. **Fonction `generer_nodes()`** :
   - Récupérez le nombre de nœuds depuis `nodes_field.value` (utilisez `try/except` pour gérer les erreurs)
   - Pour chaque nœud, générez :
     - x entre 50 et 550 (pour laisser des marges)
     - y entre 50 et 450
   - Stockez les positions dans la liste `nodes`
   - Appelez la fonction `dessiner_graphe()`

4. **Fonction `dessiner_graphe()`** :
   - Créez une liste `shapes = []`
   - Pour chaque nœud dans `nodes` :
     - Créez un `ft.Container` circulaire (20x20 pixels)
     - Utilisez `border_radius=10` pour faire un cercle
     - Positionnez-le avec `left=x-10, top=y-10` (pour centrer)
     - Ajoutez le numéro du nœud avec `content=ft.Text(...)`
     - Ajoutez-le à la liste `shapes`
   - Mettez à jour `graph_container.content` avec un `ft.Stack(controls=shapes, width=600, height=500)`
   - Appelez `page.update()`

5. **Ajoutez un bouton "Générer le Graphe"** qui appelle `generer_nodes()` au clic

6. **Générez un graphe initial** à la fin de la fonction `main()`

<details>
<summary>💡 Besoin d'aide ?</summary>

**Indices :**
- Position aléatoire : `random.uniform(50, 550)`
- Container circulaire pour les noeuds :
```python
ft.Container(
    width=20, height=20,
    bgcolor="green",
    border_radius=10,
    left=x-10, top=y-10,
    content=ft.Text(str(i), size=10, color="white"),
    alignment=ft.alignment.center
)
```
- Stack pour empiler des éléments : `ft.Stack(controls=[...], width=600, height=500)`
- Modifier le contenu du graphe pour fond blanc : `bgcolor="white"`

**Le mot-clé `nonlocal` :**
- Permet à une fonction imbriquée de **modifier** une variable de la fonction parente
- Sans `nonlocal`, Python créerait une nouvelle variable locale au lieu de modifier l'existante
- Exemple :
```python
def parent():
    compteur = 0  # Variable de la fonction parente
    
    def incrementer():
        nonlocal compteur  # On veut modifier la variable parente, pas créer une nouvelle
        compteur += 1
    
    incrementer()
    print(compteur)  # Affiche 1 (la variable parente a été modifiée)
```

</details>

<details>
<summary>🔴 Solution complète</summary>

```python
import flet as ft
import random
import math

def main(page: ft.Page):
    page.title = "Algorithme de Colonie de Fourmis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Variables globales pour stocker les données
    nodes = []  # Liste des positions (x, y) des nœuds
    
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
    
    def generer_nodes():
        """Génère des positions aléatoires pour les nœuds"""
        nonlocal nodes
        try:
            num_nodes = int(nodes_field.value)
        except ValueError:
            num_nodes = 20
        
        nodes = []
        for _ in range(num_nodes):
            x = random.uniform(50, 550)  # Marges de 50px
            y = random.uniform(50, 450)
            nodes.append((x, y))
        
        print(f"{len(nodes)} nœuds générés")
        dessiner_graphe()
    
    def dessiner_graphe():
        """Dessine les nœuds sur le graphe"""
        shapes = []
        
        # Dessiner chaque nœud comme un cercle vert
        for i, (x, y) in enumerate(nodes):
            cercle = ft.Container(
                width=20,
                height=20,
                bgcolor="green",
                border_radius=10,
                left=x - 10,  # Centrer le cercle
                top=y - 10,
                content=ft.Text(str(i), size=10, color="white"),
                alignment=ft.alignment.Alignment(0, 0)
            )
            shapes.append(cercle)
        
        # Mettre à jour le conteneur avec un Stack (empilement)
        graph_container.content = ft.Stack(
            controls=shapes,
            width=600,
            height=500
        )
        page.update()
    
    # Bouton pour générer le graphe
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
    
    # Générer un graphe initial
    generer_nodes()

if __name__ == "__main__":
    ft.app(target=main)
```

</details>

**Testez** : cliquez sur "Générer le Graphe" pour voir apparaître des points verts numérotés à des positions différentes !

---

## Partie 4 : Calculer les Distances

### Étape 4 : Matrice de distances

**Objectif :** Calculer la distance entre chaque paire de nœuds.

**Rappel mathématique :** La distance euclidienne entre deux points (x₁, y₁) et (x₂, y₂) est :
```
distance = √((x₂ - x₁)² + (y₂ - y₁)²)
```

**Ce que vous devez faire :**

1. **Créez une fonction `calculer_distances()`** qui :
   - Crée une matrice (liste de listes) de taille n×n (où n = nombre de nœuds)
   - Pour chaque paire de nœuds (i, j) :
     - Si i == j : distance = 0 (distance d'un nœud à lui-même)
     - Sinon : calcule la distance euclidienne entre nodes[i] et nodes[j]
   - Retourne la matrice complète

2. **Modifiez `generer_nodes()`** pour :
   - Appeler `calculer_distances()` après avoir généré les nœuds
   - Afficher un message de test (ex: distance entre nœud 0 et 1)

<details>
<summary>💡 Besoin d'aide ?</summary>

**Indices :**
- Créer une matrice vide : `distances = []`
- Pour chaque ligne : `row = []` puis `distances.append(row)`
- Distance euclidienne : `math.sqrt(dx*dx + dy*dy)` où `dx = x2 - x1` et `dy = y2 - y1`
- Accéder aux coordonnées : `nodes[i][0]` pour x, `nodes[i][1]` pour y

**Structure de la boucle :**
```python
for i in range(len(nodes)):
    row = []
    for j in range(len(nodes)):
        # Calculer la distance entre i et j
        # Ajouter à row
    distances.append(row)
```

</details>

<details>
<summary>🔴 Solution complète</summary>

```python
def calculer_distances():
    """Calcule la matrice des distances entre tous les nœuds"""
    distances = []
    for i in range(len(nodes)):
        row = []
        for j in range(len(nodes)):
            if i == j:
                row.append(0)
            else:
                # Distance euclidienne
                dx = nodes[i][0] - nodes[j][0]
                dy = nodes[i][1] - nodes[j][1]
                distance = math.sqrt(dx * dx + dy * dy)
                row.append(distance)
        distances.append(row)
    return distances
```

Modification de `generer_nodes()` :
```python
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
    print(f"Distance entre nœud 0 et 1 : {distances[0][1]:.2f}")
    
    dessiner_graphe()
```

</details>

---

## Partie 5 : L'Algorithme de Colonie de Fourmis

### Étape 5 : Créer la classe AntColony

**Objectif :** Implémenter l'algorithme qui trouve le meilleur chemin.

**Ce que vous devez comprendre :**

L'algorithme utilise deux facteurs pour choisir le prochain nœud :
- **Phéromones**  (α = alpha) : l'historique des bons chemins
- **Heuristique** (β = beta) : préférence pour les nœuds proches

**Probabilité** $= (phéromone^α) × (1/distance)^β$

**Ce que vous devez faire :**

Créez une classe `AntColony` au début de votre fichier (après les imports) avec :

1. `__init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2)`

- Stocke l’ensemble des paramètres de l’algorithme
- Initialise :
  - la matrice des distances
  - la matrice des phéromones (valeur initiale : `1.0` partout)
- Définit les paramètres ACO :
  - nombre de fourmis
  - nombre de meilleurs chemins
  - nombre d’itérations
  - facteur d’évaporation
  - coefficients `alpha` (phéromones) et `beta` (heuristique)
- Initialise :
  - `meilleur_chemin` à `None`
  - `meilleure_distance` à l’infini

---

2. `calculer_distance_chemin(self, chemin)`

- Prend en entrée un chemin (liste d’indices de villes)
- Calcule la somme des distances entre chaque paire de villes consécutives
- Retourne la distance totale du chemin

---

3. `generer_tous_chemins(self)`

- Génère un chemin pour chaque fourmi :
  - chaque fourmi construit son chemin pas à pas
  - les choix sont guidés par les phéromones et l’heuristique
- Calcule la distance associée à chaque chemin
- Retourne une liste de tuples :

```text
[(chemin_1, distance_1), (chemin_2, distance_2), ...]
````
Détail de la logique interne
- Au démarrage
    * Choisit une ville de départ aléatoire
    * Initialise la liste des villes visitées

- Tant que toutes les villes ne sont pas visitées
    * Calcule les probabilités de déplacement
    * Sélectionne la prochaine ville
* Ajoute la ville au chemin

---

### 5. `calculer_probabilites_mouvement(self, chemin)`

* Se base sur la dernière ville du chemin
* Pour chaque ville :

  * probabilité = `0` si la ville est déjà visitée
  * sinon :

    $(\text{phéromone}^{\alpha}) \times \left(\frac{1}{\text{distance}}\right)^{\beta}$

* Normalise les probabilités (division par la somme totale)
* Retourne la liste des probabilités

---

### 6. `choisir_ville_suivante(self, probabilites)`

* Effectue un tirage aléatoire pondéré
* Sélectionne une ville en fonction des probabilités calculées
* Retourne l’indice de la ville choisie

---

### 7. `deposer_pheromones(self, tous_chemins)`

* Trie les chemins par distance croissante
* Sélectionne les `n_meilleurs` chemins
* Pour chaque arête de ces chemins :

  * ajoute une quantité de phéromones proportionnelle à `1 / distance_du_chemin`

---

### 8. `evaporer_pheromones(self)`

* Applique l’évaporation sur toute la matrice :

```text
pheromone[i][j] *= decay
```

---

### 9. `run(self)`

* Pour chaque itération :

  * génère les chemins de toutes les fourmis
  * identifie le meilleur chemin de l’itération
  * met à jour le meilleur chemin global
  * dépose les phéromones
  * applique l’évaporation
  * appelle le callback de mise à jour (si fourni)
* S’arrête si l’événement d’arrêt est déclenché

À la fin :

* conserve le meilleur chemin trouvé et sa distance


<details>
<summary>💡 Besoin d'aide sur la structure ?</summary>

**Structure de base :**
```python
import random
import time
import threading

class AntColony:
    def __init__(self, distances : list, n_fourmis : int, n_meilleurs : int, n_iterations : int, decroissance : float, alpha : float = 1, beta : float = 2):
        """
        Initialise la colonie de fourmis.
        
        Paramètres :
        - distances : matrice des distances entre les villes ex : distances[i][j] est la distance entre la ville i et la ville j
        - n_fourmis : nombre de fourmis par itération
        - n_meilleurs : nombre de meilleurs chemins qui déposent des phéromones
        - n_iterations : nombre d'itérations de l'algorithme
        - decay : taux d'évaporation des phéromones (entre 0 et 1)
        - alpha : importance des phéromones (α)
        - beta : importance de l'heuristique (β)
        """
        self.distances = distances
        self.pheromones = [[1.0 for _ in range(len(distances))] for _ in range(len(distances))]
        self.n_fourmis = n_fourmis
        self.n_meilleurs = n_meilleurs
        self.n_iterations = n_iterations
        self.decroissance = decroissance
        self.alpha = alpha
        self.beta = beta

        # Liste de tous les indices des villes ex : 0, 1, 2, ..., n-1
        self.tous_indices = range(len(distances))

        # Variables pour stocker le meilleur chemin et la meilleure distance
        self.meilleur_chemin = None
        self.meilleure_distance = float('inf')

    def run(self, callback_maj, evenement_arret):
        """
        Exécute l'algorithme d'optimisation par colonie de fourmis.

        Paramètres
        ----------
        callback_maj : callable
            Une fonction de callback à appeler après chaque itération.
            La fonction doit prendre trois paramètres : l'itération actuelle,
            le meilleur chemin trouvé jusqu'à présent, et la matrice des phéromones.
        evenement_arret : threading.Event
            Un événement à définir pour arrêter l'algorithme.

        Retourne
        -------
        None
        """
        pass
    
    def calculer_distance_chemin(self, chemin):
        """
        Calcule la distance totale d'un chemin.

        Paramètres
        ----------
        chemin : list
            Une liste d'indices représentant un chemin.

        Retourne
        -------
        int
            La distance totale du chemin.
        """
        pass

    def generer_tous_chemins(self):
        """
        Génère tous les chemins possibles en utilisant l'algorithme d'optimisation par colonie de fourmis.

        Retourne
        -------
        list
            Une liste de tuples, où chaque tuple contient un chemin et sa distance totale.
        """
        pass

    def calculer_probabilites_mouvement(self, chemin):
        """
        Calcule la probabilité de se déplacer vers chaque ville étant donné le chemin actuel.

        Paramètres
        ----------
        chemin : list
            Une liste d'indices représentant un chemin.

        Retourne
        -------
        list
            Une liste de probabilités, où chaque probabilité est la probabilité de se déplacer vers chaque ville étant donné le chemin actuel.
        """
        pass

    def choisir_ville_suivante(self, probabilites):
        """
        Choisit la prochaine ville en fonction des probabilités données.

        Paramètres
        ----------
        probabilites : list
            Une liste de probabilités, où chaque probabilité est la probabilité de se déplacer vers chaque ville.

        Retourne
        -------
        int
            L'indice de la ville choisie comme prochaine ville.
        """
        pass

    def deposer_pheromones(self, tous_chemins):
        """
        Dépose des phéromones sur les meilleurs chemins.

        Paramètres
        ----------
        tous_chemins : list
            Une liste de tuples, où chaque tuple contient un chemin et sa distance totale.

        Retourne
        -------
        None
        """
        pass

if __name__ == "__main__":
    distances = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
    # Créer une instance de la colonie de fourmis
    colonie_fourmis = AntColony(distances, n_fourmis=3, n_meilleurs=5, n_iterations=100, decroissance=0.95, alpha=1, beta=2)
    
    def callback_maj(iteration, meilleur_chemin, pheromones):
        """
        Fonction de callback appeler après chaque itération.

        Paramètres
        ----------
        iteration : int
            L'itération actuelle.
        meilleur_chemin : tuple
            Le meilleur chemin trouvé jusqu'à présent.
        pheromones : list
            La matrice des phéromones.

        Retourne
        -------
        None
        """
        if iteration % 10 == 0:
            print(f"Itération {iteration}: Meilleur chemin {meilleur_chemin} avec distance {colonie_fourmis.meilleure_distance}")
            print("Matrice des phéromones:")
            for ligne in pheromones:
                print(ligne)

    # Créer un événement d'arrêt
    evenement_arret = threading.Event()
    # Exécuter l'algorithme dans le thread principal pour cet exemple
    colonie_fourmis.run(callback_maj, evenement_arret)
    # Meillere chemin trouvé
    print(f"Meilleur chemin trouvé : {colonie_fourmis.meilleur_chemin} avec une distance de {colonie_fourmis.meilleure_distance}")
```

</details>

<details>
<summary>🔴 Solution complète</summary>

```python
import random
import time
import threading

class AntColony:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        """
        Initialise la colonie de fourmis.
        
        Paramètres :
        - distances : matrice des distances entre les villes
        - n_ants : nombre de fourmis par itération
        - n_best : nombre de meilleurs chemins qui déposent des phéromones
        - n_iterations : nombre d'itérations de l'algorithme
        - decay : taux d'évaporation des phéromones (entre 0 et 1)
        - alpha : importance des phéromones (α)
        - beta : importance de l'heuristique (β)
        """
        self.distances = distances
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        
        # Initialiser la matrice de phéromones
        n = len(distances)
        self.pheromones = [[1.0 for _ in range(n)] for _ in range(n)]
        
        # Variables pour le meilleur chemin trouvé
        self.meilleur_chemin = None
        self.meilleure_distance = float('inf')
        
        # Toutes les indices de villes
        self.all_indices = range(n)

    def calculer_distance_chemin(self, chemin):
        """
        Calcule la distance totale d'un chemin.
        
        Paramètre :
        - chemin : liste d'indices représentant l'ordre des villes
        
        Retourne :
        - La distance totale du chemin
        """
        total = 0
        for i in range(len(chemin) - 1):
            total += self.distances[chemin[i]][chemin[i+1]]
        return total

    def generer_chemin_fourmi(self):
        """
        Génère un chemin complet pour une fourmi.
        
        Retourne :
        - Un tuple (chemin, distance) pour la fourmi
        """
        # Commencer par une ville aléatoire
        chemin = [random.randint(0, len(self.distances) - 1)]
        
        # Ajouter les autres villes
        while len(chemin) < len(self.distances):
            prochaines_probas = self.calculer_probabilites_mouvement(chemin)
            prochaine_ville = self.choisir_prochaine_ville(prochaines_probas)
            chemin.append(prochaine_ville)
        
        return (chemin, self.calculer_distance_chemin(chemin))

    def calculer_probabilites_mouvement(self, chemin):
        """
        Calcule les probabilités de mouvement vers chaque ville.
        
        Paramètre :
        - chemin : le chemin actuel de la fourmi
        
        Retourne :
        - Liste des probabilités normalisées
        """
        ville_actuelle = chemin[-1]
        probabilites = []
        
        for ville in self.all_indices:
            if ville in chemin:
                probabilites.append(0)  # Ville déjà visitée
            else:
                # Calculer la probabilité selon la formule
                pheromone = self.pheromones[ville_actuelle][ville] ** self.alpha
                heuristique = (1.0 / self.distances[ville_actuelle][ville]) ** self.beta
                probabilites.append(pheromone * heuristique)
        
        # Normaliser les probabilités
        total = sum(probabilites)
        if total > 0:
            return [p / total for p in probabilites]
        else:
            return [0] * len(probabilites)

    def choisir_prochaine_ville(self, probabilites):
        """
        Choisit la prochaine ville selon les probabilités.
        
        Paramètre :
        - probabilites : liste des probabilités normalisées
        
        Retourne :
        - L'indice de la prochaine ville
        """
        r = random.random()
        cumul = 0
        
        for i, p in enumerate(probabilites):
            cumul += p
            if cumul >= r:
                return i
        
        return len(probabilites) - 1

    def deposer_pheromones(self, tous_les_chemins):
        """
        Dépose des phéromones sur les meilleurs chemins.
        
        Paramètre :
        - tous_les_chemins : liste de tous les chemins générés
        """
        # Trier les chemins par distance (du meilleur au pire)
        chemins_tries = sorted(tous_les_chemins, key=lambda x: x[1])
        
        # Déposer des phéromones sur les n_best meilleurs chemins
        for chemin, distance in chemins_tries[:self.n_best]:
            for i in range(len(chemin) - 1):
                ville1, ville2 = chemin[i], chemin[i+1]
                # La quantité de phéromones est inversement proportionnelle à la distance
                self.pheromones[ville1][ville2] += 1.0 / distance

    def evaporer_pheromones(self):
        """
        Fait évaporer les phéromones selon le taux de décroissance.
        """
        n = len(self.pheromones)
        for i in range(n):
            for j in range(n):
                self.pheromones[i][j] *= self.decay

    def executer_iteration(self):
        """
        Exécute une itération complète de l'algorithme.
        
        Retourne :
        - Un tuple (meilleur_chemin, meilleure_distance) pour cette itération
        """
        # Générer les chemins pour toutes les fourmis
        tous_les_chemins = []
        for _ in range(self.n_ants):
            tous_les_chemins.append(self.generer_chemin_fourmi())
        
        # Trouver le meilleur chemin de cette itération
        meilleur_chemin_iteration = min(tous_les_chemins, key=lambda x: x[1])
        
        # Mettre à jour le meilleur chemin global
        if meilleur_chemin_iteration[1] < self.meilleure_distance:
            self.meilleur_chemin = meilleur_chemin_iteration[0]
            self.meilleure_distance = meilleur_chemin_iteration[1]
        
        # Déposer et évaporer les phéromones
        self.deposer_pheromones(tous_les_chemins)
        self.evaporer_pheromones()
        
        return meilleur_chemin_iteration

    def run(self, callback_maj, evenement_arret):
        """
        Exécute l'algorithme complet.
        
        Paramètres :
        - callback_maj : fonction de callback appelée après chaque itération
        - evenement_arret : threading.Event pour arrêter l'algorithme
        """
        for iteration in range(self.n_iterations):
            # Vérifier si l'arrêt a été demandé
            if evenement_arret.is_set():
                break
            
            # Exécuter une itération
            chemin_courant, distance_courante = self.executer_iteration()
            
            # Appeler le callback de mise à jour
            callback_maj(iteration, chemin_courant, self.pheromones)
            
            # Petite pause pour permettre la mise à jour de l'interface
            time.sleep(0.1)

# Exemple d'utilisation
if __name__ == "__main__":
    # Matrice de distances d'exemple (4 villes)
    distances = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
    
    # Créer la colonie de fourmis
    colonie = AntColony(
        distances=distances,
        n_ants=3,
        n_best=5,
        n_iterations=100,
        decay=0.95,
        alpha=1,
        beta=2
    )
    
    # Créer un événement d'arrêt
    evenement_arret = threading.Event()
    
    # Définir une fonction de callback
    def callback_maj(iteration, chemin, pheromones):
        if iteration % 10 == 0:
            print(f"Iteration {iteration}: Meilleur chemin = {chemin}, Distance = {colonie.meilleure_distance}")
            print("Pheromones matrix:")
            for row in pheromones:
                print(row)  
    
    # Exécuter l'algorithme
    colonie.run(callback_maj, evenement_arret)

```

</details>

---

## Partie 6 — Intégration de l’Algorithme avec l’Interface (Flet)

### Objectif

Maintenant que l’algorithme de colonie de fourmis est implementé, cette partie consiste à le connecter ensemble avec l'application flet :

- exécuter l’algorithme sans bloquer l’interface
- visualiser les phéromones en temps réel
- permettre à l’utilisateur de démarrer, arrêter et redémarrer l’algorithme

---

### Concepts clés à comprendre

- L’algorithme s’exécute dans **un thread séparé**
- L’interface Flet reste dans le **thread principal**
- La synchronisation est assurée via `threading.Event`
- Les mises à jour UI se font avec `page.run_task()`

---

### Étape 1 — Imports nécessaires

Ajoutez (ou vérifiez) les imports suivants en haut du fichier :

```python
import flet as ft
import random
import math
import time
import threading
from AntColony import AntColony
```
### Étape 2 — Variables globales de l’algorithme

Stocker l’état de l’algorithme afin qu’il puisse être :
- lu par l’interface
- modifié par le thread de calcul

Point clé :
Ces variables sont définies dans main() juste après nodes = [] et modifiées via nonlocal dans les fonctions internes.

```python
distances = []
pheromones = []
best_path = []
iteration = 0
running = False
stop_event = threading.Event()
```
### Étape 3 — Champs de paramètres supplémentaires
On veut que l’utilisateur puisse modifier les paramètres de l’algorithme depuis l’interface.
s
Point clé :
- TextField est un composant contrôlé : on lit sa valeur via .value
- Les valeurs sont toujours des chaînes de caractères → conversion nécessaire

```python
best_field = ft.TextField(label="Meilleures fourmis", value="3", width=150)
decay_field = ft.TextField(label="Décay", value="0.95", width=150)
alpha_field = ft.TextField(label="Alpha", value="1", width=150)
beta_field = ft.TextField(label="Beta", value="2", width=150)
```
### Étape 4 — Textes d’information

Afficher en temps réel :

- l’itération actuelle
- l’état des phéromones
- le meilleur chemin trouvé

Point clé :

- Modifier un texte se fait via text.value
- L’affichage est mis à jour avec page.update()

Ajoutez après status_text :

```python
iteration_text = ft.Text("Itération: 0", size=16)
pheromone_text = ft.Text("Phéromones moyennes: ", size=14)
path_text = ft.Text("Meilleur chemin: ", size=14)
```
### Étape 5 — Initialisation des phéromones
On va juste initialiser les pheromones ici pour des question d'affichage du graphes au départ du. 
```python
def generer_nodes():
    """Génère des positions aléatoires pour les nœuds"""
    nonlocal nodes, distances, pheromones

    try:
        num_nodes = int(nodes_field.value)
    except ValueError:
        num_nodes = 20

    nodes = []
    for _ in range(num_nodes):
        x = random.uniform(50, 550)
        y = random.uniform(50, 450)
        nodes.append((x, y))

    def calculer_distances():
        """Calcule la matrice des distances"""
        distances = []
        for i in range(len(nodes)):
            row = []
            for j in range(len(nodes)):
                if i == j:
                    row.append(0)
                else:
                    dx = nodes[i][0] - nodes[j][0]
                    dy = nodes[i][1] - nodes[j][1]
                    row.append(math.sqrt(dx*dx + dy*dy))
            distances.append(row)
        return distances

    distances = calculer_distances()
    pheromones = [[1.0 for _ in range(len(nodes))] for _ in range(len(nodes))]

    dessiner_graphe()
```
### Étape 6 — Affichage des arrêtes sur le graphique
Ici on dessine une arête entre deux nœuds.
On fait une fonction générale pour pouvoir l'utiliser soi pour voir les le graphes en entiers soi pour tracer des chemins avec une autres couleurs. 

Point clé :

- Flet n’a pas de composant Line donc, on simule une ligne avec un Container très fin + rotation
- atan2(dy, dx) calcule automatiquement le bon angle

```python
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
        top=y1 - thickness / 2,
        rotate=ft.Rotate(
            angle=angle,
            alignment=ft.alignment.Alignment(-1, 0)
        )
    )
```

### Étape 7 — Dessin du graphe et des phéromones
Cette fonction est responsable de la visualisation :

- des nœuds du graphe (villes)
- des arêtes pondérées par les phéromones
- du meilleur chemin courant trouvé par la colonie de fourmis

Plus une arête contient de phéromones, plus elle est épaisse et opaque.
```python
def draw_graph():
    """
    Dessine le graphe des villes avec :
    - les arêtes pondérées par les phéromones
    - le meilleur chemin courant en rouge
    - les nœuds (villes) numérotés
    """

    # Liste de formes graphiques à afficher dans le Stack
    shapes = []
    
    # ==========================
    # Dessin des arêtes (phéromones)
    # ==========================
    if pheromones and len(pheromones) > 0:
        # Valeur maximale des phéromones (pour normalisation)
        max_pheromone = max(max(row) for row in pheromones) if pheromones else 1

        # Parcours de toutes les paires de nœuds
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                # Seuil minimal pour éviter l’encombrement visuel
                if pheromones[i][j] > 0.1:
                    # Opacité proportionnelle à la quantité de phéromones
                    opacity = min(1, pheromones[i][j] / max_pheromone)

                    # Épaisseur proportionnelle aux phéromones
                    thickness = max(1, (pheromones[i][j] / max_pheromone) * 3)

                    # Création de la ligne entre les deux nœuds
                    line = create_line(
                        nodes[i][0], nodes[i][1],
                        nodes[j][0], nodes[j][1],
                        ft.Colors.with_opacity(opacity, ft.Colors.BLUE),
                        thickness
                    )
                    shapes.append(line)
    
    # ==========================
    # Dessin du meilleur chemin courant
    # ==========================
    if best_path:
        for i in range(len(best_path) - 1):
            start_idx = best_path[i]
            end_idx = best_path[i + 1]

            # Vérification de sécurité
            if start_idx < len(nodes) and end_idx < len(nodes):
                line = create_line(
                    nodes[start_idx][0], nodes[start_idx][1],
                    nodes[end_idx][0], nodes[end_idx][1],
                    "red",   # Couleur du meilleur chemin
                    3        # Épaisseur renforcée
                )
                shapes.append(line)
    
    # ==========================
    # Dessin des nœuds (villes)
    # ==========================
    for i, (x, y) in enumerate(nodes):
        shapes.append(
            ft.Container(
                width=20,
                height=20,
                bgcolor="green",
                border_radius=10,   # Cercle
                left=x - 10,
                top=y - 10,
                content=ft.Text(str(i), size=10, color="white"),
                alignment=ft.alignment.Alignment(0, 0)
            )
        )
    
    # Mise à jour du conteneur graphique
    graph_container.content = ft.Stack(controls=shapes, width=600, height=500)
    page.update()
```
### Étape 8 — Callback de mise à jour
Cette fonction est appelée à chaque itération de l’algorithme :

- elle met à jour l’itération courante
- affiche le meilleur chemin
- met à jour la visualisation et les statistiques
```python
def update_callback(iter_num, current_best_path, current_pheromones):
    """
    Callback appelé par l’algorithme à chaque itération
    pour mettre à jour l’interface graphique.
    """
    nonlocal iteration, best_path, pheromones

    # Mise à jour des variables globales
    iteration = iter_num
    best_path = current_best_path[0] if current_best_path else []
    pheromones = current_pheromones

    async def update_ui():
        # Affichage du numéro d’itération
        iteration_text.value = f"Itération: {iteration}"

        # Affichage du meilleur chemin et de sa longueur
        if current_best_path:
            path_text.value = (
                f"Meilleur chemin: {best_path} "
                f"(longueur: {current_best_path[1]:.2f})"
            )

        # Calcul de la moyenne des phéromones
        avg = sum(sum(row) for row in pheromones) / (len(nodes) ** 2)
        pheromone_text.value = f"Phéromones moyennes: {avg:.4f}"

        # Redessiner le graphe
        dessiner_graphe()

    # Lancement asynchrone pour ne pas bloquer l’UI
    page.run_task(update_ui)

```
### Étape 9 — Démarrage de l’algorithme
Il nous reste à coder ce que font les boutons de l'application dans l'étape 9 et 10. 
On rapelle la syntaxe des Button est : 
```python
object = ft.Button("Titre", on_click=fonction_activé_par_le bouton,disabled=booleen_pour_savoir_si_on_peut_clicker_dessus)
```
Cette fonction :

- récupère les paramètres utilisateur
- lance l’algorithme dans un thread séparé
- évite le blocage de l’interface graphique

<details>
<summary>Commenter ce code pour le comprendre</summary>

    def start_algorithm(e):
        nonlocal running
        if running:
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
                    float(beta_field.value),
                )
            except ValueError:
                colony = AntColony(distances, 15, 3, 100, 0.95, 1, 2)
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
```

```

</details>

<details>
<summary>🔴 Solution complète</summary>

    def start_algorithm(e):
        nonlocal running
        # Empêche un double lancement
        if running:
            return

        running = True
        stop_event.clear()

        # Mise à jour de l’interface
        start_btn.disabled = True
        stop_btn.disabled = False
        status_text.value = "En cours d'exécution..."
        status_text.color = "orange"
        page.update()

        def run_ants():
            try:
                # Création de la colonie de fourmis
                colony = AntColony(
                    distances,
                    int(ants_field.value),
                    int(best_field.value),
                    int(iterations_field.value),
                    float(decay_field.value),
                    float(alpha_field.value),
                    float(beta_field.value),
                )
            except ValueError:
                # Valeurs par défaut en cas d’erreur utilisateur
                colony = AntColony(distances, 15, 3, 100, 0.95, 1, 2)

            # Lancement de l’algorithme
            colony.run(update_callback, stop_event)

            async def finalize():
                """
                Finalize the Ant Colony Optimization algorithm
                Called when the algorithm has finished its execution
                """
                nonlocal running
                running = False
                # Enable the "Start" button and disable the "Stop" button
                start_btn.disabled = False
                stop_btn.disabled = True
                # Update the status text
                status_text.value = "Terminé"
                status_text.color = "green"

                page.update()

            page.run_task(finalize)

        # Thread pour exécution non bloquante
        threading.Thread(target=run_ants, daemon=True).start()
```

```

</details>


### Étape 10 — Arrêt et redémarrage
Permet :

- d’arrêter proprement l’algorithme
- de réinitialiser le graphe et l’interface
- de relancer une nouvelle simulation

<details>
<summary>Commenter ce code pour le comprendre</summary>

    def stop_algorithm(e):
        nonlocal running
            stop_event.set()
            start_btn.disabled = False
            stop_btn.disabled = True
            status_text.value = "Arrêté"
            status_text.color = "red"
            page.update()


    def restart_graph(e):
        nonlocal iteration, best_path, running
        running = False
        stop_event.set()
        iteration = 0
        best_path = []
        iteration_text.value = "Itération: 0"
        path_text.value = "Meilleur chemin: "
        pheromone_text.value = "Phéromones moyennes: "
        status_text.value = "Prêt"
        status_text.color = "green"
        start_btn.disabled = False
        stop_btn.disabled = True
        generer_nodes()
```

```
</details>


<details>
<summary>🔴 Solution complète</summary>

    def stop_algorithm(e):
        """
        Arrête l’algorithme en cours d’exécution.
        Called when the "Stop" button is clicked.
        """
        nonlocal running
            # Set the stop event to signal the algorithm to stop
            stop_event.set()
            # Disable the "Stop" button and enable the "Start" button
            start_btn.disabled = False
            stop_btn.disabled = True
            # Update the status text
            status_text.value = "Arrêté"
            status_text.color = "red"
            # Update the page
            page.update()


    def restart_graph(e):
        """
        Réinitialise complètement le graphe et l’interface.
        """
        nonlocal iteration, best_path, running

        running = False
        stop_event.set()

        # Réinitialisation des variables
        iteration = 0
        best_path = []

        # Réinitialisation de l’UI
        iteration_text.value = "Itération: 0"
        path_text.value = "Meilleur chemin: "
        pheromone_text.value = "Phéromones moyennes: "
        status_text.value = "Prêt"
        status_text.color = "green"

        # Disable the "Stop" button and enable the "Start" button
        start_btn.disabled = False
        stop_btn.disabled = True

        # Génération de nouveaux nœuds
        generer_nodes()
```

```
</details>

On oublie pas de mettre à jour le layout final.

---

### Étape 11. Construction et distribution de l’application avec Flet ( à faire chez vous ou si vous avez le temps)

Vous avez déjà développé une application fonctionnelle sous forme de scripts Python (interface + logique métier séparée).  
Il est maintenant possible de finaliser ce travail en transformant votre projet en **application distribuable**. 

