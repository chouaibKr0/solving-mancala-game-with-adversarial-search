"""
Configuration file for Mancala Game
Adjust these settings to customize game behavior
"""

# Game Settings
STONES_PER_PIT = 4  # Initial number of stones in each pit (standard is 4)

# AI Settings
AI_MAX_DEPTH = 6  # Maximum search depth for Minimax algorithm (higher = stronger, slower)
AI_TIMEOUT = 5.0  # Time limit for AI decisions in seconds

# Player Timeout Settings
HUMAN_TIMEOUT = 30.0  # Time limit for human player moves in seconds
ENABLE_TIMEOUT = True  # Set to False to disable timeout mechanism

# UI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 30

# Colors (R, G, B)
BACKGROUND_COLOR = (34, 139, 34)  # Forest green
BOARD_COLOR = (139, 69, 19)  # Saddle brown
PIT_COLOR = (101, 67, 33)  # Dark brown
STORE_COLOR = (160, 82, 45)  # Sienna
STONE_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (255, 255, 255)  # White
HIGHLIGHT_COLOR = (255, 215, 0)  # Gold
HOVER_COLOR = (255, 255, 0)  # Yellow
PLAYER1_COLOR = (70, 130, 180)  # Steel blue
PLAYER2_COLOR = (220, 20, 60)  # Crimson

# Animation Settings
MESSAGE_DISPLAY_TIME = 3.0  # How long messages are shown in seconds
AI_MOVE_DELAY = 0.5  # Delay after AI makes a move to show it

# Difficulty Presets
DIFFICULTY_EASY = {'max_depth': 3, 'timeout': 3.0}
DIFFICULTY_MEDIUM = {'max_depth': 6, 'timeout': 5.0}
DIFFICULTY_HARD = {'max_depth': 9, 'timeout': 10.0}

# Debug Settings
DEBUG_MODE = False  # Set to True to enable debug output
SHOW_AI_THINKING = True  # Show "AI is thinking..." message
