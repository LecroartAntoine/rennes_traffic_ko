import plotly.express as px
import numpy as np

def create_figure(data):
    """
    Crée une figure de carte interactive affichant le trafic en temps réel.

    Args:
        data (pd.DataFrame): Un DataFrame contenant les données de trafic, incluant les colonnes 'lat', 'lon', et 'traffic'.

    Returns:
        plotly.graph_objs._figure.Figure: Une figure Plotly représentant la carte du trafic.
    """
    fig_map = px.scatter_mapbox(
        data,
        title="Traffic en temps réel",  # Titre de la carte
        color="traffic",  # Colonne utilisée pour déterminer la couleur des points
        lat="lat",  # Colonne de latitude
        lon="lon",  # Colonne de longitude
        color_discrete_map={"freeFlow": "green", "heavy": "orange", "congested": "red"},  # Couleurs pour les différents états de trafic
        zoom=10,  # Niveau de zoom initial de la carte
        height=500,  # Hauteur de la carte en pixels
        mapbox_style="carto-positron",  # Style de la carte
    )

    return fig_map

def prediction_from_model(model, hour_to_predict):
    """
    Fait une prédiction de l'état du trafic à partir d'un modèle pré-entraîné pour une heure donnée.

    Args:
        model (keras.Model): Un modèle de prédiction pré-entraîné.
        hour_to_predict (str): L'heure pour laquelle faire la prédiction, sous forme de chaîne de caractères.

    Returns:
        int: La catégorie prédite (0: Libre, 1: Dense, 2: Bloqué).
    """
    # Crée un vecteur d'entrée de 24 éléments initialisé à zéro
    input_pred = np.array([0] * 24)
    # Définit l'élément correspondant à l'heure sélectionnée à 1
    input_pred[int(hour_to_predict)] = 1

    # Utilise le modèle pour faire une prédiction et renvoie l'index de la catégorie prédite
    cat_predict = np.argmax(model.predict(np.array([input_pred])))

    return cat_predict
