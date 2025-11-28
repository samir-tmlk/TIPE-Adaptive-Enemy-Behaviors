import pygame
import random
import math
from settings import *


# Classe de l'ennemi de base
class EnemyLevel1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)
        self.state = "attack"
        self.health = 100  # Points de vie de l'ennemi
        self.last_attack_time = pygame.time.get_ticks()  # Temps de la dernière attaque

    def update(self, player, other_enemies):
        distance = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)

        # Comportement basé sur les points de vie et la distance au joueur
        if self.health < 30 and distance < 200:  # Si la vie est faible, l'ennemi fuit
            self.state = "flee"
        elif distance < 200:  # Sinon, attaque si le joueur est proche
            self.state = "attack"
            self.attack(player)
        elif self.health < 30 and distance >= 250:
            self.state = "attack"
        else:
            self.state = "idle"

        if self.state == "attack":
            self.move_towards(player)
        elif self.state == "flee":
            self.move_away(player)
        #else:
         #   self.idle_movement()

        # Empêcher les ennemis de sortir du cadre
        self.stay_in_bounds()

        # Empêcher les ennemis de se chevaucher
        self.avoid_collisions(other_enemies)

    def move_towards(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.rect.x += int((dx / distance) * enemy_speed)
            self.rect.y += int((dy / distance) * enemy_speed)

    # L'IA fuit le joueur
    def move_away(self, player):
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.rect.x += int((dx / distance) * enemy_speed)
            self.rect.y += int((dy / distance) * enemy_speed)

    # Empêcher les ennemis de sortir du cadre
    def stay_in_bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.idle_direction = 'right'
        if self.rect.right > width:
            self.rect.right = width
            self.idle_direction = 'left'
        if self.rect.top < 0:
            self.rect.top = 0
            self.idle_direction = 'down'
        if self.rect.bottom > height:
            self.rect.bottom = height
            self.idle_direction = 'up'

    # Empêcher les ennemis de se chevaucher
    def avoid_collisions(self, other_enemies):
        for other_enemy in other_enemies:
            if other_enemy != self and self.rect.colliderect(other_enemy.rect):
                # Calculer le chevauchement entre les rectangles
                overlap_rect = self.rect.clip(other_enemy.rect)
                if overlap_rect.width > overlap_rect.height:
                    if self.rect.centery < other_enemy.rect.centery:
                        self.rect.y -= overlap_rect.height
                    else:
                        self.rect.y += overlap_rect.height
                else:
                    if self.rect.centerx < other_enemy.rect.centerx:
                        self.rect.x -= overlap_rect.width
                    else:
                        self.rect.x += overlap_rect.width

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= attack_cooldown:  # Vérifie si le cooldown est écoulé
            if self.rect.colliderect(player.rect):  # Vérifie si l'ennemi touche le joueur
                player.take_damage(5)  # Inflige 5 points de dégâts
            self.last_attack_time = current_time  # Met à jour le temps de la dernière attaque

    # Méthode pour infliger des dégâts à l'IA
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Supprimer l'ennemi s'il n'a plus de points de vie

class EnemyLevel2(EnemyLevel1):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)
        self.state = "attack"
        self.health = 100  # Points de vie de l'ennemi
        self.last_attack_time = pygame.time.get_ticks()  # Temps de la dernière attaque

    # se déplace vers le joueur
    def move_towards(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.rect.x += int((dx / distance) * enemy_speed)
            self.rect.y += int((dy / distance) * enemy_speed)

    # fuit le joueur
    def move_away(self, player):
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.rect.x += int((dx / distance) * enemy_speed)
            self.rect.y += int((dy / distance) * enemy_speed)

    def update(self, player, other_enemies):
        distance = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)

        # Comportement basé sur les points de vie et la distance au joueur
        if self.health < 30 and distance < 200:  # Si la vie est faible, l'ennemi fuit
            self.state = "flee"
        elif distance < 200:  # Sinon, attaque si le joueur est proche
            self.state = "attack"
            self.attack(player)
        elif self.health < 30 and distance >= 250:
            self.state = "attack"
        else:
            self.state = "idle"

        if self.state == "attack":
            self.move_towards(player)
        elif self.state == "flee":
            self.move_away(player)
        else:
            self.idle_movement()

        # Empêcher les ennemis de sortir du cadre
        self.stay_in_bounds()

        # Empêcher les ennemis de se chevaucher
        self.avoid_collisions(other_enemies)

    # Mouvement aléatoire lorsque l'ennemi est "idle"
    def idle_movement(self):
        if not hasattr(self, 'idle_direction'):
            self.idle_direction = random.choice(['up', 'down', 'left', 'right'])
        # Changer de direction aléatoirement
        if random.random() < 0.02:
            self.idle_direction = random.choice(['up', 'down', 'left', 'right'])

        if self.idle_direction == 'up':
            self.rect.y -= enemy_speed
        elif self.idle_direction == 'down':
            self.rect.y += enemy_speed
        elif self.idle_direction == 'left':
            self.rect.x -= enemy_speed
        elif self.idle_direction == 'right':
            self.rect.x += enemy_speed

    def stay_in_bounds(self):
        # Éviter les bords de la fenêtre
        if self.rect.left < 50:
            self.rect.left = 50
            self.idle_direction = 'right'
        if self.rect.right > width - 50:
            self.rect.right = width - 50
            self.idle_direction = 'left'
        if self.rect.top < 50:
            self.rect.top = 50
            self.idle_direction = 'down'
        if self.rect.bottom > height - 50:
            self.rect.bottom = height - 50
            self.idle_direction = 'up'

    # Empêcher les ennemis de se chevaucher
    def avoid_collisions(self, other_enemies):
        for other_enemy in other_enemies:
            if other_enemy != self and self.rect.colliderect(other_enemy.rect):
                # Calculer le chevauchement entre les rectangles
                overlap_rect = self.rect.clip(other_enemy.rect)
                if overlap_rect.width > overlap_rect.height:
                    if self.rect.centery < other_enemy.rect.centery:
                        self.rect.y -= overlap_rect.height
                    else:
                        self.rect.y += overlap_rect.height
                else:
                    if self.rect.centerx < other_enemy.rect.centerx:
                        self.rect.x -= overlap_rect.width
                    else:
                        self.rect.x += overlap_rect.width

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= attack_cooldown:  # Vérifie si le cooldown est écoulé
            if self.rect.colliderect(player.rect):  # Vérifie si l'ennemi touche le joueur
                player.take_damage(5)  # Inflige 5 points de dégâts
            self.last_attack_time = current_time  # Met à jour le temps de la dernière attaque

    # Méthode pour infliger des dégâts à l'IA
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Supprimer l'ennemi s'il n'a plus de points de vie

