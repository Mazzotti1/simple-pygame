import pygame

class Cell:
    def __init__(self, edges, backgroundColor, visitedColor, currentColor,
                 edgeColor, openColor, entranceColor, exitColor,
                 visited, open, current, is_entrance=False, is_exit=False):
        self.edges = edges
        self.backgroundColor = backgroundColor
        self.visitedColor = visitedColor
        self.currentColor = currentColor
        self.edgeColor = edgeColor
        self.openColor = openColor
        self.visited = visited
        self.open = open
        self.current = current

        self.entranceColor = entranceColor
        self.exitColor = exitColor
        self.is_entrance = is_entrance
        self.is_exit = is_exit

    def draw(self, screen, col, row, edge):
        start_upper_area = (col, row)
        end_upper_area = (col + edge, row)

        start_lower_area = (col, row + edge)
        end_lower_area = (col + edge, row + edge)

        start_left_area = (col, row)
        end_left_area = (col, row + edge)

        start_right_area = (col + edge, row)
        end_right_area = (col + edge, row + edge)

        if self.is_entrance:
            pygame.draw.rect(screen, self.entranceColor, (col, row, edge, edge))
        elif self.is_exit:
            pygame.draw.rect(screen, self.exitColor, (col, row, edge, edge))
        elif self.current:
            pygame.draw.rect(screen, self.currentColor, (col, row, edge, edge))
        elif self.open:
            pygame.draw.rect(screen, self.openColor, (col, row, edge, edge))
        elif self.visited:
            pygame.draw.rect(screen, self.visitedColor, (col, row, edge, edge))
        else:
            pygame.draw.rect(screen, self.backgroundColor, (col, row, edge, edge))

        # pygame.draw.line(screen, self.edgeColor, start_upper_area, end_upper_area)
        # pygame.draw.line(screen, self.edgeColor, start_lower_area, end_lower_area)
        # pygame.draw.line(screen, self.edgeColor, start_left_area, end_left_area)
        # pygame.draw.line(screen, self.edgeColor, start_right_area, end_right_area)

        # pra quebrar as linhas do labirinto, tentar ver depois
        if self.edges.top:
            pygame.draw.line(screen, self.edgeColor, start_upper_area, end_upper_area)
        if self.edges.bottom:
            pygame.draw.line(screen, self.edgeColor, start_lower_area, end_lower_area)
        if self.edges.left:
            pygame.draw.line(screen, self.edgeColor, start_left_area, end_left_area)
        if self.edges.right:
            pygame.draw.line(screen, self.edgeColor, start_right_area, end_right_area)
