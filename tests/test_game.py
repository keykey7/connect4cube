import pytest

from connect4cube.game import *


def test_too_full():
    game = Game()
    game.move(0, 0)
    game.move(0, 0)
    game.move(0, 0)
    game.move(0, 0)
    game.move(0, 0)
    with pytest.raises(RuleViolation):
        game.move(0, 0)


def test_alternating_players():
    game = Game()
    assert game.field(0, 0, 0) == EMPTY
    assert game.field(1, 1, 0) == EMPTY
    game.move(0, 0)
    assert game.field(0, 0, 0) == RED
    assert game.field(1, 1, 0) == EMPTY
    game.move(1, 1)
    assert game.field(0, 0, 0) == RED
    assert game.field(1, 1, 0) == BLUE


def test_win():
    game = Game()
    for i in range(3):
        game.move(i, 0)
        game.move(i, 0)
        assert game.winner() == EMPTY
    game.move(3, 0)
    assert game.winner() == RED
