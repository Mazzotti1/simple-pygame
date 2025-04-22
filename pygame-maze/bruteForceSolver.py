
class BruteForceSolver:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.best_solution = None

    def solve(self):
        from itertools import product
        max_length = self.rows * self.cols

        for length in range(1, max_length + 1):
            for path in product([(0,1),(1,0),(0,-1),(-1,0)], repeat=length):
                current = self.start
                visited = [current]
                valid = True

                for step in path:
                    new_pos = (current[0] + step[0], current[1] + step[1])

                    if not (0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols):
                        valid = False
                        break

                    if not self._is_valid_move(current, new_pos):
                        valid = False
                        break

                    if new_pos in visited:
                        valid = False
                        break

                    visited.append(new_pos)
                    current = new_pos

                    if current == self.end:
                        if self.best_solution is None or len(visited) < len(self.best_solution):
                            self.best_solution = visited.copy()
                        break

                if valid and current == self.end:
                    return [self.best_solution]

        return [self.best_solution] if self.best_solution else []

    def _is_valid_move(self, current, new_pos):
        dr = new_pos[0] - current[0]
        dc = new_pos[1] - current[1]
        cell = self.grid[current[0]][current[1]]

        if dr == 1: return not cell.edges.bottom
        if dr == -1: return not cell.edges.top
        if dc == 1: return not cell.edges.right
        if dc == -1: return not cell.edges.left
        return False