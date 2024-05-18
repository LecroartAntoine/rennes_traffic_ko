import pandas as pd
import requests

class GetData(object):
    def __init__(self, url) -> None:
        """
        Initialise une instance de la classe GetData.

        Args:
            url (str): L'URL de l'API pour récupérer les données de trafic.
        """
        self.url = url

        # Effectue une requête GET pour récupérer les données depuis l'URL
        response = requests.get(self.url)
        # Convertit la réponse JSON en un objet Python
        self.data = response.json()

    def processing_one_point(self, data_dict: dict):
        """
        Traite un point de données de trafic pour le convertir en DataFrame.

        Args:
            data_dict (dict): Un dictionnaire contenant les données d'un point de trafic.

        Returns:
            pd.DataFrame: Un DataFrame contenant les données traitées.
        """
        # Crée un DataFrame temporaire à partir des clés d'intérêt du dictionnaire de données
        temp = pd.DataFrame(
            {
                key: [data_dict[key]]
                for key in [
                    "datetime",
                    "geo_point_2d",
                    "averagevehiclespeed",
                    "traveltime",
                    "trafficstatus",
                ]
            }
        )
        # Renomme la colonne 'trafficstatus' en 'traffic'
        temp = temp.rename(columns={"trafficstatus": "traffic"})
        # Extrait les coordonnées latitude et longitude
        temp["lat"] = temp.geo_point_2d.map(lambda x: x["lat"])
        temp["lon"] = temp.geo_point_2d.map(lambda x: x["lon"])
        # Supprime la colonne 'geo_point_2d' qui n'est plus nécessaire
        del temp["geo_point_2d"]

        return temp

    def __call__(self):
        """
        Récupère et traite toutes les données de trafic.

        Returns:
            pd.DataFrame: Un DataFrame contenant toutes les données de trafic traitées.
        """
        res_df = pd.DataFrame({})  # DataFrame pour stocker les résultats finaux

        # Traite chaque point de données dans les données récupérées
        for data_dict in self.data:
            temp_df = self.processing_one_point(data_dict)  # Traite un point de données
            res_df = pd.concat([res_df, temp_df])  # Concatène les résultats dans le DataFrame final
            res_df = res_df[res_df.traffic != "unknown"]  # Filtre les données avec 'traffic' inconnu

        return res_df
