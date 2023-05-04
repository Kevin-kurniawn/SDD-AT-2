# Documentation of Every Lesson

## 4/5/23

Created code to make a 'quit' button, which closes the window when clicked on and changes colours when mouse hovers over it.
``` import pygame
import sys
import turtle
pygame.init()

#Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
light_shade = (170,170,170) #For button
dark_shade = (100,100,100)

#Window
size = (800,800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tic Tac Toe')
width = screen.get_width()
height = screen.get_height()

#Text
smallfont = pygame.font.SysFont('Corbel',35)

text = smallfont.render('quit' , True , WHITE)

#Main program

#Loop until done
done = False

#Clock
clock = pygame.time.Clock()

#Functions



#Main loop
while not done:
    #closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if width/2-70 <= mouse[0] <= width/2+70 and height-300 <= mouse[1] <= height-260:
                done = True
    
    #filling the screen
    screen.fill(BLACK)

    #mouse coordinates
    mouse = pygame.mouse.get_pos()

    #changing button colour whenever mouse hovers over it
    if width/2-70 <= mouse[0] <= width/2+70 and height-300 <= mouse[1] <= height-260:
        pygame.draw.rect(screen,light_shade,[width/2-70,height-300,140,40])
    else:
        pygame.draw.rect(screen,dark_shade,[width/2-70,height-300,140,40])

    #putting text on button
    screen.blit(text , (width/2-25,height-300))

    #update frames of game
    pygame.display.update()

    #Page refresh
    clock.tick(60)
    
```
    
    
