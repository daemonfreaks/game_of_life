"""
An unit test module of game_of_life.py
"""

import pytest
from game_of_life import LifeCell


def test_compute_next_state():
    cell = LifeCell()

    # born
    cell.compute_next_state(3)
    assert cell.next_alive  == True 
    # stay alive
    cell.is_alive = True
    cell.compute_next_state(2)
    assert cell.next_alive == True
    cell.compute_next_state(3)
    assert cell.next_alive == True
    # die
    cell.compute_next_state(1)
    assert cell.next_alive == False
    cell.compute_next_state(4)
    assert cell.next_alive == False
