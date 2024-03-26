import pygame
import random

class Flora(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.growth_list = [(x, y, color)]  # List to store pixel positions
        self.color = color
        self.width = width
        self.height = height
        self.growth_interval = random.randint(180, 300)  # Growth interval in frames (3-5 seconds at 60 fps)
        self.growth_counter = 0
        self.growth_size = random.randint(1, 50)

    def update(self):
        # Increment the growth counter
        self.growth_counter += 1

        # Check if it's time to grow
        if self.growth_counter >= self.growth_interval and len(self.growth_list) < self.growth_size:
            self.growth_counter = 0  # Reset the growth counter
            color_range = random.randint(-5, 5)
            color = (60 + color_range, 54 + color_range, 51 + color_range)
            last_x, last_y = self.growth_list[-1][:2]
            new_x = last_x + random.choice([-5, 0, 5])
            new_y = last_y + random.choice([-5, 5])
            self.growth_list.append((new_x, new_y, color))

    def draw(self, surface):
        for growth_info in self.growth_list:
            color = growth_info[2]
            pixel_pos = growth_info[:2]
            pygame.draw.rect(surface, color, (*pixel_pos, self.width, self.height))
