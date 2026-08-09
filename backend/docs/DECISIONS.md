# VibeLink - Architecture Decisions

Ce document recense les principales décisions techniques et métier prises pendant la conception de VibeLink.

L'objectif est de conserver le contexte et les raisons derrière les choix structurants du projet.

---

# 1. Architecture du backend

## Décision

Le MVP utilise une architecture monolithique avec FastAPI.

## Choix

- Python 3.13
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL

## Pourquoi ?

Le monolithe permet de :

- développer rapidement le MVP ;
- limiter la complexité opérationnelle ;
- centraliser la logique métier ;
- faciliter le développement initial.

L'architecture est cependant organisée par responsabilités afin de permettre une évolution progressive vers des services séparés si le produit grandit.

---

# 2. PostgreSQL

## Décision

PostgreSQL est utilisé comme base de données principale.

## Pourquoi ?

PostgreSQL est adapté au modèle relationnel de VibeLink qui contient de nombreuses relations :

- utilisateurs ;
- profils ;
- venues ;
- sessions ;
- participants ;
- likes ;
- matchs ;
- conversations ;
- messages ;
- notifications.

Il permet également d'utiliser des contraintes, des index et des types PostgreSQL pour garantir l'intégrité des données.

---

# 3. SQLAlchemy

## Décision

SQLAlchemy est utilisé comme ORM.

## Pourquoi ?

Il permet de :

- représenter les tables sous forme de modèles Python ;
- gérer les relations entre entités ;
- centraliser la définition du schéma ;
- travailler proprement avec PostgreSQL.

---

# 4. Alembic

## Décision

Alembic est utilisé pour gérer les migrations de base de données.

## Workflow

Création d'une migration :

```bash
alembic revision --autogenerate -m "description"
```

Application :

```bash
alembic upgrade head
```

## Pourquoi ?

Les changements du schéma sont versionnés avec le code et peuvent être reproduits sur différents environnements.

---

# 5. Enums métier

## Décision

Les valeurs métier ayant un ensemble fini de possibilités sont représentées par des enums Python et PostgreSQL.

Exemple :

```python
class VenueCategory(str, Enum):
    BAR = "BAR"
    RESTAURANT = "RESTAURANT"
    CLUB = "CLUB"
    CAFE = "CAFE"
    ROOFTOP = "ROOFTOP"
    SHOPPING = "SHOPPING"
    ENTERTAINMENT = "ENTERTAINMENT"
    PARC = "PARC"
    SPORT = "SPORT"
```

## Pourquoi ?

Cela permet de :

- éviter les valeurs arbitraires ;
- centraliser les catégories ;
- valider les données ;
- garantir la cohérence entre application et base de données.

---

# 6. Catégories de venues

## Décision

Les catégories représentent le type de lieu ou l'environnement dans lequel l'utilisateur peut se rendre.

Les catégories actuelles sont :

- BAR
- RESTAURANT
- CLUB
- CAFE
- ROOFTOP
- SHOPPING
- ENTERTAINMENT
- PARC
- SPORT

## Décision importante

Les festivals, soirées organisées, espaces événementiels et lieux similaires sont regroupés dans `ENTERTAINMENT` plutôt que de créer plusieurs catégories spécifiques.

L'objectif est de ne pas créer une catégorie pour chaque type d'événement.

---

# 7. Recherche géographique

## Décision

L'utilisateur ne définit pas lui-même le périmètre de recherche.

VibeLink détermine les lieux et profils pertinents selon un périmètre défini par le système / back-office.

## Pourquoi ?

Le produit doit contrôler l'expérience de découverte et éviter de demander à l'utilisateur de configurer lui-même un rayon de recherche.

La recherche géographique pourra évoluer ultérieurement vers une solution plus avancée.

---

# 8. Venue

## Décision

Une `Venue` représente un lieu physique permanent référencé par VibeLink.

Exemples :

- bar ;
- restaurant ;
- café ;
- club ;
- parc ;
- lieu de divertissement.

