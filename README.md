# data-science
Comment préparer son poste pour l'analyse de données

## Bonnes pratiques :
- Chiffrer son disque dur
- Avoir un compte GitHub avec double identification (et scalingo si tu n'utilises pas GitHub pour t'y connecter)
- Demander l'accès aux applications surscalingo

## Installations préalables

### Brew : 
Utile si tu as un Mac
https://brew.sh/

### Docker
Mac : https://docs.docker.com/docker-for-mac/install/
Linux : https://runnable.com/docker/install-docker-on-linux
Une fois installé, jouer la commande `docker pull postgres`

### Python 3
https://www.python.org/downloads/

### Environnement virtuel python
```
virtualenv venv -p /path/to/python3
source venv/bin/activate
pip install -r requirements.txt
```

## Lancer Jupyter
```
./run-jupyter.sh
```

## Pour plus d'infos
Tuto sur les environnements virtuels en utilisant conda : https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/
