import pygame
from entity import Entity
from book_projectile import BookProjectile

class Player(Entity):
    def __init__(self, x, y, width=64, height=64):
        super().__init__(x, y, width, height)
        self.speed = 200
        self.direction = 0
        self.attacking = False

        self.idle_frames = Player.load_spritesheet("Idle.png", width, height)
        self.walk_frames = Player.load_spritesheet("Walk.png", width, height)
        self.throw_book_frames = Player.load_spritesheet("Attack.png", width, height)
        self.current_frames = self.idle_frames
        
        self.frame_index = 0
        self.animation_timer = 0
        self.frame_duration = 0.1
        
        self.current_frame = self.current_frames[0]
        self.projectiles = []

    def update(self, ground_rect, dt, screen_width):
        self.apply_gravity(dt)
        self.check_collision(ground_rect)
        self.update_animation(dt)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        
    def update_animation(self, dt):
        self.animation_timer += dt

        if self.attacking:
            if self.animation_timer >= self.frame_duration:
                self.animation_timer = 0
                self.frame_index += 1

                if self.frame_index >= len(self.throw_book_frames):
                    self.attacking = False
                    self.current_frames = self.idle_frames
                    self.frame_index = 0

                    book_x = self.rect.right if self.direction >= 0 else self.rect.left - self.rect.width
                    book_y = self.rect.centery
                    book = BookProjectile(book_x, book_y, self.direction or 1)
                    self.projectiles.append(book)
                else:
                    self.current_frame = self.throw_book_frames[self.frame_index]
            return

        new_frames = self.walk_frames if self.direction != 0 else self.idle_frames
    
        if self.current_frames != new_frames:
            self.current_frames = new_frames
            self.frame_index = 0
            self.animation_timer = 0
    
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)
    
        if self.current_frames:
            self.current_frame = self.current_frames[self.frame_index]
        
    def draw(self, screen):
        frame = self.current_frame
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        frame = pygame.transform.scale(frame, (self.rect.width, self.rect.height))
        screen.blit(frame, self.rect.topleft)

    def handle_input(self, keys, dt):
        if self.attacking:
                return

        self.direction = 0
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * dt
            self.direction = -1
        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt
            self.direction = 1

        if (keys[pygame.K_w]) and self.on_ground:
            self.velocity_y = -400
            self.on_ground = False
        
        if keys[pygame.K_SPACE] and not self.attacking:
            if self.on_ground == False:
                return
            
            self.attacking = True
            self.frame_index = 0
            self.animation_timer = 0
            self.current_frames = self.throw_book_frames


    @staticmethod
    def load_spritesheet(path, frame_width, frame_height):
        image = pygame.image.load(path).convert_alpha()
        sprites = []
        for i in range(image.get_width() // frame_width):
            frame = image.subsurface((i * frame_width, 0, frame_width, frame_height))
            sprites.append(frame)
        return sprites
