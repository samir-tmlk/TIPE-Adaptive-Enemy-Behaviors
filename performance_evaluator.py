# performance_evaluator.py

import pygame
import math
from settings import player_speed, width, height

class PerformanceEvaluator:
    def __init__(self, player,
                 max_enemies: int = 3,
                 time_ref: float = 30.0,
                 epsilon: float = 1e-6,
                 w_kill: float = 0.4,
                 w_damage: float = 0.3,
                 w_time: float = 0.2,
                 w_accuracy: float = 0.1):
        """
        player       : l’instance Player
        max_enemies  : nombre max d’ennemis possibles (pour normaliser les kills)
        time_ref     : temps de référence (sec) pour le bonus rapidité
        epsilon      : pour éviter la division par zéro
        w_*          : poids pour each composante, doivent idéalement sommer à 1.0
        """
        self.player     = player
        self.max_enemies= max_enemies
        self.time_ref   = time_ref
        self.epsilon    = epsilon

        # Poids (kills, damage, time, accuracy)
        self.w_kill     = w_kill
        self.w_damage   = w_damage
        self.w_time     = w_time
        self.w_accuracy = w_accuracy

        self.reset_stats()
        self.start_time = pygame.time.get_ticks()

    def reset_stats(self):
        self.enemies_killed     = 0
        self.damage_inflicted   = 0
        self.damage_taken       = 0
        self.attacks_attempted  = 0
        self.attacks_hit        = 0
        self.total_move_error   = 0.0
        self.move_count         = 0

    # Enregistrement des événements de combat
    def record_kill(self):               self.enemies_killed    += 1
    def record_damage_inflicted(self,a): self.damage_inflicted  += a
    def record_damage_taken(self,a):     self.damage_taken      += a
    def record_attack_attempt(self):     self.attacks_attempted += 1
    def record_attack_hit(self):         self.attacks_hit       += 1

    def get_attack_accuracy(self):
        if self.attacks_attempted == 0:
            return 0.0
        return self.attacks_hit / self.attacks_attempted

    # (On conserve cette méthode si besoin d'évaluer la précision de mouvement)
    def evaluate_move_precision(self, player, enemies, move_vector):
        # … (inchangé) …
        pass

    def get_average_move_error(self):
        if self.move_count == 0:
            return 0.0
        return self.total_move_error / self.move_count

    def evaluate(self) -> float:
        """
        Challenge Function normalisée :
          Perf = w₁·(kills/Nₘₐₓ)
               + w₂·(D_out/(D_out+D_in+ε))
               + w₃·max(0,1 - t/t_ref)
               + w₄·(hits/attempts)
        Retourne un score ∈ [0,1] si w₁+…+w₄ = 1.
        """
        # 1) Temps en secondes
        t = (pygame.time.get_ticks() - self.start_time) / 1000.0

        # 2) Composantes normalisées
        kill_norm     = min(self.enemies_killed / self.max_enemies, 1.0)
        damage_norm   = self.damage_inflicted / (self.damage_inflicted + self.damage_taken + self.epsilon)
        time_norm     = max(0.0, 1.0 - (t / self.time_ref))
        acc_norm      = self.get_attack_accuracy()

        # 3) Moyenne pondérée
        perf = (
            self.w_kill     * kill_norm +
            self.w_damage   * damage_norm +
            self.w_time     * time_norm +
            self.w_accuracy * acc_norm
        )
        return perf

    def get_performance_multiplier(self,
                                   min_mult: float = 0.5,
                                   max_mult: float = 1.5) -> float:
        """
        Mappe le score ∈ [0,1] sur [min_mult, max_mult] linéairement :
          α = min_mult + perf·(max_mult - min_mult)
        """
        perf = self.evaluate()
        return min_mult + perf * (max_mult - min_mult)
