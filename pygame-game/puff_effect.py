import pygame

class PuffEffect:
    def __init__(self, x, y, width=32, height=32):
        self.frames = PuffEffect.load_spritesheet("Puff.png", frame_count=4)
        self.frame_index = 0
        self.animation_timer = 0
        self.frame_duration = 0.05
        self.rect = pygame.Rect(x, y, width, height)
        self.finished = False

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.finished = True

    def draw(self, screen):
        if not self.finished:
            frame = self.frames[self.frame_index]
            screen.blit(frame, self.rect.topleft)

    @staticmethod
    def load_spritesheet(path, frame_count=4):
        image = pygame.image.load(path).convert_alpha()
        frame_width = image.get_width() // frame_count
        frame_height = image.get_height()
        
        frames = []
        for i in range(frame_count):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frames.append(image.subsurface(rect))
        return frames