class EnemyLevel3(pygame.sprite.Sprite):
    def __init__(self, health, damage, speed, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.damage = damage
        self.health = health
        self.last_attack_time = pygame.time.get_ticks()
        self.combo_mode = False  # Indique si l'ennemi est en mode combo

    def update(self, player, enemies):
        # Vérifier si le joueur est dans une position propice pour un combo
        if self.check_combo_opportunity(player, enemies):
            self.combo_mode = True
            self.execute_combo(player, enemies)
        else:
            self.combo_mode = False
            # Utilisation de la stratégie classique
            best_action = self.select_best_action(player, enemies)
            self.execute_action(best_action, player)
        self.stay_in_bounds()

    def check_combo_opportunity(self, player, enemies):
        """
        Détermine si le joueur est dans une position vulnérable (par exemple dans un coin)
        et s'il est entouré par au moins deux ennemis proches.
        """
        corner_threshold = 150
        # Vérifier si le joueur se trouve dans l'un des coins
        in_corner = ((player.rect.x < corner_threshold and player.rect.y < corner_threshold) or
                     (player.rect.x > width - corner_threshold and player.rect.y < corner_threshold) or
                     (player.rect.x < corner_threshold and player.rect.y > height - corner_threshold) or
                     (player.rect.x > width - corner_threshold and player.rect.y > height - corner_threshold))

        # Compter le nombre d'ennemis proches du joueur
        nearby_enemies = 0
        for enemy in enemies:
            if enemy != self:
                distance = math.hypot(enemy.rect.x - player.rect.x, enemy.rect.y - player.rect.y)
                if distance < 100:
                    nearby_enemies += 1

        return in_corner and nearby_enemies >= 2

    def check_collision(self, dx, dy, enemies):
        simulated_rect = self.rect.copy()
        simulated_rect.x += dx
        simulated_rect.y += dy
        for enemy in enemies:
            if enemy != self and simulated_rect.colliderect(enemy.rect):
                return True
        return False

    def select_best_action(self, player, enemies):
        # Déplacements cardinaux et diagonaux
        actions = [
            (self.speed, 0),
            (-self.speed, 0),
            (0, self.speed),
            (0, -self.speed),
            (self.speed, self.speed),
            (self.speed, -self.speed),
            (-self.speed, self.speed),
            (-self.speed, -self.speed)
        ]
        best_score = float('-inf')
        best_action = (0, 0)

        for dx, dy in actions:
            if not self.check_collision(dx, dy, enemies):
                simulated_x = self.rect.x + dx
                simulated_y = self.rect.y + dy
                score = self.evaluate_position(simulated_x, simulated_y, player, enemies)
                if score > best_score:
                    best_score = score
                    best_action = (dx, dy)

        return best_action

    def evaluate_position(self, x, y, player, enemies):
        distance_to_player = math.hypot(x - player.rect.x, y - player.rect.y)
        score = -distance_to_player

        # Bonus de regroupement pour favoriser les attaques groupées
        grouping_bonus = 0
        for enemy in enemies:
            if enemy != self:
                distance_to_other = math.hypot(x - enemy.rect.x, y - enemy.rect.y)
                if distance_to_other < 100:
                    grouping_bonus += 10
        score += grouping_bonus

        # Pénalités pour éviter de se retrouver bloqué sur les bords
        border_penalty = 0
        close_threshold = 100
        if distance_to_player > close_threshold:
            if x < 50 or x > width - 50:
                border_penalty += 20
            if y < 50 or y > height - 50:
                border_penalty += 20
        score -= border_penalty

        # Ajustement en fonction de la santé de l'ennemi
        if self.health < 30:
            score += distance_to_player
        else:
            score -= distance_to_player

        # Bonus d'enfermement : pousser le joueur dans un coin
        if player.rect.x < 150 and player.rect.y < 150:
            if x < 150 and y < 150:
                score += 30
        elif player.rect.x > width - 150 and player.rect.y < 150:
            if x > width - 150 and y < 150:
                score += 30
        elif player.rect.x < 150 and player.rect.y > height - 150:
            if x < 150 and y > height - 150:
                score += 30
        elif player.rect.x > width - 150 and player.rect.y > height - 150:
            if x > width - 150 and y > height - 150:
                score += 30

        # Blocage des issues pour limiter l'évasion du joueur
        border_zone = 150
        if player.rect.x < border_zone and x < player.rect.x:
            score += 20
        if player.rect.x > width - border_zone and x > player.rect.x:
            score += 20
        if player.rect.y < border_zone and y < player.rect.y:
            score += 20
        if player.rect.y > height - border_zone and y > player.rect.y:
            score += 20

        return score

    def execute_action(self, action, player):
        dx, dy = action
        self.rect.x += dx
        self.rect.y += dy
        self.attack(player)

    def execute_combo(self, player, enemies):
        """
        Mode combo : l'ennemi se repositionne pour isoler le joueur et attaque soudainement.
        """
        # Calcul de l'angle entre l'ennemi et le joueur
        angle = math.atan2(self.rect.y - player.rect.y, self.rect.x - player.rect.x)
        # Position cible à une distance fixée pour encercler le joueur
        target_distance = 150
        target_x = player.rect.x + target_distance * math.cos(angle)
        target_y = player.rect.y + target_distance * math.sin(angle)

        # Calculer le déplacement vers la position cible
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed

        self.rect.x += dx
        self.rect.y += dy

        # Une fois proche du joueur, lancer l'attaque combo
        if self.rect.colliderect(player.rect) or math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery) < 50:
            self.attack(player)

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= attack_cooldown and self.rect.colliderect(player.rect):
            player.take_damage(self.damage)
            self.last_attack_time = current_time

    def stay_in_bounds(self):
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

    def take_damage(self, amount):
        self.health -= amount
        print(f"Ennemi touché ! Santé restante : {self.health}")
        if self.health <= 0:
            print("Ennemi éliminé.")
            self.kill()
            return True  # L'ennemi est mort
        return False  # L'ennemi est toujours en vie
