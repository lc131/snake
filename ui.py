import pygame
from myconstants import (
    WIDTH, HEIGHT, GRID_SIZE, BLACK, WHITE, GRAY, 
    BUTTON_COLOR, BUTTON_HOVER_COLOR, FONT_FAMILY,
    FONT_LARGE, FONT_MEDIUM, FONT_SMALL, FONT_TINY,
    BUTTON_WIDTH, BUTTON_HEIGHT,OFF_SET,DARK_GREEN,BACKGROUND_GREEN1
)

class Button:
    """
    Interactive button for menus.
    Handles rendering, hover effects, and click detection.
    """
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
        """
        Initialize a new button.
        
        Args:
            x (int): X-coordinate of top-left corner
            y (int): Y-coordinate of top-left corner
            width (int): Button width
            height (int): Button height
            text (str): Button label text
            color (tuple): RGB color for normal state
            hover_color (tuple): RGB color for hover state
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        """
        Draw the button on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw button with different color when hovered
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, 0, 10)  # Rounded corners
        
        # Draw button text
        font = pygame.font.SysFont(FONT_FAMILY, FONT_TINY)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        """
        Check if the mouse is hovering over the button.
        
        Args:
            pos (tuple): Current mouse position (x, y)
            
        Returns:
            bool: True if hovered, False otherwise
        """
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, click):
        """
        Check if the button was clicked.
        
        Args:
            pos (tuple): Current mouse position (x, y)
            click (bool): Whether a mouse click occurred
            
        Returns:
            bool: True if clicked, False otherwise
        """
        return self.rect.collidepoint(pos) and click


