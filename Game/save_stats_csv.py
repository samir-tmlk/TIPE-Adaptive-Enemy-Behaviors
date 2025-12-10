# save_stats_csv.py

import csv
import os
from datetime import datetime

def save_stats_to_csv(player_name, player_elo, performance, filename="elo_progression.csv"):
    """
    Enregistre dans un CSV le pseudo, l'Elo, le score de performance et la date de fin de chaque partie.
    Si le fichier n'existe pas encore, crée l'en-tête.
    """
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Player Name", "Elo", "Performance"])
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([date_str, player_name, int(player_elo), performance])
