import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turn-Based Combat")

# Font setup
font = pygame.font.SysFont(None, 30)

# Clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Player & Enemy setup
player = {"hp": 100, "fp": 2, "items": {"hp": 2, "fp": 1}, "rect": pygame.Rect(100, 200, 50, 50)}
enemy = {"hp": 100, "rect": pygame.Rect(490, 200, 50, 50)}

# Game states
player_turn = True
menu_open = False
menu_type = None  # 'attack' or 'item'
message = "Right-click to choose action"
game_over = False

# Damage values
def normal_attack():
    return random.randint(10, 15)

def special_attack():
    chance = random.randint(1, 5)
    if chance == 1:
        #enemy['hp'] == enemy['hp']
        #player['fp'] -= 1
        message = f"You missed!"
        return
    else:
        return random.randint(20, 30)

def draw_text(text, x, y):
    screen.blit(font.render(text, True, WHITE), (x, y))

def draw_bars():
    draw_text(f"Player HP: {player['hp']}", 10, 10)
    draw_text(f"FP: {player['fp']}", 10, 40)
    draw_text(f"Enemy HP: {enemy['hp']}", WIDTH - 150, 10)

def draw_menu(options, selected_index):
    for i, option in enumerate(options):
        color = WHITE if i != selected_index else RED
        text = font.render(option, True, color)
        screen.blit(text, (50, 300 + i * 30))

def enemy_turn():
    global message, player_turn
    if enemy['hp'] <= 0:
        return
    use_special = random.choice([True, False])
    dmg = special_attack() if use_special else normal_attack()
    player['hp'] -= dmg
    message = f"Enemy used {'Special' if use_special else 'Normal'} Attack for {dmg} damage!"
    player_turn = True

# Menu options
attack_options = ["Normal Attack", "Special Attack"]
item_options = ["Use HP Item", "Use FP Item"]
selected_index = 0

# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and player_turn:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
                if not menu_open:
                    menu_open = True
                    menu_type = 'attack'  # Default menu
                    selected_index = 0
                else:
                    # Toggle between attack and item menu
                    menu_type = 'item' if menu_type == 'attack' else 'attack'
                    selected_index = 0

            if event.type == pygame.KEYDOWN and menu_open:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % (2 if menu_type == 'attack' else 2)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % (2 if menu_type == 'attack' else 2)
                elif event.key == pygame.K_RETURN:
                    if menu_type == 'attack':
                        if selected_index == 0:  # Normal
                            dmg = normal_attack()
                            enemy['hp'] -= dmg
                            message = f"Player used Normal Attack for {dmg} damage!"
                        elif selected_index == 1:  # Special
                            if player['fp'] > 0:
                                dmg = special_attack()
                                enemy['hp'] -= dmg
                                player['fp'] -= 1
                                message = f"Player used Special Attack for {dmg} damage!"
                            else:
                                message = "Not enough FP!"
                                continue
                    elif menu_type == 'item':
                        if selected_index == 0 and player['items']['hp'] > 0:
                            player['hp'] += 30
                            player['items']['hp'] -= 1
                            message = "Used HP item! +30 HP"
                        elif selected_index == 1 and player['items']['fp'] > 0:
                            player['fp'] += 1
                            player['items']['fp'] -= 1
                            message = "Used FP item! +1 FP"
                        else:
                            message = "No item left!"
                            continue

                    menu_open = False
                    player_turn = False
                    pygame.time.set_timer(pygame.USEREVENT, 1000)

        if event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            enemy_turn()

    # Draw characters
    pygame.draw.rect(screen, WHITE, player['rect'])
    pygame.draw.rect(screen, RED, enemy['rect'])

    # Draw HP/FP
    draw_bars()

    # Draw menu if open
    if menu_open:
        if menu_type == 'attack':
            draw_menu(attack_options, selected_index)
        elif menu_type == 'item':
            draw_menu(item_options, selected_index)

    # Show message
    draw_text(message, 10, HEIGHT - 30)

    # Game over checks
    if player['hp'] <= 0:
        message = "You lost!"
        game_over = True
    elif enemy['hp'] <= 0:
        message = "You won!"
        game_over = True

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()