class DfsSolver:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.path = []
        self.solutions = []

    def solve(self):
        if not (0 <= self.start[0] < self.rows and 0 <= self.start[1] < self.cols):
            print("posição inicial invalida")
            return []
        if not (0 <= self.end[0] < self.rows and 0 <= self.end[1] < self.cols):
            print("posição final inválida")
            return []

        self._dfs(self.start[0], self.start[1])
        return self.solutions

    def _dfs(self, row, col):
        self.visited[row][col] = True
        self.path.append((row, col))

        if (row, col) == self.end:
            self.solutions.append(list(self.path))
            self.visited[row][col] = False
            self.path.pop()
            return

        right = (0, 1)
        down = (1, 0)
        left = (0, -1)
        up = (-1, 0)

        directions = [
            right,
            down,
            left,
            up
        ]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self._is_valid_move(row, col, new_row, new_col):
                self._dfs(new_row, new_col)

        self.visited[row][col] = False
        self.path.pop()

    def _is_valid_move(self, row, col, new_row, new_col):
        if not (0 <= new_row < self.rows and 0 <= new_col < self.cols):
            return False

        if self.visited[new_row][new_col]:
            return False

        dr = new_row - row
        dc = new_col - col

        cell = self.grid[row][col]

        if dr == 0 and dc == 1:
            return not cell.edges.right
        elif dr == 1 and dc == 0:
            return not cell.edges.bottom
        elif dr == 0 and dc == -1:
            return not cell.edges.left
        elif dr == -1 and dc == 0:
            return not cell.edges.top

        return False