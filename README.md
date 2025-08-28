## Tic-Tac-Toe (End-to-End)

A complete, end-to-end Tic-Tac-Toe game with:
- Core game engine (rules, win/draw detection)
- Computer opponents: random, medium, and hard (minimax with alpha-beta pruning)
- CLI entry point supporting human vs human, human vs AI, and AI vs AI demo
- Unit tests

### Quickstart

Requirements: Python 3.9+

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Run the CLI:

```bash
python -m tictactoe.cli --mode pvp
python -m tictactoe.cli --mode hvai --ai hard
python -m tictactoe.cli --mode aivai --ai1 medium --ai2 hard --games 3
```

Run tests:

```bash
pytest -q
```

### Project Layout

```
tictactoe/
  __init__.py
  engine.py
  ai.py
  cli.py
tests/
  test_engine.py
  test_ai.py
```

### Notes

- The hard AI uses minimax with alpha-beta pruning and optional depth limits.
- The board is 0-8 indexed internally; CLI renders a 3x3 grid.

