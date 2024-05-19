from flask import Flask, render_template, request, send_from_directory

from keras.models import load_model
import logging, traceback, time

from src.get_data import GetData
from src.utils import create_figure, prediction_from_model
from src.logger import check_system_metrics, send_error_email, send_metrics_alert

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration du logger
logging.basicConfig(
    filename='error.log',
    level=logging.WARNING,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Création d'une instance de GetData pour récupérer les données du trafic en temps réel
try:
    data_retriever = GetData(
        url="https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/etat-du-trafic-en-temps-reel/exports/json?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    )
    data = data_retriever()
except Exception as e:
    error_message = traceback.format_exc()
    logging.error(error_message)
    send_error_email(error_message)

# Chargement du modèle de prédiction pré-entraîné
try:
    model = load_model("model.h5")
except Exception as e:
    error_message = traceback.format_exc()
    logging.error(error_message)
    send_error_email(error_message)

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            # Si la requête est de type POST, créer la carte du trafic
            fig_map = create_figure(data)
            graph_json = fig_map.to_json()  # Convertir la figure en JSON pour l'affichage sur le front-end

            # Récupérer l'heure sélectionnée par l'utilisateur depuis le formulaire
            selected_hour = request.form["hour"]

            # Faire une prédiction à partir du modèle et de l'heure sélectionnée
            # Mesurer le temps d'exécution de la prédiction
            start_time = time.time()
            cat_predict = prediction_from_model(model, selected_hour)
            end_time = time.time()
            execution_time = end_time - start_time

            if execution_time > 2:
                alert_message = f"prediction_from_model took {execution_time} seconds to execute, exceeding the 2-second threshold."
                logging.warning(alert_message)
                send_metrics_alert("Prediction Execution Time", execution_time, 2)


            try:
                check_system_metrics()
            except Exception as e:
                error_message = traceback.format_exc()
                logging.error(error_message)
                send_error_email(error_message)

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
    except Exception as e:
        error_message = traceback.format_exc()
        logging.error(error_message)
        send_error_email(error_message)
        return "An error occurred. The administrators have been notified."

if __name__ == "__main__":
    # Démarrer l'application Flask en mode debug
    app.run(debug=True)
