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

            for drawLine in range(4):
                    pygame.draw.line(screen, self.edgeColor)
            #iterar as lines da celula