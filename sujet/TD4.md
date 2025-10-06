# TD4 - image personnalisée

Nous souhaitons créer notre propre image de notre application serveur.

Pour cela nous allons créer notre propre descripteur d'image, le fichier Dockerfile, puis fabriquer notre image localement.

Cette image s'appuiera sur l'image de base de l'interpreteur Python, et incluera :
- les bibliothèques nécessaires à notre application serveur
- le code de l'application serveur lui-même.

L'image sera configurée pour executer par défaut notre application serveur.

## 1 récupération du code source de l'application

Récupérez le projet Python fournit dans les ressources du TD. 

https://git.univ-lemans.fr/mmi3-dwebdi/my-train-auto-history


Observez l'application : 
- y-a-t'il un descripteur des biliothèques nécessaires à son fonctionnement ? 
- Quelle commande connaissez-vous qui permettrait d'installer ces dépendances ?
- Quelle commande connaissez-vous pour lancer le serveur python ?

## 2 Préparation du Dockerfile

### Rappels et explications succintes du Dockerfile

Créer dans votre dossier projet un fichier Dockerfile.

Le fichier Dockerfile permet de décrire les étapes de construction d'une image Docker. 

Rappel : Pour créer une image, docker exécutera un conteneur avec comme image de base celle sur laquelle s'apuie le Dockerfile puis y exécutera les différentes actions du Dockerfile. Il en résultera la création d'une ou plusieurs couches (layer). Si l'ensemble des opérations se déroulent correctement, Docker finalisera l'image sur la backe des layers de l'image de base et de l'ensemble des layers créés.

Dans un dockerfile, chaque étape est une action décrite par un mot-clé en majuscule (ex.: COPY, LABEL, RUN) suivit d'un ou plusieurs paramètres.

Certaines de ces actions ne font qu'ajouter des métadonnées à l'image (ex.: LABEL ajouter des information clé-valeur à l'image), et d'autre modifient le SGF de l'image (ex.: COPY qui copie des données de l'hôte dans l'image, RUN qui exécute une commande au sein du conteneur à la création de l'image). Les actions qui ont un impact sur le SGF génère un nouveau layer.

Vous pouvez retrouver toutes les commandes posssible dans un Docker file à cette adresse :  https://docs.docker.com/engine/reference/builder/

### Instructions de l'image à créer

Vous devez définir votre Dockerfile pour réaliser les actions suivantes (dans cette ordre) :

- l'image de base sur laquelle s'appuyer est python:3.11
- 3 labels doivent être ajoutés :
  - version : 1.0
  - maintainer : votre adresse mail universitaire
  - description : "My Train Autohistory server"
- répertoire de travail courant : /usr/src/app
- copie du descripteur de dépendances du serveur du projet dans le repertoire courant
- installation des dépendances. Par souci d'optimisation, nous veillerons à ce qu'aucun cache ne soit utilisé pour limiter la taille de notre image.
- copie de l'ensensemble du code source relatif au serveur dans le répertoire courant
- génération des fichiers précompilés (pycache) pour optimiser l'exécution
- définition du point d'entrée de l'image comme l'exécution du script de lancement du serveur. Pour cela consultez la docummentation des instructions COMMAND et ENTRYPOINT du Dockerfile pour savoir laquelle semble la mieux indiquée pour notre usage.

### Description du service dans le docker compose.

Créez un fichier docker-compose et déclarez-y le service __api__.

Ce dernier ne s'appuie donc pas sur une image d'un repository mais sur votre propre descripteur d'image Dockerfile que vous venez de créér. Pour spécifiez cette information, utilisez les propriétés build -> context pour spécifier le chemin relatif du dossier où se trouve le fichier Dockerfile. Spécifiez également un nom d'image pour maitriser le nom généré (ex: image: rvenant/helloWorldAPI)

Restez-en là pour l'instant, nous compléterons les propriétés de ce service plus tard.

### Fabrication de l'image

la commande `docker compose build` permet de créer toutes les images des services qui s'appuient sur un descripteur Dockerfile.

Exécutez cette commande et assurez-vous que l'image soit bien créée.

### Complétion du descripteur de service

Editez votre fichier docker-compose.yml pour compléter les information de votre service api :

- Ajoutez un service HTTP nginx pour agir comme un _reverse proxy_ vers votre service __api__. Adaptez la configuration de votre service http pour permettre de relayer toutes les requêtes http vers /api/* à votre service __api__.

- Le fonctionneemnt du serveur python est configuré par un fichier de configuration .py donné dans le code source. Trouvez un moyen de ne pas à avoir à refaire l'image à chaque changement de la configuration

Lancez la pile et testez la connexion entre un navigateur, le service http et le service api.

#### Exemples de requêtes REST

Message de bienvenue

```
GET /api/hello

{
"message": "Hello World!"
}
```


