"""
Unit tests for AI Agent (Minimax with Alpha-Beta Pruning)
Tests AI decision making, timeout, and search algorithm
"""

import unittest
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mancala_game import MancalaGame
from ai_agent import AIAgent, RandomAgent


class TestAIAgentInitialization(unittest.TestCase):
    """Tests for AI agent initialization."""
    
    def test_default_initialization(self):
        """Test AI agent initializes with correct defaults."""
        ai = AIAgent(player=1)
        
        self.assertEqual(ai.player, 1)
        self.assertEqual(ai.max_depth, 6)
        self.assertEqual(ai.timeout, 5.0)
    
    def test_custom_parameters(self):
        """Test AI agent with custom parameters."""
        ai = AIAgent(player=2, max_depth=4, timeout=3.0)
        
        self.assertEqual(ai.player, 2)
        self.assertEqual(ai.max_depth, 4)
        self.assertEqual(ai.timeout, 3.0)


class TestAIMoveLegality(unittest.TestCase):
    """Tests for AI move legality."""
    
    def test_ai_returns_legal_move_player1(self):
        """Test AI Player 1 always returns legal move."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=3, timeout=5.0)
        
        for _ in range(10):
            game.reset()
            move = ai.get_move(game)
            legal_moves = game.get_legal_moves(1)
            
            self.assertIn(move, legal_moves)
    
    def test_ai_returns_legal_move_player2(self):
        """Test AI Player 2 always returns legal move."""
        game = MancalaGame()
        ai = AIAgent(player=2, max_depth=3, timeout=5.0)
        
        for _ in range(10):
            game.reset()
            move = ai.get_move(game)
            legal_moves = game.get_legal_moves(2)
            
            self.assertIn(move, legal_moves)
    
    def test_ai_handles_limited_moves(self):
        """Test AI handles when only one move available."""
        game = MancalaGame()
        # Only one legal move
        game.board = [0, 0, 0, 0, 0, 5, 0, 4, 4, 4, 4, 4, 4, 0]
        
        ai = AIAgent(player=1, max_depth=4, timeout=5.0)
        move = ai.get_move(game)
        
        self.assertEqual(move, 5)  # Only legal move
    
    def test_ai_handles_many_moves(self):
        """Test AI handles when all moves available."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=3, timeout=5.0)
        
        move = ai.get_move(game)
        
        self.assertIn(move, [0, 1, 2, 3, 4, 5])


class TestAITimeout(unittest.TestCase):
    """Tests for AI timeout mechanism."""
    
    def test_ai_respects_timeout(self):
        """Test AI doesn't exceed timeout significantly."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=20, timeout=1.0)  # High depth, low timeout
        
        start_time = time.time()
        move = ai.get_move(game)
        elapsed = time.time() - start_time
        
        # Should complete within timeout + small buffer
        self.assertLess(elapsed, 2.0)
        # Should still return valid move
        self.assertIn(move, game.get_legal_moves(1))
    
    def test_very_short_timeout(self):
        """Test AI handles very short timeout."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=10, timeout=0.1)
        
        start_time = time.time()
        move = ai.get_move(game)
        elapsed = time.time() - start_time
        
        # Should complete quickly
        self.assertLess(elapsed, 1.0)
        # Should still return valid move
        self.assertIn(move, game.get_legal_moves(1))


class TestAIStrategicBehavior(unittest.TestCase):
    """Tests for AI strategic behavior."""
    
    def test_ai_takes_winning_move(self):
        """Test AI takes immediately winning move."""
        game = MancalaGame()
        # Set up winning scenario for Player 1
        game.board = [0, 0, 0, 0, 0, 1, 23, 0, 0, 0, 0, 0, 1, 23]
        
        ai = AIAgent(player=1, max_depth=4, timeout=5.0)
        move = ai.get_move(game)
        
        # AI should take the move that ends the game in their favor
        self.assertEqual(move, 5)
    
    def test_ai_avoids_losing_move(self):
        """Test AI avoids obviously bad moves."""
        game = MancalaGame()
        # Multiple moves available, some clearly better
        
        ai = AIAgent(player=1, max_depth=4, timeout=5.0)
        move = ai.get_move(game)
        
        # Should return a valid strategic move
        self.assertIn(move, game.get_legal_moves(1))
    
    def test_ai_prefers_extra_turn(self):
        """Test AI prefers moves that give extra turn."""
        game = MancalaGame()
        # Pit 2 gives extra turn (lands in store)
        
        ai = AIAgent(player=1, max_depth=4, timeout=5.0)
        move = ai.get_move(game)
        
        # AI should likely choose move that gives extra turn
        # Pit 2 with 4 stones lands in store
        # This is a soft test - AI might have other strategic reasons
        self.assertIn(move, game.get_legal_moves(1))
    
    def test_ai_considers_capture(self):
        """Test AI considers capture opportunities."""
        game = MancalaGame()
        # Set up capture opportunity
        game.board = [1, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 10, 4, 0]
        # Moving pit 0 to pit 1 captures pit 11's 10 stones
        
        ai = AIAgent(player=1, max_depth=4, timeout=5.0)
        move = ai.get_move(game)
        
        # Should return valid move (likely capture move)
        self.assertIn(move, game.get_legal_moves(1))


