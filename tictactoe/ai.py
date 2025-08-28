from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

from .engine import GameState, Player, TicTacToeEngine


class BaseAI:
	def choose_move(self, engine: TicTacToeEngine) -> int:
		raise NotImplementedError


class RandomAI(BaseAI):
	def choose_move(self, engine: TicTacToeEngine) -> int:
		moves = engine.legal_moves()
		if not moves:
			raise ValueError("No legal moves available")
		return random.choice(moves)


class MediumAI(BaseAI):
	"""Two-ply lookahead: win if possible, block if needed, else random."""

	def choose_move(self, engine: TicTacToeEngine) -> int:
		me = engine.current_player
		opp = Player.O if me == Player.X else Player.X
		moves = engine.legal_moves()
		board = engine.board
		# 1) Win immediately if possible
		for m in moves:
			if board.play(m, me).check_state() in (
				GameState.X_WINS,
				GameState.O_WINS,
			):
				return m
		# 2) Block opponent's immediate win
		for m in moves:
			if board.play(m, opp).check_state() in (
				GameState.X_WINS,
				GameState.O_WINS,
			):
				return m
		# 3) Heuristics: center, corners, sides
		priority = [4, 0, 2, 6, 8, 1, 3, 5, 7]
		for p in priority:
			if p in moves:
				return p
		return random.choice(moves)


class HardAI(BaseAI):
	def __init__(self, max_depth: Optional[int] = None) -> None:
		self.max_depth = max_depth

	def choose_move(self, engine: TicTacToeEngine) -> int:
		best_score = -math.inf
		best_move = None
		for move in engine.legal_moves():
			copy = engine.clone()
			state = copy.play(move)
			score = self._minimax(copy, is_maximizing=False, depth=1, alpha=-math.inf, beta=math.inf)
			if score > best_score:
				best_score = score
				best_move = move
		if best_move is None:
			raise ValueError("No legal moves available")
		return best_move

	def _score(self, state: GameState, current_player: Player, depth: int) -> int:
		if state == GameState.DRAW:
			return 0
		if state == GameState.X_WINS:
			return 10 - depth if current_player == Player.X else depth - 10
		if state == GameState.O_WINS:
			return 10 - depth if current_player == Player.O else depth - 10
		return 0

	def _minimax(self, engine: TicTacToeEngine, is_maximizing: bool, depth: int, alpha: float, beta: float) -> int:
		state = engine.state()
		if state != GameState.IN_PROGRESS:
			# Score from the perspective of the player who just moved (opposite of engine.current_player)
			previous_player = Player.O if engine.current_player == Player.X else Player.X
			return self._score(state, previous_player, depth)
		if self.max_depth is not None and depth >= self.max_depth:
			return 0

		if is_maximizing:
			value = -math.inf
			for move in engine.legal_moves():
				copy = engine.clone()
				copy.play(move)
				value = max(value, self._minimax(copy, False, depth + 1, alpha, beta))
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return int(value)
		else:
			value = math.inf
			for move in engine.legal_moves():
				copy = engine.clone()
				copy.play(move)
				value = min(value, self._minimax(copy, True, depth + 1, alpha, beta))
				beta = min(beta, value)
				if alpha >= beta:
					break
			return int(value)

