import mysql.connector
from mysql.connector import Error

class GestionMySQL:
    """Classe pour gérer la persistance multi-tables avec MySQL."""

    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.conn = None
        self.cursor = None

    def connexion(self):
        """Établit la connexion au serveur MySQL."""
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.conn, self.cursor
        except Error as e:
            print(f"Erreur de connexion MySQL : {e}")
            return None, None

    def creer_tables_multi(self):
        """Crée la structure multi-tables (Exercice 5)."""
        self.connexion()
        queries = [
            "CREATE TABLE IF NOT EXISTS sites (id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(100), ville VARCHAR(100))",
            "CREATE TABLE IF NOT EXISTS equipements (id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(100), type VARCHAR(50), id_site INT, FOREIGN KEY(id_site) REFERENCES sites(id))",
            "CREATE TABLE IF NOT EXISTS interfaces (id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(50), ip VARCHAR(20), id_equipement INT, FOREIGN KEY(id_equipement) REFERENCES equipements(id))"
        ]
        for query in queries:
            self.cursor.execute(query)
        self.conn.commit()

    def ajouter_site(self, nom, ville):
        self.cursor.execute("INSERT INTO sites (nom, ville) VALUES (%s, %s)", (nom, ville))
        self.conn.commit()
        return self.cursor.lastrowid

    def ajouter_equipement(self, nom, type_eq, id_site):
        self.cursor.execute("INSERT INTO equipements (nom, type, id_site) VALUES (%s, %s, %s)", (nom, type_eq, id_site))
        self.conn.commit()
        return self.cursor.lastrowid

    def topologie_site(self, id_site):
        """Affiche les équipements et leurs interfaces pour un site (JOIN)."""
        query = """
            SELECT s.nom, e.nom, i.ip 
            FROM sites s
            JOIN equipements e ON s.id = e.id_site
            JOIN interfaces i ON e.id = i.id_equipement
            WHERE s.id = %s
        """
        self.cursor.execute(query, (id_site,))
        for row in self.cursor.fetchall():
            print(f"Site: {row[0]} | Equipement: {row[1]} | IP: {row[2]}")

    def fermer(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()