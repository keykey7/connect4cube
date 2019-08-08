from connect4cube.game import Game, Winner
from connect4cube.player import RandomPlayer
from connect4cube.simple_board import RED, BLUE, EMPTY, Board


def test_alternating_players():
    board = Board()
    assert board.field(0, 0, 0) == EMPTY
    assert board.field(1, 1, 0) == EMPTY
    board.move(0, 0)
    assert board.field(0, 0, 0) == RED
    assert board.field(1, 1, 0) == EMPTY
    board.move(1, 1)
    assert board.field(0, 0, 0) == RED
    assert board.field(1, 1, 0) == BLUE
    assert board.round == 2


def test_win_backward():
    board = Board()
    for i in range(3):
        assert not board.move(i, 0)
        assert not board.move(i, 0)
    assert board.move(3, 0)


def test_win_forward():
    board = Board()
    for i in range(3, 0, -1):
        assert not board.move(i, 0)
        assert not board.move(i, 0)
    assert board.move(0, 0)


def test_random_game():
    game = Game(RandomPlayer(0), RandomPlayer(1))
    assert game.play() is Winner.BLUE
    game = Game(RandomPlayer(0), RandomPlayer(4))
    assert game.play() is Winner.RED


def test_draw():
    pass


def test_tostr():
    board = Board()
    board.move(0, 0)
    board.move(0, 0)
    board.move(0, 0)
    board.move(1, 0)
    board.move(3, 3)
    print("\n")
    print(board)

