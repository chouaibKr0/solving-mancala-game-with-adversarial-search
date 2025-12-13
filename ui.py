"""
Pygame UI Module for Mancala Game
Provides graphical interface and user interaction
"""

import pygame
import sys
import time
from typing import Optional, Tuple
from mancala_game import MancalaGame


# Color definitions - High contrast theme
BACKGROUND = (30, 30, 50)  # Dark blue-gray
BOARD_COLOR = (139, 90, 43)  # Warm brown
PIT_COLOR = (60, 60, 80)  # Dark slate
STORE_COLOR = (80, 80, 110)  # Lighter slate
STONE_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (255, 255, 255)  # White
HIGHLIGHT_COLOR = (0, 255, 150)  # Bright green
HOVER_COLOR = (255, 200, 100)  # Warm orange
PLAYER1_COLOR = (100, 200, 255)  # Light blue
PLAYER2_COLOR = (255, 120, 120)  # Light red/pink
BUTTON_COLOR = (70, 130, 180)  # Steel blue
BUTTON_HOVER = (100, 180, 230)  # Lighter blue


class MancalaUI:
    """
    Pygame-based UI for Mancala game.
    """
    
    def __init__(self, width: int = 1200, height: int = 600):
        """
        Initialize the pygame UI.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
        """
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Mancala Game - Adversarial Search")
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # UI layout dimensions
        self.board_x = 200
        self.board_y = 150
        self.pit_radius = 40
        self.store_width = 80
        self.store_height = 200
        self.pit_spacing = 120
        
        # Game state
        self.selected_pit = None
        self.hovered_pit = None
        
        # Animation
        self.animating = False
        self.animation_start_time = 0
        self.message = ""
        self.message_time = 0
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
    
    def draw_board(self, game: MancalaGame, current_player: int, 
                   player1_name: str = "Player 1", player2_name: str = "Player 2"):
        """
        Draw the game board with current state.
        
        Args:
            game: Current game instance
            current_player: Current player (1 or 2)
            player1_name: Display name for player 1
            player2_name: Display name for player 2
        """
        self.screen.fill(BACKGROUND)
        
        # Draw title
        title = self.title_font.render("Mancala Game", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title, title_rect)
        
        # Draw current player indicator
        current_text = f"Current Turn: {player1_name if current_player == 1 else player2_name}"
        current_color = PLAYER1_COLOR if current_player == 1 else PLAYER2_COLOR
        current_surface = self.large_font.render(current_text, True, current_color)
        current_rect = current_surface.get_rect(center=(self.width // 2, 90))
        self.screen.blit(current_surface, current_rect)
        
        # Draw board background
        board_rect = pygame.Rect(self.board_x - 50, self.board_y - 50, 
                                 self.pit_spacing * 6 + 100 + self.store_width * 2,
                                 self.store_height + 100)
        pygame.draw.rect(self.screen, BOARD_COLOR, board_rect, border_radius=20)
        
        # Draw Player 2 store (left)
        self._draw_store(13, self.board_x - 50, self.board_y + 50, game.board[13])
        
        # Draw Player 1 store (right)
        self._draw_store(6, self.board_x + self.pit_spacing * 6 + 50, 
                        self.board_y + 50, game.board[6])
        
        # Draw Player 2 pits (top row, indices 12-7, left to right)
        for i, pit_index in enumerate(range(12, 6, -1)):
            x = self.board_x + self.pit_spacing * i + self.pit_spacing // 2
            y = self.board_y + 30
            self._draw_pit(pit_index, x, y, game.board[pit_index], current_player)
        
        # Draw Player 1 pits (bottom row, indices 0-5, left to right)
        for i in range(6):
            x = self.board_x + self.pit_spacing * i + self.pit_spacing // 2
            y = self.board_y + self.store_height - 30
            self._draw_pit(i, x, y, game.board[i], current_player)
        
        # Draw player labels and scores
        p1_text = f"{player1_name}: {game.board[6]}"
        p2_text = f"{player2_name}: {game.board[13]}"
        
        p1_surface = self.font.render(p1_text, True, PLAYER1_COLOR)
        p2_surface = self.font.render(p2_text, True, PLAYER2_COLOR)
        
        self.screen.blit(p1_surface, (50, self.height - 100))
        self.screen.blit(p2_surface, (50, 130))
        
        # Draw message if any
        if self.message and (time.time() - self.message_time) < 3:
            msg_surface = self.large_font.render(self.message, True, HIGHLIGHT_COLOR)
            msg_rect = msg_surface.get_rect(center=(self.width // 2, self.height - 50))
            self.screen.blit(msg_surface, msg_rect)
        
        pygame.display.flip()
    
    def _draw_pit(self, pit_index: int, x: int, y: int, stones: int, current_player: int):
        """Draw a single pit with stones."""
        # Determine if this pit can be selected
        is_selectable = False
        if current_player == 1 and 0 <= pit_index <= 5 and stones > 0:
            is_selectable = True
        elif current_player == 2 and 7 <= pit_index <= 12 and stones > 0:
            is_selectable = True
        
        # Highlight if hovered or selected
        color = PIT_COLOR
        if pit_index == self.hovered_pit and is_selectable:
            color = HOVER_COLOR
        elif pit_index == self.selected_pit:
            color = HIGHLIGHT_COLOR
        
        # Draw pit circle
        pygame.draw.circle(self.screen, color, (x, y), self.pit_radius)
        pygame.draw.circle(self.screen, TEXT_COLOR, (x, y), self.pit_radius, 3)
        
        # Draw pit number
        pit_label = self.small_font.render(str(pit_index), True, TEXT_COLOR)
        label_rect = pit_label.get_rect(center=(x, y - self.pit_radius - 15))
        self.screen.blit(pit_label, label_rect)
        
        # Draw stone count
        stone_text = self.font.render(str(stones), True, STONE_COLOR)
        stone_rect = stone_text.get_rect(center=(x, y))
        self.screen.blit(stone_text, stone_rect)
    
    def _draw_store(self, store_index: int, x: int, y: int, stones: int):
        """Draw a store (mancala) with stones."""
        store_rect = pygame.Rect(x, y, self.store_width, self.store_height)
        pygame.draw.rect(self.screen, STORE_COLOR, store_rect, border_radius=10)
        pygame.draw.rect(self.screen, TEXT_COLOR, store_rect, 3, border_radius=10)
        
        # Draw stone count
        stone_text = self.large_font.render(str(stones), True, STONE_COLOR)
        stone_rect = stone_text.get_rect(center=(x + self.store_width // 2, 
                                                  y + self.store_height // 2))
        self.screen.blit(stone_text, stone_rect)
        
        # Draw label
        label = "P2" if store_index == 13 else "P1"
        label_surface = self.small_font.render(label, True, TEXT_COLOR)
        label_rect = label_surface.get_rect(center=(x + self.store_width // 2, 
                                                     y + self.store_height + 20))
        self.screen.blit(label_surface, label_rect)
    
    def get_clicked_pit(self, pos: Tuple[int, int], game: MancalaGame, 
                       current_player: int) -> Optional[int]:
        """
        Determine which pit was clicked based on mouse position.
        
        Args:
            pos: Mouse position (x, y)
            game: Current game instance
            current_player: Current player number
            
        Returns:
            Pit index if valid click, None otherwise
        """
        x, y = pos
        
        # Check Player 2 pits (top row)
        if current_player == 2:
            for i, pit_index in enumerate(range(12, 6, -1)):
                pit_x = self.board_x + self.pit_spacing * i + self.pit_spacing // 2
                pit_y = self.board_y + 30
                
                dist = ((x - pit_x) ** 2 + (y - pit_y) ** 2) ** 0.5
                if dist <= self.pit_radius and game.board[pit_index] > 0:
                    return pit_index
        
        # Check Player 1 pits (bottom row)
        if current_player == 1:
            for i in range(6):
                pit_x = self.board_x + self.pit_spacing * i + self.pit_spacing // 2
                pit_y = self.board_y + self.store_height - 30
                
                dist = ((x - pit_x) ** 2 + (y - pit_y) ** 2) ** 0.5
                if dist <= self.pit_radius and game.board[i] > 0:
                    return i
        
        return None
    
    def get_hovered_pit(self, pos: Tuple[int, int], game: MancalaGame, 
                       current_player: int) -> Optional[int]:
        """Determine which pit is being hovered over."""
        return self.get_clicked_pit(pos, game, current_player)
    
    def show_message(self, message: str):
        """Display a temporary message on screen."""
        self.message = message
        self.message_time = time.time()
    
    def show_game_over(self, game: MancalaGame, player1_name: str = "Player 1", 
                      player2_name: str = "Player 2") -> bool:
        """
        Display game over screen with winner and play again option.
        
        Args:
            game: Finished game instance
            player1_name: Display name for player 1
            player2_name: Display name for player 2
            
        Returns:
            True if player wants to play again, False to quit
        """
        winner = game.get_winner()
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Display winner message
        if winner == 0:
            msg = "Game Over - It's a Tie!"
            color = TEXT_COLOR
        elif winner == 1:
            msg = f"Game Over - {player1_name} Wins!"
            color = PLAYER1_COLOR
        else:
            msg = f"Game Over - {player2_name} Wins!"
            color = PLAYER2_COLOR
        
        title = self.title_font.render(msg, True, color)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(title, title_rect)
        
        # Display scores
        score1 = f"{player1_name}: {game.board[6]}"
        score2 = f"{player2_name}: {game.board[13]}"
        
        score1_surface = self.large_font.render(score1, True, PLAYER1_COLOR)
        score2_surface = self.large_font.render(score2, True, PLAYER2_COLOR)
        
        score1_rect = score1_surface.get_rect(center=(self.width // 2, self.height // 2 - 20))
        score2_rect = score2_surface.get_rect(center=(self.width // 2, self.height // 2 + 20))
        
        self.screen.blit(score1_surface, score1_rect)
        self.screen.blit(score2_surface, score2_rect)
        
        # Draw buttons
        play_again_rect = pygame.Rect(self.width // 2 - 150, self.height // 2 + 80, 140, 50)
        quit_rect = pygame.Rect(self.width // 2 + 10, self.height // 2 + 80, 140, 50)
        
        pygame.draw.rect(self.screen, BUTTON_COLOR, play_again_rect, border_radius=10)
        pygame.draw.rect(self.screen, BUTTON_COLOR, quit_rect, border_radius=10)
        
        play_text = self.font.render("Play Again", True, TEXT_COLOR)
        quit_text = self.font.render("Quit", True, TEXT_COLOR)
        
        play_text_rect = play_text.get_rect(center=play_again_rect.center)
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        
        self.screen.blit(play_text, play_text_rect)
        self.screen.blit(quit_text, quit_text_rect)
        
        pygame.display.flip()
        
        # Wait for user choice
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if play_again_rect.collidepoint(pos):
                        return True
                    elif quit_rect.collidepoint(pos):
                        return False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        return True
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return False
            
            self.clock.tick(30)
    
    def wait_for_event(self, delay: float = 0.5):
        """Wait for a short delay while still processing events."""
        start_time = time.time()
        while time.time() - start_time < delay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.clock.tick(30)
    
    def quit(self):
        """Clean up and quit pygame."""
        pygame.quit()
