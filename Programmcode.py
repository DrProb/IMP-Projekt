import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1920, 1080
windowed_size = (1536, 1024)
screen = pygame.display.set_mode(windowed_size, pygame.RESIZABLE)
pygame.display.set_caption("Joe the Square vs The Corners of Doom")
square_positions = []

clock = pygame.time.Clock()

# Joe setup
player_color = (255, 255, 0)
player_size = 50
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

background = pygame.image.load("pictures/ludoBackground.png")
bg_width, bg_height = background.get_size()

x = (WIDTH - bg_width) // 2
y = (HEIGHT - bg_height) // 2

def get_scaled_background(window_size):
    w, h = window_size
    scale_factor = h / bg_height
    new_width = int(bg_width * scale_factor)
    new_height = h
    scaled_bg = pygame.transform.smoothscale(background, (new_width, new_height))
    return scaled_bg, (w // 2 - new_width // 2, 0)

def calc_square_positions(bg_width, bg_height):
    square1 = (bg_width, bg_height)
    square2 = (bg_width, bg_height)
    square3 = (bg_width, bg_height)
    square3 = (bg_width, bg_height)
    square4 = (bg_width, bg_height)
    square5 = (bg_width, bg_height)
    square6 = (bg_width, bg_height)
    square7 = (bg_width, bg_height)
    square8 = (bg_width, bg_height)
    square9 = (bg_width, bg_height)
    square10 = (bg_width, bg_height)
    square11 = (bg_width, bg_height)
    square12 = (bg_width, bg_height)
    square13 = (bg_width, bg_height)
    square14 = (bg_width, bg_height)
    square15 = (bg_width, bg_height)
    square16 = (bg_width, bg_height)
    square17 = (bg_width, bg_height)
    square18 = (bg_width, bg_height)
    square19 = (bg_width, bg_height)
    square20 = (bg_width, bg_height)
    square21 = (bg_width, bg_height)
    squar22 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)
    square1 = (bg_width, bg_height)



# Game loop
running = True
fullscreen = False
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.VIDEORESIZE:
            #screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    windowed_size = screen.get_size()  # Vorherige Größe merken
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(windowed_size, pygame.RESIZABLE)
    window_size = screen.get_size()
    bg_scaled, bg_pos = get_scaled_background(window_size)
    screen.fill((0, 0, 0))
    screen.blit(bg_scaled, bg_pos)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed
    player_pos[0] = max(0, min(window_size[0] - player_size, player_pos[0]))
    player_pos[1] = max(0, min(window_size[1] - player_size, player_pos[1]))
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    pygame.draw.rect(screen, player_color, player_rect)
    pygame.display.flip()
    print(player_pos)
pygame.quit()
sys.exit()