import pygame
import sys

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

BACKGROUND = (20, 20, 20)
BOX_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
LABEL_COLOR = (200, 200, 200)

class TextInputScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Cryptis – Enter Message")
        self.font_big = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 40)

        self.input_text = ""
        self.box = pygame.Rect(WINDOW_WIDTH//2 - 300, WINDOW_HEIGHT//2 - 40, 600, 80)

    def draw(self):
        self.screen.fill(BACKGROUND)

        # Title
        label = self.font_big.render("Please enter your message:", True, LABEL_COLOR)
        label_rect = label.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 120))
        self.screen.blit(label, label_rect)

        # Input box
        pygame.draw.rect(self.screen, BOX_COLOR, self.box, border_radius=10)

        # Typed text
        text_surface = self.font_small.render(self.input_text, True, TEXT_COLOR)
        self.screen.blit(text_surface, (self.box.x + 15, self.box.y + 20))

        # Hint
        hint = self.font_small.render("Press ENTER to continue", True, LABEL_COLOR)
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 120))
        self.screen.blit(hint, hint_rect)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # ENTER → finish
                    if event.key == pygame.K_RETURN:
                        return self.input_text if self.input_text != "" else None

                    # BACKSPACE → remove last char
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]

                    # Normal character
                    else:
                        if len(self.input_text) < 40:   # text limit
                            self.input_text += event.unicode

            self.draw()
