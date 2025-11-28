import pygame
import random
import math
import time
from player import *
from enemy import *


def upgrade_enemies(player_level, enemies_group, player, all_ennemies):
    if len(enemies_group) == 0:
        player.health = 100  # Remettre la santé du joueur à 100 quand tous les ennemis sont tués:
    for enemy in enemies_group:
        enemy.kill()  # Supprimer les anciens ennemis

    # Choisir la classe d'ennemi appropriée en fonction du niveau
    if player_level == 1:
        EnemyClass = EnemyLevel1
    elif player_level == 2:
        EnemyClass = EnemyLevel2
    else :
        EnemyClass = EnemyLevel3

    # Créer de nouveaux ennemis avec la classe appropriée
    for _ in range(3):  # Vous pouvez ajuster le nombre d'ennemis
        new_enemy = EnemyClass()
        enemies_group.add(new_enemy)
        all_enemies.add(new_enemy)

def update_player_level(player_level, enemies_group, player):
    if len(enemies_group) == 0:
        player_level += 1
        upgrade_enemies(player_level, enemies_group)

    return player_level