import pygame
import sys
from button import Button

class App:
    def __init__(self):
      
        pygame.init()

        self.running = True
        self.current_scene = "MENU"
        
        R = 20
        C = 20
        L = 10


        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Tela inicial")
        self.clock = pygame.time.Clock()

        exit_rect = pygame.Rect(680, 335, 130, 50)
        self.exit_btn = Button(
            color="red",
            position=exit_rect.topleft,
            size=exit_rect.size,
            text="Sair",
            on_click=self.exit_maze,
            text_color="white"
        )
        
        start_rect = pygame.Rect(520, 335, 130, 50)
        self.start_btn = Button(
            color="green",
            position=start_rect.topleft,
            size=start_rect.size,
            text="Iniciar",
            on_click=self.start_maze
        )

        self.menu_buttons = [self.exit_btn, self.start_btn]

    def start_maze(self):
        self.current_scene = "MAZE"

    def exit_maze(self):
        self.running = False

    def resolve_maze():
        self.screen.fill((135, 206, 235)) 
          
    def run(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.current_scene == "MENU":
                    self.screen.fill((0, 0, 0))
                    for btn in self.menu_buttons:
                        btn.handle_event(event)
                        btn.draw(self.screen)
                        

                if(self.current_scene == "MAZE"):
                    self.screen.fill((66, 245, 215)) 

            [row, col] = ((self.screen.get_width() - (self.R * self.L)) //2,
                          (self.screen.get_height() - (self.C * self.L)) //2)
                        

            pygame.time.Clock().tick(60)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()


#Referências:
# https://github.com/ProfessorFilipo/PyGameBasico/blob/main/maze001.py
# https://github.com/Mazzotti1/aldous-broder-maze-java
# https://www.pygame.org/docs/