"""
Auteur : Mathieu Cazenave
Date : 2022-2023
Objet : projet réalisé dans le cadre du MOOC "Apprendre à coder avec Python" :
petit jeu du type jeu d’évasion (escape game) dans lequel le joueur commande au clavier
les déplacements d’un personnage au sein d’un labyrinthe représenté en plan.
Thème : Grizzy et les Lemmings
"""

from CONFIGS import *
from turtle import *
from pygame import mixer  # module pour charger la musique mp3
import time

turtle2 = (
    Turtle()
)  # création d'une 2ème tortue pour affichage des annonces et de l'inventaire

setup(750, 700)  # Largeur et hauteur de la fenêtre en px


def texte_intro():
    hideturtle()
    title("Grizzy et les Lemmings")  # titre de la fenêtre
    bgpic(fond_intro)
    mixer.init()
    mixer.music.load(son_intro)  # lecture du fichier mp3
    mixer.music.play(2)  # musite répétée 2 fois
    color("white")
    up()
    goto(-150, 150)
    write("Grizzy, les Lemmings et un poisson...", font=("Comic sans ms", 16, "bold"))
    time.sleep(1)
    goto(-325, 100)
    write(
        "Grizzy est à la pêche. Super, ça mord! Il sort un énorme poisson de l'eau.",
        font=("Comic sans ms", 11, "bold"),
    )
    goto(-325, 80)
    write(
        "Il se lèche les babines à l'idée de le manger avec du Nutella tartiné dessus.",
        font=("Comic sans ms", 11, "bold"),
    )
    goto(-325, 60)
    write(
        "Il se précipite au coeur de la forêt pour inviter sa copine à manger.",
        font=("Comic sans ms", 11, "bold"),
    )
    goto(-325, 40)
    write(
        "Les Lemmings cachés en colonne derrière un arbre, en profitent pour lui voler son poisson",
        font=("Comic sans ms", 11, "bold"),
    )
    goto(-325, 20)
    write(
        "et le cacher dans un labyrinthe magique.", font=("Comic sans ms", 11, "bold")
    )
    goto(-325, 0)
    write(
        "A son retour, Grizzy est horrifié quand il découvre que le poisson a disparu.",
        font=("Comic sans ms", 11, "bold"),
    )
    goto(-325, -40)
    write(
        "Tout à coup, il aperçoit les Lemmings sortir en courant et en ricanant du labyrinthe magique.",
        font=("Comic sans ms", 11, "bold"),
    )
    goto(-325, -60)
    write(
        "Grizzy les poursuit. Il court, il court.. Fatigué, il s'arrêté et s'appuie contre un rocher.",
        font=("Comic sans ms", 11, "bold"),
    )
    goto(-325, -80)
    write(
        "Une grotte s'ouvre! Il rentre et trouve un parchemin magique : le plan du labyrinthe!.",
        font=("Comic sans ms", 11, "bold"),
    )
    goto(-325, -100)
    write(
        "Aide Grizzy à retouver son poisson à l'aide de ce plan.",
        font=("Comic sans ms", 11, "bold"),
    )
    goto(100, -140)
    color("green")
    write("Cliquer ici", font=("Comic sans ms", 15, "bold"))
    goto(20, -170)
    write("pour commencer l'aventure!", font=("Comic sans ms", 15, "bold"))
    onscreenclick(demarrer_jeu)


def lire_matrice(fichier_encodage):
    with open(fichier_encodage, encoding="utf-8") as fichier_in:
        return [[int(colonne) for colonne in ligne.split()] for ligne in fichier_in]


