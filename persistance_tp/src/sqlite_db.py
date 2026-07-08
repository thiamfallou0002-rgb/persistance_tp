import sqlite3
from datetime import datetime

class GestionSQLite:
    def __init__(self, db_name='reseau.db'):
        """Initialise la connexion à la base SQLite."""
        self.db_name = db_name

    def _connexion(self):
        """Méthode utilitaire pour ouvrir une connexion."""
        conn = sqlite3.connect(self.db_name)
        return conn, conn.cursor()

    def creer_table(self):
        """Crée les tables equipements et logs."""
        conn, cursor = self._connexion()
        try:
            # Table Equipements (Exercice 1)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS equipements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT,
                    type TEXT,
                    ip TEXT,
                    actif INTEGER DEFAULT 1
                )
            """)
            # Table Logs (Exercice 2)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    equipement TEXT,
                    niveau TEXT,
                    message TEXT,
                    horodatage TEXT
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la création des tables SQLite: {e}")
        finally:
            conn.close()

    # --- EXERCICE 1 ---
    def ajouter(self, nom, type_eq, ip):
        """Insère un équipement réseau actif par défaut (1)."""
        conn, cursor = self._connexion()
        try:
            cursor.execute(
                "INSERT INTO equipements (nom, type, ip, actif) VALUES (?, ?, ?, 1)",
                (nom, type_eq, ip)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur d'ajout de l'équipement: {e}")
        finally:
            conn.close()

    def lister(self):
        """Retourne et affiche tous les équipements."""
        conn, cursor = self._connexion()
        try:
            cursor.execute("SELECT * FROM equipements")
            res = cursor.fetchall()
            for row in res:
                print(row)
            return res
        finally:
            conn.close()

    def rechercher(self, ip):
        """Retourne l'équipement correspondant à l'IP."""
        conn, cursor = self._connexion()
        try:
            cursor.execute("SELECT * FROM equipements WHERE ip = ?", (ip,))
            return cursor.fetchone()
        finally:
            conn.close()

    def desactiver(self, ip):
        """Met actif=0 pour l'équipement donné."""
        conn, cursor = self._connexion()
        try:
            cursor.execute("UPDATE equipements SET actif = 0 WHERE ip = ?", (ip,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur désactivation: {e}")
        finally:
            conn.close()

    # --- EXERCICE 2 ---
    def ajouter_log(self, equipement, niveau, message):
        """Insère un log avec l'horodatage actuel."""
        conn, cursor = self._connexion()
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute(
                "INSERT INTO logs (equipement, niveau, message, horodatage) VALUES (?, ?, ?, ?)",
                (equipement, niveau, message, horodatage)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur log: {e}")
        finally:
            conn.close()

    def logs_par_niveau(self, niveau):
        """Retourne tous les logs d'un niveau donné."""
        conn, cursor = self._connexion()
        try:
            cursor.execute("SELECT * FROM logs WHERE niveau = ?", (niveau,))
            return cursor.fetchall()
        finally:
            conn.close()

    def logs_par_equipement(self, nom):
        """Retourne tous les logs d'un équipement."""
        conn, cursor = self._connexion()
        try:
            cursor.execute("SELECT * FROM logs WHERE equipement = ?", (nom,))
            return cursor.fetchall()
        finally:
            conn.close()

    def statistics(self):
        """Affiche le nombre de logs par niveau."""
        conn, cursor = self._connexion()
        try:
            cursor.execute("SELECT niveau, COUNT(*) FROM logs GROUP BY niveau")
            res = cursor.fetchall()
            for row in res:
                print(f"Niveau: {row[0]} | Nombre: {row[1]}")
            return res
        finally:
            conn.close()

    def lister_logs_ordonnes(self):
        """Retourne les logs triés par horodatage décroissant."""
        conn, cursor = self._connexion()
        try:
            cursor.execute("SELECT * FROM logs ORDER BY horodatage DESC")
            return cursor.fetchall()
        finally:
            conn.close()

    # --- EXERCICE 3 ---
    def rapport_equipement(self, nom):
        """Affiche le statut d'un équipement et ses 5 derniers logs."""
        conn, cursor = self._connexion()
        try:
            cursor.execute("SELECT actif FROM equipements WHERE nom = ?", (nom,))
            eq = cursor.fetchone()
            statut = "Actif" if eq and eq[0] == 1 else "Inactif/Inexistant"
            print(f"--- Rapport pour {nom} ({statut}) ---")
            
            cursor.execute("""
                SELECT l.niveau, l.message, l.horodatage 
                FROM logs l
                JOIN equipements e ON l.equipement = e.nom
                WHERE e.nom = ?
                ORDER BY l.horodatage DESC LIMIT 5
            """, (nom,))
            logs = cursor.fetchall()
            for l in logs:
                print(f"[{l[2]}] {l[0]}: {l[1]}")
            return statut, logs
        finally:
            conn.close()

    def equipements_avec_erreurs(self):
        """Liste les équipements ayant au moins un log ERROR."""
        conn, cursor = self._connexion()
        try:
            cursor.execute("""
                SELECT DISTINCT e.nom FROM equipements e
                JOIN logs l ON e.nom = l.equipement
                WHERE l.niveau = 'ERROR'
            """)
            return cursor.fetchall()
        finally:
            conn.close()

    def top_equipements(self, n):
        """Retourne les n équipements ayant généré le plus de logs."""
        conn, cursor = self._connexion()
        try:
            cursor.execute("""
                SELECT equipement, COUNT(*) as total 
                FROM logs 
                GROUP BY equipement 
                ORDER BY total DESC 
                LIMIT ?
            """, (n,))
            return cursor.fetchall()
        finally:
            conn.close()

    def exporter_rapport(self):
        """Exporte le rapport complet dans un fichier rapport.txt avec la date du jour."""
        conn, cursor = self._connexion()
        date_jour = datetime.now().strftime("%Y-%m-%d")
        nom_fichier = f"rapport_{date_jour}.txt"
        try:
            cursor.execute("""
                SELECT e.nom, e.type, e.ip, e.actif, COUNT(l.id) 
                FROM equipements e
                LEFT JOIN logs l ON e.nom = l.equipement
                GROUP BY e.nom
            """)
            rows = cursor.fetchall()
            with open(nom_fichier, "w", encoding="utf-8") as f:
                f.write(f"RAPPORT DU {date_jour}\n")
                f.write("="*40 + "\n")
                for row in rows:
                    statut = "ACTIF" if row[3] == 1 else "INACTIF"
                    f.write(f"Nom: {row[0]} | Type: {row[1]} | IP: {row[2]} | Statut: {statut} | Total Logs: {row[4]}\n")
            print(f"Rapport exporté dans : {nom_fichier}")
        finally:
            conn.close()