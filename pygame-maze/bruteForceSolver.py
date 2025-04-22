
class BruteForceSolver:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.all_paths = []

    def solve(self):
        self._generate_all_possible_paths()

        valid_paths = []
        for path in self.all_paths:
            if self._is_valid_path(path):
                valid_paths.append(path)

        return valid_paths

    def _generate_all_possible_paths(self):
        from itertools import product

        max_length = self.rows * self.cols

        directions = [(0,1), (1,0), (0,-1), (-1,0)]

        for length in range(1, max_length + 1):
            for path in product(directions, repeat=length):
                full_path = [self.start]
                current = self.start
                valid = True

                for step in path:
                    new_row = current[0] + step[0]
                    new_col = current[1] + step[1]

                    if not (0 <= new_row < self.rows and 0 <= new_col < self.cols):
                        valid = False
                        break

                    full_path.append((new_row, new_col))
                    current = (new_row, new_col)

                if valid:
                    self.all_paths.append(full_path)

    def _is_valid_path(self, path):
        if path[-1] != self.end:
            return False

        for i in range(len(path)-1):
            row, col = path[i]
            next_row, next_col = path[i+1]

            dr = next_row - row
            dc = next_col - col

            cell = self.grid[row][col]

            if dr == 1 and cell.edges.bottom:
                return False
            elif dr == -1 and cell.edges.top:
                return False
            elif dc == 1 and cell.edges.right:
                return False
            elif dc == -1 and cell.edges.left:
                return False

        return True