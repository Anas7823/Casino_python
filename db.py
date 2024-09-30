import pymysql
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Connexion à la base de données
def connexion_db():
    print("Connexion à la base de données...")
    try:
        return pymysql.connect(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            database=os.getenv("database"),
            cursorclass=pymysql.cursors.DictCursor  # Pour retourner les résultats sous forme de dictionnaire
        )
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None

# Fonction pour récupérer les informations d'un joueur
def recuperer_joueur(pseudo):
    db = connexion_db()
    if db is None:
        return None
    
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE pseudo = %s", (pseudo,))
        joueur = cursor.fetchone()
        cursor.close()
        db.close()
        return joueur
    except pymysql.MySQLError as e:
        print(f"Erreur SQL lors de la récupération des informations : {e}")
        return None

# Fonction pour sauvegarder ou mettre à jour les statistiques du joueur
def sauvegarder_statistiques(pseudo, joueur_data):
    db = connexion_db()
    if db is None:
        print("Impossible de se connecter à la base de données.")
        return
    
    try:
        cursor = db.cursor()

        # Vérifie si le joueur existe déjà
        cursor.execute("SELECT * FROM user WHERE pseudo = %s", (pseudo))
        result = cursor.fetchone()

        if result:
            print(f"Bienvenue à nouveau {joueur_data['pseudo']} ! ") 
            # Mise à jour des statistiques du joueur
            cursor.execute("""
                UPDATE user SET best_level = %s, solde = %s, best_gain = %s
                WHERE pseudo = %s
            """, (joueur_data['best_level'], joueur_data['solde'], joueur_data['best_gain'], pseudo))
        else:
            print("Bienvenue dans notre Casion pour votre première fois !")
            # Insérer un nouveau joueur
            cursor.execute("""
                INSERT INTO user (pseudo, best_level, solde, best_gain)
                VALUES (%s, %s, %s, %s)
            """, (pseudo, joueur_data['best_level'], joueur_data['solde'], joueur_data['best_gain']))

        db.commit()
        cursor.close()
    except pymysql.MySQLError as e:
        print(f"Erreur SQL lors de la sauvegarde : {e}")
    finally:
        db.close()
