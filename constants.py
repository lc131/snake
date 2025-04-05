"""
Constants used throughout the snake game.
This centralizes all configuration values.
"""

# Window dimensions
WIDTH = 500
HEIGHT = 500

# Grid configuration
GRID_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)

# Game states
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_PAUSE = "pause"
STATE_GAME_OVER = "game_over"

# Game modes
MODE_NORMAL = 0
MODE_FAST = 1
MODE_WALLS = 2

# Speed settings (milliseconds between moves)
SPEED_NORMAL = 100
SPEED_FAST = 50

# Font settings
FONT_LARGE = 60
FONT_MEDIUM = 50
FONT_SMALL = 30
FONT_TINY = 20
FONT_FAMILY = 'comicsans'

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40