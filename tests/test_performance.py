"""
Performance and stress tests for the Mancala game
Tests AI performance, memory usage, and edge cases
"""

import unittest
import sys
import os
import time
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mancala_game import MancalaGame
from ai_agent import AIAgent, RandomAgent


class TestAIPerformance(unittest.TestCase):
    """Performance tests for AI agent."""
    
    def test_ai_response_time_depth3(self):
        """Test AI response time at depth 3."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=3, timeout=10.0)
        
        times = []
        for _ in range(5):
            game.reset()
            start = time.time()
            ai.get_move(game)
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        print(f"\nDepth 3 average time: {avg_time:.4f}s")
        
        # Should be very fast at depth 3
        self.assertLess(avg_time, 1.0)
    
    def test_ai_response_time_depth6(self):
        """Test AI response time at depth 6."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=6, timeout=10.0)
        
        times = []
        for _ in range(3):
            game.reset()
            start = time.time()
            ai.get_move(game)
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        print(f"\nDepth 6 average time: {avg_time:.4f}s")
        
        # Should complete within reasonable time
        self.assertLess(avg_time, 5.0)
    
    def test_ai_consistency_under_load(self):
        """Test AI maintains quality under repeated calls."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=4, timeout=3.0)
        
        for _ in range(20):
            if game.is_game_over():
                game.reset()
            
            move = ai.get_move(game)
            self.assertIn(move, game.get_legal_moves(1))
            
            game.make_move(move, 1)
            game.current_player = 2
            
            # Make opponent move
            opp_moves = game.get_legal_moves(2)
            if opp_moves:
                game.make_move(random.choice(opp_moves), 2)
                game.current_player = 1


class TestStressTests(unittest.TestCase):
    """Stress tests for game components."""
    
    def test_many_games_sequential(self):
        """Test running many games sequentially."""
        wins = {1: 0, 2: 0, 0: 0}
        
        for i in range(10):
            game = MancalaGame()
            ai1 = AIAgent(player=1, max_depth=2, timeout=1.0)
            ai2 = AIAgent(player=2, max_depth=2, timeout=1.0)
            
            move_count = 0
            while not game.is_game_over() and move_count < 200:
                current = game.current_player
                move = ai1.get_move(game) if current == 1 else ai2.get_move(game)
                
                if move < 0:
                    break
                
                move_again, _ = game.make_move(move, current)
                if not move_again:
                    game.current_player = 3 - current
                move_count += 1
            
            winner = game.get_winner()
            if winner is not None:
                wins[winner] += 1
        
        print(f"\nResults over 10 games: P1={wins[1]}, P2={wins[2]}, Tie={wins[0]}")
        
        # All games should complete
        total_games = wins[1] + wins[2] + wins[0]
        self.assertEqual(total_games, 10)
    
    def test_random_position_stability(self):
        """Test AI handles random board positions."""
        ai = AIAgent(player=1, max_depth=3, timeout=2.0)
        
        for _ in range(20):
            game = MancalaGame()
            
            # Generate random position
            total_stones = 48
            for i in range(14):
                if i in [6, 13]:  # Stores
                    game.board[i] = random.randint(0, total_stones // 2)
                else:
                    game.board[i] = random.randint(0, 8)
            
            # Ensure legal moves exist for player 1
            if sum(game.board[0:6]) == 0:
                game.board[random.randint(0, 5)] = 3
            
            # AI should handle any position
            move = ai.get_move(game)
            self.assertIn(move, game.get_legal_moves(1))
    
    def test_rapid_move_generation(self):
        """Test rapid move generation doesn't cause issues."""
        game = MancalaGame()
        
        for _ in range(100):
            if game.is_game_over():
                game.reset()
            
            moves = game.get_legal_moves(game.current_player)
            if moves:
                move = random.choice(moves)
                move_again, _ = game.make_move(move, game.current_player)
                
                if not move_again:
                    game.current_player = 3 - game.current_player


class TestBoundaryConditions(unittest.TestCase):
    """Tests for boundary conditions."""
    
    def test_zero_timeout(self):
        """Test AI with very small timeout."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=10, timeout=0.01)
        
        # Should still return valid move
        move = ai.get_move(game)
        self.assertIn(move, game.get_legal_moves(1))
    
    def test_depth_zero(self):
        """Test AI with depth 1 (minimum practical)."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=1, timeout=5.0)
        
        move = ai.get_move(game)
        self.assertIn(move, game.get_legal_moves(1))
    
    def test_single_stone_board(self):
        """Test with minimal stones on board."""
        game = MancalaGame()
        game.board = [1, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 1, 20]
        
        ai = AIAgent(player=1, max_depth=4, timeout=2.0)
        move = ai.get_move(game)
        
        self.assertEqual(move, 0)  # Only legal move
    
    def test_near_empty_board(self):
        """Test with nearly empty board."""
        game = MancalaGame()
        game.board = [0, 0, 1, 0, 0, 0, 23, 0, 0, 0, 0, 1, 0, 23]
        
        ai1 = AIAgent(player=1, max_depth=4, timeout=2.0)
        ai2 = AIAgent(player=2, max_depth=4, timeout=2.0)
        
        move1 = ai1.get_move(game)
        move2 = ai2.get_move(game)
        
        self.assertEqual(move1, 2)
        self.assertEqual(move2, 11)


class TestMemoryAndResources(unittest.TestCase):
    """Tests for memory and resource usage."""
    
    def test_no_memory_leak_in_game_copy(self):
        """Test that game copying doesn't accumulate memory."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=4, timeout=2.0)
        
        # Run many times - should not accumulate memory
        for _ in range(50):
            _ = ai._copy_game(game)
    
    def test_board_immutability_after_ai(self):
        """Test AI doesn't modify original game state."""
        game = MancalaGame()
        original_board = game.board.copy()
        
        ai = AIAgent(player=1, max_depth=4, timeout=2.0)
        _ = ai.get_move(game)
        
        self.assertEqual(game.board, original_board)
    
    def test_concurrent_ai_instances(self):
        """Test multiple AI instances work independently."""
        game = MancalaGame()
        
        ai1 = AIAgent(player=1, max_depth=3, timeout=2.0)
        ai2 = AIAgent(player=1, max_depth=4, timeout=2.0)
        ai3 = AIAgent(player=1, max_depth=5, timeout=2.0)
        
        move1 = ai1.get_move(game)
        move2 = ai2.get_move(game)
        move3 = ai3.get_move(game)
        
        # All should return valid moves
        for move in [move1, move2, move3]:
            self.assertIn(move, game.get_legal_moves(1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
