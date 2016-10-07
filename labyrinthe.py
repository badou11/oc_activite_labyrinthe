# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

import os
import pickle

from obstacle.mur import Mur
from obstacle.porte import Porte
from obstacle.sortie import Sortie
from robot import Robot

# Constantes
FICHIER_ENREGISTREMENT = "partie"

class Labyrinthe:

    """Classe rep'résentant un labyrinthe.

    Yn labyrinthe est une grille comprenant des murs placés à endroits fixes
    ainsi qu'un robot. D'autres types d'obstacles pourraient également s'y
    rencontrer.

    Paramètres à préciser à la construction :
        robot -- le robot
        obstacles -- une liste des obstacles déjà positionnés

    Pour créer un labyrinthe à partir d'une chaîne (par exemple à partir
    d'un fichier), considérez la fonction 'creer_labyrinthe_depuis_chaine'
    définie au-dessous de la classe.

    """

    limite_x = 20
    limite_y = 20
    def __init__(self, robot, obstacles):
        self.robot = robot
        self.grille = {}
        self.grille[robot.x, robot.y] = robot
        self.invisibles = []
        self.gagnee = False
        for obstacle in obstacles:
            if (obstacle.x, obstacle.y) in self.grille:
                raise ValueError("les coordonnées x={} y={} sont déjà " \
                        "utilisées dans cette grille".format(obstacle.x,
                        obstacle.y))

            if obstacle.x > self.limite_x or obstacle.y > self.limite_y:
                raise ValueError("l'obstacle {} a des coordonnées trop " \
                        "grandes".format(obstacle))

            self.grille[obstacle.x, obstacle.y] = obstacle

    def afficher(self):
        """Affiche le labyrinthe dans une console.

        On prend les limites pour afficher la grille. Les obstacles et
        le robot sont affichés en utilisant leur attribut de classe 'symbole'.

        """
        y = 0
        grille = ""

        while y < self.limite_y:
            x = 0
            while x < self.limite_x:
                case = self.grille.get((x, y))
                if case:
                    grille += case.symbole
                else:
                    grille += " "

                x += 1

            grille += "\n"
            y += 1

        print(grille, end="")

    def actualiser_invisibles(self):
        """Cette méthode actualise les obstacles invisibles.

        Si le robot passe sur un obstacle passable (disons une porte),
        l'obstacle ne s'affiche pas. En fait, il est supprimé de la grille,
        mais placé dans les obstacles invisibles et sera de nouveau
        afficher quand le robot se sera de nouveau déplacé.

        """
        for obstacle in list(self.invisibles):
            if (obstacle.x, obstacle.y) not in self.grille:
                self.grille[obstacle.x, obstacle.y] = obstacle
                self.invisibles.remove(obstacle)

    def deplacer_robot(self, direction, nombre):
        """Déplace le robot.

        La direction est à préciser sous la forme de chaîne, "nord",
        "est", "sud", ou "ouest". Le nombre précise le nombre de cases
        de déplacement.

        Si le robot rencontre un obstacle impassable, il s'arrête.

        """
        robot = self.robot
        coords = [robot.x, robot.y]
        if direction == "nord":
            coords[1] -= 1
        elif direction == "est":
            coords[0] += 1
        elif direction == "sud":
            coords[1] += 1
        elif direction == "ouest":
            coords[0] -= 1
        else:
            raise ValueError("direction {} inconnue".format(direction))

        x, y = coords
        if x >= 0 and x < self.limite_x and y >= 0 and y < self.limite_y:
            # On essaye de déplacer le robot
            # On vérifie qu'il n'y a pas d'obstacle à cet endroit
            obstacle = self.grille.get((x, y))
            if obstacle is None or obstacle.peut_traverser:
                if obstacle:
                    self.invisibles.append(obstacle)

                # On supprime l'ancienne position du robot
                del self.grille[robot.x, robot.y]

                # On place le robot au nouvel endroit
                self.grille[x, y] = robot
                robot.x = x
                robot.y = y
                self.actualiser_invisibles()
                self.afficher()

                # On appelle la méthode 'arriver' de l'obstacle, si il existe
                if obstacle:
                    obstacle.arriver(self, robot)

                # On enregistre la partie
                self.enregistrer()

        # Si il y a plus d'un déplacement, rappelle la méthode
        if not self.gagnee and nombre > 1:
            self.deplacer_robot(direction, nombre - 1)

    # Méthodes d'enregistrement
    def enregistrer(self):
        """Enregistre la partie en cours."""
        with open(FICHIER_ENREGISTREMENT, "wb") as fichier:
            pic = pickle.Pickler(fichier)
            pic.dump(self)

    def detruire(self):
        """Destruction du fichier de partie en cours."""
        if os.path.exists(FICHIER_ENREGISTREMENT):
            os.remove(FICHIER_ENREGISTREMENT)


def creer_labyrinthe_depuis_chaine(chaine):
    """Crée un labyrinthe depuis une chaîne.

    Les symboles sont définis par correspondance ici.

    """
    symboles = {
        "o": Mur,
        "x": Robot,
        ".": Porte,
        "u": Sortie,
    }

    x = 0
    y = 0
    robot = None
    obstacles = []
    for lettre in chaine:
        if lettre == "\n":
            x = 0
            y += 1
            continue
        elif lettre == " ":
            pass
        elif lettre.lower() in symboles:
            classe = symboles[lettre.lower()]
            objet = classe(x, y)
            if type(objet) is Robot:
                if robot:
                    raise ValueError("il ne peut y avoir qu'un robot")

                robot = objet
            else:
                obstacles.append(objet)
        else:
            raise ValueError("symbole inconnu {}".format(lettre))

        x += 1

    labyrinthe = Labyrinthe(robot, obstacles)
    return labyrinthe

def charger_labyrinthe():
    """Charge le labyrinthe si le fichier d'enregistrement est trouvé.

    Si le fichier n'existe pas, retourne None.

    """
    if os.path.exists(FICHIER_ENREGISTREMENT):
        with open(FICHIER_ENREGISTREMENT, "rb") as fichier:
            unpic = pickle.Unpickler(fichier)
            return unpic.load()

    return None
