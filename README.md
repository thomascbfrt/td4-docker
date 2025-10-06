# HelloWorld API - Projet Docker

## Description du projet

Application Flask simple déployée avec Docker et Nginx comme reverse proxy.

## Architecture

- **API Flask** : Serveur Python exposant une API REST
- **Nginx** : Reverse proxy pour router les requêtes vers l'API
- **Docker Compose** : Orchestration des services

## Fichiers créés/modifiés

### Fichiers créés pour le TD4

1. **`Dockerfile`** (HelloWorldAPI/Dockerfile)
   - Image de base : `python:3.11`
   - Labels : version, maintainer, description
   - Répertoire de travail : `/usr/src/app`
   - Installation des dépendances sans cache (`pip install --no-cache-dir`)
   - Copie du code source complet
   - Précompilation des fichiers Python (`python -m compileall .`)
   - Point d'entrée : `CMD ["python", "HelloWorldAPI.py"]`

2. **`docker-compose.yml`**
   - Service `api` : 
     - Build depuis le Dockerfile local (context: ./HelloWorldAPI)
     - Image nommée : `tfriquet/helloworldapi`
     - Volume pour config.py (permet modification sans rebuild)
     - Réseau privé `app-network`
   - Service `http` :
     - Image nginx:latest
     - Port exposé : 8080:80
     - Volume pour nginx.conf en lecture seule
     - Dépend du service api
     - Réseau privé `app-network`

3. **`README.md`** (ce fichier)

4. **`JOURNAL.md`** (journal de bord)

### Fichiers modifiés

1. **`config.py`**
   - `SERVER_HOST` : `127.0.0.1` → `0.0.0.0` (pour Docker)
   - `SERVER_PORT` : `5001` → `5000` (standardisation)

   127.0.0.1 (localhost) signifie "écoute uniquement sur l'interface locale du conteneur"
Dans Docker, si le serveur écoute sur 127.0.0.1, il n'est accessible que depuis l'intérieur du conteneur lui-même
0.0.0.0 signifie "écoute sur toutes les interfaces réseau", ce qui permet au service nginx (qui est dans un autre conteneur) de communiquer avec l'API
Le port 5000 est le standard et correspond à ce que nginx attend dans sa configuration

2. **`nginx.conf`**
   - `$rest_api_backend` : `localhost:5000` → `api:5000` (nom du service Docker)
localhost dans le conteneur nginx pointe vers le conteneur nginx lui-même, pas vers le conteneur de l'API
Dans Docker Compose, chaque service a un nom DNS correspondant à son nom de service
Le service s'appelle api dans le docker-compose.yml, donc nginx doit utiliser api:5000 pour le joindre
Docker Compose crée automatiquement un réseau où les services peuvent se parler par leur nom
Sans ces modifications, nginx ne pourrait pas communiquer avec l'API et vous auriez une erreur 502 Bad Gateway !
   

## Structure du projet

```
TD4 - ressources-20251006/
├── docker-compose.yml          # Orchestration des services
├── nginx.conf                  # Configuration du reverse proxy
├── README.md                   # Documentation du projet
├── JOURNAL.md                  # Journal de bord
└── HelloWorldAPI/
    ├── Dockerfile              # Descripteur d'image Docker
    ├── config.py               # Configuration du serveur Flask
    ├── HelloWorldAPI.py        # Point d'entrée de l'application
    ├── helloWordController.py  # Contrôleur REST
    └── requirements.txt        # Dépendances Python
```

## Dépendances Python

Les dépendances sont définies dans `requirements.txt` :
- Flask 3.0.3
- Flask-Cors 5.0.0
- Werkzeug 3.0.4
- Jinja2 3.1.4
- et autres dépendances associées

## Installation et démarrage

### Prérequis
- Docker
- Docker Compose

### Construction de l'image

```bash
docker compose build
```

### Démarrage des services

```bash
docker compose up -d
```

### Vérification de l'état

```bash
docker compose ps
```

### Arrêt des services

```bash
docker compose down
```

## Utilisation

### Endpoints disponibles

#### GET /api/hello
Retourne un message de bienvenue.

**Requête :**
```bash
curl http://localhost:8080/api/hello
```

**Réponse :**
```json
{
  "message": "Hello World!"
}
```

## Configuration

### Modification de la configuration

Le fichier `config.py` est monté comme volume dans le conteneur. Vous pouvez le modifier sans avoir à reconstruire l'image Docker.

Après modification, redémarrez simplement le service :

```bash
docker compose restart api
```

### Variables de configuration (config.py)

- `SERVER_HOST` : Adresse d'écoute du serveur (0.0.0.0 pour Docker)
- `SERVER_PORT` : Port d'écoute du serveur (5000)
- `DEBUG` : Mode debug (False en production)
- `ENABLE_CORS` : Activation de CORS (True)



## Ports

- **8080** : Port HTTP public (Nginx)
- **5000** : Port interne de l'API (accessible uniquement dans le réseau Docker)

## Réseau Docker

Un réseau bridge privé `app-network` est créé pour permettre la communication entre les services.

## Optimisations

1. **Installation sans cache** : `pip install --no-cache-dir` pour réduire la taille de l'image
2. **Précompilation** : Génération des fichiers `.pyc` au build pour optimiser le démarrage
3. **Volume pour config** : Permet de modifier la configuration sans rebuild
4. **Réseau privé** : Isolation des services

## Auteur

Thomas Friquet
