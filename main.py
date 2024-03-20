import pygame
import random
import psutil
from charging_point import ChargingPoint
from sprite import Sprite


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
charging_points = [ChargingPoint((0, 34, 77), 5, 5, (random.randint(0, 1595), random.randint(0, 1195))) for _ in range(300)]
charging_point_group = pygame.sprite.Group(charging_points)

# Draw shadows for charging points
for charging_point in charging_points:
    charging_point.draw(screen)

sprite_pool = [Sprite((160, 21, 62), 5, 5, min_delay, max_delay) for _ in range(50)]
active_sprite_group = pygame.sprite.Group(sprite_pool[0:])

# pointer = Pointer((255, 255, 255), 5, 5)
# pointer_group = pygame.sprite.GroupSingle(pointer)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update active sprites
    active_sprite_group.update(active_sprite_group, charging_point_group)

    # Clear the screen
    screen.fill((53, 55, 75))

    # Draw active sprites
    for sprite in active_sprite_group:
        sprite.draw(screen)

    for point in charging_point_group:
        point.draw(screen)

    mouse_pos = pygame.mouse.get_pos()
    charging_point_group.update(mouse_pos)
    charging_point_group.draw(screen)

    # pointer_group.update()
    # pointer_group.draw(screen)
    
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
