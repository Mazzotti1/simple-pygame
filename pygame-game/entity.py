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

  def check_collision(self, ground_rect, solids):
        self.on_ground = False

        platforms_below = []

        # Verifica chão
        if self.rect.colliderect(ground_rect):
            if self.velocity_y >= 0 and self.rect.bottom <= ground_rect.top + 10:
                self.rect.bottom = ground_rect.top
                self.velocity_y = 0
                self.on_ground = True
                return 

        # Verifica colisão com sólidos
        for solid in solids:
            if self.rect.colliderect(solid):
                if self.velocity_y >= 0 and self.rect.bottom <= solid.top + 10:
                    platforms_below.append(solid)

        for solid in platforms_below:
            if solid.left <= self.rect.centerx <= solid.right:
                self.rect.bottom = solid.top
                self.velocity_y = 0
                self.on_ground = True
                break


  def draw(self, screen, color=(255, 255, 255)):
      pygame.draw.rect(screen, color, self.rect)
      
