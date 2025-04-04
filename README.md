Snake Game
A simple Snake game implemented in Python using Pygame. This project demonstrates smooth movement, grid-based logic with wrap-around mechanics, and basic game loop handling. The snake smoothly interpolates between grid positions and wraps around the screen edges, providing a more visually appealing experience.

Features
Smooth Movement:
Uses interpolation for smooth visual movement between grid cells.

Grid-Based Gameplay:
The snake moves on a fixed grid with wrap-around behavior—when the snake reaches one edge, it reappears on the opposite side.

Wrap-Around Logic:
Implements modular arithmetic to correctly handle edge cases, ensuring that the snake’s head and body segments follow seamlessly when wrapping around the screen.

User Input:
Arrow key controls allow for responsive direction changes without allowing direct reversal.

Simple UI and Scoring:
Basic score tracking by counting the snake's length and a message box popup when the snake collides with itself.

Requirements
Python 3.x

Pygame: Used for rendering, game loop, and handling user input.

Tkinter: Used to display message boxes.

You can install Pygame using pip:
pip install pygame
Tkinter is usually included with Python on most platforms. If it isn’t available, refer to your system’s documentation for installation instructions.

Installation
Clone the Repository:
git clone https://github.com/yourusername/snake.git
cd snake
Install Dependencies:

Make sure you have Python installed. Then, install the required packages (if not already installed):

pip install pygame
Run the Game:

Execute the game by running:
python main.py

How to Play
Controls:
Use the arrow keys (Up, Down, Left, Right) to control the snake’s movement.

Objective:
Collect the green snacks that appear on the grid. Each time you collect a snack, the snake grows longer. Avoid colliding with your own body.

Game Over:
If the snake collides with itself, a message box will appear showing your score, and the game will reset.

Code Structure
main.py:
Contains the main game loop, initializes the game, handles user input, updates game state, and renders the snake and grid.

Cube Class:
Represents a segment of the snake (and the snack) with logic for smooth movement and visual interpolation.

Snake Class:
Manages the snake’s body, direction, and logic for movement, growing, and wrapping around the screen.

Utility Functions:
Helper functions such as redrawWindow, drawGrid, and randomSnack handle rendering and game logic.

Personal Notes
This project was created as a personal learning exercise to improve my Python and Pygame skills. It helped me understand key game development concepts such as frame-independent movement, interpolation for smoother animations, and handling edge cases with grid-based logic.

Future Improvements
Enhanced Graphics:
Improve the visual appearance with additional animations and effects.

Scoring System:
Implement a high-score tracking system and more detailed scoring.

Sound Effects:
Add sound effects for actions like collecting snacks and game over events.

Refactor:
Modularize the code further by separating classes and game logic into multiple files for improved maintainability.

License
This project is open-source and available under the MIT License. See the LICENSE file for details.
