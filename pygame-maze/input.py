import pygame

class Input:
    def __init__(self, position, size, default_text="", font_size=32,
                 color_active=(255, 255, 255), color_inactive=(200, 200, 200),
                 text_color=(255, 255, 255), max_length=3):
        self.rect = pygame.Rect(position, size)
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color = color_inactive
        self.text = str(default_text)
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.active = False
        self.max_length = max_length

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() and len(self.text) < self.max_length:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def get_value(self):
        try:
            return int(self.text)
        except ValueError:
            return 0