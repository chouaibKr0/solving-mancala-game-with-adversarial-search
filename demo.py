"""
Demo script to showcase AI capabilities
Runs an AI vs AI game with visualization
"""

import time
from mancala_game import MancalaGame
from ai_agent import AIAgent


def print_board(game, move_num=None):
    """Print board state in ASCII format."""
    if move_num:
        print(f"\n{'='*50}")
        print(f"Move #{move_num}")
        print('='*50)
    print(game)
    print(f"Score - Player 1: {game.board[6]}, Player 2: {game.board[13]}")
    print()


def run_demo():
    """Run a demonstration game."""
    print("\n" + "="*60)
    print(" "*15 + "MANCALA AI DEMONSTRATION")
    print("="*60)
    print("\nThis demo shows two AI players competing using")
    print("Minimax algorithm with Alpha-Beta pruning.")
    print("\nAI Settings:")
    print("  - Search Depth: 6")
    print("  - Timeout: 5 seconds")
    print("  - Evaluation: Store difference + stone distribution")
    print("\nPress Ctrl+C to stop at any time")
    print("="*60)
    
    input("\nPress Enter to start the demonstration...")
    
    # Initialize game and AIs
    game = MancalaGame(stones_per_pit=4)
    ai1 = AIAgent(player=1, max_depth=6, timeout=5.0)
    ai2 = AIAgent(player=2, max_depth=6, timeout=5.0)
    
    move_count = 0
    max_moves = 200
    
    print_board(game, 0)
    
    try:
        while not game.is_game_over() and move_count < max_moves:
            current_player = game.current_player
            player_name = "Player 1 (AI)" if current_player == 1 else "Player 2 (AI)"
            
            print(f"{player_name}'s turn...")
            
            # Get AI move
            start_time = time.time()
            
            if current_player == 1:
                move = ai1.get_move(game)
            else:
                move = ai2.get_move(game)
            
            elapsed = time.time() - start_time
            
            if move < 0:
                print("No legal moves available!")
                break
            
            print(f"  Selected pit: {move}")
            print(f"  Decision time: {elapsed:.2f}s")
            
            # Make move
            move_again, game_over = game.make_move(move, current_player)
            
            move_count += 1
            print_board(game, move_count)
            
            if move_again and not game_over:
                print(f"  → {player_name} gets another turn!\n")
            else:
                # Switch player
                game.current_player = 3 - current_player
            
            # Pause for readability
            time.sleep(0.5)
        
        # Game over
        print("\n" + "="*60)
        print(" "*20 + "GAME OVER")
        print("="*60)
        
        winner = game.get_winner()
        if winner == 0:
            print("\nResult: It's a TIE!")
        elif winner == 1:
            print("\nResult: Player 1 (AI) WINS!")
        else:
            print("\nResult: Player 2 (AI) WINS!")
        
        print(f"\nFinal Scores:")
        print(f"  Player 1: {game.board[6]} stones")
        print(f"  Player 2: {game.board[13]} stones")
        print(f"\nTotal moves: {move_count}")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        print(f"Game stopped at move {move_count}")
        print(f"Current scores - P1: {game.board[6]}, P2: {game.board[13]}")


if __name__ == "__main__":
    run_demo()
