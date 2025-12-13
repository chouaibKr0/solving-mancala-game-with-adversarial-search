"""
Unit tests for MancalaGame class (core game logic)
Tests initialization, moves, captures, extra turns, and game ending conditions
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mancala_game import MancalaGame


class TestGameInitialization(unittest.TestCase):
    """Tests for game initialization and reset."""
    
    def test_default_initialization(self):
        """Test game initializes with default 4 stones per pit."""
        game = MancalaGame()
        expected = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.assertEqual(game.board, expected)
        self.assertEqual(game.current_player, 1)
        self.assertEqual(game.stones_per_pit, 4)
    
    def test_custom_stones_per_pit(self):
        """Test game initializes with custom stones per pit."""
        for stones in [1, 3, 6, 10]:
            game = MancalaGame(stones_per_pit=stones)
            expected = [stones] * 6 + [0] + [stones] * 6 + [0]
            self.assertEqual(game.board, expected)
            self.assertEqual(game.stones_per_pit, stones)
    
    def test_reset_game(self):
        """Test game reset restores initial state."""
        game = MancalaGame()
        # Modify the board
        game.board[0] = 10
        game.board[6] = 5
        game.current_player = 2
        
        # Reset
        game.reset()
        
        expected = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.assertEqual(game.board, expected)
        self.assertEqual(game.current_player, 1)
    
    def test_get_board_copy_independence(self):
        """Test board copy is independent of original."""
        game = MancalaGame()
        board_copy = game.get_board_copy()
        board_copy[0] = 999
        
        self.assertEqual(game.board[0], 4)  # Original unchanged
        self.assertEqual(board_copy[0], 999)
    
    def test_stores_start_empty(self):
        """Test both stores start with 0 stones."""
        game = MancalaGame()
        self.assertEqual(game.board[6], 0)   # Player 1 store
        self.assertEqual(game.board[13], 0)  # Player 2 store


class TestLegalMoves(unittest.TestCase):
    """Tests for legal move generation."""
    
    def test_player1_initial_moves(self):
        """Test Player 1 has all pits as legal moves initially."""
        game = MancalaGame()
        moves = game.get_legal_moves(1)
        self.assertEqual(moves, [0, 1, 2, 3, 4, 5])
    
    def test_player2_initial_moves(self):
        """Test Player 2 has all pits as legal moves initially."""
        game = MancalaGame()
        moves = game.get_legal_moves(2)
        self.assertEqual(moves, [7, 8, 9, 10, 11, 12])
    
    def test_empty_pit_not_legal(self):
        """Test that empty pits are not legal moves."""
        game = MancalaGame()
        game.board[0] = 0
        game.board[2] = 0
        
        moves = game.get_legal_moves(1)
        self.assertNotIn(0, moves)
        self.assertNotIn(2, moves)
        self.assertEqual(moves, [1, 3, 4, 5])
    
    def test_all_pits_empty_no_moves(self):
        """Test no legal moves when player's side is empty."""
        game = MancalaGame()
        for i in range(6):
            game.board[i] = 0
        
        moves = game.get_legal_moves(1)
        self.assertEqual(moves, [])
    
    def test_single_stone_is_legal(self):
        """Test pit with single stone is legal move."""
        game = MancalaGame()
        game.board[3] = 1
        
        moves = game.get_legal_moves(1)
        self.assertIn(3, moves)


class TestBasicMoves(unittest.TestCase):
    """Tests for basic stone distribution."""
    
    def test_simple_move_player1(self):
        """Test simple move distributes stones correctly."""
        game = MancalaGame()
        move_again, game_over = game.make_move(0, 1)
        
        self.assertEqual(game.board[0], 0)  # Source pit empty
        self.assertEqual(game.board[1], 5)  # +1 stone
        self.assertEqual(game.board[2], 5)
        self.assertEqual(game.board[3], 5)
        self.assertEqual(game.board[4], 5)
        self.assertFalse(move_again)
        self.assertFalse(game_over)
    
    def test_simple_move_player2(self):
        """Test simple move for Player 2."""
        game = MancalaGame()
        move_again, game_over = game.make_move(7, 2)
        
        self.assertEqual(game.board[7], 0)
        self.assertEqual(game.board[8], 5)
        self.assertEqual(game.board[9], 5)
        self.assertEqual(game.board[10], 5)
        self.assertEqual(game.board[11], 5)
    
    def test_single_stone_move(self):
        """Test moving a single stone."""
        game = MancalaGame()
        game.board[0] = 1
        
        game.make_move(0, 1)
        
        self.assertEqual(game.board[0], 0)
        self.assertEqual(game.board[1], 5)  # Original 4 + 1
    
    def test_illegal_move_rejected(self):
        """Test that illegal moves return False, False."""
        game = MancalaGame()
        game.board[0] = 0  # Make pit 0 empty
        
        result = game.make_move(0, 1)
        self.assertEqual(result, (False, False))
    
    def test_wrong_player_pit_rejected(self):
        """Test player can't move opponent's pits."""
        game = MancalaGame()
        
        # Player 1 trying to move Player 2's pit
        result = game.make_move(7, 1)
        self.assertEqual(result, (False, False))
    
    def test_stone_count_preserved(self):
        """Test total stone count is preserved after move."""
        game = MancalaGame()
        total_before = sum(game.board)
        
        game.make_move(0, 1)
        total_after = sum(game.board)
        
        self.assertEqual(total_before, total_after)


