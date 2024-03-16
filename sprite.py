import pygame
import random
import math
from decision_module import DecisionModule
from decision import Decision
from charging_point import ChargingPoint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height, min_delay, max_delay):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, 1400)
        self.rect.y = random.randint(100, 800)
        self.sprite_color = (80, 114, 123)
        # (76, 205, 153)
        self.hungry_sprite_color = (80, 114, 123)

        self.health = 100
        self.action_penalty = 0.1

        self.max_delay = max_delay
        self.min_delay = min_delay
        # Create a decision maker with dynamic decisions
        self.decision_maker = DecisionModule()
        self.decision_maker.add_decision(Decision.MOVE_UP, 0.25)
        self.decision_maker.add_decision(Decision.MOVE_DOWN, 0.25)
        self.decision_maker.add_decision(Decision.MOVE_LEFT, 0.25)
        self.decision_maker.add_decision(Decision.MOVE_RIGHT, 0.25)
        self.decision_maker.add_decision(Decision.DO_NOTHING, 0.0)

        self.decision_delay = random.randint(min_delay, max_delay)
        self.time_since_last_decision = 0

        self.recharging = False
        self.recharge_point = None
        self.recharge_speed = 1
        self.minimum_charge_distance = 500

        self.trail_length = 10
        self.trail_width = 10
        self.trail_color = (204, 211, 202)
        self.trail_sprites = []
        self.trail_spawn_delay = 50
        self.last_trail_spawn_time = 0

    def update(self, sprites, charging_points):
        self.add_trail_sprite()
        self.time_since_last_decision += 1
        if self.time_since_last_decision >= self.decision_delay:
            _, action_name = self.do_action()
            # Avoid hitting other sprites
            self.avoid_collisions(sprites)

            if self.health <= 95: 
                if self.recharge_point not in charging_points:
                    self.recharge_point = self.__get_closest_charge(charging_points)
                if self.recharge_point:
                    self.decision_maker.add_decision(Decision.GO_CHARGE, 1000)
                    if self.__at_recharge_point():
                        self.health = 100
                        self.decision_maker.remove_decision(Decision.GO_CHARGE)
                        charging_points.remove(self.recharge_point)

            if self.health < 10:
                self.just_die(sprites)
            
            # Reset decision delay and time since last decision
            self.decision_delay = random.randint(self.min_delay, self.max_delay)
            self.time_since_last_decision = 0

    def draw(self, screen):
        if self.health <= 95:     
            self.image.fill(self.hungry_sprite_color)
        if self.__at_recharge_point():
            self.image.fill(self.sprite_color)
            
        # pygame.draw.circle(screen, (34, 40, 49), (self.rect.centerx, self.rect.centery), self.minimum_charge_distance, 1)
        for sprite, rect in self.trail_sprites:
            screen.blit(sprite, rect)
        screen.blit(self.image, self.rect)

    def go_charge(self):
        target_center_x = self.recharge_point.rect.centerx
        target_center_y = self.recharge_point.rect.centery
        follower_vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        target_vector = pygame.math.Vector2(target_center_x, target_center_y)

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

            self.rect.centerx = new_follower_vector.x
            self.rect.centery = new_follower_vector.y
            self.health -= self.action_penalty

    def add_trail_sprite(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_trail_spawn_time >= self.trail_spawn_delay:
            trail_sprite = pygame.Surface([5, 5])
            trail_sprite.fill(self.trail_color)
            trail_sprite.set_alpha(155)  # Set initial alpha value
            trail_rect = trail_sprite.get_rect()
            trail_rect.center = (self.rect.centerx, self.rect.centery)
            self.trail_sprites.append((trail_sprite, trail_rect))

            # Remove oldest trail sprite if trail length exceeds limit
            if len(self.trail_sprites) > self.trail_length:
                self.trail_sprites.pop(0)

            # Update alpha values of trail sprites
            for i, (sprite, _) in enumerate(self.trail_sprites):
                alpha = int(((i + 1) * (155 / self.trail_length)))  # Gradually decrease alpha
                sprite.set_alpha(alpha)

            self.last_trail_spawn_time = current_time

    def do_action(self):
        decision = self.__get_decision()
        action, name = self.__get_action(decision)
        action() if action else self.do_action()
        return action, name

    def __get_decision(self):
        return self.decision_maker.make_decision()

    def __get_action(self, decision):
        action_name = decision.value.lower()
        action_method = getattr(self, action_name, None)
        return action_method, action_name

    def avoid_collisions(self, sprites):
        for sprite in sprites:
            if sprite != self:
                if pygame.sprite.collide_rect(self, sprite):
                    if self.rect.x < sprite.rect.x:
                        self.move_left()
                    elif self.rect.x > sprite.rect.x:
                        self.move_right()
                    if self.rect.y < sprite.rect.y:
                        self.move_up()
                    elif self.rect.y > sprite.rect.y:
                        self.move_down()

    def __get_closest_charge(self, charging_points):
        closest_charge = None
        closest_distance = float('inf')
        for charge_point in list(charging_points):
            distance = math.sqrt((self.rect.x - charge_point.rect.x)**2 + (self.rect.y - charge_point.rect.y)**2)
            if distance < closest_distance and distance < self.minimum_charge_distance:
                closest_charge = charge_point
                closest_distance = distance
        return closest_charge

    def __at_recharge_point(self):
        if self.recharge_point:
            # Check if the sprite is at the recharge point
            return pygame.sprite.collide_rect(self, self.recharge_point)

    def move_up(self):
        self.rect.y -= 1
        self.health -= self.action_penalty

    def move_down(self):
        self.rect.y += 1
        self.health -= self.action_penalty

    def move_left(self):
        self.rect.x -= 1
        self.health -= self.action_penalty

    def move_right(self):
        self.rect.x += 1
        self.health -= self.action_penalty

    def do_nothing(self):
        pass

    def just_die(self, sprites):
        sprites.remove(self)

