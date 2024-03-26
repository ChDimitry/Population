import pygame
import random
from decision_module import DecisionModule

class WormSegment(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((130, 97 + random.randint(0, 60), 116))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Worm(pygame.sprite.Sprite):
    def __init__(self, x, y, length=5):
        super().__init__()
        self.segments = []
        for i in range(length):
            self.segments.append(WormSegment(x + i * 5, y))  # Create segments in a horizontal line
        self.rect = self.segments[-1].rect
        self.direction = 'left'
        self.move_delay = 3
        self.current_delay = 0
        self.decision_maker = DecisionModule()
        self.decision_maker.add_decision("move_up", 0.25)
        self.decision_maker.add_decision("move_down", 0.25)
        self.decision_maker.add_decision("move_left", 0.25)
        self.decision_maker.add_decision("move_right", 0.25)
        self.removed_decisions = []

        self.trail_length = 35
        self.trail_width = 10
        self.trail_color = (45, 39, 36)
        self.trail_sprites = []
        self.trail_spawn_delay = 40
        self.last_trail_spawn_time = 0

        self.speed = 2

        self.is_alive = True

    def update(self):
        if self.is_alive:
            self.current_delay += 1
            if self.current_delay >= self.move_delay:
                self.current_delay = 0
                
                for i in range(len(self.segments) - 1, 0, -1):
                    self.segments[i].update_position(self.segments[i - 1].rect.x, self.segments[i - 1].rect.y)
                # Move the head of the worm based on the direction
                if self.direction == 'up':
                    self.segments[0].rect.y -= self.speed
                elif self.direction == 'down':
                    self.segments[0].rect.y += self.speed
                elif self.direction == 'left':
                    self.segments[0].rect.x -= self.speed
                elif self.direction == 'right':
                    self.segments[0].rect.x += self.speed

                self.add_trail_sprite()

                self.do_scout()
        
            self.add_trail_sprite()

    def do_scout(self):
        decisions = self.decision_maker.get_decisions_list()
        move_decisions = [decision['name'] for decision in decisions if decision['name'].startswith('move_')]
        # Randomly select an action to prioritize
        if random.randint(0, 5) == 0:
            action_name = random.choice(move_decisions)
            # Update probabilities for all move actions
            for decision in move_decisions:
                if decision != action_name:
                    self.removed_decisions.append(decision)
                    self.decision_maker.remove_decision(decision)
            # Change direction based on the selected action
            if action_name == 'move_up':
                self.direction = 'up'
            elif action_name == 'move_down':
                self.direction = 'down'
            elif action_name == 'move_left':
                self.direction = 'left'
            elif action_name == 'move_right':
                self.direction = 'right'
        ticks = pygame.time.get_ticks()
        if ticks % 11 == 0:
            for decision in self.removed_decisions:
                self.decision_maker.add_decision(decision, 0.25)

    def add_trail_sprite(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_trail_spawn_time >= self.trail_spawn_delay:
            trail_sprite = pygame.Surface([5, 5])
            trail_sprite.fill(self.trail_color)
            trail_sprite.set_alpha(100)  # Set initial alpha value
            trail_rect = trail_sprite.get_rect()
            random_offset = random.randint(-2, 2)
            trail_rect = trail_sprite.get_rect(center=(self.rect.centerx + random_offset, self.rect.centery + random_offset))
            self.trail_sprites.append((trail_sprite, trail_rect))

            # Remove oldest trail sprite if trail length exceeds limit
            if len(self.trail_sprites) > self.trail_length:
                self.trail_sprites.pop(0)

            # Update alpha values of trail sprites
            for i, (sprite, _) in enumerate(self.trail_sprites):
                alpha = int(((i + 1) * (100 / self.trail_length)))  # Gradually decrease alpha
                sprite.set_alpha(alpha)


            self.last_trail_spawn_time = current_time

    def draw(self, surface):
        for trail_sprite, trail_rect in self.trail_sprites:
            surface.blit(trail_sprite, trail_rect)
        for segment in self.segments:
            surface.blit(segment.image, segment.rect)
