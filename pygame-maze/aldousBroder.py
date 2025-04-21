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

    def reset_maze(self):
        for row in range(self.row_size):
            for col in range(self.col_size):
                self.grid[row][col] = copy.deepcopy(self.default_cell)

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
        self.current_cell = randint(0, self.row_size - 1), (randint(0, self.col_size - 1))
        self.grid[self.current_cell[0]][self.current_cell[1]].visited = True
        self.grid[self.current_cell[0]][self.current_cell[1]].current = True

        self.generating = True
        return self.current_cell

    def step_generation(self):
        if not self.generating or self.unvisited_cells <= 0:
            self.finish_generation()
            return False

        if self.current_cell:
            prev_row, prev_col = self.current_cell
            self.grid[prev_row][prev_col].current = False

        currentCellLine, currentCellColumn = self.current_cell
        neighCellRow, neighCellColumn = self.randomize_cell(currentCellLine, currentCellColumn)

        self.grid[neighCellRow][neighCellColumn].current = True

        if not self.grid[neighCellRow][neighCellColumn].visited:
            self.grid[currentCellLine][currentCellColumn].open = True
            self.grid[neighCellRow][neighCellColumn].open = True

            if neighCellRow > currentCellLine:
                self.grid[currentCellLine][currentCellColumn].edges.bottom = True
                self.grid[neighCellRow][neighCellColumn].edges.top = True
            elif neighCellRow < currentCellLine:
                self.grid[currentCellLine][currentCellColumn].edges.top = True
                self.grid[neighCellRow][neighCellColumn].edges.bottom = True
            elif neighCellColumn > currentCellColumn:
                self.grid[currentCellLine][currentCellColumn].edges.right = True
                self.grid[neighCellRow][neighCellColumn].edges.left = True
            else:
                self.grid[currentCellLine][currentCellColumn].edges.left = True
                self.grid[neighCellRow][neighCellColumn].edges.right = True

            self.grid[neighCellRow][neighCellColumn].visited = True
            self.unvisited_cells -= 1

        self.current_cell = (neighCellRow, neighCellColumn)
        return True

    def generate_maze(self):
        self.start_generation()
        while self.step_generation():
            pass
        self.finish_generation()

    def finish_generation(self):
        if hasattr(self, 'current_cell') and self.current_cell:
            row, col = self.current_cell
            self.grid[row][col].current = False
        self.generating = False