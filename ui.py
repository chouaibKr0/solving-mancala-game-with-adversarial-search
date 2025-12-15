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
        self.pit_radius = 45
        self.store_width = 90
        self.store_height = 220
        self.pit_spacing = 130  # Spacing between pits
        self.store_margin = 70  # Space between stores and first/last pits
        
        # Calculate total board width and center it
        total_board_width = self.pit_spacing * 6 + self.store_margin * 2 + self.store_width * 2
        self.board_left = (width - total_board_width) // 2  # absolute left of the board area
        self.board_x = self.board_left + self.store_width + self.store_margin  # first pit anchor
        
        # Center board vertically with proper top margin
        board_height = self.store_height + 100
        self.board_y = 180  # Fixed position to leave room for title and turn indicator
        
        # Game state
        self.selected_pit = None
        self.hovered_pit = None
        
        # Animation
        self.animating = False
        self.animation_start_time = 0
        self.message = ""
        self.message_time = 0
        self.pulse_time = 0  # For pulsing effect on selectable pits
        
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
        self.pulse_time += 0.05  # Update pulse animation
        
        # Draw title at top with proper spacing
        title = self.title_font.render("Mancala Game", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(self.width // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Draw current player indicator
        current_text = f"Current Turn: {player1_name if current_player == 1 else player2_name}"
        current_color = PLAYER1_COLOR if current_player == 1 else PLAYER2_COLOR
        current_surface = self.large_font.render(current_text, True, current_color)
        current_rect = current_surface.get_rect(center=(self.width // 2, 75))
        self.screen.blit(current_surface, current_rect)
        
        # Draw board background
        board_width = self.pit_spacing * 6 + self.store_margin * 2 + self.store_width * 2
        board_rect = pygame.Rect(self.board_left, 
                     self.board_y - 50, 
                     board_width,
                     self.store_height + 100)
        pygame.draw.rect(self.screen, BOARD_COLOR, board_rect, border_radius=20)
        
        # Draw Player 2 store (left) with name
        p2_store_x = self.board_left + 5
        self._draw_store(13, p2_store_x, self.board_y + 50, game.board[13], player2_name)
        
        # Draw Player 1 store (right) with name
        p1_store_x = self.board_left + board_width - self.store_width - 5
        self._draw_store(6, p1_store_x, self.board_y + 50, game.board[6], player1_name)
        
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
        
        # Show score difference - position in top right corner, away from board
        p1_score = game.board[6]
        p2_score = game.board[13]
        diff = abs(p1_score - p2_score)
        
        score_y = 115  # Position between turn indicator and board
        if diff > 0:
            leader = player1_name if p1_score > p2_score else player2_name
            lead_color = PLAYER1_COLOR if p1_score > p2_score else PLAYER2_COLOR
            lead_text = f"{leader} leads by {diff}"
            lead_surface = self.font.render(lead_text, True, lead_color)
            lead_rect = lead_surface.get_rect(center=(self.width // 2, score_y))
            self.screen.blit(lead_surface, lead_rect)
        else:
            tie_text = f"Score: {p1_score} - {p2_score}"
            tie_surface = self.font.render(tie_text, True, HIGHLIGHT_COLOR)
            tie_rect = tie_surface.get_rect(center=(self.width // 2, score_y))
            self.screen.blit(tie_surface, tie_rect)
        
        # Draw message if any
        if self.message and (time.time() - self.message_time) < 3:
            msg_surface = self.large_font.render(self.message, True, HIGHLIGHT_COLOR)
            msg_rect = msg_surface.get_rect(center=(self.width // 2, self.height - 80))
            self.screen.blit(msg_surface, msg_rect)
        
        # Draw keyboard shortcuts hint at bottom
        shortcuts = "ESC: Menu  |  H: Help  |  R: Restart  |  0-5/7-12: Quick select"
        shortcuts_surface = self.small_font.render(shortcuts, True, (150, 150, 150))
        shortcuts_rect = shortcuts_surface.get_rect(center=(self.width // 2, self.height - 30))
        self.screen.blit(shortcuts_surface, shortcuts_rect)
        
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
        border_width = 3
        
        if pit_index == self.hovered_pit and is_selectable:
            color = HOVER_COLOR
            border_width = 5
        elif pit_index == self.selected_pit:
            color = HIGHLIGHT_COLOR
            border_width = 5
        elif is_selectable:
            # Add pulsing glow for selectable pits
            import math
            pulse = abs(math.sin(self.pulse_time))
            glow_color = PLAYER1_COLOR if current_player == 1 else PLAYER2_COLOR
            glow_alpha = int(100 + 100 * pulse)  # Pulse between 100-200
            glow_radius = self.pit_radius + 5 + int(3 * pulse)
            
            # Create surface with alpha for glow effect
            glow_surface = pygame.Surface((glow_radius * 2 + 10, glow_radius * 2 + 10), pygame.SRCALPHA)
            for i in range(3):
                alpha = glow_alpha - i * 30
                pygame.draw.circle(glow_surface, (*glow_color, alpha), 
                                 (glow_radius + 5, glow_radius + 5), glow_radius - i*2, 2)
            self.screen.blit(glow_surface, (x - glow_radius - 5, y - glow_radius - 5))
        
        # Draw pit circle
        pygame.draw.circle(self.screen, color, (x, y), self.pit_radius)
        pygame.draw.circle(self.screen, TEXT_COLOR, (x, y), self.pit_radius, border_width)
        
        # Draw pit number
        pit_label = self.small_font.render(str(pit_index), True, TEXT_COLOR)
        label_rect = pit_label.get_rect(center=(x, y - self.pit_radius - 15))
        self.screen.blit(pit_label, label_rect)
        
        # Draw stone count and visual representation
        if stones > 0:
            stone_text = self.font.render(str(stones), True, STONE_COLOR)
            stone_rect = stone_text.get_rect(center=(x, y))
            self.screen.blit(stone_text, stone_rect)
            
            # Draw small stone dots for visual feedback (up to 6)
            if stones <= 6:
                stone_positions = [
                    (x, y - 15),
                    (x - 12, y - 8),
                    (x + 12, y - 8),
                    (x - 12, y + 8),
                    (x + 12, y + 8),
                    (x, y + 15)
                ]
                for i in range(min(stones, 6)):
                    sx, sy = stone_positions[i]
                    pygame.draw.circle(self.screen, (200, 200, 200), (sx, sy), 3)
        else:
            stone_text = self.small_font.render("empty", True, (150, 150, 150))
            stone_rect = stone_text.get_rect(center=(x, y))
            self.screen.blit(stone_text, stone_rect)
    
    def _draw_store(self, store_index: int, x: int, y: int, stones: int, player_name: str = ""):
        """Draw a store (mancala) with stones and player name."""
        # Determine color based on player
        if store_index == 6:  # Player 1
            border_color = PLAYER1_COLOR
        else:  # Player 2
            border_color = PLAYER2_COLOR
        
        store_rect = pygame.Rect(x, y, self.store_width, self.store_height)
        pygame.draw.rect(self.screen, STORE_COLOR, store_rect, border_radius=15)
        pygame.draw.rect(self.screen, border_color, store_rect, 4, border_radius=15)
        
        # Draw stone count (larger)
        stone_text = self.title_font.render(str(stones), True, STONE_COLOR)
        stone_rect = stone_text.get_rect(center=(x + self.store_width // 2, 
                                                  y + self.store_height // 2))
        self.screen.blit(stone_text, stone_rect)
        
        # Draw player name below store
        if player_name:
            name_color = PLAYER1_COLOR if store_index == 6 else PLAYER2_COLOR
            name_surface = self.font.render(player_name, True, name_color)
            name_rect = name_surface.get_rect(center=(x + self.store_width // 2, 
                                                       y + self.store_height + 30))
            self.screen.blit(name_surface, name_rect)
    
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
    
    def draw_help_screen(self) -> bool:
        """Draw help/rules screen.
        
        Returns:
            True to continue, False to quit
        """
        running = True
        
        while running:
            self.screen.fill(BACKGROUND)
            
            # Title
            title = self.title_font.render("How to Play Mancala", True, HIGHLIGHT_COLOR)
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 30))
            
            # Rules text
            rules = [
                "GAME RULES:",
                "• Click your pit to pick up stones",
                "• Stones distribute counter-clockwise",
                "• Skip opponent's store when distributing",
                "• Land in your store = Extra turn!",
                "• Land in empty pit = Capture opposite stones",
                "• Game ends when one side is empty",
                "• Player with most stones wins",
                "",
                "CONTROLS:",
                "• Mouse: Click pit to select",
                "• ESC: Return to menu",
                "• R: Restart game (when game over)",
                "• H: Show help (in menu)",
                "",
                "VISUAL INDICATORS:",
                "• Blue: Player 1 turn",
                "• Red: Player 2 turn",
                "• Orange: Hover over valid pit",
                "• Green: Selected pit",
                "",
                "Press ESC or click below to return"
            ]
            
            y_offset = 100
            for line in rules:
                if line.startswith(("GAME", "CONTROLS", "VISUAL")):
                    text = self.large_font.render(line, True, HIGHLIGHT_COLOR)
                elif line == "":
                    y_offset += 10
                    continue
                else:
                    text = self.font.render(line, True, TEXT_COLOR)
                
                self.screen.blit(text, (80, y_offset))
                y_offset += 35
            
            # Back button
            back_rect = pygame.Rect(self.width // 2 - 100, y_offset + 10, 200, 50)
            mouse_pos = pygame.mouse.get_pos()
            color = BUTTON_HOVER if back_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.screen, color, back_rect, border_radius=10)
            
            back_text = self.font.render("Back to Menu", True, TEXT_COLOR)
            back_text_rect = back_text.get_rect(center=back_rect.center)
            self.screen.blit(back_text, back_text_rect)
            
            pygame.display.flip()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_h:
                        return True
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(pygame.mouse.get_pos()):
                        return True
            
            self.clock.tick(30)
        
        return True
    
    def quit(self):
        """Clean up and quit pygame."""
        pygame.quit()
