from __future__ import annotations

import argparse
import sys
from typing import Optional

from .ai import HardAI, MediumAI, RandomAI
from .engine import GameState, Player, TicTacToeEngine


def print_board(engine: TicTacToeEngine) -> None:
	board = engine.board
	def v(i: int) -> str:
		cell = board.cells[i]
		return cell if cell is not None else str(i)
	rows = [[v(i) for i in range(r * 3, r * 3 + 3)] for r in range(3)]
	print("\n".join([" | ".join(r) for r in rows]))


def input_move(engine: TicTacToeEngine) -> int:
	while True:
		try:
			move = input(f"Player {engine.current_player}, enter move (0-8): ")
			idx = int(move)
			if idx not in engine.legal_moves():
				print("Illegal move. Try again.")
				continue
			return idx
		except (ValueError, KeyboardInterrupt):
			print("Invalid input. Use 0-8.")


def play_game(mode: str, ai1: str, ai2: str, starting: str, games: int, depth: Optional[int]) -> int:
	def make_ai(name: str) -> RandomAI | MediumAI | HardAI:
		if name == "random":
			return RandomAI()
		if name == "medium":
			return MediumAI()
		if name == "hard":
			return HardAI(max_depth=depth)
		raise ValueError("Unknown AI: " + name)

	def result_to_char(state: GameState) -> str:
		return "X" if state == GameState.X_WINS else ("O" if state == GameState.O_WINS else "D")

	start_player = Player.X if starting.lower() == "x" else Player.O
	engine = TicTacToeEngine(starting_player=start_player)
	ai_x = make_ai(ai1)
	ai_o = make_ai(ai2)

	stats = {"X": 0, "O": 0, "D": 0}
	for g in range(games):
		engine.reset(start_player if g == 0 else (Player.X if g % 2 == 0 else Player.O))
		state = engine.state()
		while state == GameState.IN_PROGRESS:
			print_board(engine)
			if mode == "pvp":
				move = input_move(engine)
			elif mode == "hvai":
				if engine.current_player == Player.X:
					move = input_move(engine)
				else:
					move = ai_o.choose_move(engine)
			else:  # aivai or hvai (both moves by ai if aivai)
				if engine.current_player == Player.X:
					move = ai_x.choose_move(engine)
				else:
					move = ai_o.choose_move(engine)
			state = engine.play(move)
			print()
		print_board(engine)
		res = result_to_char(state)
		stats[res] += 1
		print(f"Result: {res}\n")

	print(f"Totals after {games} game(s): X={stats['X']} O={stats['O']} D={stats['D']}")
	return 0


def main(argv: Optional[list[str]] = None) -> int:
	parser = argparse.ArgumentParser(description="Tic-Tac-Toe CLI")
	parser.add_argument("--mode", choices=["pvp", "hvai", "aivai"], default="pvp")
	parser.add_argument("--ai", choices=["random", "medium", "hard"], default="hard")
	parser.add_argument("--ai1", choices=["random", "medium", "hard"], default="hard")
	parser.add_argument("--ai2", choices=["random", "medium", "hard"], default="hard")
	parser.add_argument("--start", choices=["x", "o"], default="x")
	parser.add_argument("--games", type=int, default=1)
	parser.add_argument("--depth", type=int, default=None)
	args = parser.parse_args(argv)

	mode = args.mode
	if mode == "hvai":
		return play_game(mode, args.ai, args.ai, args.start, args.games, args.depth)
	if mode == "aivai":
		return play_game(mode, args.ai1, args.ai2, args.start, args.games, args.depth)
	return play_game(mode, args.ai, args.ai, args.start, args.games, args.depth)


if __name__ == "__main__":
	sys.exit(main())

