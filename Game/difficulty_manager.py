# difficulty_manager.py

import json
import os
import math

class DifficultyManager:
    """
    Elo adaptatif avec :
     - K_n dynamique ≈ K_base / n_parties (formule USCF simplifiée)
     - lissage EMA : r_{n+1} = α·r_obs + (1−α)·r_n
    """

    def __init__(self, player_name, filepath='elo_ratings.json',
                 initial_elo=1000, k_factor=100):
        self.player_name   = player_name
        self.filepath      = filepath
        self.k             = k_factor      # K_max
        self.games_played  = 0

        # charger ou init fichier JSON
        if os.path.isfile(self.filepath):
            with open(self.filepath, 'r') as f:
                self._data = json.load(f)
        else:
            self._data = {}

        # Elo du joueur et de l'ennemi
        self.player_elo = self._data.get(self.player_name, initial_elo)
        self.enemy_elo  = self.player_elo

    def _save(self):
        self._data[self.player_name] = self.player_elo
        with open(self.filepath, 'w') as f:
            json.dump(self._data, f, indent=4)

    def expected_score(self, ra, rb):
        """E[score] = 1/(1+10^((rb−ra)/400))."""
        return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))

    def update_elo(self, player_result, performance_multiplier=1.0):
        """
        player_result ∈ {0.0, 1.0}
        performance_multiplier pour ajuster K_base = k * mult
        """
        # incrémenter le nombre de parties
        self.games_played += 1

        # score attendu
        e = self.expected_score(self.player_elo, self.enemy_elo)

        # K_base ajusté par performance
        k_base = self.k * performance_multiplier

        # K dynamique USCF simplifié
        k_n = k_base / self.games_played

        # Elo observé (Elo classique)
        r_obs = self.player_elo + k_n * (player_result - e)

        # alpha pour le lissage EMA, limité à [0, 1]
        alpha = max(0.0, min(1.0, k_n / self.k))

        # mise à jour lissée
        new_elo = alpha * r_obs + (1 - alpha) * self.player_elo

        # delta appliqué aux deux Elo
        delta = new_elo - self.player_elo
        self.player_elo += delta
        self.enemy_elo  += delta

        # persister l'Elo du joueur
        self._save()

    def get_level(self):
        """Retourne 1, 2 ou 3 selon le palier de l'Elo joueur."""
        if self.player_elo < 900:
            return 1
        elif self.player_elo < 1100:
            return 2
        else:
            return 3
