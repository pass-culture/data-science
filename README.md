# DATA SCIENCE

## Connection aux sources de données

### Matomo

1. Importez votre clé SSH dans votre environnement jupyter à la racine (nom par défaut : id_rsa)

2. Copiez / Collez le fichier `scripts/know_hosts` dans le dossier `.ssh` de votre session

# Installer les dépendances et lancer les tests des scripts

- Créer un environnement virtuel pour lancer le projet

```
# Create the virtual env
virtualenv venv -p /usr/bin/python3.7
# or
python3 -m venv venv
```

- Activer votre environnement virtuel

```
source venv/bin/activate
```

- Installer les dépendances

```
pip install -r requirements.txt
```

- Si besoin, vous pouvez le désactiver plus tard en lançant:

```
deactivate
```

# Configurer un fichier d'environment local

- copier le fichier d'environnement distant:

```
cp .env.dist .env.local
```

- renseigner les valeurs manquantes
- charger les variables d'environnement :

```
 set +a; source .env.local; set -a;
```

- ajouter la python local path :

```
 export PYTHONPATH=$PYTHONPATH:$(pwd)
```
