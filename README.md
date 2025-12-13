# Mancala Game - Adversarial Search Implementation

A complete implementation of the classic Mancala board game with AI players using Minimax algorithm with Alpha-Beta pruning. Built with Python and Pygame.

## Features

- **Multiple Game Modes**:
  - Human vs Human
  - Human vs AI
  - AI vs Human
  - AI vs AI

- **Intelligent AI**:
  - Minimax algorithm with Alpha-Beta pruning
  - Configurable search depth
  - Heuristic evaluation function
  - Iterative deepening for better timeout handling

- **Timeout Mechanism**:
  - AI players: 5-second timeout (falls back to random move)
  - Human players: 30-second timeout (auto-random move)
  - Prevents game from stalling

- **Interactive UI**:
  - Beautiful Pygame-based interface
  - Visual hover effects
  - Click or keyboard controls
  - Real-time score display
  - Turn indicators

## Game Rules

Mancala is a two-player turn-based strategy game played on a board with:
- 6 pits per player (small holes)
- 1 store per player (large holes on the sides)
- 4 stones in each pit at the start

### How to Play:

1. **Choose a Pit**: On your turn, pick one of your pits (must contain stones)
2. **Distribute Stones**: Pick up all stones from that pit and distribute them counter-clockwise, one stone per pit
3. **Skip Opponent's Store**: When distributing, skip your opponent's store
4. **Capture Rule**: If your last stone lands in an empty pit on your side, capture that stone plus all stones from the opposite pit
5. **Extra Turn**: If your last stone lands in your own store, you get another turn
6. **Game End**: The game ends when one player's side is empty
7. **Winner**: The player with the most stones in their store wins

## Installation

### Prerequisites

- Python 3.7 or higher
- Pygame library

### Setup

1. Clone or download this repository:
```bash
cd solving-mancala-game-with-adversarial-search
```

2. Install required dependencies:
```bash
pip install pygame
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Game

```bash
python main.py
```

### Controls

**Mouse Controls**:
- Click on any pit to select it (must be your turn and pit must have stones)
- Click on menu buttons to select game mode

**Keyboard Controls**:
- `0-5`: Select pits 0-5 (Player 1)
- `7-9`: Select pits 7-9 (Player 2)
- `A`: Select pit 10 (Player 2)
- `B`: Select pit 11 (Player 2)
- `C`: Select pit 12 (Player 2)
- `ESC`: Quit game or return to menu
- `SPACE/ENTER`: Play again after game over

## Project Structure

```
solving-mancala-game-with-adversarial-search/
│
├── main.py              # Main game controller and entry point
├── mancala_game.py      # Core game logic and rules
├── ai_agent.py          # AI implementation (Minimax + Alpha-Beta)
├── ui.py                # Pygame UI and graphics
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── Project 4.pdf       # Project specifications
```

## Implementation Details

### Game Logic (`mancala_game.py`)

- **MancalaGame Class**: Manages board state, move validation, and game rules
- Board represented as list of 14 integers (6 pits + 1 store per player)
- Implements stone distribution, capture logic, and win conditions
- Provides move generation and board evaluation

### AI Agent (`ai_agent.py`)

- **AIAgent Class**: Implements intelligent computer player
- **Minimax Algorithm**: Explores game tree to find optimal moves
- **Alpha-Beta Pruning**: Optimizes search by eliminating irrelevant branches
- **Iterative Deepening**: Gradually increases search depth
- **Timeout Handling**: Uses threading to enforce time limits
- **Heuristic Evaluation**: Scores board states based on:
  - Store difference (primary factor)
  - Stone distribution (secondary factor)
  - Potential captures and extra turns

### User Interface (`ui.py`)

- **MancalaUI Class**: Pygame-based graphical interface
- Visual representation of board, pits, stores, and stones
- Color-coded players and turn indicators
- Hover effects for better user experience
- Animated transitions and messages
- Game over screen with replay option

### Game Controller (`main.py`)

- **GameController Class**: Manages game flow and player interactions
- Main menu for mode selection
- Coordinates between UI, game logic, and AI agents
- Implements timeout mechanism for all player types
- Handles game state transitions

## Algorithm Details

### Minimax with Alpha-Beta Pruning

The AI uses the Minimax algorithm to determine the best move:

1. **Minimax**: Assumes both players play optimally
   - Maximizing player tries to maximize score
   - Minimizing player tries to minimize score
   - Recursively evaluates all possible moves

2. **Alpha-Beta Pruning**: Optimization technique
   - Alpha: Best score maximizer can guarantee
   - Beta: Best score minimizer can guarantee
   - Prunes branches that cannot affect final decision
   - Reduces search space significantly

3. **Evaluation Function**:
   ```
   score = (my_store - opponent_store) * 10 + 
           (my_stones - opponent_stones) * 0.5
   ```

4. **Special Cases**:
   - Extra turn when landing in own store
   - Capture when landing in empty own pit
   - Game-over terminal states

### Performance

- **Search Depth**: Default depth of 6 (configurable)
- **Timeout**: 5 seconds for AI moves
- **Move Quality**: Near-optimal play at depth 6
- **Pruning Efficiency**: ~50-70% reduction in nodes evaluated

## Configuration

You can customize the game by modifying these parameters in the code:

**In `main.py`** (`GameController.__init__`):
```python
self.ai_timeout = 5.0        # AI thinking time (seconds)
self.human_timeout = 30.0    # Human move timeout (seconds)
```

**In `ai_agent.py`** (`AIAgent.__init__`):
```python
max_depth = 6               # Search depth (higher = stronger but slower)
```

**In `mancala_game.py`** (`MancalaGame.__init__`):
```python
stones_per_pit = 4          # Initial stones per pit
```

## Troubleshooting

**Issue**: Game window doesn't open
- **Solution**: Make sure Pygame is installed: `pip install pygame`

**Issue**: AI takes too long to move
- **Solution**: Reduce `max_depth` in AIAgent initialization

**Issue**: Import errors
- **Solution**: Ensure all files are in the same directory

**Issue**: Game crashes during AI vs AI
- **Solution**: Increase timeout value or reduce search depth

## Future Enhancements

Possible improvements for the project:
- [ ] Different difficulty levels (Easy, Medium, Hard)
- [ ] Move history and undo functionality
- [ ] Save/load game states
- [ ] Statistics and win/loss tracking
- [ ] Tournament mode
- [ ] Different Mancala variants (Kalah, Oware, etc.)
- [ ] Network multiplayer
- [ ] Better graphics and animations
- [ ] Sound effects and music

## License

This project is created for educational purposes.

## Acknowledgments

- Classic Mancala game rules
- Minimax and Alpha-Beta pruning algorithms
- Pygame library for graphics
- Python threading for timeout mechanism

## Authors

Implementation for CS/AI course project demonstrating adversarial search algorithms in game playing.

---

**Enjoy playing Mancala!** 🎮
