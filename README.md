# data-science
Comment préparer son poste pour l'analyse de données

## Bonnes pratiques :
- Chiffrer son disque dur
- Avoir un compte GitHub avec double identification (et scalingo si tu n'utilises pas GitHub pour t'y connecter)
- Demander l'accès aux applications surscalingo

## Prérequis

### Python 3
https://www.python.org/downloads/

Une fois installé :
```
pip install virtualenv
```

### Docker
- Mac : https://docs.docker.com/docker-for-mac/install/
- Linux : https://runnable.com/docker/install-docker-on-linux

Une fois installé : 
```
docker pull postgres
```

### Brew (utile si tu as un Mac)
- https://brew.sh/

### GEOS 
 ```
 brew install geos 
 ```

## Configuration du projet
```
which python3
virtualenv venv -p /path/to/python3
source venv/bin/activate
pip install -r requirements.txt
nbstripout --install
```
__Attention, il faut absolument exécuter `nbstripout --install` afin qu'à chaque `git add`,
les ouputs ds notebooks soient ignorés.__

## Lancer Jupyter
```
./run-jupyter.sh
```
