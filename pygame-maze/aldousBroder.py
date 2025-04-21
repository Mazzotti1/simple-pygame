import copy
from random import randint
from grid import Grid

class AldousBroder:
    def __init__(self, row_size, col_size, edge, default_cell):
        self.row_size = row_size
        self.col_size = col_size
        self.edge = edge
        self.default_cell = default_cell
        self.grid = Grid(row_size, col_size, edge, default_cell)


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

    def generate_maze(self):
        self.reset_maze()
        unvisited_cells = self.row_size * self.col_size - 1  # subtrai a célula inicial

        currentCellLine = randint(0, self.row_size - 1)
        currentCellColumn = randint(0, self.col_size - 1)
        self.grid[currentCellLine][currentCellColumn].visited = True

        while unvisited_cells > 0:
            neighCellRow, neighCellColumn = self.randomize_cell(currentCellLine, currentCellColumn)

            if not self.grid[neighCellRow][neighCellColumn].visited:
                # Remove a parede entre as células
                if neighCellRow > currentCellLine:  # vizinho abaixo
                    self.grid[currentCellLine][currentCellColumn].edges.bottom = True
                    self.grid[neighCellRow][neighCellColumn].edges.top = True
                elif neighCellRow < currentCellLine:  # vizinho acima
                    self.grid[currentCellLine][currentCellColumn].edges.top = True
                    self.grid[neighCellRow][neighCellColumn].edges.bottom = True
                elif neighCellColumn > currentCellColumn:  # vizinho à direita
                    self.grid[currentCellLine][currentCellColumn].edges.right = True
                    self.grid[neighCellRow][neighCellColumn].edges.left = True
                else:  # vizinho à esquerda
                    self.grid[currentCellLine][currentCellColumn].edges.left = True
                    self.grid[neighCellRow][neighCellColumn].edges.right = True

                self.grid[neighCellRow][neighCellColumn].visited = True
                unvisited_cells -= 1

            currentCellLine, currentCellColumn = neighCellRow, neighCellColumn