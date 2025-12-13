# Quick Start Guide - Mancala Game

## Installation (1 minute)

```bash
# Step 1: Install Python dependency
pip install pygame

# Step 2: Run the game
python main.py
```

## How to Play (Visual Guide)

### Board Layout

```
┌─────────────────────────────────────────────────────────┐
│                    MANCALA GAME BOARD                    │
└─────────────────────────────────────────────────────────┘

         Player 2 (moves right to left)
    ┌───────────────────────────────────────┐
    │  [12] [11] [10] [9]  [8]  [7]         │
    │   4    4    4   4    4    4           │
    │                                        │
[13]│                                        │[6]
 0  │         PLAYER 2 STORE    PLAYER 1    │ 0
    │                           STORE       │
    │                                        │
    │   [0]  [1]  [2]  [3]  [4]  [5]        │
    │   4    4    4   4    4    4           │
    └───────────────────────────────────────┘
         Player 1 (moves left to right)
```

### Game Flow

```
┌──────────────────────────────────────────────────────────┐
│ STEP 1: SELECT YOUR PIT                                  │
│  - Click on any of your pits with stones                 │
│  - Or press keyboard: 0-5 for Player 1                   │
│                       7-9,A,B,C for Player 2             │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│ STEP 2: STONES ARE DISTRIBUTED                           │
│  - Pick up all stones from selected pit                  │
│  - Drop one stone in each pit counter-clockwise          │
│  - Skip opponent's store                                 │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│ STEP 3: CHECK FOR SPECIAL RULES                          │
│                                                           │
│  🎁 CAPTURE: Last stone lands in your empty pit          │
│     → Take that stone + all from opposite pit            │
│                                                           │
│  🔄 EXTRA TURN: Last stone lands in your store           │
│     → You get to move again!                             │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│ STEP 4: SWITCH TURNS                                     │
│  - Next player's turn (unless you got extra turn)        │
│  - Repeat until one side is empty                        │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│ GAME OVER: COUNT STONES IN STORES                        │
│  - Player with most stones in store WINS! 🏆            │
└──────────────────────────────────────────────────────────┘
```

## Example Move

### Before Move (Player 1 selects pit 2):
```
Player 2:   4   4   4   4   4   4
Store:   [0]                     [0]
Player 1:   4   4  [4]  4   4   4
                  ↑
             Select this pit
```

### After Move:
```
Player 2:   4   4   4   4   4   4
Store:   [0]                     [0]
Player 1:   4   4   0   5   5   5
                  ↓   ↓   ↓   ↓
             Distributed 4 stones
```

## Game Modes

### 🧑 Human vs Human
```
Perfect for:
- Playing with a friend
- Learning the game
- Casual play

Controls:
- Player 1: Click pits 0-5 or press 0-5
- Player 2: Click pits 7-12 or press 7-9,A,B,C
```

### 🤖 Human vs AI
```
Perfect for:
- Solo practice
- Challenge yourself
- Learn strategies

AI Features:
- Thinks 0.5-5 seconds
- Uses Minimax algorithm
- Strategic gameplay
```

### 🤖 AI vs AI
```
Perfect for:
- Watch AI strategies
- Study game patterns
- Entertainment

Watch As:
- Two AIs compete
- Optimal play demonstration
- Algorithm in action
```

## Controls Reference

### Mouse Controls
```
🖱️ Click on pit     → Select that pit
🖱️ Click on button  → Select menu option
🖱️ Move mouse       → Show hover effect
```

### Keyboard Shortcuts
```
⌨️ 0-5        → Select Player 1 pits 0-5
⌨️ 7-9        → Select Player 2 pits 7-9
⌨️ A,B,C      → Select Player 2 pits 10-12
⌨️ ESC        → Quit/Back to menu
⌨️ SPACE      → Play again (after game over)
```

## Tips & Strategies

### 🎯 Beginner Tips
1. **Free Turns**: Try to land in your store for extra moves
2. **Captures**: Land in empty pits to capture opponent's stones
3. **Think Ahead**: Plan 2-3 moves in advance
4. **Store First**: Prioritize getting stones in your store

### 🏆 Advanced Strategies
1. **Control the Board**: Keep more stones on your side
2. **Setup Captures**: Create opportunities for big captures
3. **Chain Moves**: Plan sequences of extra turns
4. **Defensive Play**: Block opponent's capture opportunities
5. **Endgame**: Calculate final stone counts

## Troubleshooting

### Game won't start
```bash
# Check Python installation
python --version

# Install pygame
pip install pygame

# Try running again
python main.py
```

### AI is too slow
```python
# Edit config.py
AI_MAX_DEPTH = 4  # Reduce from 6
AI_TIMEOUT = 3.0   # Reduce from 5.0
```

### Window issues
```bash
# Make sure you have display
# On Linux, check DISPLAY variable
echo $DISPLAY

# Try different backend
SDL_VIDEODRIVER=x11 python main.py
```

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│             MANCALA QUICK REFERENCE                      │
├─────────────────────────────────────────────────────────┤
│ OBJECTIVE: Get most stones in your store                │
│                                                          │
│ YOUR SIDE:                                               │
│   Player 1: Pits 0-5, Store 6                           │
│   Player 2: Pits 7-12, Store 13                         │
│                                                          │
│ BASIC RULES:                                             │
│   1. Pick a pit with stones                             │
│   2. Distribute counter-clockwise                        │
│   3. Skip opponent's store                              │
│   4. Switch turns (unless extra turn)                   │
│                                                          │
│ SPECIAL RULES:                                           │
│   • Capture: Empty own pit → take opposite              │
│   • Extra turn: Land in own store                       │
│                                                          │
│ WINNING:                                                 │
│   • Game ends when one side is empty                    │
│   • Player with most stones in store wins               │
│                                                          │
│ TIMEOUT:                                                 │
│   • AI: 5 seconds → random move                         │
│   • Human: 30 seconds → random move                     │
└─────────────────────────────────────────────────────────┘
```

## Need Help?

- **Read**: [README.md](README.md) for detailed info
- **Learn**: [DOCUMENTATION.md](DOCUMENTATION.md) for technical details
- **Watch**: Run `python demo.py` to see AI play
- **Practice**: Start with Human vs Human mode
- **Test**: Run `python test_game.py` to verify installation

---

**Ready to Play?**

```bash
python main.py
```

**Enjoy the game! 🎮**
