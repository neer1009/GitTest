from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List, Optional, Sequence, Tuple


class Player(str, Enum):
	X = "X"
	O = "O"


class GameState(str, Enum):
	IN_PROGRESS = "in_progress"
	DRAW = "draw"
	X_WINS = "x_wins"
	O_WINS = "o_wins"


WIN_LINES: Tuple[Tuple[int, int, int], ...] = (
	(0, 1, 2),
	(3, 4, 5),
	(6, 7, 8),
	(0, 3, 6),
	(1, 4, 7),
	(2, 5, 8),
	(0, 4, 8),
	(2, 4, 6),
)


@dataclass
class Board:
	"""Immutable representation of a Tic-Tac-Toe board.

	Cells are indexed 0..8 in row-major order.
	"""
	cells: Tuple[Optional[Player], ...]

	def __post_init__(self) -> None:
		if len(self.cells) != 9:
			raise ValueError("Board must have exactly 9 cells")

	def play(self, index: int, player: Player) -> "Board":
		if self.cells[index] is not None:
			raise ValueError("Cell already occupied")
		new_cells = list(self.cells)
		new_cells[index] = player
		return Board(tuple(new_cells))

	def available_moves(self) -> List[int]:
		return [i for i, c in enumerate(self.cells) if c is None]

	def check_state(self) -> GameState:
		for a, b, c in WIN_LINES:
			line = (self.cells[a], self.cells[b], self.cells[c])
			if line == (Player.X, Player.X, Player.X):
				return GameState.X_WINS
			if line == (Player.O, Player.O, Player.O):
				return GameState.O_WINS
		if all(cell is not None for cell in self.cells):
			return GameState.DRAW
		return GameState.IN_PROGRESS

	def to_rows(self) -> List[List[Optional[Player]]]:
		return [list(self.cells[i : i + 3]) for i in range(0, 9, 3)]

	def __str__(self) -> str:
		rows = self.to_rows()
		def sym(val: Optional[Player]) -> str:
			return val if val is not None else " "
		return "\n".join([" | ".join(sym(c) for c in r) for r in rows])


class TicTacToeEngine:
	def __init__(self, starting_player: Player = Player.X) -> None:
		self.current_player: Player = starting_player
		self.board: Board = Board(tuple([None] * 9))

	def reset(self, starting_player: Player = Player.X) -> None:
		self.current_player = starting_player
		self.board = Board(tuple([None] * 9))

	def state(self) -> GameState:
		return self.board.check_state()

	def play(self, index: int) -> GameState:
		self.board = self.board.play(index, self.current_player)
		self.current_player = Player.O if self.current_player == Player.X else Player.X
		return self.board.check_state()

	def legal_moves(self) -> List[int]:
		return self.board.available_moves()

	def clone(self) -> "TicTacToeEngine":
		copy = TicTacToeEngine(self.current_player)
		copy.board = Board(tuple(self.board.cells))
		return copy

