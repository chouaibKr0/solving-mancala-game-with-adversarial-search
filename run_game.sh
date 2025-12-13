#!/bin/bash
# Quick start script for Mancala Game

echo "======================================"
echo "Mancala Game - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed!"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "Using Python: $PYTHON_CMD"
echo ""

# Check if pygame is installed
echo "Checking dependencies..."
$PYTHON_CMD -c "import pygame" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "Pygame not found. Installing..."
    $PYTHON_CMD -m pip install pygame
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install pygame"
        echo "Please run: pip install pygame"
        exit 1
    fi
fi

echo "✓ All dependencies installed"
echo ""

# Run tests (optional)
read -p "Run tests first? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running tests..."
    $PYTHON_CMD test_game.py
    
    if [ $? -ne 0 ]; then
        echo "Tests failed! Please check the implementation."
        exit 1
    fi
    echo ""
fi

# Launch game
echo "Starting Mancala Game..."
echo ""
$PYTHON_CMD main.py
