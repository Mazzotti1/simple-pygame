import pygame
import sys
from button import Button
from player import Player
from puff_effect import PuffEffect

class App:
    def __init__(self):
      
        pygame.init()
        
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Tela inicial")
        self.clock = pygame.time.Clock()
        
        self.running = True
        self.current_scene = "menu"

        self.player = None
        self.enemy = None
        self.ground_rect = None
        self.puffs = []

        exit_rect = pygame.Rect(680, 335, 130, 50)
        self.exit_btn = Button(
            color="red",
            position=exit_rect.topleft,
            size=exit_rect.size,
            text="Sair",
            on_click=self.exit_game,
            text_color="white"
        )
        
        start_rect = pygame.Rect(520, 335, 130, 50)
        self.start_btn = Button(
            color="green",
            position=start_rect.topleft,
            size=start_rect.size,
            text="Iniciar",
            on_click=self.start_game
        )

        self.menu_buttons = [self.exit_btn, self.start_btn]

    def exit_game(self):
        self.running = False

    def start_game(self):
        self.current_scene = "game"
        
    def draw_scene(self, dt):
        self.create_background()
        self.ground_rect = self.create_ground()
        self.create_player(dt)
        # self.create_ui()
      
    def create_background(self):
        self.screen.fill((135, 206, 235)) 

    def create_ground(self):
        ground_height = 150
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
    
        ground_color = (139, 69, 19)
        ground_rect = pygame.Rect(0, screen_height - ground_height, screen_width, ground_height)
        pygame.draw.rect(self.screen, ground_color, ground_rect)
        
        return ground_rect

    def create_player(self, dt):
        if self.player is None:
           self.player = Player(400, 400, 128, 128)
        
        self.player.update(self.ground_rect, dt, self.screen.get_width())
        self.player.draw(self.screen)
          
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.current_scene == "menu":
                    self.screen.fill((0, 0, 0)) 
                    for btn in self.menu_buttons:
                        btn.handle_event(event)
                        btn.draw(self.screen)
                    
            if self.current_scene == "game":
                keys = pygame.key.get_pressed()
                self.draw_scene(dt)
                if self.player:
                  self.player.handle_input(keys, dt)

                  for book in self.player.projectiles[:]:
                        book.update(dt)
                        book.draw(self.screen)
                        
                        if not book.active:
                            puff = PuffEffect(book.rect.centerx - 16, book.rect.centery - 16)
                            self.puffs.append(puff)
                            self.player.projectiles.remove(book)
                        elif book.rect.x < 0 or book.rect.x > self.screen.get_width():
                            self.player.projectiles.remove(book)

                for puff in self.puffs[:]:
                    puff.update(dt)
                    puff.draw(self.screen)
                    if puff.finished:
                        self.puffs.remove(puff)

            pygame.time.Clock().tick(60)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()
