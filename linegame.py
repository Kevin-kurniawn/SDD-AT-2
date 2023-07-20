import pygame
import random

SCREEN = WIDTH, HEIGHT = 300, 300
CELLSIZE = 30
PADDING = 30
ROWS = COLS = (WIDTH - 4*PADDING) // CELLSIZE
print(ROWS, COLS)

pygame.init()
win = pygame.display.set_mode(SCREEN)

WHITE = (255,255,255)
RED = (179, 39, 29)
YELLOW = (252,180,0)
ORANGE = (235, 95, 40)
GREEN = (59, 166, 50)
BLUE = (21, 127, 176)
GREY = (166, 163, 162)
BLACK = (0,0,0)

smallfont = pygame.font.SysFont('cursive', 15)
font = pygame.font.SysFont('cursive', 25)

class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.index = self.r * ROWS + self.c

        self.rect = pygame.Rect((c*CELLSIZE + 2*PADDING, r*CELLSIZE + 3*PADDING, CELLSIZE, CELLSIZE))

        self.winner = None
    
    def count_connected_cells(self, dr, dc, player, cells):
        r, c = self.r + dr, self.c + dc
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLS:
            cell = cells[r * ROWS + c]
            if cell.winner == player:
                count += 1
                r += dr
                c += dc
            else:
                break
        return count

    def checkwin(self, winner):
        if not self.winner:
            self.winner = winner
            if winner == '1':
                self.color = BLUE
            else:
                self.color = RED
            self.text = font.render(self.winner, True, WHITE)
                
            return 1
        return 0

    def update(self, win):
        if self.winner:
            pygame.draw.rect(win, self.color, self.rect)
            win.blit(self.text, (self.rect.centerx-5, self.rect.centery-7))

def wincondition(cells):
        #Check horizontally
        for r in range(ROWS):
            for c in range(COLS-3):
                current_player = cells[r * ROWS + c].winner
                if current_player:
                    if all(cells[r * ROWS + c + i].winner == current_player for i in range(4)):
                        return True, current_player
        #Check vertically
        for r in range(ROWS-3):
            for c in range(COLS):
                current_player = cells[r * ROWS + c].winner
                if current_player:
                    if all(cells[(r + i) * ROWS + c].winner == current_player for i in range(4)):
                        return True, current_player
        #Check diagonally
        for r in range(ROWS-3):
            for c in range(COLS-3):
                current_player = cells[r * ROWS + c].winner
                if current_player:
                    if all(cells[(r + i) * ROWS + c + i].winner == current_player for i in range(4)):
                        return True, current_player

def computer_move():
    global ccell, next_turn, turn, player

    # Find available cells (not occupied by any player)
    available_cells = [cell for cell in cells if not cell.winner]

    #Check for winning move
    for cell in available_cells:
        cell.winner = player
        if wincondition(cells):
            ccell = cell
            next_turn = True
            break
        cell.winner = None
    
    #Check for blocking move
    if not next_turn:
        for cell in available_cells:
                cell.winner = players[(turn + 1) % 2]
                if wincondition(cells):
                    ccell = cell
                    next_turn = True
                    break
                cell.winner = None

    #If no available wins or blocks, randomly choose a cell
    if not next_turn:
        if available_cells:
            ccell = random.choice(available_cells)

    if ccell:
        if ccell.checkwin(player):
            next_turn = True

        # Switch to the next player
        turn = (turn + 1) % 2
        player = players[turn]
        next_turn = False

def create_cells():
    cells = []
    for r in range(ROWS):
        for c in range (COLS):
            cell = Cell(r, c)
            cells.append(cell)
    return cells

def reset_cells():
    pos = None
    ccell = None
    return pos, ccell

def reset_turn():
    turn = 0
    players = ['1', '2']
    is_human = [True, False]  # Indicates whether each player is human or computer
    player = players[turn]
    next_turn = False
    return turn, players, player, next_turn, is_human


gameover = False
cells = create_cells()
pos, ccell = reset_cells()
turn, players, player, next_turn, is_human = reset_turn()

running = True
while running:

    # Key presses and screen colour
    win.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            pos = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
            
            if event.key == pygame.K_r:
                gameover = False
                cells = create_cells()
                pos, ccell = reset_cells()
                turn, players, player, next_turn, is_human = reset_turn()
        
    for r in range(ROWS+1):
        for c in range(COLS+1):
            pygame.draw.circle(win, BLACK, (c*CELLSIZE + 2*PADDING, r*CELLSIZE + 3*PADDING), 2)
    
    for cell in cells:
        cell.update(win)
        if pos and cell.rect.collidepoint(pos):
            ccell = cell

    if ccell:
        index = ccell.index

        if ccell.checkwin(player):
            next_turn = True

        if next_turn:
            if is_human[turn]:  # Check if the current player is human
                turn = (turn + 1) % 2
                player = players[turn]
                next_turn = False

    # Computer's turn (Player 2)
    if not is_human[turn] and not next_turn and not gameover:
        computer_move()
        
    p1img = font.render('Player 1', True, BLUE)
    p1rect = p1img.get_rect()
    p1rect.x, p1rect.y = PADDING, 15

    p2img = font.render('Player 2', True, BLUE)
    p2rect = p2img.get_rect()
    p2rect.right, p2rect.y = WIDTH-PADDING, 15

    win.blit(p1img, p1rect)
    win.blit(p2img,p2rect)
    if player == '1':
        pygame.draw.line(win, BLUE, (p1rect.x, p1rect.bottom+2),
                            (p1rect.right, p1rect.bottom+2), 1)
    else:
        pygame.draw.line(win, BLUE, (p2rect.x, p2rect.bottom+2),
                            (p2rect.right, p2rect.bottom+2), 1)    

    if wincondition(cells):
        gameover = wincondition(cells)

    if gameover:
        rect = pygame.Rect((50, 100, WIDTH-100, HEIGHT-200))
        pygame.draw.rect(win, BLACK, rect)
        pygame.draw.rect(win, RED, rect, 2)

        over = font.render('Game Over', True, WHITE)
        win.blit(over, (rect.centerx-over.get_width()//2, rect.y+10))

        winner_img = font.render(f'Player {gameover[1]} Won', True, BLUE)
        win.blit(winner_img, (rect.centerx-winner_img.get_width()//2, rect.centery-10))

        msg = 'Press r:restart, q:quit'
        msgimg = font.render(msg, True, RED)
        win.blit(msgimg, (rect.centerx-msgimg.get_width()//2, rect.centery+20))

    pygame.display.update()

pygame.quit()