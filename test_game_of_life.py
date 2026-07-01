"""
An unit test module of game_of_life.py
"""

import unittest.mock

from pytest_mock import MockerFixture

from game_of_life import BaseUI, Controller, LifeCell, Universe, build_random_pattern


def dump_universe(universe: Universe) -> list[list[bool]]:
    """
    Universeの状態をリストで返すヘルパー関数
    :param universe: 状態を取得するUniverse
    :type universe: Universe
    :return: Universeの状態を表す2次元リスト
    :rtype: list of list of bool
    """
    snapshot = universe.get_snapshot()
    return [list(row) for row in snapshot.rows]

def test_build_random_pattern() -> None:
    """ランダムパターンの生成テスト"""
    for i in range(2, 10):
        pattern: list[list[bool]] = build_random_pattern(i)
        assert len(pattern) == i
        assert all(len(row) == i for row in pattern)


class TestLifeCell:
    """LifeCellのテストクラス"""

    def test_compute_next_state(self) -> None:
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
    """Universeのテストクラス"""

    def test_rows(self) -> None:
        """rowsプロパティのテスト"""
        patterns = [
            [True, False, True],
            [False, True, False],
            [True, True, True],
        ]
        universe = Universe()
        universe.build_grid(patterns)
        snapshot = universe.get_snapshot()
        assert snapshot.rows == tuple(tuple(row) for row in patterns)

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

    def test_cell_control(self) -> None:
        """セルの制御テスト"""
        pattern = [
            [False, False, False, False],
            [False, True, True, False],
            [False, True, True, False],
            [False, False, False, False],
        ]

        universe = Universe()
        universe.build_grid(pattern)

        assert universe.get_row_count() == len(pattern)
        assert all(universe.get_column_count(i) == len(
            pattern[i]) for i in range(len(pattern)))

        for i, row in enumerate(pattern):
            for j, cell_state in enumerate(row):
                universe.toggle_cell(i, j)
                snapshot = universe.get_snapshot()
                assert snapshot.rows[i][j] == (not cell_state)


class TestController:
    """Controllerのテストクラス"""

    def test_quit_requested(self) -> None:
        """終了要求のテスト"""
        ui = BaseUI()
        universe = Universe()
        controller = Controller(universe, ui)
        assert not controller.quit_requested()
        ui.event.quit = True
        assert controller.quit_requested()

    def test_is_stable(self) -> None:
        """安定状態の判定テスト"""
        pattern = [
            [True, False, False, True],
            [False, True, True, False],
            [False, True, True, False],
            [True, False, False, True],
        ]

        universe = Universe()
        universe.build_grid(pattern)
        controller = Controller(universe, BaseUI())
        assert controller.is_stable()
        controller.prev_state = universe.get_snapshot()
        controller.curr_state = universe.get_snapshot()
        assert controller.is_stable()
        universe.step()
        controller.curr_state = universe.get_snapshot()
        assert not controller.is_stable()

    def test_handle_speed_key(self) -> None:
        """速度変更キーの処理テスト"""
        ui = BaseUI()
        universe = Universe()
        controller = Controller(universe, ui)

        for _ in range(100):
            ui.event.speed_up = True
            ui.event.speed_down = False
            controller.handle_speed_key()
            assert controller.curr_time_delay >= controller.fastest_time_delay

        for _ in range(100):
            ui.event.speed_up = False
            ui.event.speed_down = True
            controller.handle_speed_key()
            assert controller.curr_time_delay <= controller.slowest_time_delay

    def test_toggle_random_cell_if_requested(self) -> None:
        """ランダムセルの切り替えテスト"""
        ui = BaseUI()

        # グリッド生成前なら何もしない
        universe = Universe()
        controller = Controller(universe, ui)
        ui.event.toggle_random_cell = True
        snapshot = universe.get_snapshot()
        controller.toggle_random_cell_if_requested()
        assert universe.get_snapshot() == snapshot
        universe.add_row()
        snapshot = universe.get_snapshot()
        controller.toggle_random_cell_if_requested()
        assert universe.get_snapshot() == snapshot

        # グリッド生成（前段で空行を追加しているため、ここからは新しいUniverseを使う）
        universe = Universe()
        controller = Controller(universe, ui)
        pattern = build_random_pattern(5)
        universe.build_grid(pattern)

        # ランダムセルの切り替えが要求されていない場合
        snapshot = universe.get_snapshot()
        ui.event.toggle_random_cell = False
        controller.toggle_random_cell_if_requested()
        assert universe.get_snapshot() == snapshot

        # ランダムセルの切り替えが要求されている場合
        ui.event.toggle_random_cell = True
        controller.toggle_random_cell_if_requested()
        assert universe.get_snapshot() != snapshot

    def test_run_for_is_stable(self, mocker: MockerFixture) -> None:
        """
        Controllerのrunメソッドのテスト

        - 進化の停滞で止まること
        """
        ui = BaseUI()
        ui_poll_key_mock: unittest.mock.MagicMock = mocker.patch.object(ui, "poll_key")
        ui_render_mock: unittest.mock.MagicMock = mocker.patch.object(ui, "render")

        universe = Universe()
        pattern = [
            [False, False, False, False],
            [False, True, True, False],
            [False, True, True, False],
            [False, False, False, False],
        ] # ブロックなので安定状態になる
        universe.build_grid(pattern)

        controller = Controller(universe, ui)
        wait_for_next_frame_mock: unittest.mock.MagicMock = mocker.patch.object(
            controller, "wait_for_next_frame")
        controller.run()

        assert ui_poll_key_mock.call_count == 2
        assert ui_render_mock.call_count == 2
        assert wait_for_next_frame_mock.call_count == 1
        assert controller.generation == 1

    def test_run_for_quit_requested(self, mocker: MockerFixture) -> None:
        """
        Controllerのrunメソッドのテスト

        - 終了要求で止まること
        """
        ui = BaseUI()
        ui_poll_key_mock: unittest.mock.MagicMock = mocker.patch.object(ui, "poll_key")
        ui_render_mock: unittest.mock.MagicMock = mocker.patch.object(ui, "render")

        universe = Universe()
        pattern = [
            [False, False, False, False],
            [False, False, True, False],
            [False, True, False, False],
            [False, False, False, False],
        ]
        universe.build_grid(pattern)

        controller = Controller(universe, ui)
        wait_for_next_frame_mock: unittest.mock.MagicMock = mocker.patch.object(
            controller, "wait_for_next_frame")
        ui.event.quit = True
        controller.run()

        assert ui_poll_key_mock.call_count == 1
        assert ui_render_mock.call_count == 1
        assert wait_for_next_frame_mock.call_count == 0
        assert controller.generation == 0
