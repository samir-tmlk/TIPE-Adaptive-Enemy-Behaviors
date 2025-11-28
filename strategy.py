# strategy.py

import random
import math
import pygame
from settings import enemy_speed, width, height, enemy_attack_cooldown

class BaseStrategy:
    def __init__(self, enemy):
        self.enemy = enemy

    def check_collision(self, dx, dy, others):
        """
        Simule un déplacement (dx, dy) et renvoie True s'il entre en collision avec un autre ennemi.
        """
        simulated = self.enemy.rect.copy()
        simulated.x += dx
        simulated.y += dy
        for other in others:
            if other is not self.enemy and simulated.colliderect(other.rect):
                return True
        return False

    def try_move(self, dx, dy, others):
        """
        Déplace l'ennemi uniquement si cela ne cause pas de collision.
        """
        if not self.check_collision(dx, dy, others):
            self.enemy.rect.x += dx
            self.enemy.rect.y += dy

    def try_attack(self, player):
        """
        Attaque le joueur si le cooldown est écoulé.
        """
        now = pygame.time.get_ticks()
        if now - self.enemy.last_attack_time >= enemy_attack_cooldown:
            self.enemy.attack(player)

    def finalize(self, others):
        """
        Après déplacement + attaque, on applique stay_in_bounds et avoid_collisions
        pour rattraper les petits cas limites.
        """
        if hasattr(self.enemy, 'stay_in_bounds'):
            self.enemy.stay_in_bounds()
        if hasattr(self.enemy, 'avoid_collisions'):
            self.enemy.avoid_collisions(others)

    def update(self, player, others):
        raise NotImplementedError


class ImmobileStrategy(BaseStrategy):
    def update(self, player, others):
        # N'attaque que si le joueur est à portée
        dx = player.rect.centerx - self.enemy.rect.centerx
        dy = player.rect.centery - self.enemy.rect.centery
        dist = math.hypot(dx, dy)

        if dist < 200:
            self.try_attack(player)

        self.finalize(others)


class RandomWalkStrategy(BaseStrategy):
    def __init__(self, enemy):
        super().__init__(enemy)
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def update(self, player, others):
        # Changer de direction aléatoirement
        if random.random() < 0.02:
            self.direction = random.choice(['up', 'down', 'left', 'right'])

        dx = dy = 0
        if self.direction == 'up':    dy = -enemy_speed
        elif self.direction == 'down':dy =  enemy_speed
        elif self.direction == 'left':dx = -enemy_speed
        else:                         dx =  enemy_speed

        # Déplacement si pas de collision
        self.try_move(dx, dy, others)
        # Attaque si possible
        self.try_attack(player)
        # Finalisation
        self.finalize(others)


class GroupAttackStrategy(BaseStrategy):
    def update(self, player, others):
        # Calcul du point cible (entre joueur et centre de groupe)
        if others:
            avg_x = sum(e.rect.centerx for e in others) / len(others)
            avg_y = sum(e.rect.centery  for e in others) / len(others)
            target_x = (player.rect.centerx + avg_x) / 2
            target_y = (player.rect.centery  + avg_y) / 2
        else:
            target_x = player.rect.centerx
            target_y = player.rect.centery

        dx = target_x - self.enemy.rect.centerx
        dy = target_y - self.enemy.rect.centery
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx = int((dx / dist) * enemy_speed)
            dy = int((dy / dist) * enemy_speed)

        # Déplacement si pas de collision
        self.try_move(dx, dy, others)
        # Attaque si possible
        self.try_attack(player)
        # Finalisation
        self.finalize(others)
