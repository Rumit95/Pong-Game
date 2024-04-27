# Pong Game

This project is a simple implementation of the classic Pong game using Python, Pygame, and Pymunk for physics simulation.

## Requirements

- Python 3.x
- Pygame
- Pymunk

You can install the required packages using pip:

`pip install pygame pymunk`

## Game Features

- 2D Pong game with basic physics.
- Score tracking for two players.
- Ball speed normalization after hitting paddles.
- Boundary walls that keep the ball within the game area.

## Controls

- Player 1:
  - Move up: `W`
  - Move down: `S`
- Player 2:
  - Move up: `Arrow Up`
  - Move down: `Arrow Down`

## Running the Game

To start the game, run the `Pong.py` file:

`python Pong.py`

## Game Mechanics

- The game consists of a ball, two paddles for the players, and four walls.
- Each player controls a paddle using the keyboard.
- The ball speeds up slightly each time it hits a paddle.
- The game tracks the score of each player, updating it whenever the ball passes a paddle.

## Quitting the Game

To exit the game, close the game window or press the quit button on your window manager.

Enjoy playing Pong!