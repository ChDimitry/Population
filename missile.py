import pygame
import math
import random
from particle import ParticleSystem
import time

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
        random_offset = random.randint(-30, 30)
        self.target_pos = (target_pos[0] + random_offset, target_pos[1])
        self.speed = 5  # Adjust speed as needed
        self.direction = self.calculate_direction()
        self.distance_to_target = math.sqrt((self.target_pos[0] - self.start_pos[0])**2 + (self.target_pos[1] - self.start_pos[1])**2)
        self.distance_traveled = 0
        self.hit_radius = 30

        self.trail_length = 50
        self.trail_width = 5
        self.trail_color = (255, 253, 215)
        self.trail_sprites = []
        self.trail_spawn_delay = 10
        self.last_trail_spawn_time = 0

        self.hit_particles = []
        self.particle_system = ParticleSystem()

        self.body_parts = []

    def calculate_direction(self):
        dx = self.target_pos[0] - self.start_pos[0]
        dy = self.target_pos[1] - self.start_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            return (0, 0)
        return (dx / distance, dy / distance)

    def update(self, worm_group):
        self.rect.x += self.direction[0] * (self.speed + (self.distance_to_target - self.distance_traveled) // 20)
        self.rect.y += self.direction[1] * (self.speed + (self.distance_to_target - self.distance_traveled) // 20)

        self.distance_traveled = math.sqrt((self.rect.centerx - self.start_pos[0])**2 + (self.rect.centery - self.start_pos[1])**2)
        if self.distance_traveled >= self.distance_to_target:
            self.rect.x = 1700
            self.rect.y = 1300
            # hide missile when it reaches target
            if not hasattr(self, 'hide_time'):
                self.hide_time = time.time() + 3  # Set hide_time to current time + 3 seconds
            elif time.time() >= self.hide_time:
                self.kill()  # Kill the sprite after 3 seconds

        for worm in worm_group:
            for worm_segment in worm.segments:
                if worm_segment not in [worm_segment for worm_segment, _ in self.body_parts]:
                    if self.distance_between_points((self.rect.centerx, self.rect.centery), (worm_segment.rect.centerx, worm_segment.rect.centery)) < 35 and self.distance_traveled >= self.distance_to_target - 10:
                        self.apply_hit_effect(worm_segment)
                        worm.is_alive = False
                        worm.trail_sprites.clear()

        self.move_body_parts()
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

    def apply_hit_effect(self, worm_segment):
        target_center_x, target_center_y = self.calculate_random_point(self.rect.centerx, self.rect.centery)
        self.body_parts.append((worm_segment, (target_center_x, target_center_y)))

    def calculate_random_point(self, center_x, center_y):
        target_x = random.choice([self.hit_radius, 0, -self.hit_radius]) + random.randint(0, self.hit_radius)
        target_y = random.choice([self.hit_radius, 0, -self.hit_radius]) + random.randint(0, self.hit_radius)
        return center_x + target_x, center_y + target_y
    
    def move_body_parts(self):
        # Move each body part to the target position
        for worm_segment, target_position in self.body_parts:
            worm_segment.is_alive = False
            follower_vector = pygame.math.Vector2(worm_segment.rect.centerx, worm_segment.rect.centery)
            target_vector = pygame.math.Vector2(target_position)
            distance = follower_vector.distance_to(target_vector)
            minimum_distance = -5
            maximum_distance = distance
            LERP_FACTOR = 0.08

            if distance > minimum_distance:
                direction_vector = (target_vector - follower_vector) / distance
                min_step = max(0, distance - maximum_distance)
                max_step = distance - minimum_distance
                step_distance = min_step + (max_step - min_step) * LERP_FACTOR
                new_follower_vector = follower_vector + direction_vector * step_distance
                worm_segment.rect.centerx = new_follower_vector.x
                worm_segment.rect.centery = new_follower_vector.y

            # check if random position is inside the charging point rect
            if worm_segment.rect.collidepoint(target_position):
                self.body_parts.remove((worm_segment, target_position))

    def add_trail_sprite(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_trail_spawn_time >= self.trail_spawn_delay:
            trail_sprite = pygame.Surface([self.trail_width, self.trail_width])
            trail_sprite.fill(self.trail_color)
            trail_sprite.set_alpha(50)  # Set initial alpha value
            random_offset = random.randint(-5, 5)
            trail_rect = trail_sprite.get_rect(center=(self.rect.centerx + random_offset, self.rect.centery + random_offset))
            self.trail_sprites.append((trail_sprite, trail_rect))

            # Remove oldest trail sprite if trail length exceeds limit
            if len(self.trail_sprites) > self.trail_length:
                self.trail_sprites.pop(0)

            # Update alpha values of trail sprites
            for i, (sprite, _) in enumerate(self.trail_sprites):
                alpha = int(((i + 1) * (50 / self.trail_length)))  # Gradually decrease alpha
                sprite.set_alpha(alpha)

            self.last_trail_spawn_time = current_time

    def distance_between_points(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5