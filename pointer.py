import math
import pygame
from missile import Missile

class Pointer(pygame.sprite.Sprite):
    def __init__(self, color, width, height, missile_group):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.missile_group = missile_group

    def update(self, mouse_clicked):
        self.clicked = mouse_clicked
        mouse_pos = pygame.mouse.get_pos()
        self.rect.center = mouse_pos

        if self.clicked:
            missile = Missile((255, 199, 0), 5, 5, (self.rect.centerx, 0), mouse_pos)
            self.missile_group.add(missile)
            print("Missile launched!")

    def draw(self, surface):
        # pygame.draw.circle(surface, (255, 0, 0), self.rect.center, 10)
        pass