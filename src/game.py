import pygame
import random
from dataclasses import dataclass
from typing import Tuple

@dataclass
class GameConfig:
    width: int = 800
    height: int = 600
    paddle_width: int = 15
    paddle_height: int = 90
    ball_size: int = 15
    paddle_speed: int = 5
    ball_speed: int = 7
    fps: int = 60
    background_color: Tuple[int, int, int] = (0, 0, 0)
    paddle_color: Tuple[int, int, int] = (255, 255, 255)
    ball_color: Tuple[int, int, int] = (255, 255, 255)
    score_color: Tuple[int, int, int] = (255, 255, 255)

class PongGame:
    def __init__(self, config: GameConfig = GameConfig()):
        pygame.init()
        self.config = config
        self.screen = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        
        # Initialize game objects
        self.reset_game()

    def reset_game(self):
        """Reset the game state."""
        self.paddle1_pos = pygame.Rect(
            50,
            self.config.height // 2 - self.config.paddle_height // 2,
            self.config.paddle_width,
            self.config.paddle_height
        )
        
        self.paddle2_pos = pygame.Rect(
            self.config.width - 50 - self.config.paddle_width,
            self.config.height // 2 - self.config.paddle_height // 2,
            self.config.paddle_width,
            self.config.paddle_height
        )
        
        self.ball_pos = pygame.Rect(
            self.config.width // 2 - self.config.ball_size // 2,
            self.config.height // 2 - self.config.ball_size // 2,
            self.config.ball_size,
            self.config.ball_size
        )
        
        # Set initial ball velocity
        angle = random.uniform(-0.5, 0.5)
        direction = 1 if random.random() > 0.5 else -1
        self.ball_vel = [direction * self.config.ball_speed * abs(angle), self.config.ball_speed]
        
        # Initialize scores
        self.score1 = 0
        self.score2 = 0

    def handle_input(self):
        """Handle player input."""
        keys = pygame.key.get_pressed()
        
        # Player 1 controls (W/S)
        if keys[pygame.K_w] and self.paddle1_pos.top > 0:
            self.paddle1_pos.y -= self.config.paddle_speed
        if keys[pygame.K_s] and self.paddle1_pos.bottom < self.config.height:
            self.paddle1_pos.y += self.config.paddle_speed
            
        # Player 2 controls (Up/Down)
        if keys[pygame.K_UP] and self.paddle2_pos.top > 0:
            self.paddle2_pos.y -= self.config.paddle_speed
        if keys[pygame.K_DOWN] and self.paddle2_pos.bottom < self.config.height:
            self.paddle2_pos.y += self.config.paddle_speed

    def update(self):
        """Update game state."""
        # Move ball
        self.ball_pos.x += self.ball_vel[0]
        self.ball_pos.y += self.ball_vel[1]
        
        # Ball collision with top and bottom
        if self.ball_pos.top <= 0 or self.ball_pos.bottom >= self.config.height:
            self.ball_vel[1] = -self.ball_vel[1]
        
        # Ball collision with paddles
        if self.ball_pos.colliderect(self.paddle1_pos) or self.ball_pos.colliderect(self.paddle2_pos):
            self.ball_vel[0] = -self.ball_vel[0]
            # Add some randomness to the bounce
            self.ball_vel[1] += random.uniform(-1, 1)
        
        # Scoring
        if self.ball_pos.left <= 0:
            self.score2 += 1
            self.reset_ball()
        elif self.ball_pos.right >= self.config.width:
            self.score1 += 1
            self.reset_ball()

    def reset_ball(self):
        """Reset ball position and velocity."""
        self.ball_pos.center = (self.config.width // 2, self.config.height // 2)
        angle = random.uniform(-0.5, 0.5)
        direction = 1 if random.random() > 0.5 else -1
        self.ball_vel = [direction * self.config.ball_speed * abs(angle), self.config.ball_speed]

    def draw(self):
        """Draw game objects."""
        # Clear screen
        self.screen.fill(self.config.background_color)
        
        # Draw paddles
        pygame.draw.rect(self.screen, self.config.paddle_color, self.paddle1_pos)
        pygame.draw.rect(self.screen, self.config.paddle_color, self.paddle2_pos)
        
        # Draw ball
        pygame.draw.rect(self.screen, self.config.ball_color, self.ball_pos)
        
        # Draw center line
        pygame.draw.aaline(
            self.screen,
            self.config.paddle_color,
            (self.config.width // 2, 0),
            (self.config.width // 2, self.config.height)
        )
        
        # Draw scores
        score1_text = self.font.render(str(self.score1), True, self.config.score_color)
        score2_text = self.font.render(str(self.score2), True, self.config.score_color)
        self.screen.blit(score1_text, (self.config.width // 4, 20))
        self.screen.blit(score2_text, (3 * self.config.width // 4, 20))
        
        # Update display
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.config.fps)
        
        pygame.quit()

if __name__ == "__main__":
    game = PongGame()
    game.run() 