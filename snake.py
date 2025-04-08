import pygame
import sys
from SnakeGame import myconstants
# from myconstants import *
from cube import Cube

class Snake:
    """
    Represents the snake in the game.
    Manages the snake's body segments, movement, and interactions.
    """
    def __init__(self, color, pos):
        """
        Initialize a new snake.
        
        Args:
            color (tuple): RGB color of the snake
            pos (tuple): Starting position (x, y) on the grid
        """
        self.color = color
        self.body = []
        self.turns = {}  # Dictionary to track turning points
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.last_move_time = 0
        self.move_delay = myconstants.SPEED_NORMAL
        self.queued_direction = None
    
    def handle_keys(self):
        """
        Process keyboard input for snake control.
        Returns the current key state for use in the main game loop.
        
        Returns:
            dict: Current state of keyboard keys
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        
        # Queue direction changes based on key presses
        # Snake can't reverse direction directly
        if keys[pygame.K_LEFT] and self.dirnx != 1:
            self.queued_direction = (-1, 0)
        elif keys[pygame.K_RIGHT] and self.dirnx != -1:
            self.queued_direction = (1, 0)
        elif keys[pygame.K_UP] and self.dirny != 1:
            self.queued_direction = (0, -1)
        elif keys[pygame.K_DOWN] and self.dirny != -1:
            self.queued_direction = (0, 1)
        
        return keys
    
    def move(self, game_mode):
        """
        Move the snake according to its current direction and game mode.
        
        Args:
            game_mode (int): Current game mode (affects speed and collision behavior)
        
        Returns:
            bool: True if the snake hit a wall in wall mode, False otherwise
        """
        # Get current time for time-based movement
        current_time = pygame.time.get_ticks()
        
        # Adjust move delay based on game mode
        # Adjust move delay based on game mode
        if game_mode == myconstants.MODE_FAST:
            self.move_delay = myconstants.SPEED_FAST
        else:
            self.move_delay = myconstants.SPEED_NORMAL
            
        # Only move at specific time intervals
        if current_time - self.last_move_time > self.move_delay:
            # Apply queued direction change if there is one
            if self.queued_direction:
                self.dirnx, self.dirny = self.queued_direction
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.queued_direction = None
                
            # Move each segment of the snake
            for i, segment in enumerate(self.body):
                p = segment.pos[:]  # Copy of current position
                
                # Handle turning points
                if p in self.turns:
                    turn = self.turns[p]
                    segment.move(turn[0], turn[1])
                    # Remove turn point after the last segment passes
                    if i == len(self.body) - 1:
                        self.turns.pop(p)
                else:
                    # Handle edge collisions based on game mode
                    if game_mode == myconstants.MODE_WALLS:
                        # In wall mode, hitting edge means game over
                        if (segment.dirnx == -1 and segment.pos[0] <= 0 or 
                            segment.dirnx == 1 and segment.pos[0] >= myconstants.GRID_SIZE - 1 or
                            segment.dirny == 1 and segment.pos[1] >= myconstants.GRID_SIZE - 1 or
                            segment.dirny == -1 and segment.pos[1] <= 0):
                            return True  # Signal collision with wall
                        else: 
                            segment.move(segment.dirnx, segment.dirny)
                    else:
                        # Normal wraparound behavior
                        # if segment.dirnx == -1 and segment.pos[0] <= 0: 
                        #     segment.pos = (myconstants.GRID_SIZE - 1, segment.pos[1])       
                        # elif segment.dirnx == 1 and segment.pos[0] >= myconstants.GRID_SIZE - 1:
                        #     segment.pos = (0, segment.pos[1])       
                        # elif segment.dirny == 1 and segment.pos[1] >= myconstants.GRID_SIZE - 1:
                        #     segment.pos = (segment.pos[0], 0)       
                        # elif segment.dirny == -1 and segment.pos[1] <= 0: 
                        #     segment.pos = (segment.pos[0], myconstants.GRID_SIZE - 1)       
                        # else: 
                        #     segment.move(segment.dirnx, segment.dirny)
                        next_pos_x = segment.pos[0] + segment.dirnx
                        next_pos_y = segment.pos[1] + segment.dirny
                        
                        # Wrap around if necessary
                        if next_pos_x < 0:
                            next_pos_x = myconstants.GRID_SIZE - 1
                        elif next_pos_x >= myconstants.GRID_SIZE:
                            next_pos_x = 0
                            
                        if next_pos_y < 0:
                            next_pos_y = myconstants.GRID_SIZE - 1
                        elif next_pos_y >= myconstants.GRID_SIZE:
                            next_pos_y = 0
                        
                        # Set the new position directly
                        segment.pos = (next_pos_x, next_pos_y)
                        
                        # Keep track of the direction (needed for visual interpolation)
                        segment.dirnx = segment.dirnx
                        segment.dirny = segment.dirny
        
            self.last_move_time = current_time
        return False  # No collision with wall
    
    def update_visual_positions(self, interpolation):
        """
        Update the visual positions of all body segments.
        
        Args:
            interpolation (float): Interpolation factor (0.0 to 1.0)
        """
        for segment in self.body:
            segment.update_visual_position(interpolation)
    
    def reset(self, pos):
        """
        Reset the snake to its initial state.
        
        Args:
            pos (tuple): Starting position (x, y)
        """
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.queued_direction = None
    
    def add_cube(self):
        """
        Add a new segment to the snake when it eats food.
        """
        # Get tail segment (last segment of the snake)
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        # Determine new segment position based on tail direction
        # (Place it behind the tail)
        # Calculate the position opposite to the tail's current direction
        # This places the new segment directly behind the tail, as if the
        # tail was there one step ago
        new_pos = (
            (tail.pos[0] - dx) % myconstants.GRID_SIZE,
            (tail.pos[1] - dy) % myconstants.GRID_SIZE
        )
        
        # Create the new segment
        new_cube = Cube(new_pos)
        
        # Set direction to match tail direction
        new_cube.dirnx = dx
        new_cube.dirny = dy
        
        # Set visual position to match logical position
        new_cube.visual_x = float(new_pos[0])
        new_cube.visual_y = float(new_pos[1])
        
        # Add the new segment to the snake
        self.body.append(new_cube)
    
    def draw(self, surface):
        """
        Draw the complete snake on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        for i, segment in enumerate(self.body):
            # Draw head with eyes, body segments without
            segment.draw(surface, i == 0)
    
    def check_collision(self):
        """
        Check if the snake's head collides with its body.
        
        Returns:
            bool: True if collision detected, False otherwise
        """
        head_pos = self.body[0].pos
        # Check all segments except head
        for segment in self.body[1:]:
            if segment.pos == head_pos:
                return True
        return False