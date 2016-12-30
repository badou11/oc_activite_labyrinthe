import socket
import pickle

hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connection():
    """connection au serveur"""

    connexion_avec_serveur.connect((hote, port))
    print("Connexion établie avec le serveur sur le port {}".format(port))

def phase_jeu():
    """Phase de jeu
    (gere la communication avec le serveur et les actions en decoulant)
    """

    fin_du_jeu = False
    while not fin_du_jeu:
        # on attend un message du serveur
        message = attendre_message_serveur()

        if message['action'] == 'attente':
            print('Le serveur ce prepare, veuillez patienter')
        elif message['action'] == 'attente_joueur':
            print('Attente de l\'autre joueur, veuillez patienter')
        elif message['action'] == 'commence':
            pret = 'non'
            while not (pret[0].lower() == 'c'):
                print('Tape c pour commencer')
                pret = input("> ")

            #envoie tu message pret au serveur
            connexion_avec_serveur.send("joueur_pret".encode())
        elif message['action'] == 'ton_tour':

            # on montre la carte present dans message['carte']
            print(message['carte'], end="")

            (action, direction, deplacement) = choix_mouvement()

            # on creer un dictionnaire pour envoyer les donnees en une fois
            mouvement = dict()
            mouvement['action'] = action
            mouvement['direction'] = direction
            mouvement['deplacement'] = deplacement

            # on formate le dictionnaire pour l'envoie
            data_string = pickle.dumps(mouvement)

            # envoie de l'action au serveur
            connexion_avec_serveur.send(data_string)

        elif message['action'] == 'carte':
            # on montre la carte present dans message['carte']
            print(message['carte'], end="")



def attendre_message_serveur():
    """boucle pour attendre un message du server"""

    dictionnaire_recu = connexion_avec_serveur.recv(4000)
    dictionnaire_decode = pickle.loads(dictionnaire_recu)
    return dictionnaire_decode


def quitter_partie():
    """Function qui envoie le message 'quite' au server
    C'est au serveur de faire quitter tout les utilisateurs dans ce cas
    """

    # Envoie du message depart
    connexion_avec_serveur.send("joueur_quitte".encode())
    return


def choix_mouvement():
    """boucle pur attendre un message du server"""

    coup_correct = False
    resulat_a_envoyer = ('', '', '')

    while not coup_correct:
        # Initialisation des movements de l'utilisateur
        action = ''
        direction = ''
        possible_deplacement = 1
        deplacement = 1

        coup = input("> ")
        if coup == "":
            continue
        elif coup.lower() == "q":
            # On quitte la partie
            quitter_partie()
            coup_correct = True
            break
        elif coup[0].lower() in "mp":
            action = coup[0].lower()

            # On verifie si l'on a bien une direction apres
            if( not (coup[1].lower() in "nseo")):
                print("Tu doit choisir une direction")
                continue
            else :
                direction = coup[1].lower()
                coup_correct = True

        elif coup[0].lower() in "nseo":
            direction = coup[0].lower()
            possible_deplacement = coup[1:]
            coup_correct = True

        else:
            print("Coups autorisés :")
            print("  Q pour quitter la partie en cours")
            print("  E pour déplacer le robot vers l'est")
            print("  S pour déplacer le robot vers le sud")
            print("  O pour déplacer le robot vers l'ouest")
            print("  N pour déplacer le robot vers le nord")
            print("  Vous pouvez préciser un nombre après la direction")
            print("  Pour déplacer votre robot plus vite. Exemple 'n3'")
            print("  Vous pouvez aussez préciser une action la direction")
            print("  L'action peut etre de murer une porte 'p', ou de percer un mur 'm'")
            print("  Exemple : 'mn' mur une porte au nord, 'pe' perce un mur a l'est")



        # On va essayer de convertir le déplacement (si present)
        if possible_deplacement == "":
            deplacement = 1
        else:
            try:
                deplacement = int(possible_deplacement)
            except ValueError:
                print("Nombre invalide : {}".format(possible_deplacement))
                coup_correct = False

        # on rentre les valeurs trouver dans un tuple a remvoyer
        resultat_a_envoyer = (action, direction, deplacement)


    # finalement, si ont a fini la boucle
    # cela veut dire que l'on a un movement correct (ou que l'on a quiter)
    # on renvoie donc la valeur dans un tuple
    return resultat_a_envoyer




