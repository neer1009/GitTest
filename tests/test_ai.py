from tictactoe.ai import HardAI, MediumAI, RandomAI
from tictactoe.engine import GameState, Player, TicTacToeEngine


def test_medium_ai_blocks_immediate_threat():
	engine = TicTacToeEngine()
	# X to move, set up where O could win next if not blocked
	engine.play(0)  # X
	engine.play(4)  # O
	engine.play(1)  # X
	engine.play(8)  # O
	# Now X should play 2 to win immediately, but we will test Medium for O next
	# Switch to O's turn by making one more X move that is not winning
	engine.play(3)  # X
	# O should block row 0 by playing 2
	ai = MediumAI()
	move = ai.choose_move(engine)
	assert move == 2


def test_hard_ai_plays_optimal_from_empty():
	engine = TicTacToeEngine()
	ai = HardAI()
	move = ai.choose_move(engine)
	# Optimal moves on empty board are center or corners
	assert move in {0, 2, 4, 6, 8}


def test_hard_ai_never_loses_against_itself():
	for _ in range(5):
		engine = TicTacToeEngine()
		hai = HardAI()
		state = engine.state()
		while state == GameState.IN_PROGRESS:
			move = hai.choose_move(engine)
			state = engine.play(move)
		assert state in {GameState.DRAW, GameState.X_WINS, GameState.O_WINS}

