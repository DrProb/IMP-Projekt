import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Fenster")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit