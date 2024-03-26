import pygame
import random

class Flora(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.growth_list = [(x, y)]  # List to store pixel positions
        self.color = color
        self.width = width
        self.height = height
        self.growth_interval = random.randint(180, 300)  # Growth interval in frames (3-5 seconds at 60 fps)
        self.growth_counter = 0
        self.growth_size = random.randint(1, 50)

    def update(self):
        # Increment the growth counter
        self.growth_counter += 0.1

        # Check if it's time to grow
        if self.growth_counter >= self.growth_interval and len(self.growth_list) < self.growth_size:
            self.growth_counter = 0  # Reset the growth counter
            last_x, last_y = self.growth_list[-1]
            new_x = last_x + random.choice([-5, 0, 5])
            new_y = last_y + random.choice([-5, 5])
            self.growth_list.append((new_x, new_y))

    def draw(self, surface):
        for pixel_pos in self.growth_list:
            pygame.draw.rect(surface, self.color, (*pixel_pos, self.width, self.height))
