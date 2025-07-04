import pygame
import sys
import random
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1920, 1080
font = pygame.font.Font(None, 144)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joe the Square vs The Corners of Doom")
square_positions = []
startingPlayer = 0
currentPlayerIdx = 0
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

clock = pygame.time.Clock()

class Player:
    def __init__(self, colorIdx, isBot):
        self.colorIdx = colorIdx
        self.pieces = []
        self.piecesPos = [None] * 4
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
            piece = Piece(self.colorIdx, i)
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
        print (f"threeMove = {threeMove} because piecesPos = {self.piecesPos}")
        return threeMove




        



class Piece:
    def __init__(self, colorIdx, pieceIdx):           
        self.idx = pieceIdx
        self.colorIdx = colorIdx
        self.currentSquare = None
        self.color = colors[colorIdx]
        self.atHome = True
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
    dice = random.randint(1,6)
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

def move(piece):
    global movesInARow, moveComplete, current_player, currentPlayerIdx
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
                oppPiece.draw(opp.homeSquares[oppPiece.idx])
                oppPiece.atHome = True
                oppPiece.currentSquare = None
                opp.piecesPos[oppPiece.idx] = None
                break
    if dice != 6: #and not (current_player.piecesPos == [None, None, None, None] and movesInARow > 3):
        currentPlayerIdx = (currentPlayerIdx + 1) % 2
        movesInARow = 0
    #print(f"Switched Player to {piece.color}")
    #print(f"piecesPos = {current_player.piecesPos}, movesInARow = {movesInARow}")                        
    moveComplete = True

# Game loop
running = True
fullscreen = False
dice_frames = [pygame.image.load(f"pictures/dice/pics/frames/frame{i}.png").convert_alpha() for i in range(1, 10)]
for i in range(len(dice_frames)):
    dice_frames[i] = pygame.transform.scale(dice_frames[i], (120, 120))  # Optional skalieren
isRolling = False
diceFrameIndex = 0
diceRollDelay = 2  # Anzahl Frames, die ein Bild angezeigt wird
diceRollCounter = 0
moveComplete = True
dice = 0
movesInARow = 0
current_player = players[currentPlayerIdx]
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and moveComplete and not current_player.bot:
                isRolling = True
                diceFrameIndex = 0
                diceRollCounter = 0
                moveComplete = False
        if event.type == pygame.MOUSEBUTTONDOWN and not moveComplete and not current_player.bot:
            mouse_pos = pygame.mouse.get_pos()
            if not moveComplete:
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
                if moveComplete:
                    for piece in current_player.pieces:
                        piece.moveable = False
    if moveComplete and current_player.bot:
        isRolling = True
        diceFrameIndex = 0
        diceRollCounter = 0
        moveComplete = False
        #print('Still Alive')
    if not moveComplete and current_player.bot and not isRolling:
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
    else:
        if 0 < dice <= 6:
            dice_image = pygame.image.load(f"pictures/dice/pics/dice{dice}.png").convert_alpha()
        else:
            dice_image = pygame.image.load(f"pictures/dice/pics/dice1.png").convert_alpha()
        dice_image = pygame.transform.scale(dice_image, (120, 120))
        screen.blit(dice_image, (WIDTH//2-92, HEIGHT//2-76))
    current_player = players[currentPlayerIdx]
    pygame.display.flip()
pygame.quit()
sys.exit()