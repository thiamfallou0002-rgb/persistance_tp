import random
from faker import Faker
from src.sqlite_db import GestionSQLite
from src.mysql_db import GestionMySQL

def test_sqlite():
    print("\n" + "="*20 + " EXÉCUTION TESTS SQLITE " + "="*20)
    db = GestionSQLite()
    db.creer_table()

    # Exercice 1
    db.ajouter("Routeur_Dakar_1", "Routeur", "192.168.1.1")
    db.ajouter("Routeur_Thies_1", "Routeur", "192.168.2.1")
    db.ajouter("Switch_Dakar_A", "Switch", "192.168.1.10")
    db.ajouter("Switch_Dakar_B", "Switch", "192.168.1.11")

    print("\n--- Liste initiale des équipements ---")
    db.lister()

    # Exercice 2
    fake = Faker()
    niveaux = ["INFO", "WARNING", "ERROR"]
    equipements_noms = ["Routeur_Dakar_1", "Routeur_Thies_1", "Switch_Dakar_A", "Switch_Dakar_B"]
    
    for _ in range(20):
        db.ajouter_log(
            equipement=random.choice(equipements_noms),
            niveau=random.choice(niveaux),
            message=fake.sentence(nb_words=5)
        )

    print("\n--- Statistiques des Logs ---")
    db.statistics()

    # Exercice 3
    print("\n--- Rapport individuel pour Routeur_Dakar_1 ---")
    db.rapport_equipement("Routeur_Dakar_1")

    print("\n--- Équipements ayant des erreurs ---")
    print(db.equipements_avec_erreurs())

    db.exporter_rapport()


def test_mysql():
    print("\n" + "="*20 + " EXÉCUTION TESTS MYSQL " + "="*20)
    try:
        # Pensez à créer la base 'reseau_db' sur votre WAMP/XAMPP au préalable
        db_mysql = GestionMySQL(host='localhost', user='root', password='', database='reseau_db')
        db_mysql.creer_table()
        
        db_mysql.ajouter("Routeur_Core", "Routeur", "10.0.0.1")
        print("\n--- Liste des équipements MySQL ---")
        print(db_mysql.lister())
        
        id_site = db_mysql.ajouter_site("Campus Dakar", "Dakar")
        id_eq = db_mysql.ajouter_equipement("DK_Switch_1", "Switch", id_site)
        db_mysql.ajouter_interface("eth0", "10.1.1.1", "255.255.255.0", id_eq)

        print("\n--- Topologie Réseau du Site ---")
        db_mysql.topologie_site(id_site)

    except Exception as e:
        print(f"\n[Note MySQL] Base de données locale hors ligne ou non créée : {e}")

if __name__ == '__main__':
    test_sqlite()
    test_mysql()