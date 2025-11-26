import pygame
import sys
from text_input import TextInputScreen
from main import commencer

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

# -------------------------------------
# Couleurs
# -------------------------------------
COLOR_BG = (18, 18, 22)            # Fond très sombre
COLOR_PANEL = (36, 30, 45)         # Violet foncé
COLOR_PRIMARY = (255, 140, 0)      # Orange profond
COLOR_PRIMARY_HOVER = (255, 170, 40)
COLOR_CREDITS = (90, 200, 110)     # Vert néon clair
COLOR_CREDITS_HOVER = (140, 255, 160)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (200, 100, 255)     # Violet lumineux
# -------------------------------------


class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Cryptis – Menu Principal")

        self.font_title = pygame.font.Font(None, 100)
        self.font_button = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 45)

        self.running = True
        self.show_credits = False
        self.fade_alpha = 0

        # Boutons : plus larges, style "gaming"
        self.btn_start = pygame.Rect(WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//2 - 20, 500, 85)
        self.btn_credits = pygame.Rect(WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//2 + 110, 500, 75)

    # ---------------------------------------------------------------------
    # Dessin d'un bouton
    # ---------------------------------------------------------------------
    def draw_button(self, rect, text, style="primary"):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)

        if style == "primary":
            color = COLOR_PRIMARY_HOVER if is_hover else COLOR_PRIMARY
        else:
            color = COLOR_CREDITS_HOVER if is_hover else COLOR_CREDITS

        pygame.draw.rect(self.screen, color, rect, border_radius=30)

        label = self.font_button.render(text, True, COLOR_TEXT)
        label_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, label_rect)

    # ---------------------------------------------------------------------
    # Titre
    # ---------------------------------------------------------------------
    def draw_title(self):
        title = self.font_title.render("CRYPTIS", True, COLOR_ACCENT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 150))
        self.screen.blit(title, title_rect)

        subtitle = self.font_small.render("Jeu de Chiffrement", True, COLOR_TEXT)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, 230))
        self.screen.blit(subtitle, subtitle_rect)

    # ---------------------------------------------------------------------
    # Fenêtre Crédits
    # ---------------------------------------------------------------------
    def draw_credits_popup(self):
        if not self.show_credits:
            return

        if self.fade_alpha < 230:
            self.fade_alpha += 12

        # Fond transparent
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(self.fade_alpha)
        self.screen.blit(overlay, (0, 0))

        # Panel central
        panel_width, panel_height = 660, 320
        panel = pygame.Surface((panel_width, panel_height))
        panel.fill(COLOR_PANEL)
        panel.set_alpha(min(self.fade_alpha + 30, 255))
        panel_rect = panel.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(panel, panel_rect)

        # Textes
        text1 = self.font_button.render("Travail réalisé par :", True, COLOR_TEXT)
        text2 = self.font_small.render("Jean Costrel de Corainville & Fadi Aloui", True, COLOR_ACCENT)

        self.screen.blit(text1, text1.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40)))
        self.screen.blit(text2, text2.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40)))

    # ---------------------------------------------------------------------
    # Menu
    # ---------------------------------------------------------------------
    def run(self):
        while self.running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # Bouton Commencer
                    if self.btn_start.collidepoint(mouse_pos):
                        text_screen = TextInputScreen()
                        message = text_screen.run()
                        if message and message.strip():
                            commencer(message)

                    # Bouton crédits
                    if self.btn_credits.collidepoint(mouse_pos):
                        self.show_credits = not self.show_credits
                        self.fade_alpha = 0

                    # Fermer popup en cliquant ailleurs
                    if self.show_credits:
                        popup_zone = pygame.Rect(WINDOW_WIDTH//2 - 330, WINDOW_HEIGHT//2 - 160, 660, 320)
                        if not popup_zone.collidepoint(mouse_pos):
                            self.show_credits = False

            self.screen.fill(COLOR_BG)

            self.draw_title()

            self.draw_button(self.btn_start, "Commencer le jeu", style="primary")
            self.draw_button(self.btn_credits, "Crédits & Auteurs", style="credits")

            self.draw_credits_popup()

            pygame.display.flip()


# --- MAIN ENTRY POINT ---
if __name__ == "__main__":
    Menu().run()