def calculer_pas(
    matrice,
):  # calcul de la longueur d'une case en px selon taille de la matrice(plan)
    hauteur_matrice = len(matrice)
    largeur_matrice = len(matrice[0])
    largeur_plan = ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0]
    hauteur_plan = ZONE_PLAN_MAXI[1] - ZONE_PLAN_MINI[1]
    if (largeur_plan // largeur_matrice) < (hauteur_plan // hauteur_matrice):
        return largeur_plan // largeur_matrice
    else:
        return hauteur_plan // hauteur_matrice


def coordonnes(
    case, pas
):  # calcul des coordonnées x,y à partir des couples de la matrice (case du plan)
    x1 = ZONE_PLAN_MINI[0]
    y1 = ZONE_PLAN_MINI[1]
    x = case[1] * pas + x1
    y = (len(matrice) - case[0]) * pas + y1
    return x, y


def tracer_carre(dimension):  # fonction1 pour dessiner le plan
    speed(0)
    begin_fill()
    for cote in range(4):
        forward(dimension)
        left(90)
    end_fill()


def tracer_case(case, couleur, pas):  # fonction2 pour dessiner le plan
    speed("fastest")
    tracer(0)
    up()
    goto(coordonnes(case, pas))
    down()
    color(couleur, couleur)
    tracer_carre(pas)


def afficher_plan(
    matrice,
):  # fonction3 (principale) pour dessiner le plan selon les paramètres (CONFIGS.py)
    hideturtle()
    for ligne in range(len(matrice)):
        for colonne in range(len(matrice[ligne])):
            c = matrice[ligne][colonne]
            if c == 0:
                c = COULEUR_CASES
            elif c == 1:
                c = COULEUR_MUR
            elif c == 2:
                c = COULEUR_OBJECTIF
            elif c == 3:
                c = COULEUR_PORTE
            elif c == 4:
                c = COULEUR_OBJET
            tracer_case((ligne, colonne), c, pas)


def creer_dictionnaire_des_objets(fichier_des_objets):  # objets = indices ici
    dico_objets = {}
    for m in open(fichier_des_objets, encoding="utf-8"):
        dico_objets.setdefault(
            eval(m)[0], eval(m)[1]
        )  # la fonction eval accepte la chaîne de caractère m et retourne un objet
    return dico_objets


def creer_dictionnaire_des_portes(
    fichier_des_portes,
):  # fichier questions/réponses pour ouvrir les portes
    dico_portes = {}
    for m in open(fichier_des_portes, encoding="utf-8"):
        dico_portes.setdefault(eval(m)[0], eval(m)[1])
    return dico_portes


# les 4 fonctions suivantes activent la fonction correspondant à la couleur de la case (voir valeur matrice dans configs)
def deplacer_gauche():  # touche Left du clavier
    global matrice, position
    onkeypress(None, "Left")  # Désactive la touche Left
    onkeypress(
        deplacer_gauche, "Left"
    )  # Réassocie la touche Left à la fonction deplacer_gauche
    if position[1] > 0:
        if matrice[position[0]][position[1] - 1] == 0:
            mouvement = (position[0], position[1] - 1)
            deplacer(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0]][position[1] - 1] == 3:
            mouvement = (position[0], position[1] - 1)
            poser_question(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0]][position[1] - 1] == 2:
            mouvement = (position[0], position[1] - 1)
            poser_question_finale(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0]][position[1] - 1] == 4:
            mouvement = (position[0], position[1] - 1)
            ramasser_objet(matrice, position, mouvement)
            position = mouvement


def deplacer_droite():  # touche Right du clavier
    global matrice, position
    onkeypress(
        None, "Right"
    )  # traitement associé à la flèche droite appuyée par le joueur
    onkeypress(deplacer_droite, "Right")
    if position[1] < len(matrice[0]) - 1:
        if matrice[position[0]][position[1] + 1] == 0:
            mouvement = (position[0], position[1] + 1)
            deplacer(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0]][position[1] + 1] == 3:
            mouvement = (position[0], position[1] + 1)
            poser_question(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0]][position[1] + 1] == 2:
            mouvement = (position[0], position[1] + 1)
            poser_question_finale(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0]][position[1] + 1] == 4:
            mouvement = (position[0], position[1] + 1)
            ramasser_objet(matrice, position, mouvement)
            position = mouvement


def deplacer_haut():  # touche Up du clavier
    global matrice, position
    onkeypress(None, "Up")  # traitement associé à la flèche haut appuyée par le joueur
    onkeypress(deplacer_haut, "Up")
    if position[0] > 0:
        if matrice[position[0] - 1][position[1]] == 0:
            mouvement = (position[0] - 1, position[1])
            deplacer(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0] - 1][position[1]] == 3:
            mouvement = (position[0] - 1, position[1])
            poser_question(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0] - 1][position[1]] == 2:
            mouvement = (position[0] - 1, position[1])
            poser_question_finale(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0] - 1][position[1]] == 4:
            mouvement = (position[0] - 1, position[1])
            ramasser_objet(matrice, position, mouvement)
            position = mouvement


