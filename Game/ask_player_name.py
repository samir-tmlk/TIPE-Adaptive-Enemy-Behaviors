import pygame
import sys

def ask_player_name(screen, width, height):
    """
    Affiche un champ de texte pour que le joueur entre son nom,
    puis renvoie la chaîne de caractères quand il appuie sur Entrée.
    """
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    # Rectangle pour la zone de saisie
    input_box = pygame.Rect(width // 2 - 100, height // 2, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    active = False   # indique si la zone de texte est sélectionnée
    text = ""        # nom en cours de saisie

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier si l'utilisateur clique dans le rectangle
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        # Validation : on retourne le nom
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        # Supprimer le dernier caractère
                        text = text[:-1]
                    else:
                        # Ajouter le nouveau caractère tapé
                        text += event.unicode

        # Effacer l'écran
        screen.fill((255, 255, 255))

        # Afficher le texte dans le rectangle
        txt_surface = font.render(text, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

        # Ajuster la largeur du rectangle si le texte dépasse
        input_box.w = max(200, txt_surface.get_width() + 10)

        # Dessiner le rectangle
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)
