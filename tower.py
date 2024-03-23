import pygame
import math
import random
from charging_point import ChargingPoint

class Tower(pygame.sprite.Sprite):
    def __init__(self, color, width, height, position):
        super().__init__()
        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        self.min_delay = 10
        self.max_delay = 20
        self.tower_radius = 25

        self.time_since_last_decision = 0

        self.produced_charging_points = []
        self.production_radius = 200
        self.production_progress = 0   
        self.production_ready = 300 

    def get_charging_point(self, charging_points):
        charging_point = ChargingPoint((179, 163, 152), 5, 5, (self.rect.centerx, self.rect.centery))
        charging_points.add(charging_point)
        return charging_point

    def shoot_charging_point(self, charging_points):
        # get a random position in a 25 px radius
        target_center_x = random.randint(self.rect.centerx - self.production_radius, self.rect.centerx + self.production_radius)
        target_center_y = random.randint(self.rect.centery - self.production_radius, self.rect.centery + self.production_radius)
        # add the charging point to the list and the random position
        charging_point = self.get_charging_point(charging_points)
        self.produced_charging_points.append((charging_point, (target_center_x, target_center_y)))

    def move_charging_points(self):
        # Move each charging point to the target position   
        for charging_point, target_position in self.produced_charging_points:
            follower_vector = pygame.math.Vector2(charging_point.rect.centerx, charging_point.rect.centery)
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
                charging_point.rect.centerx = new_follower_vector.x
                charging_point.rect.centery = new_follower_vector.y

            # check if random position is inside the charging point rect
            if charging_point.rect.collidepoint(target_position):
                self.produced_charging_points.remove((charging_point, target_position))

    def update(self, charging_points):
        # charging progress based on game tiks
        self.production_progress += 3

        if self.production_progress >= self.production_ready:
            self.production_progress = 0
            if random.randint(0, 3) == 0:
                self.shoot_charging_point(charging_points)

        if len(self.produced_charging_points) > 0:
            self.move_charging_points()


    def draw(self, surface):
        pygame.draw.circle(surface, (116, 114, 100, 100), (self.rect.centerx, self.rect.centery), (self.production_progress // (self.production_ready // self.tower_radius)), 100)
        pygame.draw.circle(surface, self.color, (self.rect.centerx, self.rect.centery), self.tower_radius, 1)

        # draw '33%' text in the center of the tower
        font = pygame.font.Font("Fonts/ConnectionIi-2wj8.otf", 14)
        text = font.render(f"{self.production_progress // (self.production_ready // 100)}%", True, (238, 237, 235))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.centery))
        surface.blit(text, text_rect)


        # # Load and scale the image
        # image = pygame.image.load("Images/eye.png").convert_alpha()
        # scaled_image = pygame.transform.scale(image, (60, self.production_progress // 5))

        # # Calculate the position to draw the image
        # image_rect = scaled_image.get_rect(center=(self.rect.centerx, self.rect.centery))

        # # Draw the scaled image
        # surface.blit(scaled_image, image_rect)