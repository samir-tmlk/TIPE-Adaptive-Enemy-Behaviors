# player.py
import pygame
import random
import math
import time
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, level=1):
        super().__init__()
        self.level = level
        self.radius = 25
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.color = BLUE
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.health = 100
        self.max_health = 100
        self.last_attack_time = pygame.time.get_ticks()
        self.is_attacking = False

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= player_speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += player_speed
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= player_speed
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += player_speed

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, height)

        current_time = pygame.time.get_ticks()
        if self.is_attacking and current_time - self.last_attack_time >= attack_cooldown:
            self.is_attacking = False
            self.color = BLUE
            self.draw()

    def attack(self, enemies, evaluator=None):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= attack_cooldown:
            # Enregistrer que le joueur a tenté une attaque
            if evaluator:
                evaluator.record_attack_attempt()
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy_died = enemy.take_damage(20)
                    # Si l'attaque touche un ennemi, enregistrer la réussite
                    if evaluator:
                        evaluator.record_attack_hit()
                        evaluator.record_damage_inflicted(20)
                    if enemy_died:
                        health_recovered = 10 * self.level
                        self.health += health_recovered
                        if self.health > self.max_health:
                            self.health = self.max_health
                        if evaluator:
                            evaluator.record_kill()
            self.last_attack_time = current_time
            self.is_attacking = True
            self.color = RED
            self.draw()

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