Les venues sont gérées par le système / back-office.

---

# 9. Venue Session

## Décision

Une `VenueSession` représente la session d'une venue pour une journée donnée.

Une venue possède au maximum une session par jour.

Contrainte :

```text
UNIQUE(venue_id, session_date)
```

## Exemple

```text
Delirium
07/08/2026
19:00 → heure de fermeture
```

Tous les utilisateurs qui s'inscrivent au Delirium le même jour rejoignent la même session.

## Pourquoi ?

Cela évite de créer une session différente pour chaque utilisateur ou pour chaque heure d'arrivée.

---

# 10. Fin de session

## Décision

La session se termine à l'heure de fermeture de la venue.

L'utilisateur ne renseigne pas manuellement son heure de départ.

## Pourquoi ?

Le départ individuel n'apporte pas suffisamment de valeur au MVP et ajouterait une action inutile pour l'utilisateur.

---

# 11. Venue Session Participants

## Décision

Une table `VenueSessionParticipant` est utilisée pour représenter la participation d'un utilisateur à une session.

Elle remplace une table `CheckIns` indépendante.

Relation :

```text
USERS N──N VENUE_SESSIONS
        via
VENUE_SESSION_PARTICIPANTS
```

## Pourquoi ?

La participation et le check-in concernent la même relation :

> un utilisateur participe à une session donnée.

La table peut donc gérer l'état de cette participation.

---

# 12. Inscription et check-in

## Décision

L'inscription et le check-in sont deux étapes d'une même participation.

### Cas 1 — utilisateur déjà sur place

L'utilisateur s'inscrit à la venue.

Si l'heure prévue correspond à sa présence immédiate, le backend peut automatiquement effectuer le check-in.

### Cas 2 — utilisateur inscrit à l'avance

L'utilisateur rejoint la session à l'avance.

À l'heure prévue, VibeLink lui envoie une notification lui permettant de confirmer sa présence.

---

# 13. Likes

## Décision

Un like est définitif dans le sens où il reste enregistré.

Contrainte :

```text
UNIQUE(sender_id, receiver_id)
```

## Conséquence

Si Steve like Julie aujourd'hui mais que Julie ne le like pas immédiatement, le like reste disponible.

Si Julie rencontre Steve lors d'une session ultérieure, elle peut toujours voir le like et décider de liker à son tour.

Le système conserve donc l'historique des likes.

---

# 14. Matches

## Décision

Un match est créé lorsqu'un like devient réciproque.

```text
Steve → like → Julie

Julie → like → Steve

↓

MATCH
```

Le match n'est donc pas directement lié à une session particulière.

## Pourquoi ?

Deux utilisateurs peuvent se matcher à des moments différents et éventuellement s'être rencontrés dans plusieurs sessions.

---

# 15. Conversation

## Décision

Un match possède une conversation.

Relation :

```text
MATCH 1──1 CONVERSATION
```

La conversation devient accessible lorsque les conditions métier nécessaires sont satisfaites.

---

# 16. Présence commune avant conversation

## Décision

Le fait d'avoir matché ne suffit pas à débloquer immédiatement la conversation.

Les deux utilisateurs doivent également avoir été présents dans une même session.

## Pourquoi ?

C'est une règle métier différenciante de VibeLink :

> le matching est basé sur une rencontre dans le monde réel.

Cette règle est principalement gérée au niveau applicatif.

---

# 17. Match Blocks

## Décision

Le blocage est représenté par une table dédiée `MatchBlocks`.

Le blocage n'est possible qu'entre deux utilisateurs ayant déjà matché.

## Pourquoi ?

Un utilisateur ne peut pas bloquer arbitrairement un profil qu'il n'a jamais rencontré ou avec lequel il n'a jamais matché.

La table permet également de conserver :

- l'utilisateur qui a bloqué ;
- le match concerné ;
- la date du blocage ;
- la possibilité de débloquer ultérieurement.

