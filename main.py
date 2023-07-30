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

smallfont = pygame.font.SysFont('cursive', 16)
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
            for c in range(COLS-4):
                current_player = cells[r * ROWS + c].winner
                if current_player:
                    if all(cells[r * ROWS + c + i].winner == current_player for i in range(5)):
                        return True, current_player
        #Check vertically
        for r in range(ROWS-4):
            for c in range(COLS):
                current_player = cells[r * ROWS + c].winner
                if current_player:
                    if all(cells[(r + i) * ROWS + c].winner == current_player for i in range(5)):
                        return True, current_player
        #Check diagonally
        for r in range(ROWS-4):
            for c in range(COLS-4):
                current_player = cells[r * ROWS + c].winner
                if current_player:
                    if all(cells[(r + i) * ROWS + c + i].winner == current_player for i in range(5)):
                        return True, current_player
        # Check diagonally (top-right to bottom-left)
        for r in range(ROWS-4):
            for c in range(4, COLS):
                current_player = cells[r * ROWS + c].winner
                if current_player:
                    if all(cells[(r + i) * ROWS + c - i].winner == current_player for i in range(5)):
                        return True, current_player

def heuristic(cells):
    # Check horizontally
    score = 0
    for r in range(ROWS):
        for c in range(COLS-4):
            count_player1 = cells[r * ROWS + c].count_connected_cells(0, 1, '1', cells)
            count_player2 = cells[r * ROWS + c].count_connected_cells(0, 1, '2', cells)
            score += (count_player2 - count_player1)

    # Check vertically
    for r in range(ROWS-4):
        for c in range(COLS):
            count_player1 = cells[r * ROWS + c].count_connected_cells(1, 0, '1', cells)
            count_player2 = cells[r * ROWS + c].count_connected_cells(1, 0, '2', cells)
            score += (count_player2 - count_player1)

    # Check diagonally (top-left to bottom-right)
    for r in range(ROWS-4):
        for c in range(COLS-4):
            count_player1 = cells[r * ROWS + c].count_connected_cells(1, 1, '1', cells)
            count_player2 = cells[r * ROWS + c].count_connected_cells(1, 1, '2', cells)
            score += (count_player2 - count_player1)

    # Check diagonally (top-right to bottom-left)
    for r in range(ROWS-4):
        for c in range(4, COLS):
            count_player1 = cells[r * ROWS + c].count_connected_cells(1, -1, '1', cells)
            count_player2 = cells[r * ROWS + c].count_connected_cells(1, -1, '2', cells)
            score += (count_player2 - count_player1)

    return score

def minimax_alpha_beta(cells, depth, alpha, beta, is_maximizing, max_depth):
    if wincondition(cells):
        if wincondition(cells)[1] == '2':  # If the computer wins
            return 1
        elif wincondition(cells)[1] == '1':  # If the human wins
            return -1
    elif not any(cell.winner is None for cell in cells):  # If the board is full
        return 0
    elif depth == max_depth:  # If the depth limit has been reached
        return heuristic(cells)  # Estimate the score of the game state

    if is_maximizing:
        best_score = -float('inf')
        for cell in cells:
            if cell.winner is None:
                cell.winner = '2'
                score = minimax_alpha_beta(cells, depth + 1, alpha, beta, False, max_depth)
                cell.winner = None
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float('inf')
        for cell in cells:
            if cell.winner is None:
                cell.winner = '1'
                score = minimax_alpha_beta(cells, depth + 1, alpha, beta, True, max_depth)
                cell.winner = None
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score

def computer_move():
    global ccell, next_turn, turn, player, gameover

    if gameover:  # Check if the game is already over
        return

    best_score = -float('inf')
    best_move = None

    for cell in cells:
        if cell.winner is None:
            cell.winner = player
            if wincondition(cells):  # Check if the human's move resulted in a win
                gameover = wincondition(cells)
                return
            score = minimax_alpha_beta(cells, 0, -float('inf'), float('inf'), False, max_depth)  # Variable depth depending on user input
            cell.winner = None
            if score > best_score:
                best_score = score
                best_move = cell

    if best_move:
        if best_move.checkwin(player):
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
    difficulty = 'Easy'
    max_depth = 0
    return turn, players, player, next_turn, is_human, difficulty, max_depth


start = False
gameover = False
vs_computer = True
cells = create_cells()
pos, ccell = reset_cells()
turn, players, player, next_turn, is_human, difficulty, max_depth = reset_turn()

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
                turn, players, player, next_turn, is_human, difficulty, max_depth = reset_turn()

            if event.key == pygame.K_1:
                max_depth = 0
                difficulty = 'Easy'
                vs_computer = True
            elif event.key == pygame.K_2:
                max_depth = 1
                vs_computer = True
                difficulty = 'Medium'
            elif event.key == pygame.K_3:
                max_depth = 2
                vs_computer = True
                difficulty = 'Hard'
            elif event.key == pygame.K_4:
                max_depth = 0
                vs_computer = False
                difficulty = '2 Player'
    
    # Start screen
    if not start and not gameover:
        rect = pygame.Rect((0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(win, BLACK, rect)

        begin = font.render('Instructions', True, GREEN)
        win.blit(begin, (rect.centerx-begin.get_width()//2, rect.y+10))

        step1 = '1. Click on a box to fill it with your color'
        step1img = smallfont.render(step1, True, GREEN)
        win.blit(step1img, (rect.centerx-step1img.get_width()//2, rect.centery-100))

        step2 = '2. Get four boxes ina row to win'
        step2img = smallfont.render(step2, True, GREEN)
        win.blit(step2img, (rect.centerx-step2img.get_width()//2, rect.centery-50))

        step3 = '3. Press 1 (Easy), 2 (Medium) or 3 (Hard) to set difficulty'
        step3img = smallfont.render(step3, True, GREEN)
        win.blit(step3img, (rect.centerx-step3img.get_width()//2, rect.centery))

        msg1 = 'Press s:start, press 4 to play against a friend'
        msg1img = smallfont.render(msg1, True, GREEN)
        win.blit(msg1img, (rect.centerx-msg1img.get_width()//2, rect.centery+100))

    for r in range(ROWS+1):
        for c in range(COLS+1):
            pygame.draw.circle(win, BLACK, (c*CELLSIZE + 2*PADDING, r*CELLSIZE + 3*PADDING), 2)
    
    for cell in cells:
        if not gameover:
            cell.update(win)
            if pos and cell.rect.collidepoint(pos):
                ccell = cell

    if vs_computer:

        if ccell and start and not gameover:
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

    else:
        if ccell and start and not gameover:
            if ccell.checkwin(player):
                next_turn = True

            if next_turn:
                turn = (turn + 1) % 2
                player = players[turn]
                next_turn = False
        
    p1img = font.render('Player 1', True, BLUE)
    p1rect = p1img.get_rect()
    p1rect.x, p1rect.y = PADDING, 15

    p2img = font.render('Player 2', True, BLUE)
    p2rect = p2img.get_rect()
    p2rect.right, p2rect.y = WIDTH-PADDING, 15
    
    diffimg = smallfont.render(f'Difficulty: {difficulty}', True, BLUE)
    diffrect = diffimg.get_rect()
    diffrect.centerx, diffrect.y = WIDTH//2, 15

    if start:
        win.blit(p1img, p1rect)
        win.blit(p2img, p2rect)
        win.blit(diffimg, diffrect)
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