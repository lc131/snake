import pygame
import sys
import tkinter as tk
from tkinter import messagebox
from snake import Snake
from food import create_food
from ui import UIManager
from myconstants import *

class GameManager:
    """
    Central manager class that controls the game flow, state management,
    and coordinates between different components.
    """
    def __init__(self):
        """
        Initialize the game manager.
        """
        # Set up the display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        
        # Initialize game state variables
        self.game_state = STATE_MENU
        self.game_mode = MODE_NORMAL
        self.score = 0
        self.high_score = 0
        self.clock = pygame.time.Clock()
        
        # Initialize game objects
        self.snake = Snake(RED, (10, 10))
        self.food = create_food(self.snake)
        
        # Initialize UI manager
        self.ui_manager = UIManager()

        # Initialize music
        self.game_music = pygame.mixer.Sound("Sounds/game_music.mp3")
    
    def show_message_box(self, title, message):
        """
        Display a message box.
        
        Args:
            title (str): Title of the message box
            message (str): Content of the message box
        """
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(title, message)
        try:
            root.destroy()
        except:
            pass
    
    def handle_menu_input(self):
        """
        Handle input in the menu state.
        
        Returns:
            bool: True if game should continue, False to exit
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        # Check button interactions
        for button in self.ui_manager.menu_buttons:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_clicked):
                if button.text == "Normal Mode":
                    self.game_mode = MODE_NORMAL
                    self.game_state = STATE_GAME
                    self.snake.reset((10, 10))
                    self.score = 0
                elif button.text == "Fast Mode":
                    self.game_mode = MODE_FAST
                    self.game_state = STATE_GAME
                    self.snake.reset((10, 10))
                    self.score = 0
                elif button.text == "Wall Mode":
                    self.game_mode = MODE_WALLS
                    self.game_state = STATE_GAME
                    self.snake.reset((10, 10))
                    self.score = 0
                elif button.text == "Quit":
                    return False
                    
        return True
    
    def handle_game_input(self):
        """
        Handle input in the game state.
        
        Returns:
            bool: True if game should continue, False to exit
        """
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    self.game_state = STATE_PAUSE
                    pygame.time.delay(200)  # Delay to prevent multiple toggles
        
        # Handle snake movement input (returns keyboard state)
        self.snake.handle_keys()
        
        return True
    
    def handle_pause_input(self):
        """
        Handle input in the pause state.
        
        Returns:
            bool: True if game should continue, False to exit
        """
        # Handle mouse position for button hover effects
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.snake.last_move_time = pygame.time.get_ticks()
                self.game_state = STATE_GAME
                pygame.time.delay(200)  # Delay to prevent multiple toggles
        
        # Check button interactions
        for button in self.ui_manager.pause_buttons:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_clicked):
                if button.text == "Resume":
                    self.snake.last_move_time = pygame.time.get_ticks()
                    self.game_state = STATE_GAME
                elif button.text == "Main Menu":
                    self.game_state = STATE_MENU
                elif button.text == "Quit":
                    return False
        
        return True
    
    def handle_game_over_input(self):
        """
        Handle input in the game over state.
        
        Returns:
            bool: True if game should continue, False to exit
        """
        # Handle mouse position for button hover effects
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        # Check button interactions
        for button in self.ui_manager.game_over_buttons:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_clicked):
                if button.text == "Play Again":
                    self.snake.reset((10, 10))
                    self.food = create_food(self.snake)
                    self.score = 0
                    self.game_state = STATE_GAME
                elif button.text == "Main Menu":
                    self.game_state = STATE_MENU
                elif button.text == "Quit":
                    return False
        
        return True
    
    def update_game(self):
        """
        Update the game state, handling movement, collisions, and score.
        """
        # Target high frame rate for smooth rendering
        dt = self.clock.tick(60) / 1000  # Delta time in seconds
        interpolation = min(1.0, dt * 10)  # Adjust for smoother/faster movement
        
        # Only apply movement and collision detection if not paused
        if self.game_state == STATE_GAME:
            interpolation = min(1.0, dt * 10)  # Adjust for smoother/faster movement
            
            # Move the snake and check for wall collision in wall mode
            wall_collision = self.snake.move(self.game_mode)
            if wall_collision:
                # Game over if we hit a wall in WALLS mode
                self.snake.wall_hit_sound.play()
                if self.score > self.high_score:
                    self.high_score = self.score
                self.game_state = STATE_GAME_OVER
                return
            
            # Update visual positions with interpolation
            self.snake.update_visual_positions(interpolation)
            
            # Check for food collision
            if self.snake.body[0].pos == self.food.pos:
                self.snake.add_cube()
                self.food = create_food(self.snake)
                self.score += 1
                self.snake.eat_sound.play()
            
            # Check for self-collision
            if self.snake.check_collision():
                self.snake.wall_hit_sound.play()
                if self.score > self.high_score:
                    self.high_score = self.score
                self.game_state = STATE_GAME_OVER
    
    def run(self):
        """
        Main game loop that handles state transitions and rendering.
        """
        running = True
        while running:
            # Handle input based on current game state
            if self.game_state == STATE_MENU:
                running = self.handle_menu_input()
            elif self.game_state == STATE_GAME:
                running = self.handle_game_input()
                self.update_game()
            elif self.game_state == STATE_PAUSE:
                running = self.handle_pause_input()
            elif self.game_state == STATE_GAME_OVER:
                running = self.handle_game_over_input()
            
            # Render the game based on current state
            self.ui_manager.draw(
                self.screen, 
                self.game_state, 
                self.snake, 
                self.food, 
                self.score, 
                self.high_score, 
                self.game_mode
            )
            
            # Control frame rate (different for menu/game states)
            if self.game_state in [STATE_MENU, STATE_PAUSE, STATE_GAME_OVER]:
                self.clock.tick(10)  # Lower frame rate for menus