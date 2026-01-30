# Projet FastAPI : Voitures d'exception avec IA

Ce projet permet de gérer une base de voitures d'exception et de générer automatiquement une description commerciale en français pour chaque modèle via l'API OpenRouter.

---

## Prérequis

- Python 3.14+
- Virtualenv recommandé
- Clé API OpenRouter

---

## Installation

1. **Cloner le projet**
```bash
git clone <repo_url>
cd <nom_du_projet>
```

2. **Creer un environnement virtuel**
```bash
python -m venv env
source env/bin/activate   # Linux/macOS
env\Scripts\activate      # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
Creer un fichier .env à la racine du projet :
```bash
API_KEY=sk-or-v1-xxxxxxxx  
OPENROUTER_MODEL=upstage/solar-pro-3:free
OPENROUTER_APP_NAME=MyCarApp
OPENROUTER_SITE_URL=http://localhost:8000
```

5. **Initialiser la base de données**
Exemple avec sqlite
```bash
python -m app.db.database
```

**Lancer l’application**
```bash
uvicorn app.main:app --reload
```