import pygame
import random
import math
import time

# Dimensions de la fenêtre
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Vitesse du joueur et de l'ennemi
player_speed = 10
enemy_speed = 8
attack_cooldown = 1000  # Délai d'attaque
enemy_attack_cooldown = 1000  # Délai d'attaque des ennemis