import pygame
from typing import List, Tuple, Callable

class MenuItem:
    def __init__(self, text: str, action: Callable, position: Tuple[int, int]):
        self.text = text
        self.action = action
        self.position = position
        self.is_selected = False

class Menu:
    def __init__(self, screen: pygame.Surface, items: List[MenuItem]):
        self.screen = screen
        self.items = items
        self.selected_index = 0
        self.items[self.selected_index].is_selected = True
        
        # Font setup
        self.font = pygame.font.Font(None, 64)
        self.selected_color = (255, 255, 0)
        self.unselected_color = (255, 255, 255)
        
        # Background
        self.background_color = (0, 0, 0)
        
        # Title
        self.title_font = pygame.font.Font(None, 96)
        self.title = "PONG"
        self.title_pos = (
            screen.get_width() // 2,
            screen.get_height() // 4
        )

    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle menu input. Returns True if menu should continue running."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.items[self.selected_index].is_selected = False
                self.selected_index = (self.selected_index - 1) % len(self.items)
                self.items[self.selected_index].is_selected = True
                
            elif event.key == pygame.K_DOWN:
                self.items[self.selected_index].is_selected = False
                self.selected_index = (self.selected_index + 1) % len(self.items)
                self.items[self.selected_index].is_selected = True
                
            elif event.key == pygame.K_RETURN:
                self.items[self.selected_index].action()
                return False
                
            elif event.key == pygame.K_ESCAPE:
                return False
        
        return True

    def draw(self):
        """Draw the menu."""
        # Clear screen
        self.screen.fill(self.background_color)
        
        # Draw title
        title_surface = self.title_font.render(self.title, True, self.unselected_color)
        title_rect = title_surface.get_rect(center=self.title_pos)
        self.screen.blit(title_surface, title_rect)
        
        # Draw menu items
        for item in self.items:
            color = self.selected_color if item.is_selected else self.unselected_color
            text_surface = self.font.render(item.text, True, color)
            text_rect = text_surface.get_rect(center=item.position)
            self.screen.blit(text_surface, text_rect)
        
        pygame.display.flip()

    def run(self):
        """Run the menu loop."""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                running = self.handle_input(event)
            
            self.draw()
            clock.tick(60)
        
        return True 