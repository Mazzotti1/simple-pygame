class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.color = (255, 0, 0)

    def update(self, ground_rect):
        self.apply_gravity()
        self.check_collision(ground_rect)

    def draw(self, screen):
        super().draw(screen, self.color)