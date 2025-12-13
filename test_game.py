"""
Test suite for Mancala Game
Tests game logic, AI behavior, and edge cases
"""

import sys
import time
from mancala_game import MancalaGame
from ai_agent import AIAgent, RandomAgent


def test_game_initialization():
    """Test game initialization."""
    print("\n=== Testing Game Initialization ===")
    game = MancalaGame(stones_per_pit=4)
    
    # Check initial state
    assert game.board == [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0], "Initial board state incorrect"
    assert game.current_player == 1, "Initial player should be 1"
    
    print("✓ Game initialization correct")
    return True


def test_legal_moves():
    """Test legal move generation."""
    print("\n=== Testing Legal Moves ===")
    game = MancalaGame()
    
    # Player 1 legal moves at start
    moves_p1 = game.get_legal_moves(1)
    assert moves_p1 == [0, 1, 2, 3, 4, 5], f"Player 1 moves incorrect: {moves_p1}"
    
    # Player 2 legal moves at start
    moves_p2 = game.get_legal_moves(2)
    assert moves_p2 == [7, 8, 9, 10, 11, 12], f"Player 2 moves incorrect: {moves_p2}"
    
    # Empty pit should not be legal
    game.board[0] = 0
    moves_p1 = game.get_legal_moves(1)
    assert 0 not in moves_p1, "Empty pit should not be legal move"
    
    print("✓ Legal move generation correct")
    return True


def test_basic_move():
    """Test basic stone distribution."""
    print("\n=== Testing Basic Move ===")
    game = MancalaGame()
    
    # Make a simple move
    move_again, game_over = game.make_move(0, 1)
    
    # After moving from pit 0 (had 4 stones), they go to pits 1,2,3,4
    assert game.board[0] == 0, "Starting pit should be empty"
    assert game.board[1] == 5, "Pit 1 should have 5 stones"
    assert game.board[2] == 5, "Pit 2 should have 5 stones"
    assert game.board[3] == 5, "Pit 3 should have 5 stones"
    assert game.board[4] == 5, "Pit 4 should have 5 stones"
    assert not move_again, "Should not get extra turn"
    assert not game_over, "Game should not be over"
    
    print("✓ Basic move works correctly")
    return True


def test_store_extra_turn():
    """Test landing in store gives extra turn."""
    print("\n=== Testing Extra Turn ===")
    game = MancalaGame()
    
    # Pit 2 has 4 stones, will land in store (index 6)
    # Path: 2 -> 3,4,5,6
    move_again, game_over = game.make_move(2, 1)
    
    assert move_again, "Should get extra turn when landing in store"
    assert game.board[6] == 1, "Store should have 1 stone"
    
    print("✓ Extra turn rule works correctly")
    return True


def test_capture():
    """Test capture rule."""
    print("\n=== Testing Capture ===")
    game = MancalaGame()
    
    # Setup: Empty pit 1, opposite pit 11 has stones
    game.board = [3, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 5, 4, 0]
    game.current_player = 1
    
    # Move from pit 0 (3 stones) -> lands in pit 3 (but we want pit 1)
    # Let's set up so last stone lands in empty pit
    game.board = [1, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 5, 4, 0]
    
    move_again, game_over = game.make_move(0, 1)
    
    # After move, should capture from opposite pit
    assert game.board[6] > 0, "Store should have captured stones"
    
    print("✓ Capture rule works correctly")
    return True


def test_game_over():
    """Test game over detection."""
    print("\n=== Testing Game Over ===")
    game = MancalaGame()
    
    # Set up end game: Player 1 side empty
    game.board = [0, 0, 0, 0, 0, 0, 20, 1, 1, 1, 1, 1, 1, 8]
    
    assert game.is_game_over(), "Game should be over when one side is empty"
    
    winner = game.get_winner()
    assert winner == 1, f"Player 1 should win with 20 stones, got winner: {winner}"
    
    print("✓ Game over detection works correctly")
    return True


def test_ai_agent():
    """Test AI agent decision making."""
    print("\n=== Testing AI Agent ===")
    game = MancalaGame()
    ai = AIAgent(player=1, max_depth=4, timeout=5.0)
    
    # AI should be able to select a legal move
    start_time = time.time()
    move = ai.get_move(game)
    elapsed = time.time() - start_time
    
    assert move in game.get_legal_moves(1), f"AI selected illegal move: {move}"
    assert elapsed < 6.0, f"AI took too long: {elapsed:.2f}s"
    
    print(f"✓ AI selected move {move} in {elapsed:.2f}s")
    return True


def test_ai_timeout():
    """Test AI timeout mechanism."""
    print("\n=== Testing AI Timeout ===")
    game = MancalaGame()
    
    # Very short timeout should trigger fallback
    ai = AIAgent(player=1, max_depth=10, timeout=0.1)
    
    start_time = time.time()
    move = ai.get_move(game)
    elapsed = time.time() - start_time
    
    assert move in game.get_legal_moves(1), "Should still make legal move after timeout"
    assert elapsed < 1.0, "Timeout should prevent long search"
    
    print(f"✓ AI timeout works (move in {elapsed:.2f}s)")
    return True


def test_full_game_simulation():
    """Simulate a full game between two AIs."""
    print("\n=== Testing Full Game Simulation ===")
    game = MancalaGame()
    ai1 = AIAgent(player=1, max_depth=4, timeout=3.0)
    ai2 = AIAgent(player=2, max_depth=4, timeout=3.0)
    
    move_count = 0
    max_moves = 200  # Prevent infinite games
    
    while not game.is_game_over() and move_count < max_moves:
        current_player = game.current_player
        
        if current_player == 1:
            move = ai1.get_move(game)
        else:
            move = ai2.get_move(game)
        
        if move < 0:
            print("No legal moves!")
            break
        
        move_again, game_over = game.make_move(move, current_player)
        
        if not move_again:
            game.current_player = 3 - current_player
        
        move_count += 1
    
    winner = game.get_winner()
    print(f"✓ Game completed in {move_count} moves")
    print(f"  Winner: {'Player 1' if winner == 1 else 'Player 2' if winner == 2 else 'Tie'}")
    print(f"  Final scores: P1={game.board[6]}, P2={game.board[13]}")
    
    assert game.is_game_over(), "Game should be over"
    assert move_count < max_moves, "Game took too many moves"
    
    return True


def run_all_tests():
    """Run all test cases."""
    print("=" * 60)
    print("MANCALA GAME TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Initialization", test_game_initialization),
        ("Legal Moves", test_legal_moves),
        ("Basic Move", test_basic_move),
        ("Extra Turn", test_store_extra_turn),
        ("Capture", test_capture),
        ("Game Over", test_game_over),
        ("AI Agent", test_ai_agent),
        ("AI Timeout", test_ai_timeout),
        ("Full Game", test_full_game_simulation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"✗ {test_name} failed")
        except AssertionError as e:
            failed += 1
            print(f"✗ {test_name} failed: {e}")
        except Exception as e:
            failed += 1
            print(f"✗ {test_name} error: {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
