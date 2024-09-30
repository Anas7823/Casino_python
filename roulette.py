# Correction
from game_rule import afficher_regles
import random
import time

# Variables globales pour suivre les statistiques
best_level = 1
total_games = 0
total_wins = 0
mise_totale = 0
nb_coups_gagnants = 0

# Fonction pour afficher les règles du jeu
afficher_regles()

# Fonction pour gérer un niveau
def jouer_niveau(level, essais, borne_sup, solde):
    nb_python = random.randint(1, borne_sup)
    print(f"Je viens de penser à un nombre entre 1 et {borne_sup}. Devinez lequel ?")
    print(f"Att : vous avez le droit à {essais} essais !")

    for essai in range(1, essais + 1):
        start_time = time.time()

        try:
            nb_user = int(input("Alors, votre nombre est : "))
        except ValueError:
            print(f"Je ne comprends pas ! Entrez un nombre entre 1 et {borne_sup} : ")
            continue

        elapsed_time = time.time() - start_time
        if elapsed_time > 10:
            print(f"Vous avez dépassé le délai de 10 secondes ! Vous perdez l'essai courant.")
            continue
        
        if nb_user == nb_python:
            print(f"Bingo ! Vous avez deviné mon nombre en {essai} coup(s) !")
            gain = calculer_gain(essai, solde)
            print(f"Vous avez emporté {gain} € !")
            return True, gain
        
        elif nb_user > nb_python:
            print("Votre nombre est trop grand !")
        else:
            print("Votre nombre est trop petit !")

        if essai == essais - 1:
            print("Il vous reste une chance !")
    
    print(f"Vous avez perdu ! Mon nombre était {nb_python} !")
    return False, 0

# Fonction pour calculer les gains
def calculer_gain(essais, mise):
    if essais == 1:
        return mise * 2
    elif essais == 2:
        return mise
    elif essais == 3:
        return mise / 2
    return 0

# Fonction pour gérer les statistiques
def afficher_statistiques():
    global total_games, total_wins, mise_totale, nb_coups_gagnants
    if total_games > 0:
        print(f"Statistiques générales depuis le début :")
        print(f" - Total de parties jouées : {total_games}")
        print(f" - Nombre de victoires : {total_wins}")
        print(f" - Gain total : {mise_totale}")
        print(f" - Moyenne des mises : {mise_totale / total_games if total_games > 0 else 0:.2f}")
        print(f" - Nombre moyen de coups gagnants : {nb_coups_gagnants / total_wins if total_wins > 0 else 0:.2f}")

# Fonction principale pour gérer le jeu
def jeu_casino():
    global best_level, total_games, total_wins, mise_totale, nb_coups_gagnants

    name_user = input("Je suis Python. Quel est votre pseudo ? ")
    print(f"Hello {name_user}, vous avez 10 € ! Très bien, installez-vous SVP à la table de pari.")
    afficher_regles()
    
    solde = 10
    level = 1

    while solde > 0:
        try:
            mise = float(input(f"Le jeu commence, entrez votre mise (entre 1 et {solde} €) : "))
            if mise <= 0 or mise > solde:
                print(f"Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et {solde} €.")
                continue
        except ValueError:
            print(f"Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et {solde} €.")
            continue

        total_games += 1
        mise_totale += mise

        if level == 1:
            gagne, gain = jouer_niveau(level, 3, 10, mise)
        elif level == 2:
            gagne, gain = jouer_niveau(level, 5, 20, mise)
        elif level == 3:
            gagne, gain = jouer_niveau(level, 7, 30, mise)

        if gagne:
            total_wins += 1
            solde += gain
            nb_coups_gagnants += 1

            if level < 3:
                level += 1
                print(f"Super ! Vous passez au Level {level} !")
            else:
                print(f"Bravo ! Vous avez terminé le jeu avec {solde} €.")
                break
        else:
            solde -= mise
            if level > 1:
                level -= 1

        if solde <= 0:
            print(f"Vous avez perdu tout votre argent. Au revoir {name_user} !")

        continuer = input("Souhaitez-vous continuer la partie (O/N) ? ").lower()
        if continuer != 'o':
            print(f"Au revoir ! Vous finissez la partie avec {solde} €.")
            break

    afficher_statistiques()

# Lancer le jeu
jeu_casino()
