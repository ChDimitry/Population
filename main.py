import pygame
import random
import psutil
from charging_point import ChargingPoint
from sprite import Sprite
from tower import Tower
from pointer import Pointer


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("Game")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Set the minimum and maximum delay values
min_delay = 2
max_delay = 2


# Create charging points
charging_point_group = pygame.sprite.Group()

sprite_pool = [Sprite((238, 237, 235), 5, 5, min_delay, max_delay) for _ in range(1)]
active_sprite_group = pygame.sprite.Group(sprite_pool[0:])

tower = Tower((116, 114, 100), 5, 5, ((1600 // 2) - 25 // 2, (1200 // 2) - 25 // 2))

missile_group = pygame.sprite.Group()

shrapnel_group = pygame.sprite.Group()

pointer = Pointer((255, 255, 255), 5, 5, missile_group)

# Game loop
running = True
while running:
    # Handle events
    mouse_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True

    # Update active sprites
    active_sprite_group.update(active_sprite_group, charging_point_group)

    # Clear the screen
    screen.fill((60, 54, 51))

    # Draw active sprites
    for sprite in active_sprite_group:
        sprite.draw(screen)

    for point in charging_point_group:
        point.draw(screen)

    for missile in missile_group:
        missile.draw(screen)

    mouse_pos = pygame.mouse.get_pos()
    charging_point_group.update(mouse_pos)
    charging_point_group.draw(screen)

    # pointer_group.update()
    # pointer_group.draw(screen)

    tower.update(charging_point_group)
    tower.draw(screen)

    pointer.update(mouse_clicked)
    pointer.draw(screen)

    missile_group.update()
    
    # Print CPU and RAM usage
    cpu_usage = float(psutil.cpu_percent())
    ram_usage = float(psutil.virtual_memory().percent)
    font = pygame.font.SysFont(None, 30)
    cpu_text = font.render(f"CPU Usage: {cpu_usage}%", True, (255, 255, 255), (0, 0, 0))
    ram_text = font.render(f"RAM Usage: {ram_usage}%", True, (255, 255, 255), (0, 0, 0))
    amount_text = font.render(f"Worker Quantity: {len(active_sprite_group)}", True, (255, 255, 255), (0, 0, 0))
    screen.blit(cpu_text, (10, 10))
    screen.blit(ram_text, (10, 40))
    screen.blit(amount_text, (10, 70))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
