import math
import pygame

class Pointer(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.center = mouse_pos
