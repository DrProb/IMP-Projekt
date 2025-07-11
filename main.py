import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joe the Square vs The Corners of Doom")

clock = pygame.time.Clock()

# Joe setup
player_color = (255, 255, 255)
player_size = 50
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

# Deadly blocks setup
enemy_color = (255, 0, 0)
enemy_size = 50
enemies = [
    pygame.Rect(0, 0, enemy_size, enemy_size),  # Top-left
    pygame.Rect(WIDTH - enemy_size, 0, enemy_size, enemy_size),  # Top-right
    pygame.Rect(0, HEIGHT - enemy_size, enemy_size, enemy_size),  # Bottom-left
    pygame.Rect(WIDTH - enemy_size, HEIGHT - enemy_size, enemy_size, enemy_size),  # Bottom-right
]

# Game loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Keep Joe on screen
    player_pos[0] = max(0, min(WIDTH - player_size, player_pos[0]))
    player_pos[1] = max(0, min(HEIGHT - player_size, player_pos[1]))

    # Joe's rect for collision
    player_rect = pygame.Rect(*player_pos, player_size, player_size)

    # Check collision with any enemy block
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            print("Joe is dead. Game over.")
            pygame.quit()
            sys.exit()

    # Draw everything
    screen.fill((0, 0, 0))  # Black background

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, enemy_color, enemy)

    # Draw player
    pygame.draw.rect(screen, player_color, player_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()