import random
# Example file showing a basic pygame "game loop"
import pygame
import math
from tkinter import messagebox
import tkinter as tk

WIDTH = 500
HEIGHT = 500
row = 20

class Cube(object):
    w = 500
    row = 20
    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False):
        dis = self.w // self.row
        i = self.pos[0]
        j = self.pos[1]
        
        #Create rectangle for segment
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis - 2, dis - 2), 0, 7) 
        # rect (surface, color, rect, width, border radius) 
        # 0 for filling color in rectangle, 7 represent border radius of rectangle
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i*dis + centre - radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)            
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class Snake(object):
    body = []
    turns = {} #dictionary to later add key value to it
    
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos) #give pos head at pos position as we pass
        self.body.append(self.head) #append the body which is list type to the head pos 
        self.dirnx = 0 # Set y or x to (x,y) then switch the other to -1 cause snake can only move 1 direction
        self.dirny = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed() # Passing dictionary of key provided by pygame
            
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1 #Moving to left according to (x,y)
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # Set pos head according to (x,y) coordinate with dict syntax
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1 #Moving to left according to (x,y)
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # Set pos head according to (x,y) coordinate with dict syntax
                elif keys[pygame.K_UP]:
                    self.dirnx = 0 #Moving to left according to (x,y)
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # Set pos head according to (x,y) coordinate with dict syntax
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0 #Moving to left according to (x,y)
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # Set pos head according to (x,y) coordinate with dict syntax

        for i, c in enumerate(self.body): # index and cube in object body
            p = c.pos[:]  # : stand for copy since pos snake not change when we move   
            if p in self.turns:
                turn = self.turns[p] # We can find index of it and find direction so we can move
                c.move(turn[0],turn[1])
                if i == len(self.body) - 1: #So the body turn coordinate according to head and recursive until the end of body
                    self.turns.pop(p) # Whenever we hit last turn, this remove the turn after turned
            else:
                #CHECKING POS TO KNOW IF IT GO TO THE EDGE OF THE SCREEN
                if c.dirnx == -1 and c.pos[0] <= 0: 
                    c.pos = (c.row - 1, c.pos[1])       
                elif c.dirnx == 1 and c.pos[0] >= c.row - 1:
                    c.pos = (0, c.pos[1])       
                elif c.dirny == 1 and c.pos[1] >= c.row - 1:
                    c.pos = (c.pos[0], 0)       
                elif c.dirny == -1 and c.pos[1] <= 0: 
                    c.pos = (c.pos[0], c.row - 1)       
                else: c.move(c.dirnx, c.dirny) # if not to the edge, just keep moving

    def reset(self,pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 0

    def addCube(self):
        tail = self.body[-1]
        dx,dy = tail.dirnx, tail.dirny
        #Append new cube to body
        if dx == 1 and dy == 0: 
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))       
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))       
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1))) 
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy 

    def draw (self, surface):
        for i, c in enumerate(self.body): # index and cube in object body
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
    
def redrawWindow(surface):
    global WIDTH, HEIGHT, row, s, snack
    # fill the screen with a color to wipe away anything from last frame
    surface.fill("black")
    s.draw(surface)
    snack.draw(surface)
    drawGrid(WIDTH, row, surface)
    pygame.display.update()

def drawGrid(w, row, surface):
    sizeBtwn = w // row

    x = 0
    y = 0
    for l in range(row):
        x = x + sizeBtwn
        y = y + sizeBtwn

        #pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
        
        #pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

def randomSnack(row, item):
    position = item.body
    while True:
        x = random.randrange(row)    
        y = random.randrange(row)
        if(len(list(filter(lambda z: z.pos == (x,y), position))) > 0): # Make sure snack not appear on the snake
            continue
        else:
            break
    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
def main():
    global WIDTH, HEIGHT, s, snack
    
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    s = Snake((255,0,0), (10, 10)) #Color, Position for snake to start 
    snack = Cube(randomSnack(row, s), color = (0,255,0))
    clock = pygame.time.Clock()
    running = True

    while running:
        # poll for events
        pygame.time.delay(70)
        clock.tick(20)  # limits FPS to 60
        # pygame.QUIT event means the user clicked X to close your window
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(row, s), color = (0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print("Score: ", len(s.body))
                message_box("You lost", "Play again!")
                s.reset((10,10))
                break

        redrawWindow(screen)
        
        # RENDER YOUR GAME HERE
            
        # flip() the display to put your work on screen
        # pygame.display.flip()

if __name__ == "__main__":
    main()