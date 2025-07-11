import pygame
import sys
import random
import sqlite3

pygame.init()
pygame.mixer.init()

connection = sqlite3.connect("game_database.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS enemy_data (
    idx INTEGER PRIMARY KEY,
    startHP INTEGER,
    message TEXT,
    music TEXT,
    sprite TEXT,
    georgAbility BOOLEAN,
    lenzfaktenAbility BOOLEAN,
    olfaayAbility BOOLEAN,
    friedrichSchmerz BOOLEAN,
    isLinus BOOLEAN,
    width INTEGER,
    height INTEGER,
    dodgingThreshold INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS piecesPos (
    idx INTEGER PRIMARY KEY,
    piece0 INTEGER,
    piece1 INTEGER,
    piece2 INTEGER,
    piece3 INTEGER
)
''')

cursor.execute("SELECT COUNT(*) FROM enemy_data")
count = cursor.fetchone()[0]

enemy_traits = [
    (0, 300, 'Du wurdest von Herr Lenz-Faktenverweigerer angegriffen', 'ThisCharmingMan8Bit', 'LenzFaktenverweigererSprite',
     False, True, False, False, False, 249, 623, 228),

    (1, 400, 'Du wurdest von Friedrich Schmerz angegriffen', 'ImTheOne8Bit', 'FriedrichSchmerzSprite', False, False, False, True, False, 408, 612, 160),

    (2, 400, 'Du wurdest von Georgbär angegriffen', 'RUMine8Bit', 'GeorgbaerSprite', True, False, False, False, False, 358, 612, 190),

    (3, 300, 'Du wurdest von Oleg, Fassan und Ayale angegriffen', 'RickRoll8Bit', 'olfaay3', False, False, True, False, False, 692, 612, 50),

    (4, 500, 'Du wurdest von Linus Torvalds angegriffen', 'TakeTheTime8Bit', 'LinusTorvaldsSprite', None, None, None, None, True, 408, 612, 150)
]

if count == 0:
    cursor.executemany('''
    INSERT INTO enemy_data (
    idx, startHP, message, music, sprite,
    georgAbility, lenzfaktenAbility, olfaayAbility,
    friedrichSchmerz, isLinus, width, height, dodgingThreshold
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', enemy_traits)
    connection.commit()

cursor.execute("SELECT COUNT(*) FROM piecesPos")
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute('''
    INSERT OR REPLACE INTO piecesPos (idx, piece0, piece1, piece2, piece3)
    VALUES (?, ?, ?, ?, ?)
    ''', (0, None, None, None, None))
    cursor.execute('''
    INSERT OR REPLACE INTO piecesPos (idx, piece0, piece1, piece2, piece3)
    VALUES (?, ?, ?, ?, ?)
    ''', (1, None, None, None, None))
    connection.commit()
    #print(f"Initialized piecesPos")

connection.close()


# Screen setup
WIDTH, HEIGHT = 1920, 1080
font = pygame.font.Font(None, 144)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Linux Wars")
square_positions = []
startingPlayer = 0
currentPlayerIdx = 0
won = False
lost = False
currentPlayerIdx = startingPlayer
colors = ["yellow", "green", "blue", "red"]
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
(624, 835),
(623, 755),
(543, 755),
(543, 835),
(625, 215),
(544, 215),
(625, 135),
(544, 135),
(1154, 217),
(1154, 135),
(1234, 135),
(1234, 217),
(1155, 755),
(1155, 835),
(1235, 755),
(1235, 835),
(895, 785), #gelb
(895, 725),
(895, 660),
(895, 600),
(610, 490),#grün
(670, 490),
(730, 490),
(790, 490),
(895, 200), #blau
(895, 260),
(895, 325),
(895, 385),
(1175, 490),#rot
(1110, 490),
(1050, 490),
(995, 490)
]
enemyWidth = 0
enemyHeight = 0
dodgingThreshold = 0

def setupFight(startHp, givenMessage, music, enemySprite, georg, lenz, olfaay, friedrich, isLinus, width, height, dodgthre):
    global playerFight, message, enemy_image, enemy, barrier_active0, barrier_timer0, barrier_active1, barrier_timer1, barrier_active2, barrier_timer2, barrier_active3, barrier_timer3, health_active, health_timer, FP_active, FP_timer, enemy_attack_image_active, enemy_attack_image_pos, enemy_attack_image_speed, use_special, flasche_active, flasche_speed, attack_image_active2, attack_image_pos2, attack_image_speed2, pending_attack_damage2, attack_image_active1, attack_image_pos1, attack_image_speed1, pending_attack_damage1, attack_image_active, attack_image_pos, attack_image_speed, pending_attack_damage, selected_index, pending_enemy_damage, game_over, block_mode, marker_x, marker_speed, block_result, player_turn, menu_open, menu_type, next_loud_timer, georgbaerSpecial, lenzFaktenVerweigererSpecial, olFaAySpecial, friedrichSchmerzSpecial, linus, background, healthInfoEnemyX, healthInfoEnemyY, enemyWidth, enemyHeight, dodgingThreshold
    dodgingThreshold = dodgthre
    georgbaerSpecial = georg
    lenzFaktenVerweigererSpecial = lenz
    olFaAySpecial = olfaay
    friedrichSchmerzSpecial = friedrich
    linus = isLinus
    enemyWidth = width
    enemyHeight = height
    enemy = {
    "hp": startHp,
    "rect": pygame.Rect(1640-width, 570-height//2, height, height)
    }
    message = givenMessage
    pygame.mixer.music.load(f'sounds/{music}.mp3')
    pygame.mixer.music.play(loops=-1)
    enemy_image = pygame.transform.scale(pygame.image.load(f"pictures/fight/{enemySprite}.png").convert_alpha(), (width, height))
    playerFight = {
    "hp": 100,
    "fp": 10,
    "items": {"hp": 2, "fp": 2},
    "rect": pygame.Rect(272, 264, 612, 612)
    }
    healthInfoEnemyX = 1640-width+width//2-120
    healthInfoEnemyY = 570-height//2-91
    
    barrier_active0 = False
    barrier_timer0 = 0

    barrier_active1 = False
    barrier_timer1 = 0

    barrier_active2 = False
    barrier_timer2 = 0

    barrier_active3 = False
    barrier_timer3 = 0

    health_active = False
    health_timer = 0

    FP_active = False
    FP_timer = 0

    enemy_attack_image_active = False
    enemy_attack_image_pos = [0, 0]
    enemy_attack_image_speed = 12

    background = pygame.image.load("pictures/fight/fightBackground.png")

    use_special = False

    flasche_active = False
    flasche_speed = 3

    attack_image_active2 = False
    attack_image_pos2 = [0, 0]
    attack_image_speed2 = 12
    pending_attack_damage2 = 0

    attack_image_active1 = False
    attack_image_pos1 = [0, 0]
    attack_image_speed1 = 12
    pending_attack_damage1 = 0

    attack_image_active = False
    attack_image_pos = [0, 0]
    attack_image_speed = 12
    pending_attack_damage = 0
    selected_index = 0

    pending_enemy_damage = 0
    game_over = False

    block_mode = False
    marker_x = 740
    marker_speed = 6
    block_result = None
    player_turn = True
    menu_open = False
    menu_type = None
    next_loud_timer = pygame.time.get_ticks() + random.randint(15000, 25000) 

def get_enemy_from_db(idx):
    connection = sqlite3.connect("game_database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM enemy_data WHERE idx = ?", (idx,))
    row = cursor.fetchone()
    connection.close()

    if row is None:
        raise ValueError(f"Kein Gegner mit idx {idx} gefunden!")

    # row = (idx, startHP, message, music, sprite, georg, lenz, olfaay, friedrich, isLinus, width, height, dodgingThreshold)

    return {
        "startHp": row[1],
        "givenMessage": row[2],
        "music": row[3],
        "enemySprite": row[4],
        "georg": bool(row[5]),
        "lenz": bool(row[6]),
        "olfaay": bool(row[7]),
        "friedrich": bool(row[8]),
        "isLinus": bool(row[9]),
        "width": row[10],
        "height": row[11],
        "dodgthre": row[12]
    }

def get_piece_positions(idx):
    connection = sqlite3.connect("game_database.db")
    cursor = connection.cursor()

    cursor.execute('''
        SELECT piece0, piece1, piece2, piece3
        FROM piecesPos
        WHERE idx = ?
    ''', (idx,))
    
    result = cursor.fetchone()
    connection.close()

    if result:
        return list(result)
    else:
        return None  # oder [] wenn du lieber leere Liste willst
    
def update_piece_positions(idx, positions):
    connection = sqlite3.connect("game_database.db")
    cursor = connection.cursor()

    cursor.execute('''
        UPDATE piecesPos
        SET piece0 = ?, piece1 = ?, piece2 = ?, piece3 = ?
        WHERE idx = ?
    ''', (positions[0], positions[1], positions[2], positions[3], idx))

    connection.commit()
    connection.close()

def reset_game():
    global diceRollCounter, moveComplete, isRolling, playerPiece, botPiece, currentPlayerIdx, fightActive, movesInARow
    for player in players:
        player.piecesPos = [None] * 4
        for piece in player.pieces:
            piece.atHome = True
            piece.currentSquare = None
            piece.moveable = False
    diceRollCounter = 0
    moveComplete = True
    isRolling = False
    playerPiece = None
    botPiece = None
    currentPlayerIdx = 0
    fightActive = False
    movesInARow = 0

healthInfoPlayer = pygame.image.load("pictures/fight/healthInfoPlayer.png").convert_alpha()
healthInfoPlayer = pygame.transform.scale(healthInfoPlayer, (240, 132))
healthInfoEnemy = pygame.image.load("pictures/fight/healthInfoEnemy.png").convert_alpha()
healthInfoEnemy = pygame.transform.scale(healthInfoEnemy, (240, 91))
dodgingDesign = pygame.image.load("pictures/fight/dodgingDesign.png").convert_alpha()
dodgingDesign = pygame.transform.scale(dodgingDesign, (500, 90))
messageDesign = pygame.image.load("pictures/fight/messageDesign5.png").convert_alpha()
#messageDesign = pygame.transform.scale(messageDesign, (982, 60))
menuDesign = pygame.image.load("pictures/fight/menuDesign.png").convert_alpha()
menuDesign = pygame.transform.scale(menuDesign, (198, 144))

# Background Music
#pygame.mixer.music.load('sounds/TakeTheTime8Bit.mp3')
#pygame.mixer.music.play(loops=-1)

# Loud Sound Setup 
loud_sound = pygame.mixer.Sound('sounds/GeorgsyndromFix.mp3')
next_loud_timer = pygame.time.get_ticks() + random.randint(15000, 25000)  # 15-25 seconds

# Font and Clock
font = pygame.font.SysFont(None, 30)
pointInfoPlayerFont = pygame.font.SysFont(None, 60)
pointInfoEnemyFont = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game State
player_image = pygame.transform.scale(pygame.image.load("pictures/fight/PlayerSprite.png").convert_alpha(), (408, 612))    
playerFight = {
    "hp": 100,
    "fp": 10,
    "items": {"hp": 2, "fp": 2},
    "rect": pygame.Rect(100, 200, 50, 50)
}

#enemy_image = pygame.transform.scale(pygame.image.load("pictures/fight/LinusTorvaldsSprite.png").convert_alpha(), (100, 150))
   
enemy = {
    "hp": 500,
    "rect": pygame.Rect(450, 175, 50, 50)
}

georgbaerSpecial = False
lenzFaktenVerweigererSpecial = False
olFaAySpecial = False
friedrichSchmerzSpecial = False
linus = False

player_turn = True
menu_open = False
menu_type = None
message = "Du wurdest von Linus Torvalds angegriffen"
game_over = False

block_mode = False
marker_x = 740
marker_speed = 6
block_result = None

attack_options = ["Normal Attack", "Heavy Attack", "Special Attack"]
item_options = ["Use HP Item", "Use FP Item"]
selected_index = 0

pending_enemy_damage = 0


# --- Utility Functions ---
def normal_attack():
    return random.randint(10, 15)
attack_image = pygame.transform.scale(pygame.image.load("pictures/fight/Flame.png").convert_alpha(), (80, 80))
attack_image_active = False
attack_image_pos = [0, 0]
attack_image_speed = 12
pending_attack_damage = 0

def heavy_attack():
    return random.randint(15, 22)
attack_image1 = pygame.transform.scale(pygame.image.load("pictures/fight/Blue Flame.png").convert_alpha(), (110, 110))
attack_image_active1 = False
attack_image_pos1 = [0, 0]
attack_image_speed1 = 12
pending_attack_damage1 = 0


def special_attack():
        return random.randint(35, 50)
attack_image2 = pygame.transform.scale(pygame.image.load("pictures/fight/Special.png").convert_alpha(), (130, 130))
attack_image_active2 = False
attack_image_pos2 = [0, 0]
attack_image_speed2 = 12
pending_attack_damage2 = 0

flasche_image = pygame.transform.scale(pygame.image.load("pictures/fight/Flasche.png").convert_alpha(), (150, 150))
flasche_rect = flasche_image.get_rect(topleft=(386, 0))
flasche_active = False
flasche_speed = 3

#enemy attack
healthInfoEnemyX = 0
healthInfoEnemyY = 0 

enemy_attack_image = pygame.transform.scale(pygame.image.load("pictures/fight/Enemy Flame.png").convert_alpha(), (80, 80))
enemy_attack_image_active = False
enemy_attack_image_pos = [0, 0]
enemy_attack_image_speed = 12

use_special = False
gameOver = False

def draw_text(text, x, y, schriftart):
    text_surface = schriftart.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_bars():
    draw_text(f"{playerFight['hp']}", 476, 188, pointInfoPlayerFont)
    draw_text(f"{playerFight['fp']}", 476, 247, pointInfoPlayerFont)
    draw_text(f"{enemy['hp']}", healthInfoEnemyX+120, 224, pointInfoEnemyFont)

def draw_menu(options, selected_index):
    screen.blit(menuDesign, (858, 890))
    for i, option in enumerate(options):
        color = WHITE if i != selected_index else RED
        text = font.render(option, True, color)
        screen.blit(text, (886, 921 + i * 30))

def draw_block_bar():
    pygame.draw.rect(screen, WHITE, (740, 570+400, 440, 10))
    pygame.draw.rect(screen, RED, (960, 570+395, 20, 20))
    pygame.draw.rect(screen, GREEN, (marker_x, 570+395, 10, 20))
    #screen.blit(dodgingDesign, (720, 100))

barrier_image0 = pygame.image.load("pictures/fight/Broken Barrier.png").convert_alpha()  
barrier_rect0 = barrier_image0.get_rect()
barrier_image3 = pygame.image.load("pictures/fight/Barrier 3.png").convert_alpha()  
barrier_rect3 = barrier_image3.get_rect()
barrier_image2 = pygame.image.load("pictures/fight/Barrier 2.png").convert_alpha()  
barrier_rect2 = barrier_image2.get_rect()
barrier_image1 = pygame.image.load("pictures/fight/Barrier 1.png").convert_alpha()  
barrier_rect1 = barrier_image1.get_rect()

barrier_active0 = False
barrier_timer0 = 0
barrier_active1 = False
barrier_timer1 = 0
barrier_active2 = False
barrier_timer2 = 0
barrier_active3 = False
barrier_timer3 = 0

health_image = pygame.transform.scale(pygame.image.load("pictures/fight/Health.png").convert_alpha(), (100, 100))
health_rect = health_image.get_rect()

health_active = False
health_timer = 0

FP_image = pygame.transform.scale(pygame.image.load("pictures/fight/FP.png").convert_alpha(), (100, 100))
FP_rect = FP_image.get_rect()

FP_active = False
FP_timer = 0

def handle_block(dmg):
    global message
    center = 955
    distance = abs(marker_x - center)
    if distance < 10:
        blocked = dmg
        global barrier_active3, barrier_timer3
        barrier_active3 = True
        message = f"Perfect block! Blocked all {dmg} damage!"
    elif distance < 40:
        blocked = int(dmg * 0.6)
        global barrier_active2, barrier_timer2
        barrier_active2 = True
        message = f"Good block! Blocked {blocked} of {dmg} damage!"
    elif distance < 80:
        blocked = int(dmg * 0.3)
        global barrier_active1, barrier_timer1
        barrier_active1 = True
        message = f"Partial block. Blocked {blocked} of {dmg} damage."
    else:
        blocked = 0
        global barrier_active0, barrier_timer0
        barrier_active0 = True
        message = f"Missed block! Took full {dmg} damage."
    return max(dmg - blocked, 0)

clock = pygame.time.Clock()

class Player:
    def __init__(self, colorIdx, isBot):
        self.colorIdx = colorIdx
        self.pieces = []
        if not isBot:
            self.piecesPos = get_piece_positions(0)
        else:
            self.piecesPos = get_piece_positions(1)
        self.colorSquare = []
        self.homeSquares = []
        self.bot = isBot
        for i in range(4):
            self.homeSquares.append(square[36+i+4*self.colorIdx])
        for i in range(9*colorIdx, 36):
            self.colorSquare.append(square[i])
        for i in range(0, 9*colorIdx):
            self.colorSquare.append(square[i])
        for i in range(4):
            self.colorSquare.append(square[52+i+4*self.colorIdx])
        self.setup()

    def setup(self):
        for i in range(4):
            piece = Piece(self.colorIdx, i, self.piecesPos[i])
            piece.draw(self.homeSquares[i])
            self.pieces.append(piece)

    def moveable(self, pos, dice, piece):
        moveable = True
        if piece.atHome:
            if dice != 6:
                moveable = False
            else:
                if 0 in self.piecesPos:
                    moveable = False
        else:
            if pos+dice >= len(self.colorSquare):
                moveable = False
            if pos+dice in self.piecesPos:
                moveable = False
        piece.moveable = moveable
        return moveable
    
    def movePossible(self, dice):
        movePossible = False
        for piece in self.pieces:
            if self.moveable(piece.currentSquare, dice, piece):
                movePossible = True
        #print(f"{colors[self.colorIdx]} kann ziehen: {movePossible}")
        return movePossible
    
    def canBeat(self, opp, dice, pos):
        canBeat = False
        if pos == None:
            newPos = 0
        else:
            newPos = pos+dice
        oppPiecesCrd = []
        for piece in opp.pieces:
            if piece.atHome:
                oppPiecesCrd.append(None)
            else:
                oppPiecesCrd.append(opp.colorSquare[piece.currentSquare])
        if self.colorSquare[newPos] in oppPiecesCrd:
            canBeat = True
        return canBeat
    
    def threeMove(self):
        threeMove = True
        atHomeCount = 0
        for piece in self.pieces:
            if piece.atHome:
                atHomeCount += 1
        for pos in self.piecesPos:
            if pos != None:
                if pos <= len(self.colorSquare)-5 + atHomeCount:
                    threeMove = False
        #print (f"threeMove = {threeMove} because piecesPos = {self.piecesPos}")
        return threeMove
    
    def won(self):
        won = True
        for pos in self.piecesPos:
            if pos == None:
                won = False
                continue
            if pos <= len(self.colorSquare)-5:
                won = False
        return won





        



class Piece:
    def __init__(self, colorIdx, pieceIdx, startPos):           
        self.idx = pieceIdx
        self.colorIdx = colorIdx
        self.currentSquare = startPos
        self.color = colors[colorIdx]
        if startPos == None:
            self.atHome = True
        else: 
            self.atHome = False
        self.onBoard = False
        self.rotation = 0
        self.player_image = pygame.image.load(f"pictures/{self.color}.png").convert_alpha()
        self.size = 65
        self.player_image = pygame.transform.scale(self.player_image, (self.size, self.size))
        self.moveable = False

    def draw(self, pos):
        if self.moveable:
            self.rotation = (self.rotation + 5) % 360
            rotated_image = pygame.transform.rotate(self.player_image, self.rotation)
            rect = rotated_image.get_rect(center=(pos[0] + self.size // 2, pos[1] + self.size // 2))
            screen.blit(rotated_image, rect.topleft)
        else:
            #self.rotation_angle = 0  
            screen.blit(self.player_image, pos)

players = [] #Player(2*i) for i in range(2)
players.append(Player(0, False))
players.append(Player(2, True))
fightActive = False
background = pygame.image.load("pictures/ludoBackground3.png")
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

def prepareMove(currentPlayerIdxGiven):
    global moveComplete, dice, currentPlayerIdx, movesInARow, current_player
    movesInARow += 1
    #currentPlayerIdx = currentPlayerIdx
    moveComplete = False
    #dice = random.randint(1,6)
    current_player = players[currentPlayerIdxGiven]
    #for piece in current_player.pieces:
        #current_player.moveable(piece.currentSquare, dice, piece)
    #print(f"{colors[current_player.colorIdx]} at turn. {movesInARow} Moves in a Row. Pieces at: {current_player.piecesPos}")
    #print(f' Player is a Bot:{current_player.bot}')
    if not current_player.movePossible(dice):
        #print(f' Player is a Bot:{current_player.bot} No Move Possible')
        moveComplete = True
        
        #print(f"idx vor Switch: {currentPlayerIdx}, also {colors[current_player.colorIdx]}")
        if dice != 6:
            currentPlayerIdx = (currentPlayerIdxGiven + 1) % 2
        if current_player.threeMove(): #and movesInARow < 3:
            currentPlayerIdx = (currentPlayerIdx+1) % 2
        if movesInARow >= 3:
            currentPlayerIdx = (currentPlayerIdx+1) % 2
            movesInARow = 0
        #print(f"Switched Player to {colors[current_player.colorIdx]}")
    return dice    

def getPiecePositions(player):
    currentPos = []
    for myPiece in player.pieces:
        if myPiece.atHome:
            currentPos.append(player.homeSquares[myPiece.idx])
        else:
            currentPos.append(player.colorSquare(myPiece.currentSquare))
    return currentPos

def endMove(losingPiece, losingPlayer):
    pygame.mixer.music.stop()
    global movesInARow, moveComplete, currentPlayerIdx
    losingPiece.draw(losingPlayer.homeSquares[losingPiece.idx])
    losingPiece.atHome = True
    losingPiece.currentSquare = None
    losingPlayer.piecesPos[losingPiece.idx] = None

    if dice != 6: #and not (current_player.piecesPos == [None, None, None, None] and movesInARow > 3):
        currentPlayerIdx = (currentPlayerIdx + 1) % 2
        movesInARow = 0
    #print(f"Switched Player to {piece.color}")
    #print(f"piecesPos = {current_player.piecesPos}, movesInARow = {movesInARow}")                        
    moveComplete = True
    if moveComplete:
        for piece in current_player.pieces:
            piece.moveable = False
    opp = players[currentPlayerIdx]
    #oppPiecePos = getPiecePositions(opp)
    for oppPiece in opp.pieces:
        oppPiece.moveable = False
        

def move(piece):
    global movesInARow, moveComplete, current_player, currentPlayerIdx, fightActive, playerPiece, botPiece, gameOver, background
    #print("move")
    if piece.atHome:
        piece.currentSquare = 0
        piece.atHome = False                         
    else:
        piece.currentSquare += dice        
    current_player.piecesPos[piece.idx] = piece.currentSquare   
    newPos = current_player.colorSquare[piece.currentSquare]
    opp = players[(currentPlayerIdx+1)%2]
    #oppPiecePos = getPiecePositions(opp)
    for oppPiece in opp.pieces:
        if oppPiece.atHome:
            continue
        else:
            if opp.colorSquare[oppPiece.currentSquare] == newPos:
                #print("Geschlagen")
                if current_player.bot:
                    playerPiece = oppPiece
                    botPiece = piece
                else:
                    playerPiece = piece
                    botPiece = oppPiece
                
                setupFight(**get_enemy_from_db(botPiece.idx)) #glof
            
                fightActive = True
                break
    
    if current_player.won():
        if not current_player.bot:
            abilities = []
            if current_player.bot:
                bot = current_player
            else:
                bot = opp
            for pos in bot.piecesPos:
                if pos == None:
                    abilities.append(False)
                    continue
                if pos >= len(bot.colorSquare)-4:
                    abilities.append(True)
                else:
                    abilities.append(False)
            lenz = abilities[0]
            friedrich = abilities[1]
            georg = abilities[2]
            olfaay = abilities[3]
            setupFight(500, 'Du wurdest von Linus Torvalds angegriffen', 'TakeTheTime8Bit', 'LinusTorvaldsSprite', georg, lenz, olfaay, friedrich, True, 408, 612, 180)
            fightActive = True
        else:
            gameOver = True
            for i in range(2):
                for j in range (4):
                    players[i].pieces[j].currentSquare = None
            background = pygame.image.load("pictures/LosingScreen.jpg")

    if not fightActive:
        if dice != 6: #and not (current_player.piecesPos == [None, None, None, None] and movesInARow > 3):
            currentPlayerIdx = (currentPlayerIdx + 1) % 2
            movesInARow = 0
    #print(f"Switched Player to {piece.color}")
    #print(f"piecesPos = {current_player.piecesPos}, movesInARow = {movesInARow}")                        
        moveComplete = True
        #print(moveComplete)


               
running = True
playerPiece = None
botPiece = None
fullscreen = False
dice_frames = [pygame.image.load(f"pictures/dice/pics/frames/frame{i}.png").convert_alpha() for i in range(1, 10)]
for i in range(len(dice_frames)):
    dice_frames[i] = pygame.transform.scale(dice_frames[i], (120, 120))  # Optional skalieren
isRolling = False
diceFrameIndex = 0
diceRollDelay = 1  # Anzahl Frames, die ein Bild angezeigt wird
diceRollCounter = 0
moveComplete = True
#fightActive = True
#setupFight(**get_enemy_from_db(1)) #glof
#setupFight(500, 'Du wurdest von Linus Torvalds angegriffen', 'TakeTheTime8Bit', 'LinusTorvaldsSprite', True, False, True, True, True, 408, 612)

dice = 0
movesInARow = 0
current_player = players[currentPlayerIdx]

# Game loop
while running:
    if not fightActive and not gameOver:
        
        #while running:
            #print("onBoard")
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT and not fightActive:
                    running = False
                if event.type == pygame.KEYDOWN and not fightActive:
                    if event.key == pygame.K_SPACE and moveComplete and not current_player.bot and not fightActive:
                        isRolling = True
                        diceFrameIndex = 0
                        diceRollCounter = 0
                        moveComplete = False
                        dice = random.randint(1,6)
                    if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        #print("STRG + R wurde gedrückt")
                        reset_game()
                if event.type == pygame.MOUSEBUTTONDOWN and not moveComplete and not current_player.bot and not fightActive:
                    mouse_pos = pygame.mouse.get_pos()
                    if not moveComplete and not fightActive:
                        current_player = players[currentPlayerIdx]
                        for piece in current_player.pieces:
                            if piece.atHome: 
                                piece_rect = pygame.Rect(current_player.homeSquares[piece.idx][0], current_player.homeSquares[piece.idx][1], piece.size, piece.size)
                            else:
                                piece_rect = pygame.Rect(current_player.colorSquare[piece.currentSquare][0], current_player.colorSquare[piece.currentSquare][1], piece.size, piece.size)
                            if piece_rect.collidepoint(mouse_pos) and current_player.moveable(piece.currentSquare, dice, piece):
                                chosenPiece = piece
                                move(chosenPiece)                        
                                break  
                                #print(f"{piece.color} ist am Zug: {moveComplete}")
                        if moveComplete and not fightActive:
                            for piece in current_player.pieces:
                                piece.moveable = False
            if moveComplete and current_player.bot and not fightActive:
                isRolling = True
                diceFrameIndex = 0
                diceRollCounter = 0
                moveComplete = False
                dice = random.randint(1,6)
                #print('Still Alive')
            if not moveComplete and current_player.bot and not isRolling and not fightActive:
                current_player = players[currentPlayerIdx]
                moveablePieces = []
                for piece in current_player.pieces:
                    if current_player.moveable(piece.currentSquare, dice, piece):
                        moveablePieces.append(piece)
                opp = players[(currentPlayerIdx+1)%2]
                beatableIdx = []
                for i, piece in enumerate(moveablePieces):
                    if current_player.canBeat(opp, dice, piece.currentSquare):
                        beatableIdx.append(i)
                if len(beatableIdx) == 0:
                    chosenPiece = moveablePieces[random.randint(0, len(moveablePieces)-1)]
                    #print("Just random")
                elif len(beatableIdx) == 1:
                    chosenPiece = moveablePieces[beatableIdx[0]]
                    #print("Bewusst geschlagen.")
                elif len(beatableIdx) > 1:
                    chosenPiece = moveablePieces[beatableIdx[random.randint(0, len(beatableIdx)-1)]]
                    #print(f"Bewusst geschlagen, eine von {len(beatableIdx)} Schlägen ausgewählt")
                move(chosenPiece)
                if moveComplete:
                    for piece in current_player.pieces:
                        piece.moveable = False


            window_size = screen.get_size()
            bg_scaled, bg_pos = get_scaled_background(window_size)
            screen.fill((0, 0, 0))
            screen.blit(bg_scaled, bg_pos)
            keys = pygame.key.get_pressed()
            #if keys[pygame.K_LEFT]:
                #player_pos[0] -= player_speed
            #player_pos[0] = max(0, min(window_size[0] - player_size, player_pos[0]))
            #player_pos[1] = max(0, min(window_size[1] - player_size, player_pos[1]))
            for player in players:
                for piece in player.pieces:
                    if piece.atHome:
                        piece.draw(player.homeSquares[piece.idx])
                    else:
                        piece.draw(player.colorSquare[piece.currentSquare])
            #if current_player.bot:
        #print(f"diceRolling. {isRolling}")
            if isRolling:
                screen.blit(dice_frames[diceFrameIndex // diceRollDelay], (WIDTH//2 - 92, HEIGHT//2 - 76))  # zentriert zeichnen
                diceRollCounter += 1
                #print("Still alive")
                if diceRollCounter >= diceRollDelay:
                    diceRollCounter = 0
                    diceFrameIndex += 1
                #if current_player.bot:
                        #print('Still alive')
                if diceFrameIndex >= len(dice_frames) * diceRollDelay:
                    isRolling = False
                    dice = prepareMove(currentPlayerIdx)
                    #actualPiecesPos = []
                    for player in players:
                        actualPiecesPos = []
                        for piece in player.pieces:
                            actualPiecesPos.append(piece.currentSquare)
                        #print(f"{player.piecesPos} actually at {actualPiecesPos}")
            else:
                if 0 < dice <= 6:
                    dice_image = pygame.image.load(f"pictures/dice/pics/dice{dice}.png").convert_alpha()
                else:
                    dice_image = pygame.image.load(f"pictures/dice/pics/dice1.png").convert_alpha()
                dice_image = pygame.transform.scale(dice_image, (120, 120))
                screen.blit(dice_image, (WIDTH//2-92, HEIGHT//2-76))
            current_player = players[currentPlayerIdx]
            pygame.display.flip()

            #print(fightActive)
    if fightActive and not gameOver:
    #setupFight(300, 'Du wurdest von Herr Lenz-Faktenverweigerer angegriffen', 'ThisCharmingMan8Bit', 'LenzFaktenverweigererSprite')
    #running = True
    #while running:
        #print("Fight started:")
        
        #pygame.display.flip()

        current_time = pygame.time.get_ticks()
        clock.tick(60)
        window_size = screen.get_size()
        losingScreen_scaled, bg_pos = get_scaled_background(window_size)
        screen.fill((0, 0, 0))
        screen.blit(losingScreen_scaled, bg_pos)
        screen.blit(healthInfoPlayer, (356, 148))
        screen.blit(healthInfoEnemy, (healthInfoEnemyX, healthInfoEnemyY))
        screen.blit(messageDesign, (468, 5))
        
        if georgbaerSpecial:
            if current_time >= next_loud_timer: #Georgsyndrom
                loud_sound.play()
                playerFight["hp"] -= 10
                message = "Georgsyndrom. 10 schaden."
                next_loud_timer = current_time + random.randint(15000, 25000)
                flasche_active = True
                flasche_rect.topleft = (386, 0) #georgsyndrom ende

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if friedrichSchmerzSpecial:
                if not block_mode and event.type == pygame.KEYDOWN: #friedrich
                    if random.random() < 1:
                        playerFight['hp'] -= 1
                        message = "Du leidest an Friedrich Schmerzen" #friedrich

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
                            if lenzFaktenVerweigererSpecial:
                                if random.random() < 0.5: #lenz
                                    message = "Angriff wurde verweigert"
                                    menu_open = False
                                    player_turn = False
                                    pygame.time.set_timer(pygame.USEREVENT, 1000)
                                    continue #lenz

                            if selected_index == 0:  # Normal
                                pending_attack_damage = normal_attack()
                                # Start the image from just beside the player
                                attack_image_pos = [playerFight['rect'].centery, playerFight['rect'].centery]
                                attack_image_active = True
                                menu_open = False
                                dmg = normal_attack()
                            elif selected_index == 1:  # Heavy
                                if playerFight['fp'] >= 1:
                                    pending_attack_damage1 = heavy_attack()
                                    # Start the image from just beside the player
                                    attack_image_pos1 = [playerFight['rect'].centery, playerFight['rect'].centery]
                                    attack_image_active1 = True
                                    menu_open = False
                                    dmg = heavy_attack()
                                    playerFight['fp'] -= 1
                                else:
                                    message = "Not enough FP for Heavy Attack!"
                                    continue
                            elif selected_index == 2:  # Special
                                if playerFight['fp'] >= 3:
                                    pending_attack_damage2 = special_attack()
                                    # Start the image from just beside the player
                                    attack_image_pos2 = [playerFight['rect'].centery, playerFight['rect'].centery]
                                    attack_image_active2 = True
                                    menu_open = False
                                    dmg = special_attack()
                                    playerFight['fp'] -= 3
                                else:
                                    message = "Not enough FP for Special Attack!"
                                    continue
                            # Backfire chance
                            if olFaAySpecial:
                                if random.random() < 0.5: #olfaay
                                    backfire = int(dmg * random.uniform(0.3, 0.7))
                                    playerFight['hp'] -= backfire
                                    message = random.choice(["Oleg meine Eier", "Fassan meine Eier", "Ayale gen"])

                        elif menu_type == 'item':
                            if selected_index == 0 and playerFight['items']['hp'] > 0:
                                playerFight['hp'] += 30
                                playerFight['items']['hp'] -= 1
                                message = "Used HP item! +30 HP"
                                health_active = True
                                health_timer = pygame.time.get_ticks()

                            elif selected_index == 1 and playerFight['items']['fp'] > 0:
                                playerFight['fp'] += 3
                                playerFight['items']['fp'] -= 1
                                message = "Used FP item! +3 FP"
                                FP_active = True
                                FP_timer = pygame.time.get_ticks()
                            else:
                                message = "No item left!"
                                continue
                        menu_open = False
                        player_turn = False
                        pygame.time.set_timer(pygame.USEREVENT, 1000)

            elif event.type == pygame.USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                if use_special:
                    pending_enemy_damage = special_attack()
                    message = "Enemy used Special Attack! Press SPACE to block!"
                else:
                    pending_enemy_damage = normal_attack()
                    message = "Enemy used Normal Attack! Press SPACE to block!"
                enemy_attack_image_pos = [enemy['rect'].left, enemy['rect'].centery]    
                block_mode = True
                marker_x = 740

            elif block_mode and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    final_dmg = handle_block(pending_enemy_damage)
                    playerFight['hp'] -= final_dmg
                    block_mode = False
                    player_turn = True




        screen.blit(player_image, playerFight['rect'])
        screen.blit(enemy_image, enemy['rect'])

        if barrier_active0:
            barrier_rect0.midleft = (playerFight['rect'].right + 5, playerFight['rect'].centery)
            screen.blit(barrier_image0, barrier_rect0)

        if barrier_active1:
            barrier_rect1.midleft = (playerFight['rect'].right + 5, playerFight['rect'].centery)
            screen.blit(barrier_image1, barrier_rect1)

        if barrier_active2:
            barrier_rect2.midleft = (playerFight['rect'].right + 5, playerFight['rect'].centery)
            screen.blit(barrier_image2, barrier_rect2)

        if barrier_active3:
            barrier_rect3.midleft = (playerFight['rect'].right + 5, playerFight['rect'].centery)
            screen.blit(barrier_image3, barrier_rect3)


        if barrier_active0 and pygame.time.get_ticks() - barrier_timer0 > 1000:  # Barrier lasts 1 second
            barrier_active0 = False

        if barrier_active1 and pygame.time.get_ticks() - barrier_timer1 > 1000:  # Barrier lasts 1 second
            barrier_active1 = False

        if barrier_active2 and pygame.time.get_ticks() - barrier_timer2 > 1000:  # Barrier lasts 1 second
            barrier_active2 = False

        if barrier_active3 and pygame.time.get_ticks() - barrier_timer3 > 1000:  # Barrier lasts 1 second
            barrier_active3 = False

        draw_bars()

        if health_active:
            health_rect.midleft = (580, 195) ###ggd
            screen.blit(health_image, health_rect)

        if health_active and pygame.time.get_ticks() - health_timer > 1000:  # show for 1 second
            health_active = False    

        if FP_active:
            #FP_rect.midleft = (playerFight['rect'].right + 50, playerFight['rect'].centery)
            FP_rect.midleft = (580, 260)
            screen.blit(FP_image, FP_rect)

        if FP_active and pygame.time.get_ticks() - FP_timer > 1000:  # show for 1 second
            FP_active = False

        if menu_open and not block_mode:
            if menu_type == 'attack':
                draw_menu(attack_options, selected_index)
            elif menu_type == 'item':
                draw_menu(item_options, selected_index)

        if block_mode and enemy['hp'] >= 1:
            draw_block_bar()
            marker_x += marker_speed
            enemy_attack_image_active = True
            # Start the projectile at the enemy's right

            enemy_attack_image_pos = [enemy['rect'].left, enemy['rect'].centery]
            if marker_x > 1170 or marker_x < 740:
                marker_speed *= -1

        draw_text(message, 960, 36, font)

        if attack_image_active:
        # Target is the center of the enemy
            target_x, target_y = enemy['rect'].center

            dx = target_x - attack_image_pos[0]
            dy = target_y - attack_image_pos[1]
            distance = (dx**2 + dy**2)**0.5

            if attack_image_pos[0] > (1640-enemyWidth)+enemyWidth//2-dodgingThreshold:
                # Damage applied on arrival
                enemy['hp'] -= pending_attack_damage
                attack_image_active = False
                
                player_turn = False
                pygame.time.set_timer(pygame.USEREVENT, 1000)
                message = f"Normal Attack hit for {pending_attack_damage} damage!"
                pending_attack_damage = 0
            else:
                # Move image toward the enemy
                attack_image_pos[0] += attack_image_speed * dx / distance
                attack_image_pos[1] += attack_image_speed * dy / distance

            # Draw the attack image
            attack_rect = attack_image.get_rect(center=(int(attack_image_pos[0]), int(attack_image_pos[1])))
            screen.blit(attack_image, attack_rect)

        if attack_image_active1:
        # Target is the center of the enemy
            target_x1, target_y1  = enemy['rect'].center

            dx1 = target_x1 - attack_image_pos1[0] 
            dy1 = target_y1 - attack_image_pos1[1] 
            distance1 = (dx1**2 + dy1**2)**0.5

            if attack_image_pos1[0] > (1640-enemyWidth)+enemyWidth//2-dodgingThreshold:
                # Damage applied on arrival
                enemy['hp'] -= pending_attack_damage1
                attack_image_active1 = False
                
                player_turn = False
                pygame.time.set_timer(pygame.USEREVENT, 1000)
                message = f"Heavy Attack hit for {pending_attack_damage1} damage!"
                pending_attack_damage1 = 0
            else:
                # Move image toward the enemy
                attack_image_pos1[0] += attack_image_speed1 * dx1 / distance1
                attack_image_pos1[1] += attack_image_speed1 * dy1 / distance1
        # Draw the attack image
            attack_rect = attack_image.get_rect(center=(int(attack_image_pos1[0]), int(attack_image_pos1[1])))
            screen.blit(attack_image1, attack_rect)

        if attack_image_active2:
        # Target is the center of the enemy
            target_x2, target_y2 = enemy['rect'].center
            dx2 = target_x2 - attack_image_pos2[0] 
            dy2 = target_y2 - attack_image_pos2[1] 
            distance2 = (dx2**2 + dy2**2)**0.5

            if attack_image_pos2[0] > (1640-enemyWidth)+enemyWidth//2-dodgingThreshold:
            # Damage applied on arrival
                enemy['hp'] -= pending_attack_damage2
                attack_image_active2 = False
                
                player_turn = False
                pygame.time.set_timer(pygame.USEREVENT, 1000)
                message = f"Special Attack hit for {pending_attack_damage2} damage!"
                pending_attack_damage2 = 0
            else:
                # Move image toward the enemy
                attack_image_pos2[0] += attack_image_speed2 * dx2 / distance2
                attack_image_pos2[1] += attack_image_speed2 * dy2 / distance2

        # Draw the attack image
            attack_rect = attack_image.get_rect(center=(int(attack_image_pos2[0]), int(attack_image_pos2[1])))
            screen.blit(attack_image2, attack_rect)

        if enemy_attack_image_active:
            # Target is the player's center
            target_x, target_y = playerFight['rect'].center
            if barrier_active0:
                dx = target_x - enemy_attack_image_pos[0] 
                dy = target_y - enemy_attack_image_pos[1]
            else:
                dx = target_x - enemy_attack_image_pos[0] + 70
                dy = target_y - enemy_attack_image_pos[1]    
            distance = (dx**2 + dy**2)**0.5 

            if distance < enemy_attack_image_speed:
                # On reaching the player, stop animation
                enemy_attack_image_active = False
            else:
                enemy_attack_image_pos[0] += enemy_attack_image_speed * dx / distance
                enemy_attack_image_pos[1] += enemy_attack_image_speed * dy / distance

             # Draw the projectile
            enemy_attack_rect = enemy_attack_image.get_rect(center=(int(enemy_attack_image_pos[0]), int(enemy_attack_image_pos[1])))
            screen.blit(enemy_attack_image, enemy_attack_rect)

        if flasche_active and georgbaerSpecial: #georg
            # Move the bottle down
            flasche_rect.y += flasche_speed

            # Check for collision with player
            if flasche_rect.colliderect(playerFight['rect']):
                flasche_active = False  # Disappear on impact

            # Draw the bottle
            screen.blit(flasche_image, flasche_rect) #georg



        if playerFight['hp'] <= 0:
            message = "You lost!"
            
            game_over = True
            if not linus:
                for player in players:
                    if not player.bot:
                        playerPlayer = player
                endMove(playerPiece, playerPlayer)
                fightActive = False
                background = pygame.image.load("pictures/LudoBackground3.png")
            else:
                gameOver = True
                for i in range(2):
                    for j in range (4):
                        players[i].pieces[j].currentSquare = None
                background = pygame.image.load("pictures/LosingScreen.jpg")
        elif enemy['hp'] <= 0:
            message = "You won!"
            
            game_over = True
            if not linus:
                for player in players:
                    if player.bot:
                        botPlayer = player
                endMove(botPiece, botPlayer)
                fightActive = False
                background = pygame.image.load("pictures/LudoBackground3.png")
            else:
                gameOver = True
                for i in range(2):
                    for j in range (4):
                        players[i].pieces[j].currentSquare = None
                background = pygame.image.load("pictures/WinningScreen.jpg")


        pygame.display.flip()
        #clock.tick(60)
    
    if gameOver:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False      
            window_size = screen.get_size()
            losingScreen_scaled, bg_pos = get_scaled_background(window_size)
            screen.fill((0, 0, 0))
            screen.blit(losingScreen_scaled, bg_pos)
            pygame.display.flip()

for i in range(2):
    for j in range(4):
        players[i].piecesPos[j] = players[i].pieces[j].currentSquare
    update_piece_positions(i, players[i].piecesPos)
    #print(f"updated {i} to {players[i].piecesPos}")

pygame.quit()
sys.exit()

#1. dice fix #5
#2. winning/losing screen #4
#3. put onboard prio #6
#4. correct enemy #done
#5. datenbanken #3
#6. richtige größe #1
#7. design #2
#8. linus fight #0
#font & symbole statt text im menü
#game icon