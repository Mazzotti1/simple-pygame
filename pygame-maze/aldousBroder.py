import copy
from random import randint
import pygame
from grid import Grid

class AldousBroder:
    def __init__(self, row_size, col_size, edge, default_cell):
        self.row_size = row_size
        self.col_size = col_size
        self.edge = edge
        self.default_cell = default_cell
        self.grid = Grid(row_size, col_size, edge, default_cell)
        self.generating = False
        self.current_cell = None
        self.neighbor_cell = None
        self.unvisited_cells = 0
        self.entrance = (1, 0)
        self.exit = (row_size-1, col_size-1)

    def reset_maze(self):
        for row in range(self.row_size):
            for col in range(self.col_size):
                self.grid[row][col] = copy.deepcopy(self.default_cell)

        self._create_entrance_exit()

    def randomize_cell(self, current_cell_row, current_cell_col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while True:
            dr, dc = directions[randint(0, 3)]
            neighCellRow = current_cell_row + dr
            neighCellColumn = current_cell_col + dc

            if (0 <= neighCellRow < self.row_size and
                0 <= neighCellColumn < self.col_size):
                return neighCellRow, neighCellColumn

    def start_generation(self):
        self.reset_maze()
        self.unvisited_cells = self.row_size * self.col_size - 1

        self.entrance = (1, 0)
        self.exit = (self.row_size-1, self.col_size-1)

        self._create_entrance_exit()

        self.current_cell = (1, 1)
        self.grid[self.current_cell[0]][self.current_cell[1]].visited = True
        self.generating = True
        return self.current_cell

    def _create_entrance_exit(self):
        self.grid[1][1].edges.left = False
        self.grid[1][1].edges.right = False
        self.grid[1][1].edges.top = False
        self.grid[1][1].edges.botoom = False

        self.grid[1][0].is_entrance = True

        self.grid[self.row_size-1][self.col_size-1].edges.left = False
        self.grid[self.row_size-1][self.col_size-1].edges.top = False
        self.grid[self.row_size-1][self.col_size-1].edges.botoom = False

        self.grid[self.row_size-1][self.col_size-1].is_exit = True

    def step_generation(self):
        if not self.generating or self.unvisited_cells <= 0:
            self.finish_generation()
            return False

        current_row, current_col = self.current_cell
        self.grid[current_row][current_col].current = False

        new_row, new_col = self.randomize_cell(current_row, current_col)
        self.current_cell = (new_row, new_col)
        self.grid[new_row][new_col].current = True

        if not self.grid[new_row][new_col].visited:
            self._connect_cells(current_row, current_col, new_row, new_col)
            self.grid[new_row][new_col].visited = True
            self.unvisited_cells -= 1

        return True

    def _connect_cells(self, row1, col1, row2, col2):

        if (row1, col1) == self.entrance or (row1, col1) == self.exit:
            return
        if (row2, col2) == self.entrance or (row2, col2) == self.exit:
            return

        if col2 > col1:
            self.grid[row1][col1].edges.right = False
            self.grid[row2][col2].edges.left = False

        elif col2 < col1:
            self.grid[row1][col1].edges.left = False
            self.grid[row2][col2].edges.right = False

        elif row2 < row1:
            self.grid[row1][col1].edges.top = False
            self.grid[row2][col2].edges.bottom = False

        elif row2 > row1:
            self.grid[row1][col1].edges.bottom = False
            self.grid[row2][col2].edges.top = False

    def generate_maze(self):
        self.start_generation()
        while self.step_generation():
            pass
        self.finish_generation()

    def finish_generation(self):
        self._create_entrance_exit()

        self.grid[self.entrance[0]][self.entrance[1]].is_entrance = True
        self.grid[self.exit[0]][self.exit[1]].is_exit = True
