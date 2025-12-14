"""
AI Agent Module - Implements Minimax with Alpha-Beta Pruning
Handles computer player decision-making with timeout support
"""

import copy
import random
import time
import threading
from typing import Optional, Tuple, List
from mancala_game import MancalaGame


class AIAgent:
    """
    AI agent using Minimax algorithm with Alpha-Beta pruning.
    Includes timeout mechanism for move decisions.
    Supports multiple heuristic strategies.
    """
    
    # Available heuristic types
    HEURISTIC_BALANCED = 'balanced'      # Store difference + stone count (default for Player 1)
    HEURISTIC_AGGRESSIVE = 'aggressive'  # Maximize captures + extra turns (default for Player 2)
    
    def __init__(self, player: int, max_depth: int = 6, timeout: float = 5.0, 
                 heuristic_type: str = None):
        """
        Initialize the AI agent.
        
        Args:
            player: Player number (1 or 2)
            max_depth: Maximum search depth for Minimax
            timeout: Time limit in seconds for move decision
            heuristic_type: 'balanced' or 'aggressive' (auto-selected by player if None)
        """
        self.player = player
        self.max_depth = max_depth
        self.timeout = timeout
        self.best_move = None
        self.search_cancelled = False
        
        # Auto-select heuristic based on player if not specified
        if heuristic_type is None:
            self.heuristic_type = self.HEURISTIC_BALANCED if player == 1 else self.HEURISTIC_AGGRESSIVE
        else:
            self.heuristic_type = heuristic_type
    
    def get_move(self, game: MancalaGame) -> int:
        """
        Get the best move for the current game state.
        Uses timeout to ensure decision is made within time limit.
        
        Args:
            game: Current game instance
            
        Returns:
            Index of the pit to select (or random legal move if timeout)
        """
        legal_moves = game.get_legal_moves(self.player)
        
        if not legal_moves:
            return -1
        
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        # Reset search state
        self.best_move = None
        self.search_cancelled = False
        
        # Start search in a separate thread with timeout
        search_thread = threading.Thread(
            target=self._search_with_timeout,
            args=(game,)
        )
        search_thread.daemon = True
        search_thread.start()
        
        # Wait for result or timeout
        search_thread.join(timeout=self.timeout)
        
        if search_thread.is_alive():
            # Timeout occurred
            self.search_cancelled = True
            print(f"AI Player {self.player} timeout - making random move")
            return random.choice(legal_moves)
        
        # Return best move found
        if self.best_move is None:
            return random.choice(legal_moves)
        
        return self.best_move
    
    def _search_with_timeout(self, game: MancalaGame):
        """Internal method to perform minimax search."""
        try:
            # Use iterative deepening for better timeout handling
            for depth in range(1, self.max_depth + 1):
                if self.search_cancelled:
                    break
                
                best_score = float('-inf')
                best_move = None
                
                legal_moves = game.get_legal_moves(self.player)
                
                # Try moves in random order to avoid predictability
                random.shuffle(legal_moves)
                
                for move in legal_moves:
                    if self.search_cancelled:
                        break
                    
                    # Simulate move
                    game_copy = self._copy_game(game)
                    move_again, game_over = game_copy.make_move(move, self.player)
                    
                    # Calculate score
                    if game_over:
                        score = self._evaluate_terminal(game_copy)
                    elif move_again:
                        # Extra turn for same player
                        score = self._minimax(
                            game_copy, depth - 1, float('-inf'), float('inf'),
                            True, self.player
                        )
                    else:
                        # Opponent's turn
                        opponent = 3 - self.player
                        score = self._minimax(
                            game_copy, depth - 1, float('-inf'), float('inf'),
                            False, opponent
                        )
                    
                    if score > best_score:
                        best_score = score
                        best_move = move
                
                # Update best move for this depth
                if best_move is not None:
                    self.best_move = best_move
        except Exception as e:
            print(f"Error in AI search: {e}")
            if self.best_move is None:
                legal_moves = game.get_legal_moves(self.player)
                if legal_moves:
                    self.best_move = random.choice(legal_moves)
    
    def _minimax(self, game: MancalaGame, depth: int, alpha: float, beta: float,
                 maximizing: bool, current_player: int) -> float:
        """
        Minimax algorithm with Alpha-Beta pruning.
        
        Args:
            game: Game state to evaluate
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing: True if maximizing player's turn
            current_player: Current player making move
            
        Returns:
            Evaluated score for this state
        """
        if self.search_cancelled:
            return 0
        
        # Terminal conditions
        if depth == 0 or game.is_game_over():
            return self._evaluate_state(game)
        
        legal_moves = game.get_legal_moves(current_player)
        
        if not legal_moves:
            # No legal moves, game should be over
            return self._evaluate_state(game)
        
        if maximizing:
            max_eval = float('-inf')
            
            for move in legal_moves:
                if self.search_cancelled:
                    break
                
                game_copy = self._copy_game(game)
                move_again, game_over = game_copy.make_move(move, current_player)
                
                if game_over:
                    eval_score = self._evaluate_terminal(game_copy)
                elif move_again:
                    # Same player moves again
                    eval_score = self._minimax(game_copy, depth - 1, alpha, beta, True, current_player)
                else:
                    # Opponent's turn
                    opponent = 3 - current_player
                    eval_score = self._minimax(game_copy, depth - 1, alpha, beta, False, opponent)
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        else:
            min_eval = float('inf')
            
            for move in legal_moves:
                if self.search_cancelled:
                    break
                
                game_copy = self._copy_game(game)
                move_again, game_over = game_copy.make_move(move, current_player)
                
                if game_over:
                    eval_score = self._evaluate_terminal(game_copy)
                elif move_again:
                    # Same player moves again
                    eval_score = self._minimax(game_copy, depth - 1, alpha, beta, False, current_player)
                else:
                    # Back to maximizing player's turn
                    opponent = 3 - current_player
                    eval_score = self._minimax(game_copy, depth - 1, alpha, beta, True, opponent)
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def _evaluate_state(self, game: MancalaGame) -> float:
        """
        Evaluate a game state using the selected heuristic function.
        
        Args:
            game: Game state to evaluate
            
        Returns:
            Heuristic score
        """
        if game.is_game_over():
            return self._evaluate_terminal(game)
        
        if self.heuristic_type == self.HEURISTIC_AGGRESSIVE:
            return self._heuristic_aggressive(game)
        else:
            return self._heuristic_balanced(game)
    
    def _heuristic_balanced(self, game: MancalaGame) -> float:
        """
        Balanced Heuristic (Player 1 default):
        Focuses on store difference and maintaining stone advantage.
        
        Strategy: Steady accumulation, defensive play
        """
        my_store = game.board[6] if self.player == 1 else game.board[13]
        opp_store = game.board[13] if self.player == 1 else game.board[6]
        
        # Store difference (most important)
        score = (my_store - opp_store) * 10
        
        # Stones on my side (potential captures)
        if self.player == 1:
            my_stones = sum(game.board[0:6])
            opp_stones = sum(game.board[7:13])
        else:
            my_stones = sum(game.board[7:13])
            opp_stones = sum(game.board[0:6])
        
        score += (my_stones - opp_stones) * 0.5
        
        return score
    
    def _heuristic_aggressive(self, game: MancalaGame) -> float:
        """
        Aggressive Heuristic (Player 2 default):
        Prioritizes captures, extra turns, and attacking opponent's stones.
        
        Strategy: High-risk, high-reward plays
        """
        my_store = game.board[6] if self.player == 1 else game.board[13]
        opp_store = game.board[13] if self.player == 1 else game.board[6]
        
        # Base score from stores (weighted higher)
        score = (my_store - opp_store) * 15
        
        # Determine my pits and opponent pits
        if self.player == 1:
            my_pits = range(6)
            opp_pits = range(7, 13)
            my_store_idx = 6
        else:
            my_pits = range(7, 13)
            opp_pits = range(0, 6)
            my_store_idx = 13
        
        # Count capture opportunities (empty pits with stones opposite)
        capture_potential = 0
        for pit in my_pits:
            if game.board[pit] == 0:  # Empty pit on my side
                opposite = 12 - pit
                if game.board[opposite] > 0:  # Opponent has stones opposite
                    capture_potential += game.board[opposite]
        
        score += capture_potential * 3
        
        # Count extra turn opportunities (pits that can land in store)
        extra_turn_potential = 0
        for pit in my_pits:
            stones = game.board[pit]
            if stones > 0:
                # Calculate where last stone lands
                distance_to_store = my_store_idx - pit
                if stones == distance_to_store:
                    extra_turn_potential += 2
        
        score += extra_turn_potential * 4
        
        # Penalize opponent's stones heavily (aggressive stance)
        opp_stones = sum(game.board[pit] for pit in opp_pits)
        score -= opp_stones * 0.8
        
        return score
    
    def _evaluate_terminal(self, game: MancalaGame) -> float:
        """
        Evaluate terminal game state.
        
        Args:
            game: Terminal game state
            
        Returns:
            Win/loss/draw score
        """
        winner = game.get_winner()
        
        if winner == self.player:
            return 10000  # Win
        elif winner == 0:
            return 0  # Draw
        else:
            return -10000  # Loss
    
    def _copy_game(self, game: MancalaGame) -> MancalaGame:
        """Create a deep copy of the game state."""
        game_copy = MancalaGame(game.stones_per_pit)
        game_copy.board = copy.deepcopy(game.board)
        game_copy.current_player = game.current_player
        return game_copy


class RandomAgent:
    """Simple agent that makes random legal moves."""
    
    def __init__(self, player: int):
        """
        Initialize random agent.
        
        Args:
            player: Player number (1 or 2)
        """
        self.player = player
    
    def get_move(self, game: MancalaGame) -> int:
        """
        Get a random legal move.
        
        Args:
            game: Current game instance
            
        Returns:
            Random legal pit index
        """
        legal_moves = game.get_legal_moves(self.player)
        return random.choice(legal_moves) if legal_moves else -1
