# Journal de bord - Projet Docker

---

## TD4 - Image personnalisée (6 octobre 2025)

### Objectif
Créer une image Docker personnalisée pour l'application HelloWorld API et la déployer avec Nginx comme reverse proxy.

### Étapes réalisées

#### 1. Analyse de l'application

**Questions du TD :**

- **Y-a-t'il un descripteur des bibliothèques nécessaires à son fonctionnement ?**
  - ✅ Oui : `requirements.txt`

- **Quelle commande permet d'installer ces dépendances ?**
  - `pip install -r requirements.txt`

- **Quelle commande permet de lancer le serveur python ?**
  - `python HelloWorldAPI.py`

#### 2. Création du Dockerfile

**Fichier créé :** `HelloWorldAPI/Dockerfile`

**Commandes utilisées dans le Dockerfile :**
```dockerfile
FROM python:3.11
LABEL version="1.0"
LABEL maintainer="votre.email@univ-lemans.fr"
LABEL description="My Train Autohistory server"
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m compileall .
CMD ["python", "HelloWorldAPI.py"]
```

**Explications :**
- `FROM python:3.11` : Image de base Python 3.11
- `LABEL` : Métadonnées de l'image (version, maintainer, description)
- `WORKDIR` : Définit le répertoire de travail
- `COPY requirements.txt .` : Copie le fichier de dépendances (optimisation pour le cache Docker)
- `RUN pip install --no-cache-dir` : Installation sans cache pour réduire la taille
- `COPY . .` : Copie tout le code source
- `RUN python -m compileall .` : Précompilation des fichiers Python
- `CMD` : Point d'entrée par défaut (choisi car plus flexible que ENTRYPOINT)

#### 3. Création du docker-compose.yml

**Fichier créé :** `docker-compose.yml`

**Configuration initiale :**
```yaml
version: '3.8'

services:
  api:
    build:
      context: ./HelloWorldAPI
    image: rvenant/helloworldapi
    volumes:
      - ./HelloWorldAPI/config.py:/usr/src/app/config.py
    networks:
      - app-network

  http:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

#### 4. Modifications nécessaires pour Docker

**Fichier modifié :** `HelloWorldAPI/config.py`

**Changements :**
```python
# Avant
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5001

# Après
SERVER_HOST = '0.0.0.0'  # Pour écouter sur toutes les interfaces dans Docker
SERVER_PORT = 5000       # Port standardisé
```

**Raison :** Dans un conteneur Docker, il faut écouter sur `0.0.0.0` pour accepter les connexions du réseau Docker.

**Fichier modifié :** `nginx.conf`

**Changement :**
```nginx
# Avant
set $rest_api_backend localhost:5000;

# Après
set $rest_api_backend api:5000;  # Utilise le nom du service Docker
```

**Raison :** Dans Docker Compose, les services communiquent par leur nom de service.

#### 5. Construction de l'image

**Commande :**
```bash
docker compose build
```

**Problèmes rencontrés :**

1. **Permission denied sur Docker socket**
   - Erreur : `permission denied while trying to connect to the Docker daemon socket`
   - Solution : Utiliser `sudo docker compose build`

2. **Nom d'image invalide**
   - Erreur : `invalid tag "rvenant/helloWorldAPI": repository name must be lowercase`
   - Solution : Changé en `rvenant/helloworldapi`

**Résultat :**
```
[+] Building 147.7s (11/11) FINISHED
=> naming to docker.io/rvenant/helloworldapi
```

**Vérification de l'image créée :**
```bash
sudo docker images | grep helloworldapi
```

**Résultat :**
```
rvenant/helloworldapi    latest    0b66cbe58024   20 seconds ago   1.17GB
```

#### 6. Démarrage de la pile

**Commande :**
```bash
sudo docker compose up -d
```

**Problème rencontré :**
- Erreur : `Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use`
- Solution : Changé le port de `80:80` à `8080:80` dans docker-compose.yml

**Résultat après correction :**
```
[+] Running 2/2
✔ Container td4-ressources-20251006-api-1   Running
✔ Container td4-ressources-20251006-http-1  Started
```

#### 7. Vérification du fonctionnement

**Commande de vérification des conteneurs :**
```bash
sudo docker compose ps
```

**Résultat :**
```
NAME                             IMAGE                   STATUS              PORTS
td4-ressources-20251006-api-1    rvenant/helloworldapi   Up 27 seconds
td4-ressources-20251006-http-1   nginx:latest            Up 12 seconds       0.0.0.0:8080->80/tcp
```

**Test de l'API :**
```bash
curl http://localhost:8080/api/hello
```

**Résultat :**
```json
{"message":"Hello World!"}
```

✅ **L'API fonctionne correctement !**

#### 8. Changement du nom de l'image

**Modification du docker-compose.yml :**
```yaml
# Avant
image: rvenant/helloworldapi

# Après
image: tfriquet/helloworldapi
```

**Commandes exécutées :**
```bash
# Arrêt des conteneurs
sudo docker compose down

# Reconstruction de l'image avec le nouveau nom
sudo docker compose build

# Redémarrage de la pile
sudo docker compose up -d

# Test de l'API
curl http://localhost:8080/api/hello
```

**Résultat :**
```json
{"message":"Hello World!"}
```

✅ **L'image a été reconstruite avec succès sous le nom `tfriquet/helloworldapi`**

### Points clés du TD

1. **Volume pour config.py** : Permet de modifier la configuration sans reconstruire l'image
   ```yaml
   volumes:
     - ./HelloWorldAPI/config.py:/usr/src/app/config.py
   ```

2. **Optimisation de l'image** :
   - `--no-cache-dir` pour pip : réduit la taille de l'image
   - Précompilation Python : améliore les performances au démarrage
   - Multi-stage non utilisé ici car application simple

3. **Réseau Docker** : Communication entre services via noms de services (api, http)

4. **Reverse proxy** : Nginx route `/api/*` vers le service Flask

### Commandes utiles mémorisées

```bash
# Construction
sudo docker compose build

# Démarrage
sudo docker compose up -d

# Arrêt
sudo docker compose down

# Logs
sudo docker compose logs -f api
sudo docker compose logs -f http

# Redémarrage d'un service
sudo docker compose restart api

# Liste des images
sudo docker images

# Liste des conteneurs
sudo docker compose ps
```

### Améliorations possibles

- [ ] Utiliser un utilisateur non-root dans le Dockerfile
- [ ] Ajouter un healthcheck
- [ ] Mettre en place des variables d'environnement
- [ ] Créer un .dockerignore pour exclure les fichiers inutiles
- [ ] Utiliser multi-stage build pour réduire la taille de l'image

### Conclusion

✅ Dockerfile créé et fonctionnel
✅ Image Docker construite : `tfriquet/helloworldapi`
✅ Docker Compose configuré avec Nginx en reverse proxy
✅ Configuration externalisée via volume
✅ API testée et opérationnelle sur http://localhost:8080/api/hello

---
