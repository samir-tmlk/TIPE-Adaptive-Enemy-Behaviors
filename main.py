# main.py

import pygame, random, time, sys
from settings                import *
from player                  import Player
from performance_evaluator   import PerformanceEvaluator
from ask_player_name         import ask_player_name
from save_stats_csv          import save_stats_to_csv
from difficulty_manager      import DifficultyManager
from enemy_factory           import EnemyFactory
import settings              # pour ajuster enemy_speed

# — Initialisation Pygame —
pygame.init()

# — Demande du pseudo AVANT tout —
player_name = ask_player_name(screen, width, height)

# — Création du manager et de la factory (UNE SEULE FOIS) —
dm      = DifficultyManager(player_name)
factory = EnemyFactory(dm)

# — Créer le joueur + évaluateur —
player                = Player(level=1)
performance_evaluator = PerformanceEvaluator(player)

# — S’assurer que enemy_speed ne dépasse pas player_speed —
if settings.enemy_speed > player_speed:
    settings.enemy_speed = player_speed

# — Groupes de sprites —
all_sprites = pygame.sprite.Group(player)
enemies     = pygame.sprite.Group()

# — Vague initiale (3 ennemis) —
for e in factory.create_enemies():
    # clamp speed si nécessaire
    if hasattr(e, 'speed') and e.speed > player_speed:
        e.speed = player_speed
    enemies.add(e)
    all_sprites.add(e)

game_over   = False
stats_saved = False
clock       = pygame.time.Clock()

while True:
    clock.tick(60)
    screen.fill(WHITE)

    # — Événements —
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Déplacements → évaluer la précision
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                dx = dy = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:  dx -= player_speed
                if keys[pygame.K_RIGHT]: dx += player_speed
                if keys[pygame.K_UP]:    dy -= player_speed
                if keys[pygame.K_DOWN]:  dy += player_speed
                performance_evaluator.evaluate_move_precision(player, enemies, (dx, dy))

            if game_over:
                # Recommencer (R)
                if event.key == pygame.K_r:
                    # Ne pas recréer dm ni factory !
                    player = Player(level=1)
                    player.health = player.max_health
                    performance_evaluator = PerformanceEvaluator(player)
                    all_sprites.empty()
                    all_sprites.add(player)
                    enemies.empty()

                    # Nouvelle vague
                    for e in factory.create_enemies():
                        # Clamp de la vitesse au maximum du joueur
                        if hasattr(e, 'speed') and e.speed > player_speed:
                            e.speed = player_speed

                        enemies.add(e)
                        all_sprites.add(e)

                    game_over   = False
                    stats_saved = False

                # Quitter (Q)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            else:
                # Attaque (Espace)
                if event.key == pygame.K_SPACE:
                    player.attack(enemies, performance_evaluator)
                # Quitter mid-game (Q)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    # — Logique de jeu —
    if not game_over:
        if player.health > 0:
            # Mettre à jour le joueur
            keys = pygame.key.get_pressed()
            player.update(keys)

            # Mettre à jour chaque ennemi via sa strategy
            enemies.update(player, enemies)

            # Vague terminée ?
            if len(enemies) == 0:
                # Menu Victoire
                font = pygame.font.Font(None, 40)
                msg1 = font.render("Bravo ! Tous les ennemis sont morts.", True, BLACK)
                msg2 = font.render("C=Continuer  S=Sauver  Q=Quitter",   True, BLACK)
                screen.blit(msg1, (width//2 - 250, height//2 - 30))
                screen.blit(msg2, (width//2 - 200, height//2 + 10))
                pygame.display.flip()

                # Choix
                while True:
                    ev = pygame.event.wait()
                    if ev.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_c:
                            # Victoire → mise à jour Elo
                            result = 1.0
                            pm     = performance_evaluator.get_performance_multiplier()
                            dm.update_elo(result, pm)
                            player.health = player.max_health
                            # Reset stats & nouvelle vague
                            performance_evaluator.reset_stats()
                            all_sprites = pygame.sprite.Group(player)
                            enemies.empty()
                            for e in factory.create_enemies():
                                # Clamp de la vitesse au maximum du joueur
                                if hasattr(e, 'speed') and e.speed > player_speed:
                                    e.speed = player_speed

                                enemies.add(e)
                                all_sprites.add(e)
                            break

                        elif ev.key == pygame.K_s:
                            current_elo  = dm.player_elo
                            current_perf = performance_evaluator.evaluate()
                            save_stats_to_csv(player_name, current_elo, current_perf)

                        elif ev.key == pygame.K_q:
                            pygame.quit(); sys.exit()

            else:
                # Affichage HUD
                font = pygame.font.Font(None, 36)
                screen.blit(font.render(f"Elo Joueur: {int(dm.player_elo)}", True, BLACK), (10,  10))
                screen.blit(font.render(f"Elo Ennemi:  {int(dm.enemy_elo)}",  True, BLACK), (10,  50))
                screen.blit(font.render(f"Health:     {player.health}",     True, BLACK), (10,  90))
                screen.blit(font.render(f"Perf:       {int(performance_evaluator.evaluate())}", True, BLACK), (10, 130))

                all_sprites.draw(screen)

        else:
            # Passage en Game Over
            game_over   = True
            final_score = performance_evaluator.evaluate()

    else:
        # Écran Game Over
        font = pygame.font.Font(None, 74)
        screen.blit(font.render("GAME OVER", True, RED), (width//2 - 150, height//2 - 50))

        sf = pygame.font.Font(None, 36)
        screen.blit(sf.render("R=Recommencer  Q=Quitter", True, BLACK), (width//2 - 180, height//2 + 10))
        screen.blit(sf.render(f"Score:       {int(final_score)}", True, BLACK), (width//2 - 100, height//2 + 60))
        screen.blit(sf.render(f"Précision:   {performance_evaluator.get_attack_accuracy():.1f}%", True, BLACK), (width//2 - 100, height//2 + 100))
        screen.blit(sf.render(f"Err. avg:    {performance_evaluator.get_average_move_error():.2f}", True, BLACK), (width//2 - 100, height//2 + 140))

        # Mise à jour Elo sur défaite (une seule fois)
        if not stats_saved:
            result = 0.0
            pm     = performance_evaluator.get_performance_multiplier()
            dm.update_elo(result, pm)
            stats_saved = True

    pygame.display.flip()
