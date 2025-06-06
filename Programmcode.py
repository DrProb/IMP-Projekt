import pygame
import sys

pygame.init()

width = 800
height = 600
fullscreen = False
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Spiel")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width = event.w
            height = event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    width, height = screen.get_size()
                else:
                    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                    width, height = 800, 600
            elif event.key == pygame.K_ESCAPE:
                fullscreen = not fullscreen
                if not fullscreen:
                    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                    width, height = 800, 600
    screen.fill((0, 0, 0))
    rect_width = width // 2
    rect_height = height // 2
    rect_x = (width - rect_width) // 2
    rect_y = (height - rect_height) // 2
    pygame.draw.rect(screen, (200, 100, 100), (rect_x, rect_y, rect_width, rect_height))
    pygame.display.flip()

    clock.tick(60)
    print(clock.get_fps())

pygame.quit()
sys.exit