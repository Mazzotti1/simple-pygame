import pygame
from entity import Entity
import math 

class BookProjectile(Entity):
    def __init__(self, x, y, direction, speed=200, width=64, height=64):
        super().__init__(x, y, width, height)
        self.direction = direction
        self.speed = speed
        self.frames = BookProjectile.load_spritesheet("Book.png", width, height)
        self.frame_index = 0
        self.animation_timer = 0
        self.frame_duration = 0.1
        self.current_frame = self.frames[0]
        self.active = True  
        self.original_y = y

    def update(self, dt):
        self.rect.x += self.speed * dt * self.direction
        self.rect.y = self.original_y + math.sin(pygame.time.get_ticks() * 0.01) * 5

        self.animation_timer += dt
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.active = False
            else:
                self.current_frame = self.frames[self.frame_index]


    def draw(self, screen):
        frame = pygame.transform.flip(self.current_frame, self.direction == -1, False)
        frame = pygame.transform.scale(frame, (self.rect.width, self.rect.height))
        screen.blit(frame, self.rect.topleft)

    @staticmethod
    def load_spritesheet(path, width, height):
        image = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(image.get_width() // width):
            frames.append(image.subsurface((i * width, 0, width, height)))
        return frames
