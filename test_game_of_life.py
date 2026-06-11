"""
An unit test module of game_of_life.py
"""

from game_of_life import LifeCell, Universe


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


class TestUniverse:

    def test_get_count_of_around_alive_cell(self):
        universe = Universe()
        universe.build_grid(3)

        for i in range(3):
            for j in range(3):
                universe.rows[i][j].is_alive = True
        assert universe.get_count_of_around_alive_cell(1, 1) == 8

        for i in range(3):
            for j in range(3):
                universe.rows[i][j].is_alive = False
        assert universe.get_count_of_around_alive_cell(1, 1) == 0

        universe.rows[0][0].is_alive = True
        universe.rows[1][0].is_alive = True
        universe.rows[2][2].is_alive = True
        assert universe.get_count_of_around_alive_cell(1, 1) == 3