## Pourquoi ne pas utiliser uniquement `MatchStatus` ?

Parce qu'un blocage est une action effectuée par un utilisateur précis et qu'elle doit pouvoir être annulée.

Une table dédiée permet de conserver cette information proprement.

---

# 18. Messages

## Décision

Les messages appartiennent à une conversation.

Relation :

```text
CONVERSATIONS 1──N MESSAGES
```

Chaque message possède notamment :

- un auteur ;
- un contenu ;
- une date de création ;
- une date de lecture éventuelle.

---

# 19. Notifications

## Décision

Les notifications sont persistées dans une table dédiée.

Elles sont utilisées pour plusieurs événements de VibeLink.

Exemples :

- nouveau like ;
- nouveau match ;
- nouveau message ;
- rappel de check-in ;
- confirmation de rencontre IRL.

## Pourquoi ?

Les notifications font partie de l'expérience utilisateur et doivent pouvoir être consultées après leur émission.

---

# 20. Match Meetings

## Décision

Une table `MatchMeetings` est utilisée pour enregistrer si deux personnes se sont réellement rencontrées.

## Pourquoi ?

Le matching VibeLink ne représente pas nécessairement une rencontre réelle.

Après une session, les utilisateurs peuvent confirmer :

> "Nous nous sommes réellement rencontrés."

Cette information est importante pour :

- mesurer la qualité des matchs ;
- améliorer l'expérience ;
- alimenter de futures fonctionnalités ;
- potentiellement améliorer les recommandations.

---

# 21. IA

## Décision

L'IA fait partie de la vision future de VibeLink mais n'est pas une composante du MVP actuel.

L'architecture doit rester compatible avec une intégration future de services IA.

Les usages envisagés comprennent notamment :

- recommandations de profils ;
- recommandations de venues ;
- amélioration du matching ;
- modération ;
- détection de comportements suspects ;
- assistance utilisateur.

## Pourquoi ne pas l'intégrer maintenant ?

Les fondations métier et le modèle de données doivent d'abord être stabilisés.

Les besoins réels en IA pourront être définis à partir des données et des usages observés.

---

# 22. Architecture AI-ready

## Décision

Aucune infrastructure IA spécifique n'est ajoutée au MVP.

Aucune base vectorielle ou service IA n'est imposé à ce stade.

## Pourquoi ?

Le choix d'une technologie IA dépendra des besoins réels :

- embeddings ;
- recherche sémantique ;
- recommandations ;
- LLM ;
- modération.

Ces choix seront réalisés lorsque les fonctionnalités IA seront effectivement conçues.

---

# 23. Monolithe avant microservices

## Décision

VibeLink reste un monolithe pour le MVP.

Une architecture microservices pourra être envisagée ultérieurement.

## Pourquoi ?

Les microservices apporteraient une complexité opérationnelle importante :

- déploiements multiples ;
- communication inter-services ;
- observabilité ;
- gestion des erreurs distribuées ;
- infrastructure supplémentaire.

Cette complexité n'est pas justifiée pour le MVP.

---

# 24. Documentation

## Décision

La documentation technique est séparée en plusieurs fichiers.

```text
docs/

├── ONBOARDING.md
├── ARCHITECTURE.md
├── DATABASE.md
├── BUSINESS_RULES.md
├── DECISIONS.md
└── API.md
```

`API.md` sera complété lorsque les endpoints seront suffisamment stabilisés.

## Pourquoi attendre ?

Documenter trop tôt les endpoints risquerait de créer une documentation rapidement obsolète.

---

# 25. Principe général

Les décisions du MVP suivent une même philosophie :

> **Construire le minimum nécessaire pour valider le produit, tout en gardant une architecture suffisamment propre pour permettre son évolution.**

Le MVP privilégie donc :

- simplicité ;
- cohérence ;
- intégrité des données ;
- séparation des responsabilités ;
- évolutivité ;
- réduction de la complexité inutile.
