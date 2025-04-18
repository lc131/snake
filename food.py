import random
from cube import Cube
from myconstants import GRID_SIZE, GREEN

def create_food(snake):
    """
    Create a new food cube at a random position that doesn't overlap with the snake.
    
    Args:
        snake: Snake object
    
    Returns:
        Cube: A new food cube
    """
    position = snake.body
    
    # Keep generating positions until we find one that's not on the snake
    while True:
        x = random.randrange(GRID_SIZE)
        y = random.randrange(GRID_SIZE)
        
        # Check if the position overlaps with any snake segment
        if len(list(filter(lambda z: z.pos == (x, y), position))) > 0:
            continue
        else:
            break
    
    # Create and return a food cube at the valid position
    return Cube((x, y), color=GREEN)