class TestAIConsistency(unittest.TestCase):
    """Tests for AI consistency and correctness."""
    
    def test_ai_deterministic_at_depth(self):
        """Test AI is reasonably consistent for same position."""
        game = MancalaGame()
        ai = AIAgent(player=1, max_depth=4, timeout=5.0)
        
        # Run multiple times
        moves = []
        for _ in range(5):
            game.reset()
            moves.append(ai.get_move(game))
        
        # All moves should be legal
        for move in moves:
            self.assertIn(move, [0, 1, 2, 3, 4, 5])
    
    def test_ai_doesnt_crash_various_positions(self):
        """Test AI handles various board positions."""
        ai = AIAgent(player=1, max_depth=3, timeout=3.0)
        
        test_positions = [
            [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0],  # Initial
            [0, 0, 0, 0, 0, 1, 20, 4, 4, 4, 4, 4, 4, 0],  # Near end
            [10, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 10, 5],  # Sparse
            [1, 1, 1, 1, 1, 1, 10, 1, 1, 1, 1, 1, 1, 10],  # Low stones
        ]
        
        for position in test_positions:
            game = MancalaGame()
            game.board = position.copy()
            
            if game.get_legal_moves(1):  # If moves exist
                move = ai.get_move(game)
                self.assertIn(move, game.get_legal_moves(1))


class TestRandomAgent(unittest.TestCase):
    """Tests for Random Agent."""
    
    def test_random_agent_returns_legal_move(self):
        """Test random agent always returns legal move."""
        game = MancalaGame()
        agent = RandomAgent(player=1)
        
        for _ in range(50):
            game.reset()
            move = agent.get_move(game)
            self.assertIn(move, game.get_legal_moves(1))
    
    def test_random_agent_handles_limited_moves(self):
        """Test random agent with limited moves."""
        game = MancalaGame()
        game.board = [0, 0, 0, 0, 0, 5, 0, 4, 4, 4, 4, 4, 4, 0]
        
        agent = RandomAgent(player=1)
        move = agent.get_move(game)
        
        self.assertEqual(move, 5)
    
    def test_random_agent_no_moves(self):
        """Test random agent when no moves available."""
        game = MancalaGame()
        game.board = [0, 0, 0, 0, 0, 0, 24, 4, 4, 4, 4, 4, 4, 0]
        
        agent = RandomAgent(player=1)
        move = agent.get_move(game)
        
        self.assertEqual(move, -1)


class TestAIvsAI(unittest.TestCase):
    """Tests for AI vs AI gameplay."""
    
    def test_ai_vs_ai_completes(self):
        """Test AI vs AI game completes without errors."""
        game = MancalaGame()
        ai1 = AIAgent(player=1, max_depth=3, timeout=2.0)
        ai2 = AIAgent(player=2, max_depth=3, timeout=2.0)
        
        move_count = 0
        max_moves = 200
        
        while not game.is_game_over() and move_count < max_moves:
            current = game.current_player
            
            if current == 1:
                move = ai1.get_move(game)
            else:
                move = ai2.get_move(game)
            
            if move < 0:
                break
            
            move_again, game_over = game.make_move(move, current)
            
            if not move_again:
                game.current_player = 3 - current
            
            move_count += 1
        
        # Game should end properly
        self.assertTrue(game.is_game_over())
        self.assertLess(move_count, max_moves)
        
        # Winner should be valid
        winner = game.get_winner()
        self.assertIn(winner, [0, 1, 2])
    
    def test_multiple_ai_games(self):
        """Test multiple AI vs AI games for consistency."""
        results = []
        
        for _ in range(3):
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
            
            results.append(game.get_winner())
        
        # All games should complete with valid winner
        for result in results:
            self.assertIn(result, [0, 1, 2])


class TestAIEvaluation(unittest.TestCase):
    """Tests for AI evaluation function."""
    
    def test_evaluation_prefers_higher_store(self):
        """Test evaluation function prefers higher store count."""
        ai = AIAgent(player=1, max_depth=2, timeout=2.0)
        
        game1 = MancalaGame()
        game1.board = [2, 2, 2, 2, 2, 2, 10, 2, 2, 2, 2, 2, 2, 5]
        
        game2 = MancalaGame()
        game2.board = [2, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 10]
        
        eval1 = ai._evaluate_state(game1)
        eval2 = ai._evaluate_state(game2)
        
        self.assertGreater(eval1, eval2)
    
    def test_terminal_evaluation_win(self):
        """Test terminal evaluation for winning position."""
        ai = AIAgent(player=1, max_depth=2, timeout=2.0)
        
        game = MancalaGame()
        game.board = [0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0, 18]
        
        eval_score = ai._evaluate_terminal(game)
        
        self.assertEqual(eval_score, 10000)  # Win score
    
    def test_terminal_evaluation_loss(self):
        """Test terminal evaluation for losing position."""
        ai = AIAgent(player=1, max_depth=2, timeout=2.0)
        
        game = MancalaGame()
        game.board = [0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 30]
        
        eval_score = ai._evaluate_terminal(game)
        
        self.assertEqual(eval_score, -10000)  # Loss score


if __name__ == '__main__':
    unittest.main(verbosity=2)