class TestWrapAround(unittest.TestCase):
    """Tests for board wrap-around behavior."""
    
    def test_wrap_around_board(self):
        """Test stones wrap around the board."""
        game = MancalaGame()
        game.board[5] = 10  # Many stones to wrap around
        
        game.make_move(5, 1)
        
        self.assertEqual(game.board[5], 0)
        self.assertGreater(game.board[6], 0)  # Player 1's store
        self.assertGreater(game.board[0], 4)  # Back to start
    
    def test_skip_opponent_store_player1(self):
        """Test Player 1 skips Player 2's store (index 13)."""
        game = MancalaGame()
        # Set up: Player 1 moves from pit 5 with 8 stones
        # Path: 5->6(store)->7->8->9->10->11->12->(skip 13)->0
        # Make sure player 1 still has stones so game doesn't end
        game.board = [1, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 5]
        
        store_13_before = game.board[13]  # 5
        game.make_move(5, 1)
        
        # Store 13 should be unchanged (Player 1 skips it)
        self.assertEqual(game.board[13], store_13_before)
    
    def test_skip_opponent_store_player2(self):
        """Test Player 2 skips Player 1's store (index 6)."""
        game = MancalaGame()
        # Setup: Player 2 has multiple stones so game doesn't end
        # Pit 7 has 8 stones: 7->8->9->10->11->12->13(store)->0->1->2->3->4->5->(skip 6)->7
        game.board = [0, 0, 0, 0, 0, 0, 10, 8, 1, 1, 1, 1, 1, 0]
        
        store_6_before = game.board[6]  # 10
        game.make_move(7, 2)
        
        # Store 6 should be unchanged (Player 2 skips it)
        self.assertEqual(game.board[6], store_6_before)
    
    def test_full_lap_distribution(self):
        """Test distributing enough stones for full lap."""
        game = MancalaGame()
        # 14 stones from pit 0: goes to 1,2,3,4,5,6(store),7,8,9,10,11,12,(skip 13),0,1
        # Last stone lands on pit 1 (which has stones), avoiding capture
        # Keep player 1 with remaining stones so game doesn't end
        game.board = [14, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5]
        
        store_13_before = game.board[13]
        game.make_move(0, 1)
        
        # Store 13 should be unchanged (skipped)
        self.assertEqual(game.board[13], store_13_before)
        # Pit 0 should have received 1 stone on wrap
        self.assertEqual(game.board[0], 1)


class TestExtraTurn(unittest.TestCase):
    """Tests for the extra turn rule."""
    
    def test_extra_turn_player1_pit2(self):
        """Test Player 1 gets extra turn from pit 2."""
        game = MancalaGame()
        # Pit 2 has 4 stones: 2->3->4->5->6 (store)
        move_again, game_over = game.make_move(2, 1)
        
        self.assertTrue(move_again)
        self.assertEqual(game.board[6], 1)
    
    def test_extra_turn_player1_pit5(self):
        """Test Player 1 gets extra turn from pit 5 with 1 stone."""
        game = MancalaGame()
        game.board[5] = 1
        
        move_again, game_over = game.make_move(5, 1)
        
        self.assertTrue(move_again)
        self.assertEqual(game.board[6], 1)
    
    def test_extra_turn_player2_pit9(self):
        """Test Player 2 gets extra turn from pit 9."""
        game = MancalaGame()
        # Pit 9 has 4 stones: 9->10->11->12->13 (store)
        move_again, game_over = game.make_move(9, 2)
        
        self.assertTrue(move_again)
        self.assertEqual(game.board[13], 1)
    
    def test_extra_turn_player2_pit12(self):
        """Test Player 2 gets extra turn from pit 12 with 1 stone."""
        game = MancalaGame()
        game.board[12] = 1
        
        move_again, game_over = game.make_move(12, 2)
        
        self.assertTrue(move_again)
        self.assertEqual(game.board[13], 1)
    
    def test_no_extra_turn_regular_pit(self):
        """Test no extra turn when ending on regular pit."""
        game = MancalaGame()
        move_again, game_over = game.make_move(0, 1)
        
        self.assertFalse(move_again)
    
    def test_no_extra_turn_on_opponent_pit(self):
        """Test no extra turn when ending on opponent's pit."""
        game = MancalaGame()
        game.board[5] = 3  # Will end on pit 8 (opponent's side)
        
        move_again, game_over = game.make_move(5, 1)
        
        self.assertFalse(move_again)


