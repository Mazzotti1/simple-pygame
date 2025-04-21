import copy


class Grid:
    def __init__(self, rows_size, col_size, edge, default_cell):
        self.rows_size = rows_size
        self.col_size = col_size
        self.edge = edge
        self.default_cell = default_cell
        self.grid = self.createGrid()

    def __len__(self):
        return len(self.grid)

    def __iter__(self):
        return iter(self.grid)

    def __getitem__(self, index):
        return self.grid[index]

    def __setitem__(self, index, value):
        self.grid[index] = value

    def __aslist__(self):
        return self.grid

    def createGrid(self):
        grid = []
        for row in range(self.rows_size):
            grid_row = []
            for col in range(self.col_size):
                grid_row.append(copy.deepcopy(self.default_cell))
            grid.append(grid_row)
        return grid

    def drawMaze(self, screen, col_offset, row_offset):
        for row in range(self.rows_size):
            for col in range(self.col_size):
                x = col_offset + col * self.edge
                y = row_offset + row * self.edge
                self.grid[row][col].draw(screen, x, y, self.edge)
