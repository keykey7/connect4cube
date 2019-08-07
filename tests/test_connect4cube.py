from connect4cube.simple_board import RED, BLUE, EMPTY, Board


def test_alternating_players():
    game = Board()
    assert game.field(0, 0, 0) == EMPTY
    assert game.field(1, 1, 0) == EMPTY
    game.move(0, 0)
    assert game.field(0, 0, 0) == RED
    assert game.field(1, 1, 0) == EMPTY
    game.move(1, 1)
    assert game.field(0, 0, 0) == RED
    assert game.field(1, 1, 0) == BLUE
    assert game.round == 2


def test_win_backward():
    game = Board()
    for i in range(3):
        assert not game.move(i, 0)
        assert not game.move(i, 0)
    assert game.move(3, 0)


def test_win_forward():
    game = Board()
    for i in range(3, 0, -1):
        assert not game.move(i, 0)
        assert not game.move(i, 0)
    assert game.move(0, 0)
