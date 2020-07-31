## Recommandations d'offres pour le pass Culture

### Installer le package
``python setup.py bdist_wheel
``
Cela crée un dossier `dist/` à la racine du projet.
Pour installer le package sur un environnement, il suffit de l'activer et de faire la commande suivante : 
``
cd passculture_recommendation_toolbox
pip install ./dist/name_of_the_package.whl
``

### Configuration du projet
``
conda create --name pc-recommendation
``

``
pip3 install -r requirements.txt
``

``
cd passculture_recommendation_tools
``

``
pip3 install -e .
``
### Lancer Jupyter 
``
cd ..
``

``
jupyter notebook
``