class UIManager:
    """
    Manages all UI elements and rendering operations.
    """
    def __init__(self):
        """
        Initialize the UI manager and create UI elements.
        """
        # Create menu buttons
        self.menu_buttons = [
            Button(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT, "Normal Mode"),
            Button(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 60, BUTTON_WIDTH, BUTTON_HEIGHT, "Fast Mode"),
            Button(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 120, BUTTON_WIDTH, BUTTON_HEIGHT, "Wall Mode"),
            Button(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 180, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")
        ]
        
        # Create pause menu buttons
        self.pause_buttons = [
            Button(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT, "Resume"),
            Button(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 60, BUTTON_WIDTH, BUTTON_HEIGHT, "Main Menu"),
            Button(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 120, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")
        ]
        
        # Create game over buttons
        self.game_over_buttons = [
            Button(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT, "Play Again"),
            Button(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 60, BUTTON_WIDTH, BUTTON_HEIGHT, "Main Menu"),
            Button(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 120, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")
        ]
    
    def draw_grid(self, surface):
        """
        Draw the game grid on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        cell_size = WIDTH // GRID_SIZE
        
        # Draw vertical and horizontal grid lines
        for i in range(GRID_SIZE):
            # x = (i + 1) * cell_size
            # y = (i + 1) * cell_size
            
            # # Draw light grid lines
            # pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
            # pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))
            if i % 2 == 0: 
                for col in range(cell_size):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * GRID_SIZE,i * GRID_SIZE,GRID_SIZE,GRID_SIZE)
                        pygame.draw.rect(surface,BACKGROUND_GREEN1,grass_rect)
            else:
                for col in range(cell_size):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * GRID_SIZE,i * GRID_SIZE,GRID_SIZE,GRID_SIZE)
                        pygame.draw.rect(surface,BACKGROUND_GREEN1,grass_rect)
            
    def draw_menu(self, surface):
        """
        Draw the main menu screen.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Fill background
        surface.fill(DARK_GREEN)
        
        # Draw title
        font = pygame.font.SysFont('comicsansms', FONT_LARGE)
        title = font.render("SNAKE GAME", True, (0, 255, 0))
        title_width = title.get_width()
        surface.blit(title, (WIDTH//2 - title_width//2, HEIGHT//4))
        
        # Draw instructions
        font = pygame.font.SysFont(FONT_FAMILY, FONT_TINY)
        instr = font.render("Select Game Mode:", True, WHITE)
        instr_width = instr.get_width()
        surface.blit(instr, (WIDTH//2 - instr_width//2, HEIGHT//2 - 50))

        # Draw pause instruction
        #pause_text = font.render("Press SPACE to pause", True, WHITE)
        #pause_width = pause_text.get_width()
        #surface.blit(pause_text, (WIDTH//2 - pause_width//2, 10))
        
        # Draw buttons
        for button in self.menu_buttons:
            button.draw(surface)
    
    def draw_game(self, surface, snake, snack, score, high_score, game_mode):
        """
        Draw the main game screen.
        
        Args:
            surface: Pygame surface to draw on
            snake: Snake object
            snack: Cube object (food)
            score (int): Current score
            high_score (int): Highest score
            game_mode (int): Current game mode
        """
        # Fill background
        surface.fill(DARK_GREEN)
        
        
        # Draw game elements
        self.draw_grid(surface)
        snake.draw(surface)
        snack.draw(surface)
        
        
        # Draw score at the top
        font = pygame.font.SysFont(FONT_FAMILY, FONT_TINY)
        score_text = font.render(f'Score: {score}  High Score: {high_score}', True, WHITE)
        surface.blit(score_text, (10, 10))
        
        # Draw game mode indicator
        mode_names = ["Normal Mode", "Fast Mode", "Wall Mode"]
        mode_text = font.render(mode_names[game_mode], True, WHITE)
        text_width = mode_text.get_width()
        surface.blit(mode_text, (WIDTH - text_width - 10, 10))
        
    
    def draw_pause(self, surface, snake, snack):
        """
        Draw the pause screen.
        
        Args:
            surface: Pygame surface to draw on
            snake: Snake object
            snack: Cube object (food)
        """
        # Draw the game in the background (dimmed)
        self.draw_grid(surface)
        snake.draw(surface)
        snack.draw(surface)
        
        
        # Add semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5,71,42,128))  # Background with 50% transparency
        surface.blit(overlay, (0, 0))
        
        # Draw pause title
        font = pygame.font.SysFont(FONT_FAMILY, FONT_MEDIUM)
        pause_title = font.render("PAUSED", True, WHITE)
        title_width = pause_title.get_width()
        surface.blit(pause_title, (WIDTH//2 - title_width//2, HEIGHT//4))
        
        # Draw pause menu buttons
        for button in self.pause_buttons:
            button.draw(surface)
    
    def draw_game_over(self, surface, score):
        """
        Draw the game over screen.
        
        Args:
            surface: Pygame surface to draw on
            score (int): Final score
        """
        # Fill background
        surface.fill(BLACK)
        
        # Draw game over text
        font = pygame.font.SysFont(FONT_FAMILY, FONT_MEDIUM)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        text_width = game_over_text.get_width()
        surface.blit(game_over_text, (WIDTH//2 - text_width//2, HEIGHT//4))
        
        # Draw score
        font = pygame.font.SysFont(FONT_FAMILY, FONT_SMALL)
        score_text = font.render(f'Score: {score}', True, WHITE)
        score_width = score_text.get_width()
        surface.blit(score_text, (WIDTH//2 - score_width//2, HEIGHT//2 - 50))
        
        # Draw game over buttons
        for button in self.game_over_buttons:
            button.draw(surface)
    
    def draw(self, surface, game_state, snake=None, snack=None, score=0, high_score=0, game_mode=0):
        """
        Main drawing method that dispatches to appropriate drawing method based on game state.
        
        Args:
            surface: Pygame surface to draw on
            game_state (str): Current game state
            snake: Snake object
            snack: Cube object (food)
            score (int): Current score
            high_score (int): Highest score
            game_mode (int): Current game mode
        """
        if game_state == "menu":
            self.draw_menu(surface)
        elif game_state == "game":
            self.draw_game(surface, snake, snack, score, high_score, game_mode)
        elif game_state == "pause":
            self.draw_pause(surface, snake, snack)
        elif game_state == "game_over":
            self.draw_game_over(surface, score)
        
        # Update the display
        pygame.display.update()