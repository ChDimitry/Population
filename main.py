import pygame
import random
import psutil
from charging_point import ChargingPoint
from sprite import Sprite
from tower import Tower
from pointer import Pointer
from flora import Flora
from worm import Worm

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

# Create flora group
flora_group = pygame.sprite.Group()
# Spawn 500 plants at random locations
for _ in range(500):
    x = random.randint(0, 1595)  # Adjusted to fit within screen width
    y = random.randint(0, 1195)  # Adjusted to fit within screen height
    color_range = random.randint(-5, 5)
    color = (60 + color_range, 54 + color_range, 51 + color_range)
    flora = Flora(color, 5, 5, x, y)
    flora_group.add(flora)

# Create worm group
worm_group = pygame.sprite.Group()
# Spawn 5 worms at random locations
for _ in range(10):
    x = random.randint(0, 1595)  # Adjusted to fit within screen width
    y = random.randint(0, 1195)  # Adjusted to fit within screen height
    worm = Worm(x, y, 5)
    worm_group.add(worm)


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
    for flora in flora_group:
        flora.draw(screen)
        
    for sprite in active_sprite_group:
        sprite.draw(screen)

    for point in charging_point_group:
        point.draw(screen)

    for missile in missile_group:
        missile.draw(screen)

    for worm in worm_group:
        worm.update()
        worm.draw(screen)

    mouse_pos = pygame.mouse.get_pos()
    charging_point_group.update(mouse_clicked, mouse_pos)
    charging_point_group.draw(screen)

    # pointer_group.update()
    # pointer_group.draw(screen)

    tower.update(charging_point_group)
    tower.draw(screen)

    pointer.update(mouse_clicked, mouse_pos)
    pointer.draw(screen)

    missile_group.update(worm_group)
    
    flora_group.update()

    # Print CPU and RAM usage
    cpu_usage = float(psutil.cpu_percent())
    ram_usage = float(psutil.virtual_memory().percent)
    font = pygame.font.Font("Fonts/ConnectionIi-2wj8.otf", 20)
    cpu_text = font.render(f"{cpu_usage}%", True, (255, 255, 255), (0, 0, 0))
    ram_text = font.render(f"{ram_usage}%", True, (255, 255, 255), (0, 0, 0))
    screen.blit(cpu_text, (10, 10))
    screen.blit(ram_text, (10, 40))


    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
