#IMP
import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turn-Based Combat")
pygame.mixer.music.load('BreakingAllIllusions8Bit.mp3')
pygame.mixer.music.play(loops=-1)

font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

player = {
    "hp": 100,
    "fp": 10,
    "items": {"hp": 2, "fp": 2},
    "rect": pygame.Rect(100, 200, 50, 50)
}
enemy = {
    "hp": 500,
    "rect": pygame.Rect(490, 200, 50, 50)
}

player_turn = True
menu_open = False
menu_type = None
message = "Right-click to choose action"
game_over = False

block_mode = False
marker_x = 100
marker_speed = 6
block_result = None

def normal_attack():
    return random.randint(10, 15)

def heavy_attack():
    return random.randint(15, 22)

def special_attack():
    #chance = random.randint(1, 5)
    #if chance == 1:
        #enemy['hp'] == enemy['hp']
        #player['fp'] -= 1
        #message = f"You missed!"
        #return
    #else:
        return random.randint(35, 50)

def draw_text(text, x, y):
    screen.blit(font.render(text, True, WHITE), (x, y))

def draw_bars():
    draw_text(f"Player HP: {player['hp']}", 10, 10)
    draw_text(f"FP: {player['fp']}", 10, 40)
    draw_text(f"Enemy HP: {enemy['hp']}", WIDTH - 200, 10)

def draw_menu(options, selected_index):
    for i, option in enumerate(options):
        color = WHITE if i != selected_index else RED
        text = font.render(option, True, color)
        screen.blit(text, (50, 300 + i * 30))

def draw_block_bar():
    pygame.draw.rect(screen, WHITE, (100, 400, 440, 10))
    pygame.draw.rect(screen, RED, (310, 395, 20, 20))
    pygame.draw.rect(screen, GREEN, (marker_x, 395, 10, 20))

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

attack_options = ["Normal Attack", "Heavy Attack", "Special Attack"]
item_options = ["Use HP Item", "Use FP Item"]
selected_index = 0

pending_enemy_damage = 0

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and player_turn and not block_mode:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if not menu_open:
                    menu_open = True
                    menu_type = 'attack'
                    selected_index = 0
                else:
                    menu_type = 'item' if menu_type == 'attack' else 'attack'
                    selected_index = 0

            if event.type == pygame.KEYDOWN and menu_open:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % (3 if menu_type == 'attack' else 2)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % (3 if menu_type == 'attack' else 2)
                elif event.key == pygame.K_RETURN:
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

                    menu_open = False
                    player_turn = False
                    pygame.time.set_timer(pygame.USEREVENT, 1000)

        elif event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            use_special = random.choice([True, False])
            pending_enemy_damage = special_attack() if use_special else normal_attack()
            message = f"Enemy used {'Special' if use_special else 'Normal'} Attack! Press SPACE to block!"
            block_mode = True
            marker_x = 100

        elif block_mode and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                final_dmg = handle_block(pending_enemy_damage)
                player['hp'] -= final_dmg
                block_mode = False
                player_turn = True

    pygame.draw.rect(screen, WHITE, player['rect'])
    pygame.draw.rect(screen, RED, enemy['rect'])

    draw_bars()

    if menu_open and not block_mode:
        if menu_type == 'attack':
            draw_menu(attack_options, selected_index)
        elif menu_type == 'item':
            draw_menu(item_options, selected_index)

    if block_mode:
        draw_block_bar()
        marker_x += marker_speed
        if marker_x > 530 or marker_x < 100:
            marker_speed *= -1

    draw_text(message, 10, HEIGHT - 30)

    if player['hp'] <= 0:
        message = "You lost!"
        game_over = True
    elif enemy['hp'] <= 0:
        message = "You won!"
        game_over = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()