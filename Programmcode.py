import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1920, 1080
#windowed_size = (1536, 1024)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joe the Square vs The Corners of Doom")
square_positions = []
square = [
(815, 860),
(815, 785),
(815, 700),
(815, 615),
(750, 575),
(680, 575),
(605, 575),
(530, 575),
(530, 485),
(530, 400),
(605, 400),
(675, 400),
(750, 400),
(810, 360),
(810, 280),
(810, 200),
(810, 120),
(895, 120),
(970, 115),
(975, 195),
(975, 280),
(975, 360),
(1035, 400),
(1110, 400),
(1180, 400),
(1255, 400),
(1255, 485),
(1255, 575),
(1180, 575),
(1110, 575),
(1035, 575),
(975, 615),
(975, 700),
(975, 780),
(975, 860),
(895, 860),
(625, 835),
(620, 750),
(540, 750),
(540, 835),
(625, 215),
(540, 215),
(625, 135),
(540, 135),
(1150, 215),
(1150, 135),
(1230, 135),
(1230, 215),
(1155, 755),
(1155, 835),
(1235, 755),
(1235, 835),
(895, 785),
(895, 725),
(895, 660),
(895, 600),
(610, 490),
(670, 490),
(730, 490),
(790, 490),
(895, 200),
(895, 260),
(895, 325),
(895, 385),
(1175, 490),
(1110, 490),
(1050, 490),
(995, 490)
]

clock = pygame.time.Clock()

# Joe setup
player_image = pygame.image.load("pictures/blue.png").convert_alpha()
player_size = 65
player_image = pygame.transform.scale(player_image, (player_size, player_size))
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




#with open ("square position.txt", "w") as datei:
    #datei.write("square[\n")
# Game loop
running = True
fullscreen = False
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_RETURN:
                #with open ("square position.txt", "a") as datei:
                    #datei.write(f"({player_pos[0]}, {player_pos[1]})\n")
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
    for i in range(68):
        screen.blit(player_image, square[i])
    pygame.display.flip()
    print(player_pos)
pygame.quit()
sys.exit()