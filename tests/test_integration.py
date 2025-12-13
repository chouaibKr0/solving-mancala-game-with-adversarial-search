"""
Integration tests for complete game scenarios
Tests full game simulations and component interactions
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mancala_game import MancalaGame
from ai_agent import AIAgent, RandomAgent


class TestCompleteGameScenarios(unittest.TestCase):
    """Tests for complete game scenarios."""
    
    def test_full_game_random_vs_random(self):
        """Test complete game with random agents."""
        game = MancalaGame()
        agent1 = RandomAgent(player=1)
        agent2 = RandomAgent(player=2)
        
        move_count = 0
        max_moves = 500
        
        while not game.is_game_over() and move_count < max_moves:
            current = game.current_player
            
            if current == 1:
                move = agent1.get_move(game)
            else:
                move = agent2.get_move(game)
            
            if move < 0:
                break
            
            move_again, game_over = game.make_move(move, current)
            
            if not move_again:
                game.current_player = 3 - current
            
            move_count += 1
        
        # Verify game ended properly
        self.assertTrue(game.is_game_over())
        
        # Verify scores are valid
        total_stones = game.board[6] + game.board[13]
        self.assertEqual(total_stones, 48)  # 4 stones * 12 pits
    
    def test_stone_conservation(self):
        """Test total stones are conserved throughout game."""
        game = MancalaGame()
        ai1 = AIAgent(player=1, max_depth=2, timeout=1.0)
        ai2 = AIAgent(player=2, max_depth=2, timeout=1.0)
        
        initial_total = sum(game.board)
        
        for _ in range(50):  # Play 50 moves
            if game.is_game_over():
                break
            
            current = game.current_player
            move = ai1.get_move(game) if current == 1 else ai2.get_move(game)
            
            if move < 0:
                break
            
            move_again, _ = game.make_move(move, current)
            
            # Verify stone conservation
            current_total = sum(game.board)
            self.assertEqual(current_total, initial_total)
            
            if not move_again:
                game.current_player = 3 - current
    
    def test_extra_turn_chain(self):
        """Test chain of extra turns works correctly."""
        game = MancalaGame()
        game.current_player = 1
        
        # Set up for multiple extra turns
        game.board = [1, 2, 3, 4, 1, 1, 0, 4, 4, 4, 4, 4, 4, 0]
        
        # Move pit 4 (1 stone) -> lands in pit 5
        move_again, _ = game.make_move(4, 1)
        self.assertFalse(move_again)  # Lands on pit 5, not store
        
        # Reset for extra turn test
        game.board = [1, 2, 3, 4, 1, 1, 0, 4, 4, 4, 4, 4, 4, 0]
        
        # Move pit 5 (1 stone) -> lands in store
        move_again, _ = game.make_move(5, 1)
        self.assertTrue(move_again)  # Extra turn!
    
    def test_capture_scenario(self):
        """Test capture mechanic in real game scenario."""
        game = MancalaGame()
        
        # Set up capture scenario
        game.board = [1, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 6, 4, 0]
        game.current_player = 1
        
        # Store before capture
        store_before = game.board[6]
        opposite_stones = game.board[11]
        
        # Make capture move
        game.make_move(0, 1)
        
        # Verify capture occurred
        self.assertEqual(game.board[1], 0)   # Capture pit empty
        self.assertEqual(game.board[11], 0)  # Opposite pit empty
        self.assertEqual(game.board[6], store_before + 1 + opposite_stones)
    
    def test_endgame_collection(self):
        """Test endgame stone collection."""
        game = MancalaGame()
        
        # Near endgame state - total should be 48 (standard game)
        # 15 + 10 = 25 in stores, 1 + 2+3+4+5+6+7 = 28 in pits = 53 total
        # Use proper setup: 48 total stones
        game.board = [0, 0, 0, 0, 0, 1, 10, 2, 3, 4, 5, 6, 7, 10]  # Total: 48
        
        # Make final move
        move_again, game_over = game.make_move(5, 1)
        
        # Game should be over
        self.assertTrue(game_over)
        
        # Player 2's pits should be collected
        self.assertEqual(sum(game.board[7:13]), 0)
        
        # All stones should be in stores
        total_in_stores = game.board[6] + game.board[13]
        self.assertEqual(total_in_stores, 48)


class TestGameRules(unittest.TestCase):
    """Tests for specific game rules."""
    
    def test_player1_cannot_use_player2_pits(self):
        """Test Player 1 can only use their own pits."""
        game = MancalaGame()
        
        for pit in range(7, 13):
            result = game.make_move(pit, 1)
            self.assertEqual(result, (False, False))
    
    def test_player2_cannot_use_player1_pits(self):
        """Test Player 2 can only use their own pits."""
        game = MancalaGame()
        
        for pit in range(6):
            result = game.make_move(pit, 2)
            self.assertEqual(result, (False, False))
    
    def test_opposite_pit_calculation(self):
        """Test opposite pit indices are correct."""
        # Opposite pairs: (0,12), (1,11), (2,10), (3,9), (4,8), (5,7)
        pairs = [(0, 12), (1, 11), (2, 10), (3, 9), (4, 8), (5, 7)]
        
        for pit, opposite in pairs:
            calculated = 12 - pit
            self.assertEqual(calculated, opposite)
    
    def test_store_indices(self):
        """Test store indices are correct."""
        game = MancalaGame()
        
        # Player 1's store is index 6
        game.board[6] = 99
        self.assertEqual(game.get_score(1), 99)
        
        # Player 2's store is index 13
        game.board[13] = 88
        self.assertEqual(game.get_score(2), 88)


class TestEdgeCaseScenarios(unittest.TestCase):
    """Tests for edge case game scenarios."""
    
    def test_minimum_stones_game(self):
        """Test game with minimum stones (1 per pit)."""
        game = MancalaGame(stones_per_pit=1)
        
        self.assertEqual(sum(game.board), 12)  # 12 pits * 1 stone
        
        # Game should be playable
        move = game.get_legal_moves(1)
        self.assertEqual(len(move), 6)
    
    def test_maximum_reasonable_stones(self):
        """Test game with many stones per pit."""
        game = MancalaGame(stones_per_pit=10)
        
        self.assertEqual(sum(game.board), 120)  # 12 pits * 10 stones
        
        # Make a move and verify integrity
        game.make_move(0, 1)
        self.assertEqual(sum(game.board), 120)
    
    def test_rapid_game_ending(self):
        """Test scenario where game ends quickly."""
        game = MancalaGame()
        
        # Set up for quick ending
        game.board = [1, 0, 0, 0, 0, 0, 20, 4, 4, 4, 4, 4, 4, 0]
        
        move_again, game_over = game.make_move(0, 1)
        
        self.assertTrue(game_over)
    
    def test_tie_game_scenario(self):
        """Test scenario that results in tie."""
        game = MancalaGame()
        
        # Force a tie
        game.board = [0, 0, 0, 0, 0, 1, 23, 0, 0, 0, 0, 0, 1, 23]
        
        # Player 1 makes final move
        game.make_move(5, 1)
        game.current_player = 2
        
        # If game not over, player 2 moves
        if not game.is_game_over():
            game.make_move(12, 2)
        
        winner = game.get_winner()
        self.assertEqual(winner, 0)  # Tie


class TestSequenceOfMoves(unittest.TestCase):
    """Tests for specific sequences of moves."""
    
    def test_opening_sequence(self):
        """Test common opening moves."""
        game = MancalaGame()
        
        # Common opening: pit 2 (extra turn)
        move_again, _ = game.make_move(2, 1)
        self.assertTrue(move_again)
        self.assertEqual(game.board[6], 1)
        
        # Follow up with pit 5
        move_again, _ = game.make_move(5, 1)
        self.assertFalse(move_again)  # Should switch to player 2
    
    def test_back_and_forth_play(self):
        """Test alternating moves between players."""
        game = MancalaGame()
        
        moves = [
            (0, 1),   # Player 1
            (7, 2),   # Player 2
            (1, 1),   # Player 1
            (8, 2),   # Player 2
        ]
        
        for pit, player in moves:
            legal = game.get_legal_moves(player)
            if pit in legal:
                move_again, _ = game.make_move(pit, player)
                if not move_again:
                    game.current_player = 3 - player
        
        # Game should still be in progress
        self.assertFalse(game.is_game_over())
    
    def test_multi_lap_move(self):
        """Test move that goes around board multiple times."""
        game = MancalaGame()
        
        # Large number of stones
        game.board = [26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        # Make move (26 stones goes around twice)
        game.make_move(0, 1)
        
        # Verify distribution (skipping opponent store)
        self.assertEqual(game.board[13], 0)  # Opponent store skipped
        self.assertEqual(sum(game.board), 26)  # Conservation


if __name__ == '__main__':
    unittest.main(verbosity=2)
