import pygame

class Cell:
    def __init__(self, edges, backgroundColor, visitedColor, edgeColor, openColor, visited, open):
        self.edges = edges
        self.backgroundColor = backgroundColor
        self.visitedColor = visitedColor
        self.edgeColor = edgeColor
        self.openColor = openColor
        self.visited = visited
        self.open = open


    def draw(self, screen, col, row, edge):
        start_upper_area = (col, row)
        end_upper_area = (col + edge, row)

        start_lower_area = (col, row + edge)
        end_lower_area = (col + edge, row + edge)

        start_left_area = (col, row)
        end_left_area = (col, row + edge)

        start_right_area = (col + edge, row)
        end_right_area = (col + edge, row + edge)

        if (self.open):
                pygame.draw.rect(screen, self.openColor, (col, row, edge, edge))
        else:
                pygame.draw.rect(screen, self.backgroundColor, (col, row, edge, edge))

        # pygame.draw.line(screen, self.edgeColor, start_upper_area, end_upper_area)
        # pygame.draw.line(screen, self.edgeColor, start_lower_area, end_lower_area)
        # pygame.draw.line(screen, self.edgeColor, start_left_area, end_left_area)
        # pygame.draw.line(screen, self.edgeColor, start_right_area, end_right_area)

        # para quebrar as linhas do labirinto
        if self.edges.top:
            pygame.draw.line(screen, self.edgeColor, start_upper_area, end_upper_area)
        if self.edges.bottom:
            pygame.draw.line(screen, self.edgeColor, start_lower_area, end_lower_area)
        if self.edges.left:
            pygame.draw.line(screen, self.edgeColor, start_left_area, end_left_area)
        if self.edges.right:
            pygame.draw.line(screen, self.edgeColor, start_right_area, end_right_area)