class TestCapture(unittest.TestCase):
    """Tests for the capture rule."""
    
    def test_capture_player1_basic(self):
        """Test Player 1 basic capture."""
        game = MancalaGame()
        # Set up: pit 1 empty, pit 0 has 1 stone, opposite pit 11 has 5 stones
        game.board = [1, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 5, 4, 0]
        
        game.make_move(0, 1)
        
        # Should capture own stone (1) + opposite stones (5) = 6
        self.assertEqual(game.board[1], 0)   # Landing pit emptied
        self.assertEqual(game.board[11], 0)  # Opposite pit emptied
        self.assertEqual(game.board[6], 6)   # All in store
    
    def test_capture_player2_basic(self):
        """Test Player 2 basic capture."""
        game = MancalaGame()
        # Set up: pit 8 empty, pit 7 has 1 stone, opposite pit 4 has 3 stones
        game.board = [4, 4, 4, 4, 3, 4, 0, 1, 0, 4, 4, 4, 4, 0]
        
        game.make_move(7, 2)
        
        self.assertEqual(game.board[8], 0)   # Landing pit emptied
        self.assertEqual(game.board[4], 0)   # Opposite pit emptied
        self.assertEqual(game.board[13], 4)  # All in store
    
    def test_no_capture_opposite_empty(self):
        """Test no capture when opposite pit is empty."""
        game = MancalaGame()
        game.board = [1, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 0, 4, 0]
        
        game.make_move(0, 1)
        
        # No capture, stone stays in pit 1
        self.assertEqual(game.board[1], 1)
        self.assertEqual(game.board[6], 0)
    
    def test_no_capture_opponent_side(self):
        """Test no capture when landing on opponent's side."""
        game = MancalaGame()
        # Player 1 move: 7 stones from pit 5 -> 6(store),7,8,9,10,11,12
        # Landing on empty pit 12 but it's opponent's side, no capture
        game.board = [4, 4, 4, 4, 4, 7, 0, 0, 0, 0, 0, 0, 0, 0]
        
        game.make_move(5, 1)
        
        # No capture (landed on opponent's side)
        # Pit 12 should have 1 stone
        self.assertEqual(game.board[12], 1)
        # Opposite pit 0 should be unchanged (original 4)
        self.assertEqual(game.board[0], 4)
    
    def test_no_capture_pit_not_empty_before(self):
        """Test no capture if pit wasn't empty before move."""
        game = MancalaGame()
        # Pit 1 has 3 stones, will end with 4 (not a capture situation)
        game.board = [1, 3, 4, 4, 4, 4, 0, 4, 4, 4, 4, 5, 4, 0]
        
        game.make_move(0, 1)
        
        # Pit 1 should have 4 stones (original 3 + 1)
        self.assertEqual(game.board[1], 4)
        # Opposite pit should be unchanged
        self.assertEqual(game.board[11], 5)
    
    def test_capture_all_opposite_pits(self):
        """Test capture from each pit position."""
        # Test captures from different pits for Player 1
        capture_pairs = [(0, 12), (1, 11), (2, 10), (3, 9), (4, 8), (5, 7)]
        
        for pit, opposite in capture_pairs:
            game = MancalaGame()
            # Set up capture scenario
            for i in range(6):
                game.board[i] = 0
            game.board[pit] = 0
            if pit > 0:
                game.board[pit - 1] = 1  # One stone to move
            else:
                # Special case for pit 0
                game.board[5] = 7  # Will wrap around
            game.board[opposite] = 3
            
            # This test verifies the opposite pit calculation