def deplacer_bas():  # touche Down du clavier
    global matrice, position
    onkeypress(None, "Down")  # traitement associé à la flèche bas appuyée par le joueur
    onkeypress(deplacer_bas, "Down")
    if position[0] < len(matrice) - 1:
        if matrice[position[0] + 1][position[1]] == 0:
            mouvement = (position[0] + 1, position[1])
            deplacer(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0] + 1][position[1]] == 3:
            mouvement = (position[0] + 1, position[1])
            poser_question(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0] + 1][position[1]] == 2:
            mouvement = (position[0] + 1, position[1])
            poser_question_finale(matrice, position, mouvement)
            position = mouvement
        elif matrice[position[0] + 1][position[1]] == 4:
            mouvement = (position[0] + 1, position[1])
            ramasser_objet(matrice, position, mouvement)
            position = mouvement


def deplacer(
    matrice, position, mouvement
):  # déplacement dans les couloirs (cases vides blanches)
    speed(4)
    tracer_case(position, "white", pas)
    up()
    x, y = coordonnes(mouvement, pas)
    goto(x + RATIO_PERSONNAGE * pas, y + RATIO_PERSONNAGE * pas)
    dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)


def ramasser_objet(matrice, position, mouvement):  # case verte (indices)
    x_a = POINT_AFFICHAGE_ANNONCES[0] + 25
    y_a = POINT_AFFICHAGE_ANNONCES[1] + 10
    tracer_case(position, "white", pas)
    tracer_case(mouvement, "white", pas)
    up()
    x, y = coordonnes(mouvement, pas)
    goto(x + RATIO_PERSONNAGE * pas, y + RATIO_PERSONNAGE * pas)
    dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
    matrice[mouvement[0]][mouvement[1]] = 0
    turtle2.up()
    turtle2.goto(x_a, y_a)
    turtle2.down()
    turtle2.color("black")
    objets = creer_dictionnaire_des_objets(fichier_indices)
    indice = objets[mouvement]
    turtle2.color("green")
    turtle2.write(
        "Bravo! Tu as trouvé un indice : " + indice,
        font=("Comic sans ms", 14, "normal"),
    )
    onkeypress(None, "Left")  # désactivation des flèches pour éviter les "bugs"
    onkeypress(None, "Right")
    onkeypress(None, "Up")
    onkeypress(None, "Down")
    update()
    time.sleep(2)
    turtle2.undo()
    maj_inventaire(indice, mouvement)
    onkeypress(deplacer_gauche, "Left")
    onkeypress(deplacer_droite, "Right")
    onkeypress(deplacer_haut, "Up")
    onkeypress(deplacer_bas, "Down")


def maj_inventaire(
    indice, mouvement
):  # pour chaque indice ramassé, l'inventaire est mis à jour et réécrit en bas à droite
    x = POINT_AFFICHAGE_INVENTAIRE[0] + 50
    y = POINT_AFFICHAGE_INVENTAIRE[1] - 435
    turtle2.up()
    turtle2.goto(x, y)
    turtle2.color("white")
    turtle2.write("INDICES : ", font=("Comic sans ms", 14, "bold"))
    inventaire.append(indice)
    turtle2.up()
    for indice in inventaire:
        turtle2.goto(x, y - 20)
        turtle2.color("white")
        turtle2.write(str(indice), font=("Comic sans ms", 12, "bold"))
        y -= 20


def poser_question(matrice, position, mouvement):  # cases oranges (portes)
    x_a = POINT_AFFICHAGE_ANNONCES[0] + 25
    y_a = POINT_AFFICHAGE_ANNONCES[1] + 10
    turtle2.up()
    turtle2.goto(x_a, y_a)
    turtle2.color("red")
    turtle2.write("Cette porte est fermée.", font=("Comic sans ms", 15, "normal"))
    update()
    time.sleep(2)
    turtle2.undo()
    portes = creer_dictionnaire_des_portes(fichier_questions)
    question = portes[mouvement][0]
    
    while True:
        reponse = textinput("Question-clé", question)
        if reponse != portes[mouvement][1]:
            turtle2.color("red")
            turtle2.write(
                "Mauvaise réponse. La porte reste fermée!",
                font=("Comic sans ms", 15, "bold"),
            )
            update()
            time.sleep(2)
            turtle2.undo()
        elif reponse == portes[mouvement][1]:
            turtle2.color("green")
            turtle2.write(
                "Bravo! La porte est ouverte!", font=("Comic sans ms", 15, "bold")
            )
            update()
            time.sleep(1)
            turtle2.undo()
            return ouverture_porte(matrice, position, mouvement)


def ouverture_porte(
    matrice, position, mouvement
):  # en cas de bonne réponse, la porte s'ouvre ainsi
    tracer_case(position, "white", pas)
    tracer_case(mouvement, "white", pas)
    up()
    x, y = coordonnes(mouvement, pas)
    goto(x + RATIO_PERSONNAGE * pas, y + RATIO_PERSONNAGE * pas)
    dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
    matrice[mouvement[0]][mouvement[1]] = 0
    listen()


