import random
# Example file showing a basic pygame "game loop"
import pygame
import math
from tkinter import messagebox
import tkinter as tk
import sys
import time

WIDTH = 500
HEIGHT = 500
row = 20

class Cube(object):
    w = 500
    row = 20
    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)):
        self.pos = start # logical postion -> game logic, snake moves by grid
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        # For smooth movement, add visual position (floating point) separate from logical position (grid-based)
        self.visual_x = start[0]
        self.visual_y = start[1]
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    # At each render frame, the method gradually slides the visual position towards the logical position:
    def update_visual_position(self, interpolation):
        # Update visual position to smoothly move toward logical position
        target_x = self.pos[0]
        target_y = self.pos[1]
        
        # Interpolate between current visual position and target position
        #self.visual_x += (target_x - self.visual_x) * interpolation
        #self.visual_y += (target_y - self.visual_y) * interpolation
        # Calculate the differences normally
        dx = target_x - self.visual_x
        dy = target_y - self.visual_y
        
        # Adjust dx for wrap-around: if the difference is more than half the grid, 
        # it should wrap the other way.
        # This fix the problem of head teleporting when hitting edge
        if dx > self.row / 2:
            dx -= self.row
        elif dx < -self.row / 2:
            dx += self.row
            
        if dy > self.row / 2:
            dy -= self.row
        elif dy < -self.row / 2:
            dy += self.row

        # Update visual position with interpolation
        self.visual_x += dx * interpolation
        self.visual_y += dy * interpolation
        
        # Keep visual position within grid bounds for consistency
        self.visual_x %= self.row
        self.visual_y %= self.row

    def draw(self, surface, eyes = False):
        dis = self.w // self.row
        
        # Use visual position for drawing instead of grid position
        i = self.visual_x
        j = self.visual_y
        
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
        self.last_move_time = 0 # At the start of the game
        # Setting time-based control rather than frame-based control
        self.move_delay = 100  # Milliseconds between moves (adjust for speed)
        self.queued_direction = None  # Store the next direction change
    
    def move(self):
        current_time = pygame.time.get_ticks()
        # Current time in ms

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed() # Passing dictionary of key provided by pygame
            
            # Careful prevent the snake from moving opposite direction of its current movement
            # condition to change dirnx, dirny with checking
            # Snake can not reverse direction directly
            # Queue direction changes based on key presses
            # This allows for more responsive controls
            # When the player presses a key, this variable stores the desired direction as a tuple (dirnx, dirny)(e.g., (1, 0)to go right)
            if keys[pygame.K_LEFT] and self.dirnx != 1:
                self.queued_direction = (-1, 0)
            elif keys[pygame.K_RIGHT] and self.dirnx != -1:
                self.queued_direction = (1, 0)
            elif keys[pygame.K_UP] and self.dirny != 1:
                self.queued_direction = (0, -1)
            elif keys[pygame.K_DOWN] and self.dirny != -1:
                self.queued_direction = (0, 1)
            """ THIS IS LOGIC OF GRID MOVE SNAKE
            for key in keys:
                if keys[pygame.K_LEFT] and self.dirnx != 1: #Make sure it not moving right
                    self.dirnx = -1 #Moving to left according to (x,y)
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # Set pos head according to (x,y) coordinate with dict syntax
                elif keys[pygame.K_RIGHT] and self.dirnx != -1:  # Not moving left
                    self.dirnx = 1 #Moving to left according to (x,y)
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # Set pos head according to (x,y) coordinate with dict syntax
                elif keys[pygame.K_UP] and self.dirny != 1:  # Not moving down
                    self.dirnx = 0 #Moving to left according to (x,y)
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # Set pos head according to (x,y) coordinate with dict syntax
                elif keys[pygame.K_DOWN] and self.dirny != -1:  # Not moving up
                    self.dirnx = 0 #Moving to left according to (x,y)
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # Set pos head according to (x,y) coordinate with dict syntax
                    """
        # Only move the snake at specific time intervals
        if current_time - self.last_move_time > self.move_delay:
            # Apply the queued direction change if there is one
            if self.queued_direction:
                self.dirnx, self.dirny = self.queued_direction
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # Copy of the current position of the snake's head (used as a key in the dictionary)
                # Set new value to the key in dict turn
                self.queued_direction = None
            for i, c in enumerate(self.body): # index and cube in object body
                p = c.pos[:]  # : stand for copy since pos snake not change when we move   
                if p in self.turns:
                    turn = self.turns[p] # We can find index of it and find direction so we can move
                    c.move(turn[0],turn[1])
                    if i == len(self.body) - 1: #So the body turn coordinate according to head and recursive until the end of body
                        self.turns.pop(p) # Whenever we hit last turn, this remove the turn after turned
                else:
                    # Instead of conditionally teleporting when reaching the edge,
                    # update position with modulo arithmetic for wrap-around:
                    #new_x = (c.pos[0] + c.dirnx) % c.row
                    #new_y = (c.pos[1] + c.dirny) % c.row
                    #c.pos = (new_x, new_y)

                    if c.dirnx == -1 and c.pos[0] <= 0: 
                        c.pos = (c.row - 1, c.pos[1])       
                    elif c.dirnx == 1 and c.pos[0] >= c.row - 1:
                        c.pos = (0, c.pos[1])       
                    elif c.dirny == 1 and c.pos[1] >= c.row - 1:
                        c.pos = (c.pos[0], 0)       
                    elif c.dirny == -1 and c.pos[1] <= 0: 
                        c.pos = (c.pos[0], c.row - 1)       
                    else: c.move(c.dirnx, c.dirny) # if not to the edge, just keep moving
        
            self.last_move_time = current_time

    def update_visual_positions(self, interpolation):
        # Update visual positions of all body segments
        for segment in self.body:
            segment.update_visual_position(interpolation)

    def reset(self,pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.queued_direction = None

    def addCube(self):
        tail = self.body[-1]
        dx,dy = tail.dirnx, tail.dirny
        # Append new cube to body
        if dx == 1 and dy == 0: 
            new_cube = Cube((tail.pos[0]-1, tail.pos[1]))      
        elif dx == -1 and dy == 0:
            new_cube = Cube((tail.pos[0]+1, tail.pos[1]))      
        elif dx == 0 and dy == 1:
            new_cube = Cube((tail.pos[0], tail.pos[1]-1))
        elif dx == 0 and dy == -1:
            new_cube = Cube((tail.pos[0], tail.pos[1]+1))

        # self.body[-1].dirnx = dx
        # self.body[-1].dirny = dy 
        # Set the visual position immediately to match the logical position
        new_cube.visual_x = new_cube.pos[0]
        new_cube.visual_y = new_cube.pos[1]
        
        new_cube.dirnx = dx
        new_cube.dirny = dy
        
        self.body.append(new_cube)

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

        # For a cleaner look, you might want light grid lines
        pygame.draw.line(surface, (50, 50, 50), (x, 0), (x, w))
        pygame.draw.line(surface, (50, 50, 50), (0, y), (w, y))

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

def message_box(subject, content): # TK message box overlay
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
    pygame.display.set_caption("Snake Game")
    s = Snake((255,0,0), (10, 10)) #Color, Position for snake to start 
    snack = Cube(randomSnack(row, s), color = (0,255,0))
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Target high frame rate for smooth rendering
        dt = clock.tick(60) / 1000  # Delta time in seconds
        interpolation = min(1.0, dt * 10)  # Adjust the multiplier for smoother/faster movement
        # Handle game logic at a fixed rate
        s.move()  # This now checks time internally
        
        # Update visual positions with interpolation
        s.update_visual_positions(interpolation)
        
        # Check for snack collision
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(row, s), color = (0,255,0))

        # Check for self-collision
        head_pos = s.body[0].pos
        for segment in s.body[1:]:  # Check all segments except the head
            if segment.pos == head_pos:
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