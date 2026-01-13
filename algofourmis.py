import random
import time
import threading

class AntColony:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        self.distances = distances
        self.pheromone = [[1 / len(distances) for _ in range(len(distances))] for _ in range(len(distances))]
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        n = len(distances)
        self.pheromones = [[1.0 for _ in range(n)] for _ in range(n)]
        self.meilleur_chemin = None
        self.meilleure_distance = float('inf')
        self.all_indices = range(len(distances))
    def calculer_distance_chemin(self, chemin):
        longueur = 0.0
        for i in range(len(chemin) - 1):
            longueur += self.distances[chemin[i]][chemin[i + 1]]
        return longueur
    def generer_chemin_fourmi(self):
        chemin = [random.randint(0, len(self.distances) - 1)]
        while len(chemin) < len(self.distances):
            prochaines_probas = self.calculer_probabilites_mouvement(chemin)
            prochaine_ville = self.choisir_prochaine_ville(prochaines_probas)
            chemin.append(prochaine_ville)
            
        return (chemin, self.calculer_distance_chemin(chemin))
    def calculer_probabilites_mouvement(self, chemin):
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
        r = random.random()
        cumulative = 0.0
        for i, p in enumerate(probabilites):
            cumulative += p
            if r <= cumulative:
                return i
        return len(probabilites) - 1  # Retourner la dernière ville si rien n'est choisi
    def deposer_pheromones(self,tous_les_chemins):
        chemins_tries=sorted(tous_les_chemins, key=lambda x: x[1])
        for chemin, distance in chemins_tries[:self.n_best]:
            for i in range(len(chemin) - 1):
                self.pheromones[chemin[i]][chemin[i + 1]] += 1.0 / distance
    def evaporer_pheromones(self):
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones[i])):
                self.pheromones[i][j] *=  self.decay
    def executer_iterations(self):
        tous_les_chemins = []
        for _ in range(self.n_ants):
            tous_les_chemins.append(self.generer_chemin_fourmi())
        meilleur_chemin = min(tous_les_chemins, key=lambda x: x[1])
        if meilleur_chemin[1] < self.meilleure_distance:
            self.meilleur_chemin = meilleur_chemin[0]
            self.meilleure_distance = meilleur_chemin[1]
        self.deposer_pheromones(tous_les_chemins)
        self.evaporer_pheromones()
        return meilleur_chemin
    def run(self, callback_maj, evenement_arret):
        for i in range(self.n_iterations):
            if evenement_arret.is_set():
                break
            chemin_courant, distance_courante = self.executer_iterations()
            callback_maj(i, chemin_courant, self.pheromones)
            time.sleep(0.1)

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

    ##Partie 5 finie mais ca marche pa strop encore
