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

    nb_case_voisine, lig_voisin, col_voisin = choix_voisin_autour(grille, ligne, col, Contenu.VIDE)
    #changer la case voisine par les propriete(etat, animal) de ancienne case
    
    etat = obtenir_etat(grille, ligne, col)
    definir_etat(grille, etat, lig_voisin, col_voisin)
    definir_animal(grille, animal, lig_voisin, col_voisin)
    definir_disponibilite(animal, False)
    vider_case(grille, ligne, col)
    #vider ancienne case
    vider_case(grille, ligne, col)

    pass


def executer_cycle_proie(grille, ligne, col, animal):
    # TODO: Gérer le cycle de vie d'une proie à une position donnée sur la grille.
    # 1. Vieillir l'animal. Si l'âge dépasse MAX_AGE_PROIE, le retirer de la grille et décrémenter le compteur de proies.
    incrementer_age(animal, NB_JRS_PUBERTE_PROIE)
    if obtenir_age(animal) > MAX_AGE_PROIE:
        vider_case(grille, ligne, col)
        decrementer_nb_proies(grille)
    # 2. Si l'animal est en âge de se reproduire et a attendu suffisamment (NB_JRS_GESTATION_PROIE), tenter de générer un nouveau bébé proie.
    #    Pour ce faire, chercher un voisin vide autour de la proie. Si un voisin est trouvé, créer un bébé proie et le placer dans la grille.
    elif obtenir_age(animal) >= NB_JRS_PUBERTE_PROIE and obtenir_jours_gestation(animal) >= NB_JRS_GESTATION_PROIE:
        nb_voisin_dispo, lig_voisin, col_voisin = choix_voisin_autour(grille, ligne, col, Contenu.VIDE)
        if nb_voisin_dispo > 0 and check_nb_proies(grille, NB_MAX_PROIES):
            nouv_proie = creer_case(Contenu.PROIE, creer_animal())
            definir_case(grille, nouv_proie, lig_voisin, col_voisin)
            incrementer_nb_proies(grille)
            definir_jours_gestation(animal, 0)
    # 3. Sinon, déplacer l'animal vers une case vide à proximité.
    else:
        nb_voisin_dispo, lig_voisin, col_voisin = choix_voisin_autour(grille, ligne, col, Contenu.VIDE)
        if nb_voisin_dispo > 0:
            case = obtenir_case(grille, ligne, col)
            definir_case(grille, case, lig_voisin, col_voisin)
            vider_case(grille, ligne, col)
        else: 
            pass


def executer_cycle_predateur(grille, ligne, col, animal):
    incrementer_age(animal, NB_JRS_PUBERTE_PRED)
    if obtenir_energie(animal) < MIN_SANTE_PRED or obtenir_age(animal) > MAX_AGE_PRED:
        vider_case(grille, ligne, col)
        decrementer_nb_predateurs(grille)

    nb_proie_a_manger, lig_proie, col_proie = choix_voisin_autour(grille, ligne, col, Contenu.PROIE)
    if nb_proie_a_manger > 0:
        definir_disponibilite(animal, False)
        ajouter_energie(animal, AJOUT_ENERGIE)
        case_pred = obtenir_case(grille, ligne, col)
        definir_case(grille, case_pred, lig_proie, col_proie)
        vider_case(grille, ligne, col)
        decrementer_nb_proies(grille)
        if obtenir_age(animal) >= NB_JRS_PUBERTE_PRED and obtenir_jours_gestation(animal) >= NB_JRS_GESTATION_PRED:
            definir_jours_gestation(animal, 0)
            nb_case_vide_proche, lig_voisin, col_voisin = choix_voisin_autour(grille, lig_proie, col_proie, Contenu.VIDE)
            if nb_case_vide_proche > 0:
                nouv_pred = creer_case(Contenu.PREDATEUR, creer_animal())
                definir_case(grille, nouv_pred, lig_voisin, col_voisin)
                incrementer_nb_predateurs(grille)
    # 3. Sinon, déplacer l'animal vers une case vide à proximité et décrémenter son énergie de 1.
    else:
        ajouter_energie(animal, -1)
        nb_voisins, lig_voisin, col_voisin = choix_voisin_autour(grille, ligne, col, Contenu.VIDE)
        if  nb_voisins > 0:
            case = obtenir_case(grille, ligne, col)
            definir_case(grille, case, lig_voisin, col_voisin)
            vider_case(grille, ligne, col)
        else:
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
                if obtenir_disponibilite(animal) is True:
                    if obtenir_etat(grille, ligne, col) == Contenu.PROIE:
                        executer_cycle_proie(grille, ligne, col, obtenir_animal(grille, ligne, col))
                    elif obtenir_etat(grille, ligne, col) == Contenu.PREDATEUR:
                        executer_cycle_predateur(grille, ligne, col, obtenir_animal(grille, ligne, col))
                    else: 
                        pass

