# Tug of War

A small Pygame tug-of-war game where the player alternates `A` and `D` to pull the flag left while the computer pulls right.

## Features

- Alternating-key input fix so rapid back-and-forth presses do not deadlock the controls
- Dynamic computer surge difficulty once the player is close to winning
- Rope tension animation and puller leaning to reflect match momentum
- Match timer with sudden-death mode after 45 seconds
- Restart support with `R` after a win

## Setup

1. Install Python 3.10+
2. Install Pygame:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

## Controls

- `A` / `D`: alternate quickly to pull left
- `R`: reset the match after game over
- Close the window to quit

## Project structure

```text
.
├── game/
│   ├── game_engine.py
│   ├── player.py
│   └── rope.py
├── main.py
├── README.md
└── .gitignore
```
