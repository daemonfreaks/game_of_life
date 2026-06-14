"""
An unit test module of game_of_life.py
"""

from game_of_life import LifeCell, Universe


def build_universe(pattern):
    """
    指定したパターンのUniverseを構築するヘルパー関数
    :param pattern: グリッドの状態を表す2次元リスト
    :type pattern: list of list of bool
    :return: 指定したパターンのUniverse
    :rtype: Universe
    """
    universe = Universe()
    for row in pattern:
        universe.add_row()
        for is_alive in row:
            life_cell = LifeCell()
            life_cell.is_alive = is_alive
            universe.add_cell(len(universe.rows) - 1, life_cell)
    return universe

def dump_universe(universe):
    """
    Universeの状態をリストで返すヘルパー関数
    :param universe: 状態を取得するUniverse
    :type universe: Universe
    :return: Universeの状態を表す2次元リスト
    :rtype: list of list of bool
    """
    return [[cell.is_alive for cell in row] for row in universe.rows]

def test_compute_next_state():
    """LifeCellのcompute_next_stateのテスト"""
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
        """周囲の生きているセルの数を数えるテスト"""
        patterns = [
            [True, True, True, False, False, False],
            [True, False, True, False, True, False],
            [True, True, True, False, False, False],
            [True, False, True, False, False, False],
            [False, True, True, False, False, False],
            [False, False, True, False, False, False],
        ]
        universe = build_universe(patterns)
        # 境界値
        assert universe.get_count_of_around_alive_cell(1, 1) == 8
        assert universe.get_count_of_around_alive_cell(4, 4) == 0
        # 角
        assert universe.get_count_of_around_alive_cell(0, 0) == 2
        # 端
        assert universe.get_count_of_around_alive_cell(5, 1) == 3

    def test_step_keeps_block_stable(self):
        """block静止パターン"""
        pattern = [
            [False, False, False, False],
            [False, True, True, False],
            [False, True, True, False],
            [False, False, False, False],
        ]

        universe = build_universe(pattern)
        universe.step()
        assert dump_universe(universe) == pattern

    def test_step_oscillates_blinker(self):
        """blinker振動パターン"""
        first_pattern = [
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, True, True, True, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
        ]
        second_pattern = [
            [False, False, False, False, False],
            [False, False, True, False, False],
            [False, False, True, False, False],
            [False, False, True, False, False],
            [False, False, False, False, False],
        ]

        universe = build_universe(first_pattern)

        universe.step()
        assert dump_universe(universe) == second_pattern

        universe.step()
        assert dump_universe(universe) == first_pattern
