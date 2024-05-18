from flask import Flask, render_template, request, send_from_directory
import flask_monitoringdashboard as dashboard
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from keras.models import load_model
from src.get_data import GetData
from src.utils import create_figure, prediction_from_model
import os

# Initialisation de l'application Flask
app = Flask(__name__)

# Création d'une instance de GetData pour récupérer les données du trafic en temps réel
data_retriever = GetData(
    url="https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/etat-du-trafic-en-temps-reel/exports/json?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
)

# Récupération des données de trafic
data = data_retriever()

# Chargement du modèle de prédiction pré-entraîné
model = load_model("model.h5")

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Route principale de l'application.
    Gère les requêtes GET et POST pour afficher la carte du trafic et faire des prédictions.
    """
    if request.method == "POST":
        # Si la requête est de type POST, créer la carte du trafic
        fig_map = create_figure(data)
        graph_json = fig_map.to_json()  # Convertir la figure en JSON pour l'affichage sur le front-end

        # Récupérer l'heure sélectionnée par l'utilisateur depuis le formulaire
        selected_hour = request.form["hour"]

        # Faire une prédiction à partir du modèle et de l'heure sélectionnée
        cat_predict = prediction_from_model(model, selected_hour)

        # Dictionnaire pour mapper les catégories de prédiction à des messages et des couleurs
        color_pred_map = {
            0: ["Prédiction : Libre", "green"],
            1: ["Prédiction : Dense", "orange"],
            2: ["Prédiction : Bloqué", "red"],
        }

        # Rendre le template HTML avec les informations de la carte et la prédiction
        return render_template(
            "index.html",
            graph_json=graph_json,
            text_pred=color_pred_map[cat_predict][0],
            color_pred=color_pred_map[cat_predict][1],
        )
    else:
        # Si la requête est de type GET, afficher la carte du trafic sans prédiction
        fig_map = create_figure(data)
        graph_json = fig_map.to_json()  # Convertir la figure en JSON pour l'affichage sur le front-end

        # Rendre le template HTML avec seulement la carte du trafic
        return render_template("index.html", graph_json=graph_json)

if __name__ == "__main__":
    # Lier le dashboard de monitoring à l'application Flask
    dashboard.bind(app)
    # Démarrer l'application Flask en mode debug
    app.run(debug=True)
