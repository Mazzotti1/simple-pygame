import pygame

class Entity:
  def __init__(self, x, y, width, height):
      self.rect = pygame.Rect(x, y, width, height)
      self.velocity_y = 0
      self.on_ground = False
      
  def apply_gravity(self, dt):
      if not self.on_ground:
          gravity = 1500
          self.velocity_y += gravity * dt
          self.rect.y += self.velocity_y * dt

  def check_collision(self, ground_rect):
      if self.rect.colliderect(ground_rect):
          self.rect.bottom = ground_rect.top
          self.velocity_y = 0
          self.on_ground = True
      else:
          self.on_ground = False

  def draw(self, screen, color=(255, 255, 255)):
      pygame.draw.rect(screen, color, self.rect)
      
