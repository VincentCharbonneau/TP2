from enum import Enum
import random

from simulation_constants import *
from animal import *


class Contenu(Enum):
    VIDE = 0
    PROIE = 1
    PREDATEUR = 2


def creer_case(etat=Contenu.VIDE, animal=None):
    # TODO: Créer et retourner un dictionnaire représentant une case. Utiliser les arguments pour initialiser l'état et l'animal dans la case.
    case = {"etat": etat, "animal" : animal}
    
    return case



def creer_grille(nb_lignes, nb_colonnes):
    # TODO: Créer une matrice 2D de cases vides et la retourner sous forme de dictionnaire
    grille = []



    for i in range(nb_lignes):
        lignes = [creer_case() for y in range(nb_colonnes)]
        grille.append(lignes)

        

    # TODO: Dans le dictionnaire, ajouter des métadonnées décrites dans l'énoncé (nombre de proies, de prédateurs, etc.)

    matrix = {"matrice": grille, "nb_proies": 0, "nb_predateurs" : 0, "nb_lignes": nb_lignes, "nb_colonnes":nb_colonnes}

    return matrix


def obtenir_case(grille, ligne, colonne):
    # TODO: Creer une fonction qui recupere un case specifique dans la grille

    #entrer dans le dictionnaire pour acceder a la matrice

    dans_matrice = grille["matrice"]

    #selectionner la case specifique 
    case_specifique = dans_matrice[ligne][colonne]

    return case_specifique

def obtenir_etat(grille, ligne, colonne):
    
    # TODO: Creer une fonction qui recupere un case specifique dans la grille et revoie simplement etat de la case

    #entrer dans le dictionnaire pour acceder a la matrice

    dans_matrice = grille["matrice"]
    

    #selectionner la case specifique 
    case_specifique = dans_matrice[ligne][colonne]
    #selection la secontion etat dans la case
    etat_dans_case = case_specifique["etat"]

    return etat_dans_case

def obtenir_animal(grille, ligne, colonne):
    # TODO: Retourner l'animal présent dans la case aux coordonnées données (ligne, col) (Dict)

    dans_matrice = grille["matrice"]

    #selectionner la case specifique 
    case_specifique = dans_matrice[ligne][colonne]
    animal = case_specifique["animal"]

    return animal

	
grille = creer_grille(3, 3)
for i in range(3):
    for j in range(3):
        print(obtenir_animal(grille, i, j))



def obtenir_population(grille):
    # TODO: Retourner un tuple contenant le nombre actuel de proies et de prédateurs dans la grille (Tuple[Int, Int])
    print()

    pass


def obtenir_dimensions(grille):
    # TODO: Retourner un tduple avec le nombre de lignes et de colonnes de la grille (Tuple[Int, Int])

    pass


def obtenir_animal(grille, ligne, col):
    # TODO: Retourner l'animal présent dans la case aux coordonnées données (ligne, col) (Dict)
    pass


def incrementer_nb_proies(grille):
    # TODO: Augmenter le compteur du nombre de proies dans la grille de 1 (Int)
    pass


def decrementer_nb_proies(grille):
    # TODO: Diminuer le compteur du nombre de proies dans la grille de 1 (Int)
    pass


def incrementer_nb_predateurs(grille):
    # TODO: Augmenter le compteur du nombre de prédateurs dans la grille de 1 (Int)
    pass


def decrementer_nb_predateurs(grille):
    # TODO: Diminuer le compteur du nombre de prédateurs dans la grille de 1 (Int)
    pass


def check_nb_proies(grille, max_val):
    # TODO: Vérifier si le nombre actuel de proies dans la grille est inférieur à max_val (Booléen)
    pass


def vider_case(grille, ligne, col):
    # TODO: Écraser la case située à la ligne et la colonne données avec une case vide
    pass


def definit_etat(grille, etat, ligne, col):
    # TODO: Mettre à jour l'état de la case située à la ligne et la colonne données.
    # Utiliser le paramètre 'etat', qui est une valeur de l'Enum Contenu (VIDE, PROIE, PREDATEUR).
    pass


def definir_animal(grille, animal, ligne, col):
    # TODO: Placer un animal (sous forme de dictionnaire) sur la case indiquée par les coordonnées (ligne, col).
    pass


def obtenir_etat(grille, ligne, col):
    # TODO: Obtenir et retourner l'état actuel de la case à la position (ligne, col).
    # Le type de retour est une valeur de l'Enum Contenu (VIDE, PROIE, PREDATEUR).
    pass


def generer_entier(min_val, max_val):
    # TODO: Utiliser une librairie pour générer un nombre entier aléatoire entre min_val et max_val inclus.
    # Le résultat doit être un entier.
    pass


def ajuster_position_pour_grille_circulaire(lig, col, dim_lig, dim_col):
    # TODO: Ajuster la position (ligne, colonne) pour une grille circulaire en utilisant les dimensions de la grille.
    # Indice: Un modulo (%) peut être utile.
    pass


def choix_voisin_autour(grille, ligne, col, contenu: Contenu):
    # TODO: Chercher tous les voisins autour de la cellule (ligne, col) qui correspondent au "contenu" donné (Enum).
    # TODO: Renvoyer le nombre total de ces voisins, ainsi que les coordonnées d'un voisin choisi aléatoirement (Tuple).
    #       Si le contenu n'est pas VIDE, le voisin doit être disponible (voir la fonction obtenir_disponibilite).
    # Indice: Utiliser la fonction "ajuster_position_pour_grille_circulaire" pour ajuster les positions des voisins qui sont en dehors de la grille.
    pass


def remplir_grille(grille, pourcentage_proie, pourcentage_predateur):
    # TODO: Obtenir les dimensions de la grille.
    
    # TODO: Calculer le nombre total de cases dans la grille.
    
    # TODO: Calculer le nombre de proies à placer dans la grille.
    
    # TODO: Calculer le nombre de prédateurs à placer dans la grille.
    
    # TODO: Générer et mélanger aléatoirement la liste de toutes les positions possibles.
    
    # TODO: Placer les proies dans la grille.
    # Utilisez MAX_AGE_PROIE pour générer un âge aléatoire entre 0 et l'âge maximum de la proie.
    # Utilisez NB_JRS_GESTATION_PROIE et NB_JRS_PUBERTE_PROIE pour déterminer la période de gestation si la proie est en âge de procréer.
    
    # TODO: Mettre à jour le compteur du nombre de proies.
    
    # TODO: Placer les prédateurs dans la grille.
    # Utilisez MAX_AGE_PRED pour générer un âge aléatoire entre 0 et l'âge maximum du prédateur.
    # Utilisez NB_JRS_GESTATION_PRED et NB_JRS_PUBERTE_PRED pour déterminer la période de gestation si le prédateur est en âge de procréer.
    # Utilisez AJOUT_ENERGIE pour initialiser la quantité d'énergie du prédateur.
    
    # TODO: Mettre à jour le compteur du nombre de prédateurs.
    
    pass