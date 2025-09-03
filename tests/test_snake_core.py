from collections import deque
from snakerun import SnakeGame
import os
import pytest
import sys


def set_terminal_small(rows=15, cols=40):
    """
    Resize the terminal window to specified dimensions.

    Args:
        rows (int): Number of rows for the terminal.
        cols (int): Number of columns for the terminal.
    """
    if sys.platform.startswith("win"):
        # Windows: use 'mode' command
        os.system(f"mode con: cols={cols} lines={rows}")
    else:
        # Linux/macOS: ANSI escape sequence
        os.system(f"printf '\\e[8;{rows};{cols}t'")


class TestSnakeGame:
    """
    Unit tests for the SnakeGame class.

    Tests the core functionality of the game, including:
        - Snake initialization
        - Food spawning
        - Snake movement
        - Collision detection
        - Game state management
    """

    def setup_method(self):
        """
        Setup a fresh SnakeGame instance before each test.

        Creates a new game object in test mode to avoid curses initialization.
        """
        self.game = SnakeGame(test_mode=True)

    def teardown_method(self, method):
        """Cleanup after each test method."""
        del self.game

    def test_init_snake(self):
        """Verify the snake is initialized correctly."""
        self.game.init_snake()
        assert len(self.game.snake) == 3
        head_x, head_y = self.game.snake[0]
        assert (head_x, head_y) == (self.game.width // 2, self.game.height // 2)

    def test_spawn_food_not_on_snake(self):
        """Verify that spawned food does not overlap the snake."""
        self.game.init_snake()
        self.game.spawn_food()
        assert self.game.food is not None
        assert self.game.food not in self.game.snake

    def test_move_snake_forward(self):
        """Verify snake moves correctly in the current direction."""
        self.game.init_snake()
        head_before = self.game.snake[0]
        self.game.move_snake()
        head_after = self.game.snake[0]
        assert head_after[0] == head_before[0] + 1  # moved right
        assert head_after[1] == head_before[1]

    def test_snake_eats_food_and_grows(self):
        """Verify snake grows and score increases when eating food."""
        self.game.init_snake()
        head_x, head_y = self.game.snake[0]
        self.game.food = (head_x + 1, head_y)  # Place food directly ahead
        initial_length = len(self.game.snake)

        self.game.move_snake()

        assert len(self.game.snake) == initial_length + 1
        assert self.game.score == 1
        assert self.game.food is not None  # Respawned

    def test_snake_collision_with_wall(self):
        """Verify game detects collision with wall."""
        self.game.snake = deque([(self.game.width - 2, 5)])  # near right wall
        self.game.direction = "RIGHT"
        self.game.move_snake()
        assert self.game.game_over is True

    def test_snake_collision_with_itself(self):
        """Verify game detects snake colliding with itself."""
        self.game.snake = deque([(5, 5), (4, 5), (3, 5), (3, 6), (4, 6), (5, 6)])
        self.game.direction = "UP"
        self.game.snake.appendleft((5, 6))  # force head into body
        assert self.game.check_collision((5, 6)) is True

    def test_restart_game_resets_state(self):
        """Verify restarting the game resets state."""
        self.game.init_snake()
        self.game.score = 10
        self.game.game_over = True
        self.game.restart_game()

        assert self.game.score == 0
        assert self.game.game_over is False
        assert len(self.game.snake) == 3
        assert self.game.food is not None


class TestSmallTerminalSnakegame:
    """
    Tests for validating behavior in small terminal environments.

    Skips automatically on Windows because pseudo-terminals are not supported.
    """

    @pytest.mark.skipif(sys.platform == "win32", reason="Pseudo-terminal not supported on Windows")
    def test_window_terminal_validity_print(self):
        """
        Test that the game rejects terminals that are too small.
        """

        with pytest.raises(Exception) as exc_info:
            SnakeGame()
        assert "Terminal too small" in str(exc_info.value)
        assert "Minimum required: 24x44" in str(exc_info.value)
