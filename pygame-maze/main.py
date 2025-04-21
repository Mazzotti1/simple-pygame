import pygame
import sys
from button import Button
from edges import Edges
from cell import Cell
from aldousBroder import AldousBroder

class App:
    def __init__(self):

        pygame.init()

        self.running = True
        self.current_scene = "MENU"

        self.row_size = 60
        self.col_size = 60
        self.edge_size = 10

        default_cell = Cell(Edges(False, False, False, False), 'black', 'white', 'white', 'white', False, False)
        self.maze = AldousBroder(self.row_size, self.col_size, self.edge_size, default_cell)
        self.maze.generate_maze()

        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Tela inicial")
        self.clock = pygame.time.Clock()

        exit_rect = pygame.Rect(680, 335, 130, 50)
        self.exit_btn = Button(
            color="red",
            position=exit_rect.topleft,
            size=exit_rect.size,
            text="Sair",
            on_click=self.exit_maze_game,
            text_color="white"
        )

        start_rect = pygame.Rect(520, 335, 130, 50)
        self.start_btn = Button(
            color="green",
            position=start_rect.topleft,
            size=start_rect.size,
            text="Iniciar",
            on_click=self.start_maze_game
        )

        self.menu_buttons = [self.exit_btn, self.start_btn]

    def start_maze_game(self):
        self.current_scene = "MAZE"

    def exit_maze_game(self):
        self.running = False

    def resolve_maze(self):
        pass

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
                    self.screen.fill('gray')

                    col = (self.screen.get_width() - (self.col_size * self.edge_size)) // 2
                    row = (self.screen.get_height() - (self.row_size * self.edge_size)) // 2


                    self.maze.grid.drawMaze(self.screen, col, row)

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
# https://weblog.jamisbuck.org/2011/1/17/maze-generation-aldous-broder-algorithm
# https://github.com/takos22/Maze-generator