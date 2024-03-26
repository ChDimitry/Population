import pygame
from missile import Missile

class Pointer(pygame.sprite.Sprite):
    def __init__(self, color, width, height, missile_group):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.missile_group = missile_group
        self.fire_rate = 50
        self.fire_delay = 0

    def update(self, mouse_clicked, mouse_pos):
        self.clicked = mouse_clicked
        self.rect.center = mouse_pos

        self.fire_delay -= 1

        if self.clicked and self.fire_delay <= 0:
            missile = Missile(color=(251, 250, 218), width=5, height=5, start_pos=(self.rect.centerx, 0), target_pos=mouse_pos)
            self.missile_group.add(missile)
            self.fire_delay = self.fire_rate  # Reset fire delay

    def draw(self, surface):
        pass
