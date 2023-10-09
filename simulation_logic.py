from enum import Enum
import random

from simulation_constants import *
from animal import *
from grille_animaux import *

def simulation_est_terminee(grille):
    # TODO: Vérifier si la simulation est terminée.
    # Elle se termine lorsque le nombre de proies ou le nombre de prédateurs est égal à zéro.
    # Renvoyer un booléen indiquant l'état de la simulation.

    if grille["nb_proies"] == 0 or grille["nb_predateurs"] == 0:
        return True
    else:
        return False

def rendre_animaux_disponibles(grille):
    # TODO: Parcourir chaque case de la grille et rendre tous les animaux disponibles (Booléen à True) pour la prochaine itération.

    matrice = grille["matrice"]
    for ligne in matrice:
        for col in ligne:
            if col["animal"] != None:
                col["animal"]["disponible"] = True
            else:
                pass
            
            

    pass
	
	
def deplacer_animal(grille, ligne, col, animal):
    # TODO: Trouver un voisin vide où déplacer l'animal, effectuer le déplacement et mettre à jour l'état
    # et la disponibilité de l'animal. Utiliser "choix_voisin_autour", "definit_etat", "definir_animal",
    # "definir_disponibilite" et "vider_case" pour réaliser ces étapes.

    #Trouver un case voisine ou on peut deplacer

    nb_case_voisine, lig_voisin, col_voisin = choix_voisin_autour(grille, ligne, col, Contenu.VIDE)

    #changer la case voisine par les propriete(etat, animal) de ancienne case
    definir_animal(grille, animal, lig_voisin, col_voisin)
    definir_disponibilite(animal, False)

    #vider ancienne case
    vider_case(grille, ligne, col)

    pass


def executer_cycle_proie(grille, ligne, col, animal):
    # TODO: Gérer le cycle de vie d'une proie à une position donnée sur la grille.
    # 1. Vieillir l'animal. Si l'âge dépasse MAX_AGE_PROIE, le retirer de la grille et décrémenter le compteur de proies.
    incrementer_age(animal, NB_JRS_PUBERTE_PROIE)
    if animal["age"] > MAX_AGE_PROIE:
        vider_case(grille, ligne, col)
        decrementer_nb_proies(grille)
    # 2. Si l'animal est en âge de se reproduire et a attendu suffisamment (NB_JRS_GESTATION_PROIE), tenter de générer un nouveau bébé proie.
    #    Pour ce faire, chercher un voisin vide autour de la proie. Si un voisin est trouvé, créer un bébé proie et le placer dans la grille.
    elif animal["age"] >= NB_JRS_PUBERTE_PROIE and animal["jrs_gestation"] >= NB_JRS_GESTATION_PROIE:
        nb_voisin_dispo, lig_voisin, col_voisin = choix_voisin_autour(grille, ligne, col, Contenu.VIDE)
        if nb_voisin_dispo > 0 and check_nb_proies(grille, NB_MAX_PROIES):
            case = creer_case(Contenu.PROIE)
            definir_case(grille, case, lig_voisin, col_voisin)
            incrementer_nb_proies(grille)
        animal["jrs_gestation"] = 0
    # 3. Sinon, déplacer l'animal vers une case vide à proximité.
    else:
        deplacer_animal(grille, ligne, col, animal)
    
    pass


def executer_cycle_predateur(grille, ligne, col, animal):
    # TODO: Gérer le cycle de vie d'un prédateur à une position donnée sur la grille.
    # 1. Vieillir l'animal. Si l'âge dépasse MAX_AGE_PRED ou si le prédateur manque d'énergie (énergie < MIN_ENERGIE), le retirer
    #    de la grille et décrémenter le compteur de prédateurs.

    incrementer_age(animal, NB_JRS_PUBERTE_PRED)
    if animal["energie"] < MIN_SANTE_PRED or animal["age"] > MAX_AGE_PRED:
        vider_case(grille, ligne, col)
        decrementer_nb_predateurs(grille)
    
    # 2. Si le prédateur peut manger une proie dans une case voisine, le faire en le déplaçant dans la case de la proie et en
    #    incrémentant son énergie de AJOUT_ENERGIE (n'oubliez pas de décrémenter le compteur de proies). Après avoir mangé, si le
    #    prédateur est en âge de se reproduire et a attendu suffisamment (NB_JRS_GESTATION_PRED), tenter de générer un nouveau bébé
    #    prédateur. Pour ce faire, chercher un voisin vide autour du prédateur. Si un voisin est trouvé, créer un bébé prédateur et
    #    le placer dans la grille.

    nb_proie_a_manger, lig_proie, col_proie = choix_voisin_autour(grille, ligne, col, Contenu.PROIE)
    nb_voisin_vide, lig_voisin_vide, col_voisin_vide = choix_voisin_autour(grille, ligne, col, Contenu.VIDE)
    if nb_proie_a_manger > 0:
        #rend deplacement impossible apres manger
        animal["disponible"] = False
        #ajouter energie car manger
        ajouter_energie(animal, AJOUT_ENERGIE)
        #change la case proie par pred
        case_pred = creer_case(Contenu.PREDATEUR, animal)
        definir_case(grille, case_pred, lig_proie, col_proie)
        #vide ancienne case pred
        vider_case(grille, ligne, col)
        #decremente nb_proie
        decrementer_nb_proies(grille)
        if animal["age"] >= NB_JRS_PUBERTE_PRED and animal["jrs_gestation"] >= NB_JRS_GESTATION_PRED:
            animal["jrs_gestation"] = 0
            case_pred = creer_case(Contenu.PREDATEUR, animal)
            definir_case(grille, case_pred, lig_proie, col_proie)
            nb_case_vide_proche, lig_voisin, col_voisin = choix_voisin_autour(grille, lig_proie, col_proie, Contenu.VIDE)
            if nb_case_vide_proche > 0:
                nouv_pred = creer_case(Contenu.PREDATEUR)
                definir_case(grille, nouv_pred, lig_voisin, col_voisin)
                incrementer_nb_predateurs(grille)
    # 3. Sinon, déplacer l'animal vers une case vide à proximité et décrémenter son énergie de 1.
    else:
        deplacer_animal(grille, lig_voisin_vide, col_voisin_vide, animal)
        animal["energie"] -= 1
    pass



def executer_cycle(grille):
    # TODO: Marquer tous les animaux comme disponibles pour ce cycle, puis parcourir la grille pour exécuter la bonne procédure
    # du cycle de vie pour chaque animal. Il est nécessaires d'utiliser au minimum les fonctions "rendre_animaux_disponibles",
    # "executer_cycle_proie" et "executer_cycle_predateur".

    rendre_animaux_disponibles(grille)
    nb_lig, nb_col = obtenir_dimensions(grille)

    for ligne in range(0, nb_lig):
        for col in range(0, nb_col):
            if obtenir_etat(grille, ligne, col) != Contenu.VIDE:
                animal = obtenir_animal(grille, ligne, col)
                if animal["disponible"] == True:
                    if obtenir_etat(grille, ligne, col) == Contenu.PROIE:
                        executer_cycle_proie(grille, ligne, col, animal)
                    else:
                        executer_cycle_predateur(grille, ligne, col, animal)

    pass
