# VibeLink - Architecture

## 1. Vue d'ensemble

VibeLink est une plateforme de rencontre basée sur les lieux physiques. Contrairement aux applications de rencontre classiques, les interactions entre utilisateurs sont déclenchées par leur présence dans un même lieu et pendant une même session.

L'architecture a été pensée selon une approche modulaire afin de faciliter l'évolution du projet vers une architecture orientée services (microservices) sans remettre en cause les fondations actuelles.

---

# 2. Architecture actuelle

Le MVP repose sur une architecture monolithique.

```
                    Frontend (Angular)

                            │
                            │ HTTPS / REST API
                            │
                    Backend (FastAPI)

                            │
                            │ SQLAlchemy
                            │
                      PostgreSQL
```

Cette architecture permet de développer rapidement le produit tout en conservant une excellente maintenabilité.

---

# 3. Stack technique

## Frontend

- Angular
- TypeScript
- Angular Material
- RxJS

## Backend

- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Uvicorn

## Base de données

- PostgreSQL

## Outils

- Docker
- Git
- GitHub
- PgAdmin

---

# 4. Architecture backend

Le backend est organisé selon une architecture par responsabilités.

```
backend/

├── alembic/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── enums/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── docs/
│
├── requirements.txt
│
└── docker-compose.yml
```

---

# 5. Description des dossiers

## api/

Contient les endpoints REST.

Exemples :

- Authentification
- Profils
- Venues
- Matchs
- Conversations

---

## core/

Configuration globale de l'application :

- Settings
- Sécurité
- JWT
- Configuration

---

## db/

Gestion de la base de données :

- connexion
- session SQLAlchemy
- classe Base

---

## enums/

Centralise tous les enums du projet.

Exemples :

- UserRole
- VenueCategory
- MatchStatus
- NotificationType

---

## models/

Toutes les entités SQLAlchemy.

Exemple :

- User
- Profile
- Venue
- VenueSession
- Match
- Conversation

---

## schemas/

Tous les modèles Pydantic.

Séparation claire entre :

- Request DTO
- Response DTO

---

## services/

Contient la logique métier.

Les routes REST ne contiennent aucune logique métier.

Exemple :

```
POST /matches

↓

MatchService.create_match()

↓

Repository SQLAlchemy
```

---

# 6. Architecture de la base de données

Le modèle relationnel est organisé autour de plusieurs domaines.

## Authentification

```
USERS
    │
    ├──────── PROFILE
    │
    └──────── MATCH_PREFERENCES
```

---

## Venues

```
VENUES

      │

VENUE_SESSIONS

      │

VENUE_SESSION_PARTICIPANTS
```

---

## Social

```
LIKES

↓

MATCHES

↓

CONVERSATIONS

↓

MESSAGES
```

---

## Expérience utilisateur

```
NOTIFICATIONS

MATCH_MEETINGS

MATCH_BLOCKS
```

---

# 7. Principe des sessions

Une venue ne possède qu'une seule session par jour.

Exemple :

```
Delirium

07/08/2026

19h → fermeture
```

Tous les utilisateurs présents rejoignent cette même session.

Cette approche permet :

- d'éviter les doublons de sessions ;
- de simplifier le matching ;
- de réduire le nombre d'enregistrements.

---

# 8. Principe du matching

Le workflow métier est le suivant.

```
Venue

↓

Venue Session

↓

Participant

↓

Like

↓

Match

↓

Conversation

↓

Messages

↓

Confirmation IRL
```

---

# 9. Philosophie de développement

Le projet suit plusieurs principes.

## Responsabilité unique

Chaque module possède une responsabilité clairement définie.

---

## Séparation des couches

Les responsabilités sont séparées :

```
API

↓

Services

↓

SQLAlchemy

↓

PostgreSQL
```

---

## Évolutivité

Le MVP privilégie une architecture simple.

Les composants pourront être extraits en microservices sans réécriture majeure.

---

# 10. Vision de l'architecture

À moyen terme, VibeLink évoluera progressivement vers une architecture composée de plusieurs services.

```
                    Angular

                        │

                 API Gateway

                        │

 ┌────────────┬──────────────┬──────────────┐
 │            │              │              │
Auth     Matching      Messaging     Notifications
Service     Service        Service        Service
 │            │              │              │
 └────────────┴──────────────┴──────────────┘
                 PostgreSQL
```

Cette évolution ne sera entreprise que lorsque la croissance du produit le justifiera.

---

# 11. Intelligence Artificielle

L'architecture est conçue pour accueillir des services d'intelligence artificielle.

Ces services ne font pas partie du MVP mais sont prévus dans la feuille de route du projet.

Les usages envisagés sont notamment :

- recommandations de profils ;
- recommandations de lieux ;
- amélioration de l'algorithme de matching ;
- suggestions conversationnelles ;
- assistance utilisateur ;
- modération automatique ;
- détection de comportements frauduleux ;
- analyse des interactions afin d'améliorer l'expérience utilisateur.

L'objectif est de conserver une architecture "AI-ready", permettant d'intégrer progressivement ces fonctionnalités sans modifier les fondations du projet.

---

# 12. Évolutions futures

Les évolutions envisagées comprennent notamment :

- Redis (cache)
- WebSockets pour la messagerie temps réel
- Service de notifications push
- Intégration IA
- Recherche géographique avancée
- Géolocalisation optimisée
- Tableau de bord d'administration
- Monitoring
- Observabilité
- CI/CD complète
- Déploiement cloud