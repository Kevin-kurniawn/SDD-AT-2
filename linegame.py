import pygame

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

    def checkwin(self, winner):
        if not self.winner:
            if cell.rect.collidepoint(pos):
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

def reset_score():
    p1_score = 0
    p2_score = 0
    return p1_score, p2_score

def reset_player():
    turn = 0
    players = ['1', '2']
    player = players[turn]
    next_turn = False
    return turn, players, player, next_turn

start = False
gameover = False
cells = create_cells()
pos, ccell = reset_cells()
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
                pos, ccell = reset_cells()
                p1_score, p2_score = reset_score()
                turn, players, player, next_turn = reset_player()
        
    for r in range(ROWS+1):
        for c in range(COLS+1):
            pygame.draw.circle(win, BLACK, (c*CELLSIZE + 2*PADDING, r*CELLSIZE + 3*PADDING), 2)
    
    for cell in cells:
        cell.update(win)
        if pos and cell.rect.collidepoint(pos):
            ccell = cell

    if ccell:
        index = ccell.index
        ccell.winner = player
        next_turn = True

        res = ccell.checkwin(player)
        if res:
            if player == '1':
                p1_score += 1
            else:
                p2_score += 1

            if p1_score or p2_score == 5:
                print(p1_score, p2_score)
                gameover = True

    pygame.display.update()

pygame.quit()