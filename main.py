"""
Main Game Controller
Handles game flow, player management, and game modes
"""

import pygame
import sys
import time
from typing import Optional
from mancala_game import MancalaGame
from ai_agent import AIAgent, RandomAgent
from ui import MancalaUI


class GameController:
    """
    Main game controller that manages the game flow.
    Supports Human vs Human, Human vs AI, and AI vs AI modes.
    """
    
    def __init__(self):
        """Initialize the game controller."""
        self.game = MancalaGame(stones_per_pit=4)
        self.ui = MancalaUI()
        
        # Player configuration
        self.player1_type = None  # 'human' or 'ai'
        self.player2_type = None
        self.player1_agent = None
        self.player2_agent = None
        
        # Timeout settings
        self.ai_timeout = 5.0  # seconds
        self.human_timeout = 30.0  # seconds
        
        # Player names
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        
        # Turn timer
        self.turn_start_time = None
    
    def show_main_menu(self) -> bool:
        """
        Display main menu and get game mode selection.
        
        Returns:
            True to start game, False to quit
        """
        menu_running = True
        
        while menu_running:
            self.ui.screen.fill((34, 139, 34))
            
            # Title
            title = self.ui.title_font.render("Mancala Game", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.ui.width // 2, 80))
            self.ui.screen.blit(title, title_rect)
            
            # Subtitle
            subtitle = self.ui.font.render("Select Game Mode", True, (255, 255, 255))
            subtitle_rect = subtitle.get_rect(center=(self.ui.width // 2, 140))
            self.ui.screen.blit(subtitle, subtitle_rect)
            
            # Menu options
            menu_options = [
                ("Human vs Human", 200),
                ("Human vs AI", 270),
                ("AI vs Human", 340),
                ("AI vs AI", 410),
                ("Help", 480),
                ("Quit", 550)
            ]
            
            buttons = []
            for text, y in menu_options:
                button_rect = pygame.Rect(self.ui.width // 2 - 150, y, 300, 50)
                buttons.append((button_rect, text))
                
                # Check hover
                mouse_pos = pygame.mouse.get_pos()
                color = (100, 149, 237) if button_rect.collidepoint(mouse_pos) else (70, 130, 180)
                
                pygame.draw.rect(self.ui.screen, color, button_rect, border_radius=10)
                
                text_surface = self.ui.font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=button_rect.center)
                self.ui.screen.blit(text_surface, text_rect)
            
            pygame.display.flip()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    for button_rect, text in buttons:
                        if button_rect.collidepoint(pos):
                            if text == "Human vs Human":
                                self.setup_game('human', 'human')
                                return True
                            elif text == "Human vs AI":
                                self.setup_game('human', 'ai')
                                return True
                            elif text == "AI vs Human":
                                self.setup_game('ai', 'human')
                                return True
                            elif text == "AI vs AI":
                                self.setup_game('ai', 'ai')
                                return True
                            elif text == "Help":
                                if not self.ui.draw_help_screen():
                                    return False
                            elif text == "Quit":
                                return False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return False
                    elif event.key == pygame.K_h:
                        if not self.ui.draw_help_screen():
                            return False
            
            self.ui.clock.tick(30)
        
        return False
    
    def setup_game(self, player1_type: str, player2_type: str):
        """
        Setup game with specified player types.
        
        Args:
            player1_type: 'human' or 'ai'
            player2_type: 'human' or 'ai'
        """
        self.player1_type = player1_type
        self.player2_type = player2_type
        
        # Create AI agents if needed
        if player1_type == 'ai':
            self.player1_agent = AIAgent(player=1, max_depth=6, timeout=self.ai_timeout)
            self.player1_name = "AI Player 1"
        else:
            self.player1_agent = None
            self.player1_name = "Human Player 1"
        
        if player2_type == 'ai':
            self.player2_agent = AIAgent(player=2, max_depth=6, timeout=self.ai_timeout)
            self.player2_name = "AI Player 2"
        else:
            self.player2_agent = None
            self.player2_name = "Human Player 2"
        
        # Reset game
        self.game.reset()
    
    def play_game(self):
        """Main game loop."""
        running = True
        
        while running:
            current_player = self.game.current_player
            
            # Draw current state
            self.ui.draw_board(self.game, current_player, 
                             self.player1_name, self.player2_name)
            
            # Check if game is over
            if self.game.is_game_over():
                play_again = self.ui.show_game_over(self.game, 
                                                    self.player1_name, 
                                                    self.player2_name)
                if play_again:
                    if self.show_main_menu():
                        continue
                    else:
                        running = False
                else:
                    running = False
                continue
            
            # Get move based on player type
            move = None
            
            if current_player == 1 and self.player1_type == 'ai':
                # AI Player 1's turn
                self.ui.show_message(f"{self.player1_name} is thinking...")
                self.ui.draw_board(self.game, current_player, 
                                 self.player1_name, self.player2_name)
                
                self.turn_start_time = time.time()
                move = self.player1_agent.get_move(self.game)
                
                print(f"AI Player 1 selected pit {move}")
                self.ui.wait_for_event(0.5)  # Brief pause to show move
                
            elif current_player == 2 and self.player2_type == 'ai':
                # AI Player 2's turn
                self.ui.show_message(f"{self.player2_name} is thinking...")
                self.ui.draw_board(self.game, current_player, 
                                 self.player1_name, self.player2_name)
                
                self.turn_start_time = time.time()
                move = self.player2_agent.get_move(self.game)
                
                print(f"AI Player 2 selected pit {move}")
                self.ui.wait_for_event(0.5)  # Brief pause to show move
                
            else:
                # Human player's turn
                move = self._get_human_move(current_player)
                
                if move is None:  # User quit
                    running = False
                    continue
            
            # Execute move
            if move is not None and move >= 0:
                move_again, game_over = self.game.make_move(move, current_player)
                
                if move_again and not game_over:
                    self.ui.show_message(f"{self.player1_name if current_player == 1 else self.player2_name} gets another turn!")
                else:
                    # Switch player
                    self.game.current_player = 3 - current_player
        
        self.ui.quit()
    
    def _get_human_move(self, player: int) -> Optional[int]:
        """
        Get move from human player with timeout support.
        
        Args:
            player: Player number (1 or 2)
            
        Returns:
            Pit index to select, or None if quit
        """
        self.turn_start_time = time.time()
        waiting = True
        
        while waiting:
            # Check timeout
            elapsed = time.time() - self.turn_start_time
            if elapsed > self.human_timeout:
                # Timeout - make random move
                import random
                legal_moves = self.game.get_legal_moves(player)
                if legal_moves:
                    self.ui.show_message("Timeout! Random move selected.")
                    return random.choice(legal_moves)
                return -1
            
            # Update hover state
            mouse_pos = pygame.mouse.get_pos()
            self.ui.hovered_pit = self.ui.get_hovered_pit(mouse_pos, self.game, player)
            
            # Draw board with hover effect
            self.ui.draw_board(self.game, player, 
                             self.player1_name, self.player2_name)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked_pit = self.ui.get_clicked_pit(pos, self.game, player)
                    
                    if clicked_pit is not None:
                        return clicked_pit
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    
                    if event.key == pygame.K_h:
                        # Show help screen
                        self.ui.draw_help_screen()
                        self.ui.draw_board(self.game, player, 
                                         self.player1_name, self.player2_name)
                    
                    if event.key == pygame.K_r:
                        # Restart game - show confirmation
                        self.ui.show_message("Press R again to restart")
                        self.ui.draw_board(self.game, player, 
                                         self.player1_name, self.player2_name)
                    
                    # Allow keyboard input for pit selection
                    if event.key in [pygame.K_0, pygame.K_1, pygame.K_2, 
                                    pygame.K_3, pygame.K_4, pygame.K_5]:
                        pit = event.key - pygame.K_0
                        if player == 1 and pit in self.game.get_legal_moves(1):
                            return pit
                    
                    if event.key in [pygame.K_7, pygame.K_8, pygame.K_9]:
                        pit = event.key - pygame.K_0
                        if player == 2 and pit in self.game.get_legal_moves(2):
                            return pit
                    
                    # Keys for pits 10-12
                    if event.key == pygame.K_a and player == 2:
                        if 10 in self.game.get_legal_moves(2):
                            return 10
                    if event.key == pygame.K_b and player == 2:
                        if 11 in self.game.get_legal_moves(2):
                            return 11
                    if event.key == pygame.K_c and player == 2:
                        if 12 in self.game.get_legal_moves(2):
                            return 12
            
            self.ui.clock.tick(30)
        
        return None
    
    def run(self):
        """Run the game application."""
        try:
            while True:
                if self.show_main_menu():
                    self.play_game()
                else:
                    break
        except KeyboardInterrupt:
            print("\nGame interrupted by user")
        finally:
            self.ui.quit()
            pygame.quit()
            sys.exit()


def main():
    """Main entry point."""
    print("=" * 60)
    print("Mancala Game - Adversarial Search Implementation")
    print("=" * 60)
    print("\nGame Features:")
    print("- Human vs Human")
    print("- Human vs AI (Minimax with Alpha-Beta Pruning)")
    print("- AI vs AI")
    print("- Timeout mechanism for all players")
    print("\nControls:")
    print("- Click on a pit to select it")
    print("- Or use keyboard: 0-5 for Player 1, 7-9,A,B,C for Player 2")
    print("- ESC to quit")
    print("=" * 60)
    print()
    
    controller = GameController()
    controller.run()


if __name__ == "__main__":
    main()
