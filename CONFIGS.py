ZONE_PLAN_MINI = (-240, -240)  # Coin inférieur gauche de la zone d'affichage du plan
ZONE_PLAN_MAXI = (50, 200)  # Coin supérieur droit de la zone d'affichage du plan
POINT_AFFICHAGE_ANNONCES = (-240, 240)  # Point d'origine de l'affichage des annonces
POINT_AFFICHAGE_INVENTAIRE = (70, 210)  # Point d'origine de l'affichage de l'inventaire



""" Matrice :
valeur 0 pour une case vide,
valeur 1 pour un mur (infranchissable),
valeur 2 pour la case de sortie/victoire,
valeur 3 pour une porte qui sera franchissable en répondant à une question,
valeur 4 pour une case contenant un objet à collecter.
"""
# Les valeurs ci-dessous définissent les couleurs des cases du plan
COULEUR_CASES = 'white'
COULEUR_MUR = 'grey'
COULEUR_OBJECTIF = 'yellow'
COULEUR_PORTE = 'orange'
COULEUR_OBJET = 'green'


# Couleur et dimension du personnage
COULEUR_PERSONNAGE = 'brown'
RATIO_PERSONNAGE = 0.6  # Rapport entre diamètre du personnage et dimension des cases


# Désignation des fichiers de données à utiliser
son_intro = 'grizzy_intro.mp3'
son_jeu = 'grizzy_jouer.mp3'
fond_intro = "Grizzy.png"
fond_jeu = "fond1.png"
fond_FIN = "poisson.png"
fichier_plan = 'plan_chateau.txt'
fichier_questions = 'dico_portes.txt'
fichier_indices = 'dico_objets.txt'

#initialisation de l'inventaire affiché en bas à droite de la fenêtre
inventaire = []
