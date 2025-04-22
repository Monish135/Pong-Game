import pytest
import pygame
from src.game import PongGame, GameConfig

@pytest.fixture
def game():
    pygame.init()
    game = PongGame(GameConfig())
    yield game
    pygame.quit()

def test_initialization(game):
    """Test game initialization."""
    assert game.score1 == 0
    assert game.score2 == 0
    assert isinstance(game.paddle1_pos, pygame.Rect)
    assert isinstance(game.paddle2_pos, pygame.Rect)
    assert isinstance(game.ball_pos, pygame.Rect)

def test_reset_game(game):
    """Test game reset functionality."""
    # Change some values
    game.score1 = 5
    game.score2 = 3
    game.ball_pos.x = 0
    game.ball_pos.y = 0
    
    # Reset game
    game.reset_game()
    
    # Check values are reset
    assert game.score1 == 0
    assert game.score2 == 0
    assert game.ball_pos.centerx == game.config.width // 2
    assert game.ball_pos.centery == game.config.height // 2

def test_paddle_movement(game):
    """Test paddle movement."""
    initial_y = game.paddle1_pos.y
    
    # Simulate paddle movement
    keys = {pygame.K_w: True}
    with pytest.monkeypatch.context() as m:
        m.setattr(pygame.key, "get_pressed", lambda: keys)
        game.handle_input()
    
    assert game.paddle1_pos.y < initial_y

def test_ball_collision_with_top(game):
    """Test ball collision with top of screen."""
    # Position ball at top of screen
    game.ball_pos.y = 0
    game.ball_vel[1] = -5
    
    # Update game
    game.update()
    
    # Ball should bounce down
    assert game.ball_vel[1] > 0

def test_ball_collision_with_paddle(game):
    """Test ball collision with paddle."""
    # Position ball next to paddle
    game.ball_pos.x = game.paddle1_pos.right
    game.ball_pos.y = game.paddle1_pos.centery
    initial_vel_x = game.ball_vel[0]
    
    # Update game
    game.update()
    
    # Ball should bounce off paddle
    assert game.ball_vel[0] != initial_vel_x

def test_scoring(game):
    """Test scoring system."""
    # Move ball past left edge
    game.ball_pos.x = -10
    initial_score2 = game.score2
    
    # Update game
    game.update()
    
    # Player 2 should score
    assert game.score2 == initial_score2 + 1
    
    # Ball should be reset to center
    assert game.ball_pos.centerx == game.config.width // 2 