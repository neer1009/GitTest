from tictactoe.engine import Board, GameState, Player, TicTacToeEngine


def test_empty_board_in_progress():
	engine = TicTacToeEngine()
	assert engine.state() == GameState.IN_PROGRESS
	assert set(engine.legal_moves()) == set(range(9))


def test_x_wins_row():
	engine = TicTacToeEngine()
	engine.play(0)
	engine.play(3)
	engine.play(1)
	engine.play(4)
	state = engine.play(2)
	assert state == GameState.X_WINS


def test_o_wins_diag():
	engine = TicTacToeEngine(starting_player=Player.O)
	engine.play(0)  # O
	engine.play(1)  # X
	engine.play(4)  # O
	engine.play(2)  # X
	state = engine.play(8)  # O
	assert state == GameState.O_WINS


def test_draw():
	engine = TicTacToeEngine()
	# Valid draw sequence (no winners): X0 O1 X2 O4 X3 O5 X7 O6 X8
	moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]
	state = GameState.IN_PROGRESS
	for m in moves:
		state = engine.play(m)
	assert state == GameState.DRAW

