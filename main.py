#!/usr/bin/env python3
"""Main entry point for the Pong game."""

import pygame
import sys
from src.game import PongGame, GameConfig
from src.menu import Menu, MenuItem

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create game window
    config = GameConfig()
    screen = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption("Pong")
    
    # Create game instance
    game = PongGame(config)
    
    def start_game():
        """Start a new game."""
        game.reset_game()
        game.run()
    
    def quit_game():
        """Quit the game."""
        pygame.quit()
        sys.exit()
    
    # Create menu items
    screen_center_x = config.width // 2
    items = [
        MenuItem(
            "Start Game",
            start_game,
            (screen_center_x, config.height // 2)
        ),
        MenuItem(
            "Quit",
            quit_game,
            (screen_center_x, config.height // 2 + 100)
        )
    ]
    
    # Create and run menu
    menu = Menu(screen, items)
    
    while True:
        if not menu.run():
            break

if __name__ == "__main__":
    main()
