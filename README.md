# Library

**Le projet n'est pas encore fini !**

Ce guide explique comment pouvoir lancer ce logiciel sur votre ordinateur

## Prérequis
Avant de commencer, assurez-vous que vous avez installé les éléments suivants sur votre système :

- [MAMP](https://www.mamp.info/en/downloads/): Un serveur pour exécuter du SQL.

- [Python](https://www.python.org/downloads/): Le langage de programmation utilisé par ce logiciel.

## Instructions

1. Clonez le référentiel :

   ```bash
   git clone https://github.com/Saadiinho/Library.git

2. Ouvrez votre terminal ou invite de commande.
  
3. Vérifiez que vous avez bien installé Python :

   ```bash
   python --version

4. Accédez au répertoire contenant le fichier .py en utilisant la commande `cd` (change directory). Par exemple, si le fichier est dans le dossier "mon_projet", vous pouvez entrer :

   ```bash
   cd chemin/vers/mon_projet

5. Lancer MAMP et accéder à phpMyAdmin
   
6. Créez une base de données nommé library et importez dans cette base de données le fichier library.sql

7. Lancez le code en entrant la commande suivante dans votre terminal :

   ```bash
   python main.py

Il ne vous reste plus qu'à profiter de ce logiciel de gestion de bibliothèque !
