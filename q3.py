import re
import os
import pandas as pd
from tqdm import tqdm
from q2 import download_audio, cut_audio
from typing import List


import pandas as pd

def data_pipeline(df: pd.DataFrame, label: str) -> pd.DataFrame:
    """
    Exécute un pipeline de traitement des données.

    Parameters:
    df : pd.DataFrame - DataFrame à traiter.
    label : str - Label à filtrer.

    Returns:
    pd.DataFrame - DataFrame filtré avec les corrélations.
    """
    filtered_df = filter_df(df, label)  # Appelle la fonction filter_df()
    correlations = get_correlation(filtered_df, label_1, label_2)  # Assure-toi de passer les bons labels
    return filtered_df, correlations




def filter_df(csv_path: str, label: str) -> List[str]:
    """
    Écrivez une fonction qui prend le path vers le csv traité (dans la partie notebook de q1) et renvoie un df avec seulement les rangées qui contiennent l'étiquette `label`.

    Par exemple:
    get_ids("audio_segments_clean.csv", "Speech") ne doit renvoyer que les lignes où l'un des libellés est "Speech"
    """
    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(csv_path)
    
    # Filtrer les lignes contenant l'étiquette
    filtered_df = df[df['positive_labels'].str.contains(label, na=False)]
    
    # Retourner les IDs ou une autre colonne souhaitée
    return filtered_df['# YTID'].tolist()  # Remplace '# YTID' par la colonne appropriée si nécessaire



def rename_files(path_cut: str, csv_path: str) -> None:
    """
    Renomme les fichiers dans path_cut en utilisant les données du csv_path.

    Renomme les fichiers de "<ID>.mp3" à "<ID>_<start_seconds_int>_<end_seconds_int>_<length_int>.mp3".
    
    Parameters:
    path_cut : str - chemin vers le dossier avec les fichiers audio.
    csv_path : str - chemin vers le fichier CSV contenant les informations de temps.
    """
    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(csv_path)

    # Parcourir chaque ligne du DataFrame
    for index, row in df.iterrows():
        # Extraire l'ID, start_seconds, end_seconds et duration
        yt_id = row['# YTID'].strip()  # Assurez-vous d'enlever les espaces
        start_seconds = row['start_seconds']
        end_seconds = row['end_seconds']
        duration = end_seconds - start_seconds  # Calculer la durée

        # Construire le nouveau nom de fichier
        old_filename = f"{yt_id}.mp3"
        new_filename = f"{yt_id}_{start_seconds}_{end_seconds}_{duration}.mp3"

        # Chemin complet pour l'ancien et le nouveau fichier
        old_file_path = os.path.join(path_cut, old_filename)
        new_file_path = os.path.join(path_cut, new_filename)

        # Renommer le fichier si l'ancien fichier existe
        if os.path.isfile(old_file_path):
            os.rename(old_file_path, new_file_path)



if __name__ == "__main__":
    print(filter_df("audio_segments_clean.csv", "Laughter"))
    data_pipeline("audio_segments_clean.csv", "Laughter")
    rename_files("Laughter_cut", "audio_segments_clean.csv")