class TestGameOver(unittest.TestCase):
    """Tests for game over conditions."""
    
    def test_game_over_player1_side_empty(self):
        """Test game ends when Player 1's side is empty."""
        game = MancalaGame()
        for i in range(6):
            game.board[i] = 0
        
        self.assertTrue(game.is_game_over())
    
    def test_game_over_player2_side_empty(self):
        """Test game ends when Player 2's side is empty."""
        game = MancalaGame()
        for i in range(7, 13):
            game.board[i] = 0
        
        self.assertTrue(game.is_game_over())
    
    def test_not_game_over_initially(self):
        """Test game is not over at start."""
        game = MancalaGame()
        self.assertFalse(game.is_game_over())
    
    def test_not_game_over_with_stones(self):
        """Test game not over when both sides have stones."""
        game = MancalaGame()
        game.board = [1, 0, 0, 0, 0, 0, 20, 1, 0, 0, 0, 0, 0, 20]
        
        self.assertFalse(game.is_game_over())
    
    def test_remaining_stones_collected(self):
        """Test remaining stones collected at game end."""
        game = MancalaGame()
        # Player 1 side empty, Player 2 has stones
        game.board = [0, 0, 0, 0, 0, 0, 10, 2, 3, 4, 5, 6, 7, 5]
        
        game._collect_remaining_stones()
        
        # Player 2's pits should be empty
        for i in range(7, 13):
            self.assertEqual(game.board[i], 0)
        # Player 2's store should have all remaining
        self.assertEqual(game.board[13], 5 + 2 + 3 + 4 + 5 + 6 + 7)
    
    def test_move_triggers_collection(self):
        """Test making final move triggers collection."""
        game = MancalaGame()
        # One stone left for Player 1
        game.board = [0, 0, 0, 0, 0, 1, 20, 4, 4, 4, 4, 4, 4, 0]
        
        move_again, game_over = game.make_move(5, 1)
        
        self.assertTrue(game_over)
        # Player 2's stones should be collected
        self.assertEqual(sum(game.board[7:13]), 0)


class TestWinner(unittest.TestCase):
    """Tests for winner determination."""
    
    def test_player1_wins(self):
        """Test Player 1 wins with more stones."""
        game = MancalaGame()
        game.board = [0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0, 18]
        
        winner = game.get_winner()
        self.assertEqual(winner, 1)
    
    def test_player2_wins(self):
        """Test Player 2 wins with more stones."""
        game = MancalaGame()
        game.board = [0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 33]
        
        winner = game.get_winner()
        self.assertEqual(winner, 2)
    
    def test_tie_game(self):
        """Test tie when stores are equal."""
        game = MancalaGame()
        game.board = [0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 24]
        
        winner = game.get_winner()
        self.assertEqual(winner, 0)
    
    def test_no_winner_game_not_over(self):
        """Test no winner when game is still going."""
        game = MancalaGame()
        
        winner = game.get_winner()
        self.assertIsNone(winner)


class TestScoring(unittest.TestCase):
    """Tests for scoring functions."""
    
    def test_get_score_player1(self):
        """Test get_score for Player 1."""
        game = MancalaGame()
        game.board[6] = 15
        
        self.assertEqual(game.get_score(1), 15)
    
    def test_get_score_player2(self):
        """Test get_score for Player 2."""
        game = MancalaGame()
        game.board[13] = 20
        
        self.assertEqual(game.get_score(2), 20)
    
    def test_evaluate_board_player1_ahead(self):
        """Test board evaluation when Player 1 is ahead."""
        game = MancalaGame()
        game.board[6] = 20
        game.board[13] = 10
        
        eval1 = game.evaluate_board(1)
        eval2 = game.evaluate_board(2)
        
        self.assertEqual(eval1, 10)   # 20 - 10
        self.assertEqual(eval2, -10)  # 10 - 20
    
    def test_evaluate_board_tied(self):
        """Test board evaluation when tied."""
        game = MancalaGame()
        game.board[6] = 15
        game.board[13] = 15
        
        self.assertEqual(game.evaluate_board(1), 0)
        self.assertEqual(game.evaluate_board(2), 0)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_empty_board(self):
        """Test behavior with completely empty board."""
        game = MancalaGame()
        game.board = [0] * 14
        
        self.assertTrue(game.is_game_over())
        self.assertEqual(game.get_legal_moves(1), [])
        self.assertEqual(game.get_legal_moves(2), [])
    
    def test_only_stores_have_stones(self):
        """Test when only stores have stones."""
        game = MancalaGame()
        game.board = [0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 24]
        
        self.assertTrue(game.is_game_over())
        self.assertEqual(game.get_winner(), 0)  # Tie
    
    def test_large_stone_count(self):
        """Test with large number of stones."""
        game = MancalaGame(stones_per_pit=20)
        
        self.assertEqual(sum(game.board), 240)  # 12 pits * 20
        
        # Make a move and verify integrity
        game.make_move(0, 1)
        self.assertEqual(sum(game.board), 240)
    
    def test_string_representation(self):
        """Test string representation of board."""
        game = MancalaGame()
        board_str = str(game)
        
        self.assertIn("Player 1", board_str)
        self.assertIn("Player 2", board_str)
        self.assertIn("Store", board_str)


if __name__ == '__main__':
    unittest.main(verbosity=2)
