import pygame
import math
import random
from particle import ParticleSystem

class Missile(pygame.sprite.Sprite):
    def __init__(self, color, width, height, start_pos, target_pos):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Choose a random x coordinate within a range
        start_x = random.randint(target_pos[0] - 500, target_pos[0] + 500)
        self.rect = self.image.get_rect(center=(start_x, start_pos[1]))
        self.start_pos = (start_x, start_pos[1])
        self.target_pos = target_pos
        self.speed = 10  # Adjust speed as needed
        self.direction = self.calculate_direction()
        self.distance_to_target = math.sqrt((self.target_pos[0] - self.start_pos[0])**2 + (self.target_pos[1] - self.start_pos[1])**2)
        self.distance_traveled = 0

        self.trail_length = 5
        self.trail_width = 5
        self.trail_color = (45, 39, 36)
        self.trail_sprites = []
        self.trail_spawn_delay = 30
        self.last_trail_spawn_time = 0

        self.hit_particles = []
        self.particle_system = ParticleSystem()

    def calculate_direction(self):
        dx = self.target_pos[0] - self.start_pos[0]
        dy = self.target_pos[1] - self.start_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            return (0, 0)
        return (dx / distance, dy / distance)

    def update(self):
        self.rect.x += self.direction[0] * (self.speed + (self.distance_to_target - self.distance_traveled) // 50)
        self.rect.y += self.direction[1] * (self.speed + (self.distance_to_target - self.distance_traveled) // 50)

        self.distance_traveled = math.sqrt((self.rect.centerx - self.start_pos[0])**2 + (self.rect.centery - self.start_pos[1])**2)
        if self.distance_traveled >= self.distance_to_target:
            self.kill()

        self.add_trail_sprite()
        self.particle_system.update()

    def draw(self, surface):
        
        # get ticks to control trail size
        size = (self.distance_to_target - self.distance_traveled) // 60
        pygame.draw.rect(surface, self.color, (self.rect.centerx, self.rect.centery, self.width + size, self.height + size))
        for trail_sprite, trail_rect in self.trail_sprites:
            surface.blit(trail_sprite, trail_rect)

        if self.distance_traveled >= self.distance_to_target - 10:
            pygame.draw.circle(surface, (255, 255, 255, 100), (self.rect.x, self.rect.y + 10), 40, 100, True, True, False, False)

            # self.particle_system.add_particle(self.target_pos[0], self.target_pos[1], (255, 255, 255))

        self.particle_system.draw(surface)

    def add_trail_sprite(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_trail_spawn_time >= self.trail_spawn_delay:
            trail_sprite = pygame.Surface([self.trail_width, self.trail_width])
            trail_sprite.fill(self.trail_color)
            trail_sprite.set_alpha(255)  # Set initial alpha value
            trail_rect = trail_sprite.get_rect(center=(self.rect.centerx, self.rect.centery))
            self.trail_sprites.append((trail_sprite, trail_rect))

            # Remove oldest trail sprite if trail length exceeds limit
            if len(self.trail_sprites) > self.trail_length:
                self.trail_sprites.pop(0)

            # Update alpha values of trail sprites
            for i, (sprite, _) in enumerate(self.trail_sprites):
                alpha = int(((i + 1) * (255 / self.trail_length)))  # Gradually decrease alpha
                sprite.set_alpha(alpha)

            self.last_trail_spawn_time = current_time
