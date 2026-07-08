# TP Persistance des Données - L2 RI

Ce projet implémente la gestion de la persistance des données réseau en utilisant SQLite et MySQL sous Python.

## Structure du Projet
- `main.py` : Point d'entrée unique des tests.
- `src/sqlite_db.py` : Gestion des équipements et logs avec SQLite.
- `src/mysql_db.py` : Gestion multi-tables et topologie avec MySQL.

## Installation
```bash
python -m venv venv
source venv/bin/activate  # Ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python main.py
