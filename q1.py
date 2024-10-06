import json
import pandas as pd


def count_labels(labels: str) -> int:
    """
    Étant donné une chaine de charactères d'étiquettes non traitées, retourne le nombre d'étiquettes distinctes.

    Par exemple:
    "/m/04rlf,/m/06_fw,/m/09x0r" -> 3
    """
    # TODO

    # Vérifier si la chaîne est vide
    if not labels:
        return 0

    # Séparer la chaîne par des virgules et enlever les espaces éventuels
    etiquettes = labels.split(',')
    
    # Supprimer les étiquettes vides éventuelles (si la chaîne contient ",,")
    etiquettes = [etiquette.strip() for etiquette in etiquettes if etiquette.strip()]

    # Utiliser un set pour obtenir les étiquettes distinctes
    etiquettes_distinctes = set(etiquettes)
    
    # Retourner le nombre d'étiquettes distinctes
    return len(etiquettes_distinctes)


def convert_id(ID: str) -> str:
    """
    Créez une fonction qui prend un ID d'étiquette (par exemple "/m/09x0r") et renvoie le nom d'étiquette correspondant (par exemple "Speech")

    Pour ce faire, utilisez la bibliothèque `json` et le fichier `data/ontology.json`, une description du fichier peut être trouvée
    sur https://github.com/audioset/ontology

    Même si lire le fichier à chaque fois et parcourir les éléments pour trouver une correspondance fonctionne assez bien dans notres cas.
    Pensez à des moyens d'accélérer ce processus si, par exemple, cette fonction devait être exécutée 100 000 fois.
    """
    # TODO
    with open('data/ontology.json', 'r') as f:
        ontology = json.load(f)
    
    # Dictionnaire pour associer les IDs aux noms d'étiquettes
    id_to_label = {item['id']: item['name'] for item in ontology}
    
    # Rechercher l'ID dans le dictionnaire et retourner le nom correspondant
    return id_to_label.get(ID, "Unknown")


def convert_ids(labels: str) -> str:
    """
    À l'aide de convert_id(), créez une fonction qui prend les colonnes d'étiquettes (c'est-à-dire une chaîne de charactères d'ID d'étiquettes séparées par des virgules)
    et renvoie une chaîne de noms d'étiquettes, séparés par des tubes "|".

    Par exemple:
    "/m/04rlf,/m/06_fw,/m/09x0r" -> "Musique|Skateboard|Discours"
    """
    # TODO
    # Séparer la chaîne d'ID par des virgules pour obtenir une liste
    id_list = labels.split(',')
    
    # Utiliser convert_id() pour chaque ID et obtenir les noms correspondants
    label_names = [convert_id(id.strip()) for id in id_list]
    
    # Joindre les noms d'étiquettes avec le séparateur "|"
    return '|'.join(label_names)


import pandas as pd

def contains_label(labels: pd.Series, label: str) -> pd.Series:
    """
    Crée une fonction qui prend une pandas Series de chaînes de caractères
    et renvoie une pandas Series avec juste les valeurs qui incluent `label`.
    """
    return labels[labels.str.contains(label, na=False)]





def get_correlation(labels: pd.Series, label_1: str, label_2: str) -> float:
    """
    Calcule la corrélation entre deux labels dans une pandas Series formatée.
    """
    filtered_labels = labels[labels.str.contains(label_1) | labels.str.contains(label_2)]
    label_1_series = filtered_labels.str.contains(label_1).astype(int)
    label_2_series = filtered_labels.str.contains(label_2).astype(int)
    return label_1_series.corr(label_2_series)



if __name__ == "__main__":
    print(count_labels("/m/04rlf,/m/06_fw,/m/09x0r"))
    print(convert_id("/m/04rlf"))
    print(convert_ids("/m/04rlf,/m/06_fw,/m/09x0r"))

    series = pd.Series([
        "Music|Skateboard|Speech",
        "Voice|Speech",
        "Music|Piano"
    ])
    print(contains_label(series, "Music"))
    print(get_correlation(series, "Music", "Piano"))
