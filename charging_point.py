import pygame
import math

class ChargingPoint(pygame.sprite.Sprite):
    def __init__(self, color, width, height, position):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        self.repulsion_distance = 30
        self.repulsion_force = 2

    def update(self, mouse_pos):
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        
        if distance < self.repulsion_distance:
            norm = (dx ** 2 + dy ** 2) ** 0.5
            if norm:
                dx /= norm
                dy /= norm
                repulsion_factor = 1 - (distance / self.repulsion_distance)
                dx *= self.repulsion_force * repulsion_factor
                dy *= self.repulsion_force * repulsion_factor
                self.rect.centerx -= dx
                self.rect.centery -= dy