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

    case = grille["matrice"][ligne][colonne]

    return case


def obtenir_etat(grille, ligne, colonne):
    
    # TODO: Creer une fonction qui recupere un case specifique dans la grille et revoie simplement etat de la case

    return grille["matrice"][ligne][colonne]["etat"]


def definir_etat(grille, etat, ligne, col):
    # TODO: Mettre à jour l'état de la case située à la ligne et la colonne données.
    # Utiliser le paramètre 'etat', qui est une valeur de l'Enum Contenu (VIDE, PROIE, PREDATEUR).

    grille["matrice"][ligne][col]["etat"] = etat

    return grille


def obtenir_animal(grille, ligne, colonne):
    # TODO: Retourner l'animal présent dans la case aux coordonnées données (ligne, col) (Dict)

    dans_matrice = grille["matrice"]

    #selectionner la case specifique 
    case_specifique = dans_matrice[ligne][colonne]
    animal = case_specifique["animal"]

    return animal #dict


def definir_animal(grille, animal, ligne, col):
    # TODO: Placer un animal (sous forme de dictionnaire) sur la case indiquée par les coordonnées (ligne, col).

    #creer une case
    case = obtenir_case(grille, ligne, col)

    #remplace la case avec animal et son contenu
    case["animal"] = animal
    
    return grille


def definir_case(grille, case, ligne, col):
    #TODO cette fonction actuallise la case

    #remplace la case avec animal et son contenu
    grille["matrice"][ligne][col] = case
    
    return grille


def vider_case(grille, ligne, col):
    # TODO: Écraser la case située à la ligne et la colonne données avec une case vide

    
    #matrice 
    dans_matrice = grille["matrice"]

    #case vide
    case_vide = {"etat": Contenu.VIDE, "animal" : None}

    #remplace la case avec animal et son contenu
    dans_matrice[ligne][col] = case_vide

    pass


def obtenir_population(grille):
    # TODO: Retourner un tuple contenant le nombre actuel de proies et de prédateurs dans la grille (Tuple[Int, Int])
    
    #grille = dict
    #dans_matrice = liste qui contient les liste(ligne)
    #liste(ligne) = liste qui contient des case
    #case = dict qui contiennnet un etat qui est une cle

    dans_matrice = grille["matrice"]

    nb_proie = 0
    nb_predateur = 0

    for ligne in dans_matrice:
        for case in ligne:
            

            if case["etat"] is Contenu.PROIE:
                nb_proie += 1
            if case["etat"] is Contenu.PREDATEUR:
                nb_predateur += 1
        

    return (nb_proie, nb_predateur)
    

def obtenir_dimensions(grille):
    # TODO: Retourner un tduple avec le nombre de lignes et de colonnes de la grille (Tuple[Int, Int])


    matrice = grille["matrice"]

    nb_ligne = 0
    nb_col = 0

    for ligne in matrice:
        nb_ligne += 1
        for col in ligne:
            nb_col += 1

    nb_col /= nb_ligne

    return (nb_ligne, int(nb_col))


def incrementer_nb_proies(grille):
    # TODO: Augmenter le compteur du nombre de proies dans la grille de 1 (Int)
    
    grille["nb_proies"] += 1
    
    pass


def decrementer_nb_proies(grille):
    # TODO: Diminuer le compteur du nombre de proies dans la grille de 1 (Int)

    if grille["nb_proies"] > 0:
        grille["nb_proies"] -= 1
    else:
        pass


def incrementer_nb_predateurs(grille):
    # TODO: Augmenter le compteur du nombre de prédateurs dans la grille de 1 (Int)
    
    grille["nb_predateurs"] += 1

    pass


def decrementer_nb_predateurs(grille):
    # TODO: Diminuer le compteur du nombre de prédateurs dans la grille de 1 (Int)

    if grille["nb_predateurs"] > 0:
        grille["nb_predateurs"] -= 1
    else:
        pass
    

def check_nb_proies(grille, max_val):
    # TODO: Vérifier si le nombre actuel de proies dans la grille est inférieur à max_val (Booléen)

    if grille["nb_proies"] < max_val:
        return True
    else:
        return False


def ajuster_position_pour_grille_circulaire(lig, col, dim_lig, dim_col):
    # TODO: Ajuster la position (ligne, colonne) pour une grille circulaire en utilisant les dimensions de la grille.
    # Indice: Un modulo (%) peut être utile.

    
    if lig <= -1:
        lig %= dim_lig

    elif lig >= (dim_lig):
        lig %= dim_lig

    if col <= -1:
        col %= dim_col

    elif col >= (dim_col):
        col %= dim_col
        
    return (lig, col)


