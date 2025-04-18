import pygame
import sys
from SnakeGame import game_manager
#from game_manager import GameManager

def main():
    """
    Main entry point for the Snake Game.
    Initializes pygame, creates the game manager, and starts the game loop.
    """
    # Initialize pygame
    pygame.init()
    
    # Create game manager instance that controls the entire game
    manager = game_manager.GameManager()
    manager.game_music.play(-1)
    # Start the main game loop
    manager.run()
    
    # Clean up when the game exits
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()