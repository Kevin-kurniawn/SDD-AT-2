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
                fillcount, p1_score, p2_score = reset_score()
                turn, players, player, next_turn = reset_player()
            
    # Creating grid
    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            pygame.draw.circle(win, BLACK, (c*CELLSIZE + 2*PADDING, r*CELLSIZE + 3*PADDING), 2)
    
    #Start screen
    if not start and not gameover:
        rect = pygame.Rect((0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(win, BLACK, rect)

        begin = font.render('Instructions', True, GREEN)
        win.blit(begin, (rect.centerx-begin.get_width()//2, rect.y+10))

        step1 = '1. Click on a box to make it yours'
        step1img = smallfont.render(step1, True, GREEN)
        win.blit(step1img, (rect.centerx-step1img.get_width()//2, rect.centery-100))

        step2 = '2. Try to connect the boxes of your colour'
        step2img = smallfont.render(step2, True, GREEN)
        win.blit(step2img, (rect.centerx-step2img.get_width()//2, rect.centery-50))

        step3 = '3. Whoever creates the longest line wins!'
        step3img = smallfont.render(step3, True, GREEN)
        win.blit(step3img, (rect.centerx-step3img.get_width()//2, rect.centery))

        msg1 = 'Press s:start'
        msg1img = font.render(msg1, True, GREEN)
        win.blit(msg1img, (rect.centerx-msg1img.get_width()//2, rect.centery+100))
    
    for cell in cells:
        pygame.draw.rect(win, GREY, cell.rect)
        if pos and cell.rect.collidepoint(pos):
            ccell = cell
    
    