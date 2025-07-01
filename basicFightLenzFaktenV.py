import pygame
import sys
import random

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen size
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turn-Based Combat")

# Load and play background music
pygame.mixer.music.load('ThisCharmingMan8Bit.mp3')
pygame.mixer.music.play(loops=-1)

# Font and clock setup
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Player and enemy initial stats
player = {
    "hp": 100,
    "fp": 10,
    "items": {"hp": 2, "fp": 2},
    "rect": pygame.Rect(100, 200, 50, 50)
}
enemy = {
    "hp": 300,
    "rect": pygame.Rect(490, 200, 50, 50)
}

# Game state flags
player_turn = True
menu_open = False
menu_type = None
message = "Du wurdest von Herrn Lenz-Faktenverweigerer angegriffen!"  # ✅ NEW: Intro message
game_over = False

# Block mode variables
block_mode = False
marker_x = 100
marker_speed = 6
block_result = None

# Random damage for different attacks
def normal_attack():
    return random.randint(10, 15)

def heavy_attack():
    return random.randint(15, 22)

def special_attack():
    return random.randint(35, 50)

# Function to draw text on screen
def draw_text(text, x, y):
    screen.blit(font.render(text, True, WHITE), (x, y))

# Function to draw HP and FP bars
def draw_bars():
    draw_text(f"Player HP: {player['hp']}", 10, 10)
    draw_text(f"FP: {player['fp']}", 10, 40)
    draw_text(f"Enemy HP: {enemy['hp']}", WIDTH - 200, 10)

# Function to draw attack/item menu
def draw_menu(options, selected_index):
    for i, option in enumerate(options):
        color = WHITE if i != selected_index else RED
        text = font.render(option, True, color)
        screen.blit(text, (50, 300 + i * 30))

# Draw the block bar mini-game
def draw_block_bar():
    pygame.draw.rect(screen, WHITE, (100, 400, 440, 10))  # Main bar
    pygame.draw.rect(screen, RED, (310, 395, 20, 20))     # Target area
    pygame.draw.rect(screen, GREEN, (marker_x, 395, 10, 20))  # Moving marker

# Handle block result based on distance from center
def handle_block(dmg):
    global message
    center = 320
    distance = abs(marker_x - center)
    if distance < 10:
        blocked = dmg
        message = f"Perfect block! Blocked all {dmg} damage!"
    elif distance < 40:
        blocked = int(dmg * 0.6)
        message = f"Good block! Blocked {blocked} of {dmg} damage!"
    elif distance < 80:
        blocked = int(dmg * 0.3)
        message = f"Partial block. Blocked {blocked} of {dmg} damage."
    else:
        blocked = 0
        message = f"Missed block! Took full {dmg} damage."
    return max(dmg - blocked, 0)

# Menu options
attack_options = ["Normal Attack", "Heavy Attack", "Special Attack"]
item_options = ["Use HP Item", "Use FP Item"]
selected_index = 0

pending_enemy_damage = 0

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle player's turn if not blocking or game over
        if not game_over and player_turn and not block_mode:

            # Right-click toggles between attack and item menus
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if not menu_open:
                    menu_open = True
                    menu_type = 'attack'
                    selected_index = 0
                else:
                    menu_type = 'item' if menu_type == 'attack' else 'attack'
                    selected_index = 0

            # Menu navigation with keyboard
            if event.type == pygame.KEYDOWN and menu_open:

                # Navigation
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % (3 if menu_type == 'attack' else 2)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % (3 if menu_type == 'attack' else 2)

                # Select menu option
                elif event.key == pygame.K_RETURN:

                    # 50% chance for attack denial before any action (✅ NEW)
                    if menu_type == 'attack' and random.random() < 0.5:
                        message = "Ich Leugne, dass du mich angegriffen hast"
                        menu_open = False
                        player_turn = False
                        pygame.time.set_timer(pygame.USEREVENT, 1000)
                        continue

                    # ATTACK MENU OPTIONS
                    if menu_type == 'attack':
                        if selected_index == 0:  # Normal
                            dmg = normal_attack()
                            enemy['hp'] -= dmg
                            message = f"Player used Normal Attack for {dmg} damage!"
                        elif selected_index == 1:  # Heavy
                            if player['fp'] >= 1:
                                dmg = heavy_attack()
                                enemy['hp'] -= dmg
                                player['fp'] -= 1
                                message = f"Player used Heavy Attack for {dmg} damage!"
                            else:
                                message = "Not enough FP for Heavy Attack!"
                                continue
                        elif selected_index == 2:  # Special
                            if player['fp'] >= 3:
                                dmg = special_attack()
                                enemy['hp'] -= dmg
                                player['fp'] -= 3
                                message = f"Player used Special Attack for {dmg} damage!"
                            else:
                                message = "Not enough FP for Special Attack!"
                                continue

                    # ITEM MENU OPTIONS
                    elif menu_type == 'item':
                        if selected_index == 0 and player['items']['hp'] > 0:
                            player['hp'] += 30
                            player['items']['hp'] -= 1
                            message = "Used HP item! +30 HP"
                        elif selected_index == 1 and player['items']['fp'] > 0:
                            player['fp'] += 3
                            player['items']['fp'] -= 1
                            message = "Used FP item! +3 FP"
                        else:
                            message = "No item left!"
                            continue

                    # End player's turn
                    menu_open = False
                    player_turn = False
                    pygame.time.set_timer(pygame.USEREVENT, 1000)

        # Handle enemy attack after delay
        elif event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            use_special = random.choice([True, False])
            pending_enemy_damage = special_attack() if use_special else normal_attack()
            message = f"Enemy used {'Special' if use_special else 'Normal'} Attack! Press SPACE to block!"
            block_mode = True
            marker_x = 100

        # Player attempts to block
        elif block_mode and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                final_dmg = handle_block(pending_enemy_damage)
                player['hp'] -= final_dmg
                block_mode = False
                player_turn = True

    # Draw player and enemy rectangles
    pygame.draw.rect(screen, WHITE, player['rect'])
    pygame.draw.rect(screen, RED, enemy['rect'])

    # Draw HP/FP bars
    draw_bars()

    # Draw menus if open
    if menu_open and not block_mode:
        if menu_type == 'attack':
            draw_menu(attack_options, selected_index)
        elif menu_type == 'item':
            draw_menu(item_options, selected_index)

    # Draw block bar mini-game if in block mode
    if block_mode:
        draw_block_bar()
        marker_x += marker_speed
        if marker_x > 530 or marker_x < 100:
            marker_speed *= -1

    # Display message
    draw_text(message, 10, HEIGHT - 30)

    # Check win/lose condition
    if player['hp'] <= 0:
        message = "You lost!"
        game_over = True
    elif enemy['hp'] <= 0:
        message = "You won!"
        game_over = True

    # Refresh screen
    pygame.display.flip()
    clock.tick(60)

# Clean up on quit
pygame.quit()
sys.exit()