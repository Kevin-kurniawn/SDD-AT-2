# From PyGuru 

import pygame

SCREEN = WIDTH, HEIGHT = 300, 300
CELLSIZE = 30
PADDING = 30
ROWS = COLS = (WIDTH - 4*PADDING) // CELLSIZE
print(ROWS, COLS)

pygame.init()
win = pygame.display.set_mode(SCREEN)

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

smallfont = pygame.font.SysFont('cursive', 10)
font = pygame.font.SysFont('cursive', 25)

class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.index = self.r * ROWS + self.c

        self.rect = pygame.Rect((c*CELLSIZE + 2*PADDING, r*CELLSIZE + 3*PADDING, CELLSIZE, CELLSIZE))

        self.left = self.rect.left
        self.top = self.rect.top
        self.right = self.rect.right
        self.bottom = self.rect.bottom

        self.edges = [
                        [(self.left, self.top), (self.right, self.top)],
                        [(self.right, self.top), (self.right, self.bottom)],
                        [(self.right, self.bottom), (self.left, self.bottom)],
                        [(self.left, self.bottom), (self.left, self.top)]
                    ]
        
        self.sides = [False, False, False, False]
        self.winner = None

    def checkwin(self, winner):
        if not self.winner:
            if self.sides == [True]*4:
                self.winner = winner
                if winner == '1':
                    self.color = GREEN
                else:
                    self.color = RED
                self.text = font.render(self.winner, True, WHITE)

                return 1
        return 0

    def update(self, win):
        if self.winner:
            pygame.draw.rect(win, self.color, self.rect)
            win.blit(self.text, (self.rect.centerx-5, self.rect.centery-7))
        for index, side in enumerate(self.sides):
            if side:
                pygame.draw.line(win, BLACK, (self.edges[index][0]),
                                 self.edges[index][1], 2)
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
    up = False
    right = False
    bottom = False
    left = False
    return pos, ccell, up, right, bottom, left

def reset_score():
    fillcount = 0
    p1_score = 0
    p2_score = 0
    return fillcount, p1_score, p2_score

def reset_player():
    turn = 0
    players = ['1', '2']
    player = players[turn]
    next_turn = False
    return turn, players, player, next_turn

start = False
gameover = False
cells = create_cells()
pos, ccell, up, right, bottom, left = reset_cells()
fillcount, p1_score, p2_score = reset_score()
turn, players, player, next_turn = reset_player()

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

            if event.key == pygame.K_r or event.key == pygame.K_s:
                start = True
                gameover = False
                cells = create_cells()
                pos, ccell, up, right, bottom, left = reset_cells()
                fillcount, p1_score, p2_score = reset_score()
                turn, players, player, next_turn = reset_player()
            if start and not gameover:
                if event.key == pygame.K_UP:
                    up = True 
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_DOWN:
                    bottom = True 
                if event.key == pygame.K_LEFT:
                    left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
               up = False 
            if event.key == pygame.K_RIGHT:
               right = False
            if event.key == pygame.K_DOWN:
               bottom = False 
            if event.key == pygame.K_LEFT:
               left = False 

    # Creating grid
    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            pygame.draw.circle(win, BLACK, (c*CELLSIZE + 2*PADDING, r*CELLSIZE + 3*PADDING), 2)
    
    # Creating 'cells' - the boxes - and detecting which cell is clicked
    for cell in cells:
        cell.update(win)
        if pos and cell.rect.collidepoint(pos):
            ccell = cell
    
    # Selects a specific cell, as defined by the mouse pointer
    if ccell:
        index = ccell.index
        if not ccell.winner:
            pygame.draw.circle(win, RED, (ccell.rect.centerx, ccell.rect.centery), 2)

        if up and not ccell.sides[0]:
            ccell.sides[0] = True
            if index - ROWS >= 0:
                cells[index - ROWS].sides[2] = True
                next_turn = True
        if right and not ccell.sides[1]:
            ccell.sides[1] = True
            if (index + 1) % COLS > 0:
                cells[index+1].sides[3] = True
                next_turn = True
        if bottom and not ccell.sides[2]:
            ccell.sides[2] = True
            if (index + ROWS) < len(cells):
                cells[index + ROWS].sides[0] = True
                next_turn = True
        if left and not ccell.sides[3]:
            ccell.sides[3] = True
            if index % COLS > 0:
                cells[index-1].sides[1] = True
                next_turn = True

        res = ccell.checkwin(player)
        if res:
            fillcount += res
            if player == '1':
                p1_score += 1
            else:
                p2_score += 1

            if fillcount == ROWS * COLS:
                print(p1_score, p2_score)
                gameover = True

        if next_turn:
            turn = (turn + 1) % len(players)
            player = players[turn]
            next_turn = False
        
    p1img = font.render(f'Player 1 : {p1_score}', True, BLUE)
    p1rect = p1img.get_rect()
    p1rect.x, p1rect.y = PADDING, 15

    p2img = font.render(f'Player 2 : {p2_score}', True, BLUE)
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
    
    if gameover:
        rect = pygame.Rect((50, 100, WIDTH-100, HEIGHT-200))
        pygame.draw.rect(win, BLACK, rect)
        pygame.draw.rect(win, RED, rect, 2)

        over = font.render('Game Over', True, WHITE)
        win.blit(over, (rect.centerx-over.get_width()//2, rect.y+10))

        winner = '1' if p1_score > p2_score else '2'
        winner_img = font.render(f'Player {winner} Won', True, GREEN)
        win.blit(winner_img, (rect.centerx-winner_img.get_width()//2, rect.centery-10))

        msg = 'Press r:restart, q:quit'
        msgimg = font.render(msg, True, RED)
        win.blit(msgimg, (rect.centerx-msgimg.get_width()//2, rect.centery+20))

    pygame.display.update()

pygame.quit()