import pygame

SCREEN = WIDTH, HEIGHT = 300, 300
CELLSIZE = 30
PADDING = 30
ROWS = COLS = (WIDTH - 4*PADDING) // CELLSIZE
print(ROWS, COLS)

pygame.init()
win = pygame.display.set_mode(SCREEN)

WHITE = (255,255,255)
RED = (239,48,97)
YELLOW = (252,180,0)
ORANGE = (247,101,59)
BLUE = (255,130,255)
GREY = (171,171,171)
BLACK = (0,0,0)

smallfont = pygame.font.SysFont('cursive', 15)
font = pygame.font.SysFont('cursive', 25)

start = False
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
    
    if not start:
        rect = pygame.Rect((0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(win, BLACK, rect)

        begin = font.render('Instructions', True, WHITE)
        win.blit(begin, (rect.centerx-begin.get_width()//2, rect.y+10))

        step1 = '1. Click on a box'
        step1img = smallfont.render(step1, True, WHITE)
        win.blit(step1img, (rect.centerx-step1img.get_width()//2, rect.centery-100))

        step2 = ['2. Click the arrow key matching the side of the box you select']
        step2img = smallfont.render('2. Click the arrow key matching the side of the box', True, WHITE)
        win.blit(step2img, (rect.centerx-step2img.get_width()//2, rect.centery-50))

        step3 = ['3. Whoever draws the line to create a box gets a']
        step3 = smallfont.render('3. Whoever draws the line to create a box gets a point', True, WHITE)
        win.blit(step3, (rect.centerx-step3.get_width()//2, rect.centery))

        msg1 = 'Press s:start'
        msg1img = font.render(msg1, True, WHITE)
        win.blit(msg1img, (rect.centerx-msg1img.get_width()//2, rect.centery+100))

    pygame.display.update()

pygame.quit()

