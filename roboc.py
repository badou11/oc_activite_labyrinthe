# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

"""

import os

from carte import Carte
from labyrinthe import charger_labyrinthe

# On charge les cartes existantes
cartes = []
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier)
        nom_carte = nom_fichier[:-3].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
            try:
                carte = Carte(nom_carte, contenu)
            except ValueError as err:
                print("Erreur lors de la lecture de {} : {}.".format(
                        chemin, str(err)))
            else:
                cartes.append(carte)

# On affiche les cartes existantes
print("Labyrinthes existants :")
for i, carte in enumerate(cartes):
    print("  {} - {}".format(i + 1, carte.nom))

# Si il y a une partie sauvegardée
partie = charger_labyrinthe()
if partie:
    print("  R pour rejouer la partie sauvegardée")

# Choix de la carte
labyrinthe = None
while labyrinthe is None:
    choix = input("Entrez un numéro de labyrinthe pour commencer à jouer : ")
    if choix.lower() == "r":
        if partie:
            labyrinthe = partie
        else:
            print("Il n'y a aucune partie enregistrée pour l'heure.")
    else:
        # Si le joueur n'a pas entré R, on s'attend à un nombre
        try:
            choix = int(choix)
        except ValueError:
            print("Choix invalide : {}".format(choix))
        else:
            if choix < 1 or choix > len(cartes):
                print("Numéro invalide : ".format(choix))
                continue

            carte = cartes[choix - 1]
            labyrinthe = carte.labyrinthe

# Maintenant, affiche la carte et permet de jouer à chaque tour
labyrinthe.afficher()
while not labyrinthe.gagnee:
    coup = input("> ")
    if coup == "":
        continue
    elif coup.lower() == "q":
        # On quitte la partie
        break
    elif coup[0].lower() in "nseo":
        lettre = coup[0].lower()
        if lettre == "e":
            direction = "est"
        elif lettre == "s":
            direction = "sud"
        elif lettre == "o":
            direction = "ouest"
        else: # On sait que c'est n
            direction = "nord"

        # On va essayer de convertir le déplacement
        coup = coup[1:]
        if coup == "":
            nombre = 1
        else:
            try:
                nombre = int(coup)
            except ValueError:
                print("Nombre invalide : {}".format(coup))
                continue

        labyrinthe.deplacer_robot(direction, nombre)
    else:
        print("Coups autorisés :")
        print("  Q pour sauvegarder et quitter la partie en cours")
        print("  E pour déplacer le robot vers l'est")
        print("  S pour déplacer le robot vers le sud")
        print("  O pour déplacer le robot vers l'ouest")
        print("  N pour déplacer le robot vers le nord")
        print("  Vous pouvez préciser un nombre après la direction")
        print("  Pour déplacer votre robot plus vite. Exemple n3")

if labyrinthe.gagnee:
    print("Félicitation ! Vous aez gagné !")
    labyrinthe.detruire()
else:
    print("Votre partie a été sauvegardée.")
