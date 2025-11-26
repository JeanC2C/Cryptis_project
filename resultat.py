import pygame
import sys

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

COLOR_BG = (18, 18, 22)
COLOR_PANEL = (36, 30, 45)
COLOR_WIN = (90, 200, 110)      # vert victoire
COLOR_LOSE = (255, 90, 90)      # rouge défaite
COLOR_TEXT = (240, 240, 240)


def afficher_resultat(result_type: str):
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Cryptis – Résultat")

    font_title = pygame.font.Font(None, 90)
    font_text = pygame.font.Font(None, 50)
    font_small = pygame.font.Font(None, 36)

    if result_type == "joueur":
        title_text = "BRAVO !"
        line1 = "Tu as cassé la clé"
        line2 = "avant la machine."
        color_main = COLOR_WIN
    elif result_type == "ai":
        title_text = "OUPS..."
        line1 = "La machine a terminé"
        line2 = "avant toi."
        color_main = COLOR_LOSE
    else:
        title_text = "FIN DE LA PARTIE"
        line1 = "La manche est terminée."
        line2 = ""
        color_main = COLOR_TEXT

    running = True
    alpha_bg = 0

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # n'importe quelle touche ou clic -> quitter
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        # fond
        screen.fill(COLOR_BG)

        # petit effet de fade sur un panneau central
        if alpha_bg < 230:
            alpha_bg += 10

        panel_width, panel_height = 700, 350
        panel = pygame.Surface((panel_width, panel_height))
        panel.fill(COLOR_PANEL)
        panel.set_alpha(min(alpha_bg + 25, 255))
        panel_rect = panel.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(panel, panel_rect)

        # titre
        title_surface = font_title.render(title_text, True, color_main)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        screen.blit(title_surface, title_rect)

        # lignes de texte
        text1_surface = font_text.render(line1, True, COLOR_TEXT)
        text1_rect = text1_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text1_surface, text1_rect)

        if line2:
            text2_surface = font_text.render(line2, True, COLOR_TEXT)
            text2_rect = text2_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            screen.blit(text2_surface, text2_rect)

        # instruction
        hint_surface = font_small.render("Appuie sur une touche ou clique pour quitter.", True, COLOR_TEXT)
        hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 140))
        screen.blit(hint_surface, hint_rect)

        pygame.display.flip()
        clock.tick(60)

    # on quitte proprement après l'écran résultat
    pygame.quit()
    sys.exit()
