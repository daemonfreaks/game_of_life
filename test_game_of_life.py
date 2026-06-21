"""
An unit test module of game_of_life.py
"""

from game_of_life import LifeCell, Universe


def dump_universe(universe: Universe) -> list[list[bool]]:
    """
    Universeの状態をリストで返すヘルパー関数
    :param universe: 状態を取得するUniverse
    :type universe: Universe
    :return: Universeの状態を表す2次元リスト
    :rtype: list of list of bool
    """
    snapshot = universe.get_snapshot()
    return [[cell for cell in row] for row in snapshot.rows]

def test_compute_next_state() -> None:
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

    def test_alive_neighbors(self) -> None:
        """周囲の生きているセルの数を数えるテスト"""
        patterns = [
            [True, True, True, False, False, False],
            [True, False, True, False, True, False],
            [True, True, True, False, False, False],
            [True, False, True, False, False, False],
            [False, True, True, False, False, False],
            [False, False, True, False, False, False],
        ]
        universe = Universe()
        universe.build_grid(patterns)
        # 境界値
        assert universe.count_alive_neighbors(1, 1) == 8
        assert universe.count_alive_neighbors(4, 4) == 0
        # 角
        assert universe.count_alive_neighbors(0, 0) == 2
        # 端
        assert universe.count_alive_neighbors(5, 1) == 3

    def test_step_keeps_block_stable(self) -> None:
        """block静止パターン"""
        pattern = [
            [False, False, False, False],
            [False, True, True, False],
            [False, True, True, False],
            [False, False, False, False],
        ]

        universe = Universe()
        universe.build_grid(pattern)
        universe.step()
        assert dump_universe(universe) == pattern

    def test_step_oscillates_blinker(self) -> None:
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

        universe = Universe()
        universe.build_grid(first_pattern)

        universe.step()
        assert dump_universe(universe) == second_pattern

        universe.step()
        assert dump_universe(universe) == first_pattern
