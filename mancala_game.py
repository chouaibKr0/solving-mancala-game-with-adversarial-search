"""
Mancala Game Logic Module
Implements the core game mechanics and board state management
"""

import copy
from typing import List, Tuple, Optional


class MancalaGame:
    """
    Mancala game implementation with standard rules.
    
    Board layout (indices):
    Player 2 side (top):    [12][11][10][9][8][7]
    Stores:           [13]                      [6]
    Player 1 side (bottom): [0][1][2][3][4][5]
    
    - Player 1 owns pits 0-5 and store 6
    - Player 2 owns pits 7-12 and store 13
    """
    
    def __init__(self, stones_per_pit: int = 4):
        """
        Initialize the Mancala game board.
        
        Args:
            stones_per_pit: Number of stones to start in each pit (default: 4)
        """
        self.stones_per_pit = stones_per_pit
        self.board = None
        self.current_player = None
        self.reset()
    
    def reset(self):
        """Reset the game to initial state."""
        # Initialize board: 6 pits per player + 2 stores
        self.board = [self.stones_per_pit] * 6 + [0] + [self.stones_per_pit] * 6 + [0]
        self.current_player = 1  # Player 1 starts
    
    def get_board_copy(self) -> List[int]:
        """Return a copy of the current board state."""
        return copy.deepcopy(self.board)
    
    def get_legal_moves(self, player: int) -> List[int]:
        """
        Get list of legal moves for the specified player.
        
        Args:
            player: Player number (1 or 2)
            
        Returns:
            List of pit indices that can be selected
        """
        if player == 1:
            # Player 1 can select pits 0-5
            return [i for i in range(6) if self.board[i] > 0]
        else:
            # Player 2 can select pits 7-12
            return [i for i in range(7, 13) if self.board[i] > 0]
    
    def make_move(self, pit_index: int, player: int) -> Tuple[bool, bool]:
        """
        Execute a move by picking stones from the selected pit and distributing them.
        
        Args:
            pit_index: Index of the pit to select
            player: Player number (1 or 2)
            
        Returns:
            Tuple of (move_again, game_over)
            - move_again: True if player gets another turn
            - game_over: True if the game has ended
        """
        if pit_index not in self.get_legal_moves(player):
            return False, False
        
        # Pick up stones from selected pit
        stones = self.board[pit_index]
        self.board[pit_index] = 0
        
        # Determine the opponent's store to skip
        opponent_store = 13 if player == 1 else 6
        
        # Distribute stones counter-clockwise
        current_index = pit_index
        while stones > 0:
            current_index = (current_index + 1) % 14
            
            # Skip opponent's store
            if current_index == opponent_store:
                continue
            
            self.board[current_index] += 1
            stones -= 1
        
        # Check for capture (last stone lands in empty pit on player's side)
        move_again = False
        player_store = 6 if player == 1 else 13
        
        # Check if last stone landed in player's store (extra turn)
        if current_index == player_store:
            move_again = True
        else:
            # Check for capture
            if player == 1 and 0 <= current_index <= 5:
                if self.board[current_index] == 1:  # Was empty before last stone
                    opposite_pit = 12 - current_index
                    if self.board[opposite_pit] > 0:
                        # Capture stones
                        self.board[player_store] += self.board[current_index] + self.board[opposite_pit]
                        self.board[current_index] = 0
                        self.board[opposite_pit] = 0
            elif player == 2 and 7 <= current_index <= 12:
                if self.board[current_index] == 1:  # Was empty before last stone
                    opposite_pit = 12 - current_index
                    if self.board[opposite_pit] > 0:
                        # Capture stones
                        self.board[player_store] += self.board[current_index] + self.board[opposite_pit]
                        self.board[current_index] = 0
                        self.board[opposite_pit] = 0
        
        # Check if game is over
        game_over = self.is_game_over()
        
        if game_over:
            self._collect_remaining_stones()
        
        return move_again, game_over
    
    def is_game_over(self) -> bool:
        """
        Check if the game is over (one side has no stones).
        
        Returns:
            True if game is over, False otherwise
        """
        player1_empty = all(self.board[i] == 0 for i in range(6))
        player2_empty = all(self.board[i] == 0 for i in range(7, 13))
        
        return player1_empty or player2_empty
    
    def _collect_remaining_stones(self):
        """Collect remaining stones into respective stores at game end."""
        # Collect Player 1's remaining stones
        for i in range(6):
            self.board[6] += self.board[i]
            self.board[i] = 0
        
        # Collect Player 2's remaining stones
        for i in range(7, 13):
            self.board[13] += self.board[i]
            self.board[i] = 0
    
    def get_winner(self) -> Optional[int]:
        """
        Determine the winner based on store counts.
        
        Returns:
            1 if Player 1 wins, 2 if Player 2 wins, 0 for tie, None if game not over
        """
        if not self.is_game_over():
            return None
        
        player1_score = self.board[6]
        player2_score = self.board[13]
        
        if player1_score > player2_score:
            return 1
        elif player2_score > player1_score:
            return 2
        else:
            return 0  # Tie
    
    def get_score(self, player: int) -> int:
        """
        Get the current score (store count) for a player.
        
        Args:
            player: Player number (1 or 2)
            
        Returns:
            Number of stones in player's store
        """
        return self.board[6] if player == 1 else self.board[13]
    
    def evaluate_board(self, player: int) -> int:
        """
        Evaluate the board state from the perspective of the given player.
        
        Args:
            player: Player number (1 or 2)
            
        Returns:
            Score difference (player's store - opponent's store)
        """
        if player == 1:
            return self.board[6] - self.board[13]
        else:
            return self.board[13] - self.board[6]
    
    def __str__(self) -> str:
        """String representation of the board."""
        lines = []
        lines.append("=" * 50)
        lines.append(f"Player 2:  {self.board[12]:2} {self.board[11]:2} {self.board[10]:2} {self.board[9]:2} {self.board[8]:2} {self.board[7]:2}")
        lines.append(f"Store: [{self.board[13]:2}]" + " " * 26 + f"[{self.board[6]:2}]")
        lines.append(f"Player 1:  {self.board[0]:2} {self.board[1]:2} {self.board[2]:2} {self.board[3]:2} {self.board[4]:2} {self.board[5]:2}")
        lines.append("=" * 50)
        return "\n".join(lines)