def choix_voisin_autour(grille, ligne, col, contenu: Contenu):
    # TODO: Chercher tous les voisins autour de la cellule (ligne, col) qui correspondent au "contenu" donné (Enum).
    # TODO: Renvoyer le nombre total de ces voisins, ainsi que les coordonnées d'un voisin choisi aléatoirement (Tuple).
    #       Si le contenu n'est pas VIDE, le voisin doit être disponible (voir la fonction obtenir_disponibilite).
    # Indice: Utiliser la fonction "ajuster_position_pour_grille_circulaire" pour ajuster les positions des voisins qui sont en dehors de la grille.

    lig_voisin, col_voisin = None, None
    tabcases = []
    nb_ligne, nb_col = obtenir_dimensions(grille)

    for i in range(ligne - 1, ligne + 2):   
        for j in range(col - 1, col + 2):
            if i != ligne or j != col:
                i2, j2 = ajuster_position_pour_grille_circulaire(i, j, nb_ligne, nb_col)
                animal = obtenir_animal(grille, i2, j2)
                if obtenir_etat(grille, i2, j2) == contenu and obtenir_animal(grille, i2, j2) == None:
                    tabcases.append((i2, j2))
                elif obtenir_etat(grille, i2, j2) == contenu and obtenir_animal(grille, i2, j2) == True:
                    tabcases.append((i2, j2))


    if tabcases != []:
        lig_voisin, col_voisin = random.choice(tabcases)
        return len(tabcases), lig_voisin, col_voisin
        
    else: 
        return len(tabcases), None, None

        
def remplir_grille(grille, pourcentage_proie, pourcentage_predateur):
    # TODO: Obtenir les dimensions de la grille.
    nb_ligne, nb_col = obtenir_dimensions(grille)

    # TODO: Calculer le nombre total de cases dans la grille.
    nb_de_case = nb_ligne * nb_col

    # TODO: Calculer le nombre de proies à placer dans la grille.
    nb_proies_a_placer = nb_de_case * pourcentage_proie

    # TODO: Calculer le nombre de prédateurs à placer dans la grille.
    nb_preateur_a_placer = nb_de_case * pourcentage_predateur

    # TODO: Générer et mélanger aléatoirement la liste de toutes les positions possibles.
    positions_possibles = []

    for i in range(nb_ligne):
        for j in range(nb_col):
            positions_possibles.append((i, j))
    random.shuffle(positions_possibles)
    

    # TODO: Placer les proies dans la grille.
    # Utilisez MAX_AGE_PROIE pour générer un âge aléatoire entre 0 et l'âge maximum de la proie.
    # Utilisez NB_JRS_GESTATION_PROIE et NB_JRS_PUBERTE_PROIE pour déterminer la période de gestation si la proie est en âge de procréer.
    for i in range(int(nb_proies_a_placer)):
        case_aleatoire = random.choice(positions_possibles)
        positions_possibles.pop(positions_possibles.index(case_aleatoire))
        age = random.randint(0, MAX_AGE_PROIE)
        if age > NB_JRS_PUBERTE_PROIE:
            nb_jours_gestation = generer_entier(1, NB_JRS_GESTATION_PROIE)
            case = creer_case(Contenu.PROIE, creer_animal(age, nb_jours_gestation, MIN_ENERGIE, True))
            definir_case(grille, case, case_aleatoire[0], case_aleatoire[1])    
    # TODO: Mettre à jour le compteur du nombre de proies.
            incrementer_nb_proies(grille)

    
    # TODO: Placer les prédateurs dans la grille.
    # Utilisez MAX_AGE_PRED pour générer un âge aléatoire entre 0 et l'âge maximum du prédateur.
    # Utilisez NB_JRS_GESTATION_PRED et NB_JRS_PUBERTE_PRED pour déterminer la période de gestation si le prédateur est en âge de procréer.
    # Utilisez AJOUT_ENERGIE pour initialiser la quantité d'énergie du prédateur.
    for w in range(int(nb_preateur_a_placer)):
        case_aleatoire_2 = random.choice(positions_possibles)
        positions_possibles.pop(positions_possibles.index(case_aleatoire_2))
        age_2 = random.randint(0, MAX_AGE_PRED)
        if age_2 > NB_JRS_PUBERTE_PRED:
            nb_jours_gestation_2 = generer_entier(0, NB_JRS_GESTATION_PRED)
            case = creer_case(Contenu.PREDATEUR, creer_animal(age_2, nb_jours_gestation_2, MIN_ENERGIE, True))
            definir_case(grille, case, case_aleatoire_2[0], case_aleatoire_2[1])  
    # TODO: Mettre à jour le compteur du nombre de prédateurs.
            incrementer_nb_predateurs(grille)
    pass




def generer_entier(min_val, max_val):
    random_number = random.randint(min_val, max_val + 1)
    return random_number

