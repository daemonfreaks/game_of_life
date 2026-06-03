"""
An unit test module of game_of_life.py
"""

from game_of_life import LifeCell


def test_compute_next_state():
    cell = LifeCell()

    # born
    cell.compute_next_state(3)
    assert cell.next_alive

    # stay alive
    cell.is_alive = True
    cell.compute_next_state(2)
    assert cell.next_alive
    cell.compute_next_state(3)
    assert cell.next_alive

    # die
    cell.compute_next_state(1)
    assert not cell.next_alive
    cell.compute_next_state(4)
    assert not cell.next_alive
