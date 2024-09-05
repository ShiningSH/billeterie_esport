# Projet Django

Ce document décrit comment cloner, configurer et lancer ce projet Django, ainsi que comment effectuer des opérations de base comme les migrations et l'ajout de nouvelles entités.

## Prérequis

- Python 3.x
- pip (gestionnaire de paquets Python)
- Git

## Installation

1. Cloner le projet

   Clonez le dépôt Git sur votre machine locale :

```
git clone https://github.com/nom_utilisateur/nom_du_projet.git cd nom_du_projet
````


2. Créer un environnement virtuel

Créez un environnement virtuel pour isoler les dépendances du projet :

```
python -m venv venv
```


3. Activer l'environnement virtuel

- Sur Windows :

  ```
  venv\Scripts\activate
  ```

- Sur macOS/Linux :

  ```
  source venv/bin/activate
  ```

4. Installer les dépendances

Installez les dépendances du projet définies dans le fichier `requirements.txt` :

```
pip install -r requirements.txt
```


## Configuration de la base de données

1. Effectuer les migrations

Pour créer les tables nécessaires à la base de données, exécutez les commandes suivantes :

```
python manage.py makemigrations python manage.py migrate
```


2. Charger les fixtures

Si des fixtures (données pré-enregistrées) sont disponibles, vous pouvez les charger avec :

```
python manage.py loaddata nom_de_la_fixture.json
```


## Lancer le serveur de développement

Pour lancer le serveur de développement Django, exécutez :

```
python manage.py runserver
```


Accédez ensuite au projet via http://127.0.0.1:8000.

## Ajouter des entités et des champs

1. Créer une nouvelle entité (modèle)

   Pour ajouter une nouvelle entité, modifiez le fichier `models.py` de l'application concernée et ajoutez votre modèle :

```py
from django.db import models

class NouvelleEntite(models.Model): nom = models.CharField(max_length=100) description = models.TextField()
```

2. Appliquer les modifications

Une fois vos modifications effectuées, exécutez les commandes suivantes pour appliquer les migrations :

```
python manage.py makemigrations python manage.py migrate
```

3. Ajouter des champs à une entité existante

Modifiez l'entité dans le fichier `models.py` en ajoutant le champ souhaité, puis appliquez les migrations comme décrit ci-dessus.

## Support

Si vous avez des questions ou des problèmes, n'hésitez pas à ouvrir une issue sur le dépôt GitHub.