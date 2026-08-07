# VibeLink Backend - Developer Onboarding

## 1. Présentation du projet

VibeLink est une application permettant aux utilisateurs de découvrir et d'interagir avec des personnes présentes dans les mêmes lieux physiques.

Le backend est responsable de :
- l'authentification des utilisateurs ;
- la gestion des profils ;
- la gestion des venues et sessions ;
- le système de likes et matchs ;
- les conversations ;
- les notifications.

À terme, la plateforme intégrera des services d'intelligence artificielle afin d'améliorer l'expérience utilisateur (recommandations, assistance, modération et autres fonctionnalités intelligentes).

---

# 2. Architecture technique

## Backend

Technologies principales :

- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker
- Uvicorn

## Base de données

La base de données utilisée est PostgreSQL.

L'administration peut être réalisée avec PgAdmin.


Pour faciliter l'exploration de la base de données pendant le développement, nous recommandons l'utilisation de **PgAdmin 4**.

Téléchargement :

https://www.pgadmin.org/download/

Une fois installé, créez une nouvelle connexion avec les paramètres définis dans votre fichier `.env` ou dans votre configuration Docker.

Exemple :

| Paramètre | Valeur |
|-----------|--------|
| Host | localhost |
| Port | 5432 |
| Database | vibelink |
| Username | postgres |
| Password | ******** |

PgAdmin permet notamment de :

- visualiser les tables ;
- exécuter des requêtes SQL ;
- inspecter les contraintes et index ;
- suivre les migrations Alembic ;
- vérifier rapidement les données pendant le développement.

---

# 3. Prérequis

Avant de commencer, installer :

- Git
- Python 3.13+
- Docker
- Docker Compose

Optionnel :

- PgAdmin (gestion graphique PostgreSQL)

---

# 4. Installation selon le système d'exploitation

## Windows

Deux possibilités sont possibles.

### Option 1 : Installation native

Installer :

- Python
- Git
- Docker Desktop

Puis cloner le projet.

### Option 2 : Utilisation de WSL 2 (recommandé)

WSL 2 permet d'utiliser un environnement Linux directement dans Windows.

Installation :

```bash
wsl --install
```

Installer une distribution Linux (exemple Debian).

Vérifier :

```bash
wsl --list --verbose
```

Puis travailler dans l'environnement Linux.

---

## macOS

Installer les outils nécessaires avec Homebrew :

```bash
brew install python git
```

Installer Docker Desktop depuis le site officiel Docker.

---

## Linux

Installer les dépendances :

```bash
sudo apt update
sudo apt install python3 python3-venv git
```

Installer Docker et Docker Compose.

---

# 5. Récupération du projet

Cloner le repository :

```bash
git clone <repository_url>
```

Accéder au projet :

```bash
cd vibelink/backend
```

---

# 6. Configuration de l'environnement Python

Créer l'environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement.

## Linux / macOS / WSL

```bash
source .venv/bin/activate
```

## Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

# 7. Configuration des variables d'environnement

Créer un fichier :

```
.env
```

Ajouter les variables nécessaires :

```env
DATABASE_URL=
JWT_SECRET=
```

---

# 8. Lancement des services Docker

Démarrer PostgreSQL :

```bash
docker compose up -d
```

Vérifier les conteneurs :

```bash
docker ps
```

---

# 9. Initialisation de la base de données

Appliquer les migrations :

```bash
alembic upgrade head
```

Créer une nouvelle migration :

```bash
alembic revision --autogenerate -m "description"
```

---

# 10. Lancer le serveur backend

Démarrer FastAPI :

```bash
uvicorn app.main:app --reload
```

Le serveur est disponible sur :

```
http://localhost:8000
```

Documentation Swagger :

```
http://localhost:8000/docs
```

---

# 11. Structure du projet

```
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── enums/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── alembic/
├── docs/
├── .env
├── requirements.txt
└── docker-compose.yml
```

---

# 12. Workflow de développement

Avant de commencer :

```bash
git pull
```

Créer une branche :

```bash
git checkout -b feature/name
```

Après modification :

```bash
git add .
git commit -m "description"
git push
```

---

# 13. Outils recommandés

Pour une meilleure expérience de développement, les outils suivants sont recommandés :

- Visual Studio Code
- Docker Desktop
- PgAdmin 4
- Git
- Postman ou Bruno (pour tester les API)

# 14. Documentation complémentaire

- Architecture :
`docs/ARCHITECTURE.md`

- Base de données :
`docs/DATABASE.md`

- Règles métier :
`docs/BUSINESS_RULES.md`

- API :
`docs/API.md`