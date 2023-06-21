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

    def checkwin(self, winner, cells):
        if not self.winner:
            self.winner = winner
            if winner == '1':
                self.color = BLUE
            else:
                self.color = RED
            self.text = font.render(self.winner, True, WHITE)
            
            connected_cells = 1
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                connected_cells += self.count_connected_cells(dr, dc, winner, cells)
                
            return connected_cells
        return 0

    def update(self, win):
        if self.winner:
            pygame.draw.rect(win, self.color, self.rect)
            win.blit(self.text, (self.rect.centerx-5, self.rect.centery-7))

cells = []
for r in range(ROWS):
    for c in range (COLS):
        cell = Cell(r, c)
        cells.append(cell)

pos = None
ccell = None


p1_score = 0
p2_score = 0


turn = 0
players = ['1', '2']
player = players[turn]
next_turn = False

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
        
    for r in range(ROWS+1):
        for c in range(COLS+1):
            pygame.draw.circle(win, BLACK, (c*CELLSIZE + 2*PADDING, r*CELLSIZE + 3*PADDING), 2)
    
    for cell in cells:
        cell.update(win)
        if pos and cell.rect.collidepoint(pos):
            ccell = cell

    if ccell:
        index = ccell.index

        connected_cells = ccell.checkwin(player, cells)
        if connected_cells > 0:
            next_turn = True
            if player == '1':
                p1_score = connected_cells
            else:
                p2_score = connected_cells

        if next_turn:
            turn = (turn + 1) % 2
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

    pygame.display.update()

pygame.quit()