def poser_question_finale(
    matrice, position, mouvement
):  # case jaune (sortie/objectif : le poisson!)
    x_a = POINT_AFFICHAGE_ANNONCES[0] - 40
    y_a = POINT_AFFICHAGE_ANNONCES[1] + 45
    turtle2.up()
    turtle2.goto(x_a, y_a)
    turtle2.down()
    turtle2.color("red")
    turtle2.write(
        "Ca sent le poisson derrière cette porte...!",
        font=("Comic sans ms", 15, "normal"),
    )
    update()
    time.sleep(3)
    turtle2.undo()
    portes = creer_dictionnaire_des_objets(fichier_questions)
    question = portes[mouvement][0]
    while True:
        reponse = textinput("Question finale!", question)
        if (
            reponse == portes[mouvement][1] or reponse == portes[mouvement][2]
        ):  # 2ème réponse avec majuscule
            return the_end()
        elif (
            reponse == portes[mouvement][3] or reponse == portes[mouvement][4]
        ):  # 2 réponses avec erreur "classique" d'orthographe
            turtle2.write(
                "Es-tu sûr que ça s'écrit comme ça?", font=("Comic sans ms", 16, "bold")
            )
            update()
            time.sleep(2)
            turtle2.undo()
        else:
            turtle2.write(
                "Réfléchie encore... Grizzy veut manger avec son amie!",
                font=("Comic sans ms", 16, "bold"),
            )
            update()
            time.sleep(2)
            turtle2.undo()


def demarrer_jeu(
    a, b
):  # 2ème fenêtre après l'intro : le jeu lui-même (affichage nouveau fond, plan, indication pour le joueur...)
    clearscreen()
    title("Aide Grizzy à retrouver son poisson")  # titre de la fenêtre
    bgpic(fond_jeu)
    mixer.music.load(son_intro)
    mixer.music.stop
    reset()
    afficher_plan(matrice)
    turtle2 = Turtle()
    turtle2.hideturtle()
    x_a = POINT_AFFICHAGE_ANNONCES[0] - 40
    y_a = POINT_AFFICHAGE_ANNONCES[1] + 45
    turtle2.up()
    turtle2.color("green")
    turtle2.goto(x_a, y_a)
    turtle2.write(
        "Déplace Grizzy avec les flèches de ton clavier.",
        font=("Comic sans ms", 15, "normal"),
    )
    update()
    time.sleep(3)
    turtle2.undo()
    up()
    x, y = coordonnes(position, pas)
    goto(x + RATIO_PERSONNAGE * pas, y + RATIO_PERSONNAGE * pas)
    dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
    up()
    jouer()


def jouer():  # musique d'ambiance, associations des flèches du clavier aux fonctions déplacer_...
    mixer.init()
    mixer.music.load(son_jeu)  # ouvre le fichier mp3
    mixer.music.play(2)  # musite répétée 2 fois
    listen()  # Déclenche l’écoute du clavier
    onkeypress(
        deplacer_gauche, "Left"
    )  # Associe à la touche Left une fonction appelée deplacer_gauche
    onkeypress(
        deplacer_droite, "Right"
    )  # Associe à la touche Left une fonction appelée deplacer_droite
    onkeypress(
        deplacer_haut, "Up"
    )  # Associe à la touche Left une fonction appelée deplacer_haut
    onkeypress(
        deplacer_bas, "Down"
    )  # Associe à la touche Left une fonction appelée deplacer_bas
    mainloop()  # Place le programme en position d’attente d’une action du joueur


def the_end():  # phrase de félicitations puis nouvelle fenêtre de Fin
    turtle2.color("green")
    turtle2.write(
        "FELICITATIONS! Grizzy va enfin pouvoir manger!",
        font=("comic sans ms", 16, "bold"),
    )
    update()
    time.sleep(3)
    turtle2.undo()
    clearscreen()
    up()
    hideturtle()
    title("Grizzy et les Lemmings")  # nouveau titre de la fenêtre
    bgpic(fond_FIN)
    goto(-30, -150)
    color("grey")
    write("Fin", font=("comic sans ms", 30, "bold"))
    mixer.music.load(son_jeu)  # arrête la musique du jeu
    mixer.music.stop


# variables constantes
matrice = lire_matrice(fichier_plan)
pas = calculer_pas(matrice)


# lancement du jeu
texte_intro()
position = (0, 1)  # entrée du château
mainloop()
