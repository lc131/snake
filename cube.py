import pygame
from SnakeGame import myconstants
#from myconstants import WIDTH, GRID_SIZE, BLACK

class Cube:
    """
    Represents a single segment of the snake or the food.
    Handles its own movement, visual positioning, and rendering.
    """
    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        """
        Initialize a new cube segment.
        
        Args:
            start (tuple): Starting position (x, y) on the grid
            dirnx (int): Initial x direction (-1, 0, 1)
            dirny (int): Initial y direction (-1, 0, 1)
            color (tuple): RGB color for the cube
        """
        self.pos = start  # Logical position (grid coordinates)
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
        
        # Visual position (for smooth rendering)
        self.visual_x = start[0]
        self.visual_y = start[1]
    
    def move(self, dirnx, dirny):
        """
        Move the cube in the specified direction.
        
        Args:
            dirnx (int): New x direction
            dirny (int): New y direction
        """
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def update_visual_position(self, interpolation):
        """
        Update the visual position to smoothly transition to the logical position.
        
        Args:
            interpolation (float): Interpolation factor (0.0 to 1.0)
        """
        # Logical position (target)
        target_x = self.pos[0]
        target_y = self.pos[1]
        
        # Calculate the differences
        dx = target_x - self.visual_x
        dy = target_y - self.visual_y
        
        # Adjust for wrap-around (prevents teleporting when hitting edges)
        if dx > myconstants.GRID_SIZE / 2:
            dx -= myconstants.GRID_SIZE
        elif dx < -myconstants.GRID_SIZE / 2:
            dx += myconstants.GRID_SIZE
            
        if dy > myconstants.GRID_SIZE / 2:
            dy -= myconstants.GRID_SIZE
        elif dy < -myconstants.GRID_SIZE / 2:
            dy += myconstants.GRID_SIZE

        # Apply interpolation for smooth movement
        self.visual_x += dx * interpolation
        self.visual_y += dy * interpolation
        
        # Keep visual position within grid bounds
        self.visual_x %= myconstants.GRID_SIZE
        self.visual_y %= myconstants.GRID_SIZE

    def draw(self, surface, eyes=False):
        """
        Draw the cube on the given surface.
        
        Args:
            surface: Pygame surface to draw on
            eyes (bool): Whether to draw eyes (for the snake's head)
        """
        # Calculate the size of each grid cell
        dis = myconstants.WIDTH // myconstants.GRID_SIZE
        
        # Use visual position for drawing
        i = self.visual_x
        j = self.visual_y
        
        # Draw the cube with rounded corners
        pygame.draw.rect(
            surface, 
            self.color, 
            (i*dis+1, j*dis+1, dis-2, dis-2), 
            0,  # Fill the rectangle
            7   # Border radius
        )
        
        # Draw eyes if this is the head
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i*dis + centre - radius, j*dis + 8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis + 8)
            pygame.draw.circle(surface, myconstants.BLACK, circleMiddle, radius)            
            pygame.draw.circle(surface, myconstants.BLACK, circleMiddle2, radius)