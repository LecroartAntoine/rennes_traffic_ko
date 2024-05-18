Guide d'Utilisation de l'Application de Surveillance du Trafic de Rennes
=======================================================================

Bienvenue dans l'application de surveillance du trafic de Rennes ! Cette application vous permet de visualiser en temps réel les données de trafic et d'obtenir des prédictions sur l'état de la circulation dans le centre-ville. Suivez ces étapes simples pour utiliser l'application :

1. Création de l'Environnement Virtuel

Avant de commencer, nous vous recommandons de créer un environnement virtuel pour isoler les dépendances de cette application. Voici comment procéder :

.. code-block:: bash

    # Créer un environnement virtuel nommé 'venv'
    python -m venv venv

    # Activer l'environnement virtuel
    # Sur Windows
    venv\Scripts\activate
    # Sur macOS/Linux
    source venv/bin/activate

2. Installation des Dépendances

Une fois que l'environnement virtuel est activé, vous devez installer les dépendances nécessaires à l'application en utilisant le fichier requirements.txt. Assurez-vous d'être dans le répertoire racine de l'application où se trouve ce fichier.

.. code-block:: bash

    pip install -r requirements.txt


3. Accès à l'Application

Pour accéder à l'application, vous devez exécuter le script Python qui lance le serveur web.

.. code-block:: bash

    python app.py


Après avoir exécuté le script, l'application sera accessible via un navigateur web à l'adresse : http://localhost:5000/

4. Visualisation des Données de Trafic

Une fois que vous avez accédé à l'application, vous verrez une carte interactive affichant les données de trafic de Rennes en temps réel. Vous pouvez zoomer, déplacer la carte pour explorer différentes régions de la ville.

5. Prédiction de l'État de la Circulation

Pour obtenir une prédiction sur l'état de la circulation dans le centre-ville pour une heure spécifique, suivez ces étapes :

    Dans la section "Prédiction d'embouteillage pour le centre-ville", sélectionnez une heure à partir du menu déroulant. Les heures sont répertoriées de 0h à 23h.
    Cliquez sur le bouton "Envoyer".
    Une fois la requête envoyée, vous verrez s'afficher une prédiction concernant l'état de la circulation pour l'heure sélectionnée. La prédiction sera accompagnée d'un texte indiquant si la circulation est libre, dense ou bloquée, ainsi que d'une couleur correspondante pour une meilleure visualisation.

6. Arrêt de l'Application

Lorsque vous avez terminé d'utiliser l'application, vous pouvez arrêter le serveur en appuyant sur Ctrl + C dans le terminal où le script Python est en cours d'exécution.

Profitez de l'application de surveillance du trafic de Rennes pour obtenir des informations précieuses sur l'état de la circulation et planifier vos déplacements de manière plus efficace ! Si vous avez des questions ou des commentaires, n'hésitez pas à nous contacter.