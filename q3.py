import re
import os
import pandas as pd
from tqdm import tqdm
from q2 import download_audio, cut_audio
from typing import List


def filter_df(csv_path: str, label: str) -> pd.DataFrame:
    """
    Filtre le DataFrame pour inclure uniquement les lignes qui contiennent le label spécifié.
    """
    df = pd.read_csv(csv_path)
    return df[df['positive_labels'].str.contains(label, na=False)]



def data_pipeline(csv_path: str, label: str) -> pd.DataFrame:
    """
    Exécute un pipeline de traitement des données.
    """
    df = filter_df(csv_path, label)
    # Effectue d'autres traitements ici si nécessaire
    return df



import os

def rename_files(path_cut: str, csv_path: str) -> None:
    """
    Renomme les fichiers dans path_cut en utilisant les données du csv_path.
    """
    df = pd.read_csv(csv_path)
    for index, row in df.iterrows():
        yt_id = row['# YTID'].strip()
        start_seconds = row['start_seconds']
        end_seconds = row['end_seconds']
        duration = end_seconds - start_seconds
        old_filename = f"{yt_id}.mp3"
        new_filename = f"{yt_id}_{start_seconds}_{end_seconds}_{duration}.mp3"
        old_file_path = os.path.join(path_cut, old_filename)
        new_file_path = os.path.join(path_cut, new_filename)
        if os.path.isfile(old_file_path):
            os.rename(old_file_path, new_file_path)




if __name__ == "__main__":
    print(filter_df("audio_segments_clean.csv", "Laughter"))
    data_pipeline("audio_segments_clean.csv", "Laughter")
    rename_files("Laughter_cut", "audio_segments_clean.csv")
