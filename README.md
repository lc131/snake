![image](https://github.com/user-attachments/assets/b03b08f7-2b12-4c59-b0d9-46d1de920eb7)

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
Spacebar to pause and esc to get menu

Simple UI and Scoring:
Basic score tracking by counting the snake's length and a message box popup when the snake collides with itself.

How to Play
Controls:
Use the arrow keys (Up, Down, Left, Right) to control the snake’s movement.

Objective:
Collect the green snacks that appear on the grid. Each time you collect a snack, the snake grows longer. Avoid colliding with your own body.

Game Over:
If the snake collides with itself, a message box will appear showing your score, and the game will reset.

Personal Notes
This project was created as a personal learning exercise to improve my Python and Pygame skills. It helped me understand key game development concepts such as frame-independent movement, interpolation for smoother animations, and handling edge cases with grid-based logic.

License
This project is open-source and available under the MIT License.
