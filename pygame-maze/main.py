import pygame
import sys
from button import Button
from input import Input
from edges import Edges
from cell import Cell
from aldousBroder import AldousBroder
from bruteForceSolver import BruteForceSolver
from dfsSolver import DfsSolver

class App:
    def __init__(self):
        pygame.init()
        self.running = True
        self.current_scene = "MENU"

        self.row_size = 15
        self.col_size = 15
        self.edge_size = 10

        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Labirinto com Aldous-Broder")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)

        self.generating_maze = False
        self.visualization_speed = 0
        self.generation_complete = False

        self.solving = False
        self.solution_path = None
        self.current_solution_step = 0
        self.solution_speed = 5
        self.solution_complete = False
        self.show_full_path = False

        self.create_ui_elements()
        self.create_ui_maze()
        self.create_maze()

    def create_ui_elements(self):
        self.row_input = Input(
            position=(520, 335),
            size=(130, 50),
            default_text=str(self.row_size),
            max_length=3
        )

        self.col_input = Input(
            position=(680, 335),
            size=(130, 50),
            default_text=str(self.col_size),
            max_length=3
        )

        self.exit_btn = Button(
            color="red",
            position=(680, 435),
            size=(130, 50),
            text="Sair",
            on_click=self.exit_maze_game,
            text_color="white"
        )

        self.start_btn = Button(
            color="green",
            position=(520, 435),
            size=(130, 50),
            text="Iniciar",
            on_click=self.start_maze_game
        )

        self.ui_elements = [self.row_input, self.col_input, self.exit_btn, self.start_btn]

    def create_ui_maze(self):
        self.back_btn = Button(
            color="red",
            position=(50, 100),
            size=(180, 50),
            text="Voltar (ESC)",
            on_click=self.back_to_menu,
            text_color="white"
        )

        self.brute_force = Button(
            color="yellow",
            position=(50, 200),
            size=(180, 50),
            text="Força bruta (B)",
            on_click=self.solve_maze("brute_force"),
            text_color="black"
        )

        self.dfs = Button(
            color="purple",
            position=(50, 300),
            size=(180, 50),
            text="DFS (D)",
            on_click=self.solve_maze("dfs"),
            text_color="white"
        )

        self.step_btn = Button(
            color="blue",
            position=(50, 400),
            size=(180, 50),
            text="Passo (Espaço)",
            on_click=self.step_generation,
            text_color="white"
        )

        self.fast_btn = Button(
            color="green",
            position=(50, 500),
            size=(180, 50),
            text="Rápido (F)",
            on_click=self.fast_generation,
            text_color="black"
        )

        self.reset_btn = Button(
            color="orange",
            position=(50, 600),
            size=(180, 50),
            text="Resetar (R)",
            on_click=self.reset_generation,
            text_color="white"
        )

        self.instant_btn = Button(
            color="orange",
            position=(1000, 100),
            size=(180, 50),
            text="Instantâneo (I)",
            on_click=self.generate_instant,
            text_color="white"
        )
        self.ui_elements_game = [self.back_btn, self.brute_force, self.dfs, self.step_btn, self.fast_btn, self.reset_btn, self.instant_btn]

    def create_maze(self):

        default_cell = Cell(
                edges=Edges(False, False, False, False),
                backgroundColor='white',
                visitedColor='white',
                currentColor='blue',
                edgeColor='black',
                openColor='white',
                entranceColor='green',
                exitColor='yellow',
                visited=False,
                open=False,
                current=False,
                is_entrance=False,
                is_exit=False
        )

        self.maze = AldousBroder(self.row_size, self.col_size, self.edge_size, default_cell)
        self.maze.grid[1][0].is_entrance = True
        self.maze.grid[self.row_size-1][self.col_size-1].is_exit = True

        self.generating_maze = False

    def start_visualization(self):
        self.generating_maze = True
        self.maze.start_generation()

    def start_maze_game(self):
        self.row_size = max(1, min(100, self.row_input.get_value()))
        self.col_size = max(1, min(100, self.col_input.get_value()))

        self.create_maze()
        self.current_scene = "MAZE"
        self.generation_complete = False
        self.visualization_speed = 0

    def exit_maze_game(self):
        self.running = False

    def back_to_menu(self):
        self.current_scene = "MENU"
        self.create_ui_elements()

    def step_generation(self):
        if not self.generation_complete:
            if not self.generating_maze:
                self.maze.start_generation()
                self.generating_maze = True
            else:
                if not self.maze.step_generation():
                    self.generation_complete = True
                    self.generating_maze = False

    def fast_generation(self):
        if self.generation_complete:
            return

        if not self.generating_maze:
            self.maze.start_generation()
            self.generating_maze = True

        self.visualization_speed = 10

    def reset_generation(self):
        self.create_maze()
        self.generating_maze = False
        self.generation_complete = False
        self.visualization_speed = 0
        self.solution_path = None
        self.solving = False
        self.show_full_path = False
        self.current_solution_step = 0

    def generate_instant(self):

        if self.generating_maze:
            return

        self.reset_generation()

        for btn in [self.back_btn, self.brute_force, self.dfs]:
            btn.disabled = True

        self.generating_maze = True
        self.generation_complete = False

        self.maze.generate_maze()

        self.maze.grid[self.maze.entrance[0]][self.maze.entrance[1]].is_entrance = True
        self.maze.grid[self.maze.exit[0]][self.maze.exit[1]].is_exit = True

        for btn in [self.back_btn, self.brute_force, self.dfs]:
            btn.disabled = False

        self.generation_complete = True
        self.generating_maze = False

        for row in range(self.maze.row_size):
            for col in range(self.maze.col_size):
                self.maze.grid[row][col].current = False

    def solve_maze(self, type):
        if not self.generation_complete:
            return

        self.solving = True
        self.show_full_path = False
        self.solution_path = None
        self.current_solution_step = 0

        self.maze.grid[1][0].edges.right = False
        self.maze.grid[1][1].edges.left = False

        self.maze.grid[self.row_size-1][self.col_size-2].edges.right = False
        self.maze.grid[self.row_size-1][self.col_size-1].edges.left = False

        if type == "brute_force":
            solver = BruteForceSolver(
                grid=self.maze.grid.grid,
                start=(1, 0),
                end=(self.row_size-1, self.col_size-1)
            )
        else:
            solver = DfsSolver(
                grid=self.maze.grid.grid,
                start=(1, 0),
                end=(self.row_size-1, self.col_size-1)
            )

        solutions = solver.solve()

        if solutions:
            self.solution_path = solutions[0]
            print(f"solucao , distancia: {len(self.solution_path)}")
        else:
            print("n achou solucao")
            self.solving = False

    def draw_solution(self):
        if not self.solution_path:
            return

        col_offset = (self.screen.get_width() - (self.col_size * self.edge_size)) // 2
        row_offset = (self.screen.get_height() - (self.row_size * self.edge_size)) // 2

        if self.show_full_path:
            for i in range(len(self.solution_path)-1):
                row1, col1 = self.solution_path[i]
                row2, col2 = self.solution_path[i+1]

                x1 = col_offset + col1 * self.edge_size + self.edge_size // 2
                y1 = row_offset + row1 * self.edge_size + self.edge_size // 2
                x2 = col_offset + col2 * self.edge_size + self.edge_size // 2
                y2 = row_offset + row2 * self.edge_size + self.edge_size // 2

                pygame.draw.line(self.screen, (0, 255, 0), (x1, y1), (x2, y2), 3)
        else:
            for i in range(self.current_solution_step):
                row1, col1 = self.solution_path[i]
                row2, col2 = self.solution_path[i+1]

                x1 = col_offset + col1 * self.edge_size + self.edge_size // 2
                y1 = row_offset + row1 * self.edge_size + self.edge_size // 2
                x2 = col_offset + col2 * self.edge_size + self.edge_size // 2
                y2 = row_offset + row2 * self.edge_size + self.edge_size // 2

                pygame.draw.line(self.screen, (0, 255, 0), (x1, y1), (x2, y2), 3)

            if self.solving and self.current_solution_step < len(self.solution_path)-1:
                self.current_solution_step += 1
            elif self.current_solution_step >= len(self.solution_path)-1:
                self.show_full_path = True
                self.solving = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.current_scene == "MENU":
                    for element in self.ui_elements:
                        if hasattr(element, 'handle_event'):
                            element.handle_event(event)

                elif self.current_scene == "MAZE":

                    if self.generating_maze and not self.generation_complete:
                        pygame.draw.circle(self.screen, 'white', (100, 100), 20, 2)

                    for element in self.ui_elements_game:
                        if hasattr(element, 'handle_event'):
                            element.handle_event(event)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and not self.generating_maze:
                            self.start_visualization()
                        elif event.key == pygame.K_SPACE and self.generating_maze:
                            self.maze.step_generation()
                        elif event.key == pygame.K_r:
                            self.reset_generation()
                        elif event.key == pygame.K_f:
                            self.fast_generation()
                        elif event.key == pygame.K_i:
                            self.generate_instant()
                        elif event.key == pygame.K_ESCAPE:
                            self.back_to_menu()
                        elif event.key == pygame.K_b:
                            self.solve_maze("brute_force")
                        elif event.key == pygame.K_d:
                            self.solve_maze("dfs")

            self.screen.fill((0, 0, 0))

            if self.current_scene == "MENU":
                row_label = self.font.render("Linhas:", True, (255, 255, 255))
                col_label = self.font.render("Colunas:", True, (255, 255, 255))
                self.screen.blit(row_label, (520, 305))
                self.screen.blit(col_label, (680, 305))

                for element in self.ui_elements:
                    element.draw(self.screen)

            elif self.current_scene == "MAZE":
                self.screen.fill('gray')
                col = (self.screen.get_width() - (self.col_size * self.edge_size)) // 2
                row = (self.screen.get_height() - (self.row_size * self.edge_size)) // 2

                if self.visualization_speed > 0 and not self.generation_complete:
                    for _ in range(self.visualization_speed):
                        if not self.maze.step_generation():
                            self.generation_complete = True
                            self.visualization_speed = 0
                            break

                status_text = "Pronto!" if self.generation_complete else "Escolha uma opçao..."
                status = self.font.render(status_text, True, (0, 0, 0))
                self.screen.blit(status, (50, 50))

                self.maze.grid.drawMaze(self.screen, col, row)

                for element in self.ui_elements_game:
                    element.draw(self.screen)

                if self.solving and not self.show_full_path:
                                if pygame.time.get_ticks() % 100 == 0:
                                    self.current_solution_step = min(self.current_solution_step + 1, len(self.solution_path)-1)
                                    if self.current_solution_step >= len(self.solution_path)-1:
                                        self.show_full_path = True
                                        self.solving = False

                if self.solution_path:
                    self.draw_solution()

            pygame.display.flip()
            self.clock.tick(60)

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
# https://www.ic.unicamp.br/~zanoni/teaching/mc102/2013-2s/aulas/aula21.pdf
# https://algorithm-visualizer.org/brute-force/depth-first-search