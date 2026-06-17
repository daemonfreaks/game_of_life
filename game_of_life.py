"""
A simple implementation of Conway's Game of Life.
"""

import argparse
import curses
import random
import time
from dataclasses import dataclass


def build_random_pattern(count: int) -> list[list[bool]]:
    """
    ランダムなパターンを生成する。
    :param count: パターンの行数と列数
    :type count: int
    :return: ランダムなパターン
    :rtype: list[list[bool]]
    """
    return [[bool(int(random.random() + 0.5)) for _ in range(count)]
            for _ in range(count)]


@dataclass
class LifeCell:
    """セルのクラス"""
    is_alive: bool = False
    next_alive: bool = False

    def apply_next_state(self) -> None:
        """次の世代の状態を現在の状態に適用する。"""
        self.is_alive = self.next_alive

    def compute_next_state(self, alive_neighbors: int) -> None:
        """
        次の世代の状態を計算する。
         - 周囲の生きているセルが3つであれば、死んでいるセルは生まれる。
         - 周囲の生きているセルが2つか3つであれば生きているセルは生き続ける。
         - それ以外の場合は、セルは死ぬ。

        :param alive_neighbors: 周囲の生きているセルの数
        :type alive_neighbors: int
        """
        if (not self.is_alive and alive_neighbors == 3) or \
            (self.is_alive and alive_neighbors in (2, 3)):
            self.next_alive = True
        else:
            self.next_alive = False


class Universe:
    """Universeのクラス"""

    def __init__(self, cell_class: type = LifeCell) -> None:
        """
        Universeを初期化する。

        :param cell_class: セルのクラス
        :type cell_class: type
        """
        self.rows: list[list[LifeCell]] = []
        self.cell_class: type = cell_class

    def build_grid(self, pattern: list[list[bool]]) -> None:
        """
        グリッドを構築する。

        :param pattern: グリッドのパターン
        :type pattern: list[list[bool]]
        """
        for row in pattern:
            self.add_row()
            for is_alive in row:
                life_cell = self.cell_class()
                life_cell.is_alive = is_alive
                self.add_cell(len(self.rows) - 1, life_cell)

    def add_row(self) -> None:
        """行を追加する。"""
        self.rows.append([])

    def add_cell(self, row_no: int, cell: LifeCell) -> None:
        """行にセルを追加する。

        :param row_no: 行番号
        :type row_no: int
        :param cell: 追加するセル
        :type cell: LifeCell
        """
        self.rows[row_no].append(cell)

    def count_alive_neighbors(self, y: int, x: int) -> int:
        """周囲の生きているセルの数を数える。

        :param y: セルの行番号
        :type y: int
        :param x: セルの列番号
        :type x: int
        :return: 周囲の生きているセルの数
        :rtype: int
        """
        alive_cell_count = 0
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    continue
                cell = self._get_cell(y + i, x + j)
                if cell is None:
                    continue
                if cell.is_alive:
                    alive_cell_count += 1
        return alive_cell_count

    def step(self) -> None:
        """世代を1ステップ進める。"""
        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                count_neighbors = self.count_alive_neighbors(y, x)
                cell.compute_next_state(count_neighbors)

        for row in self.rows:
            for cell in row:
                cell.apply_next_state()

    def get_cell_randomly(self) -> LifeCell:
        """
        ランダムにセルを取得する。

        :return: ランダムに取得したセル
        :rtype: LifeCell
        """
        row_index = random.choice(range(len(self.rows)))
        row = self.rows[row_index]
        cell_index = random.choice(range(len(row)))
        return row[cell_index]

    def _get_cell(self, y: int, x: int) -> LifeCell | None:
        """
        セルを取得する。範囲外の場合はNoneを返す。

        :param y: セルの行番号
        :type y: int
        :param x: セルの列番号
        :type x: int
        :return: セル
        :rtype: LifeCell or None
        """
        if y < 0 or x < 0:
            return None
        try:
            return self.rows[y][x]
        except IndexError:
            return None


class BaseUI:
    """UIの基底クラス"""

    def __init__(self, universe: Universe) -> None:
        """UIを初期化する。"""
        self.universe = universe

    def render(self) -> None:
        """Universeの状態を描画する。"""
        raise NotImplementedError

    def format_board(self) -> str:
        """Boardの状態を描画するための状態を生成する。"""
        raise NotImplementedError

    def finalize(self) -> None:
        """UIの終了処理を行う。"""
        raise NotImplementedError


class CursesUI(BaseUI):
    """cursesを使用したUIクラス"""

    def __init__(self, universe: Universe,
                 show_generation_counter: bool = False) -> None:
        """
        CursesUIを初期化する。

        :param universe: 描画するUniverse
        :type universe: Universe
        :param show_generation_counter: 世代カウンターを表示するかどうか
        :type show_generation_counter: bool
        """
        super().__init__(universe)
        self.stdscr: curses.window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)

        # 世代カウンター用
        self.show_generation_counter: bool = show_generation_counter
        self.generation: int = 0

        # 進化状態の比較用
        self.prev_state: str = ""
        self.curr_state: str = ""

        # 描画スピードの調整用
        self.min_speed: float = 1.0
        self.max_speed: float = 0.1
        self.curr_speed: float = 0.5
        self.speed_step: float = 0.1

        # キー操作記憶用
        self.pressed_key: int | None = None

    def render(self) -> None:
        """
        Universeの状態を描画する。
        描画前に、現在の状態をprev_stateに保存し、描画後
         - prev_stateとcurr_stateが同じであれば、進化が停滞していると判断する。
         - show_generation_counterがTrueであれば、世代カウンターを表示する。
        """
        self.prev_state = self.curr_state
        self.curr_state = self.format_board()
        y = 0  # 描画開始位置
        if self.show_generation_counter:
            self.stdscr.addstr(0, 0, f"Generation: {self.generation}\n")
            self.generation += 1
            y = 1
        self.stdscr.addstr(y, 0, self.curr_state)
        self.stdscr.refresh()

    def poll_key(self) -> None:
        """キー入力をポーリングする。"""
        self.pressed_key = self.stdscr.getch()

    def format_board(self) -> str:
        """
        Universeの状態を描画するための文字列を生成する。
        生きているセルは"0"、死んでいるセルは"."で表現する。

        :return: 描画するための文字列
        :rtype: str
        """
        v: list[str] = []
        for row in self.universe.rows:
            for cell in row:
                v.append("0" if cell.is_alive else ".")
                v.append(" ")
            v.append("\n")
        return "".join(v)

    def finalize(self) -> None:
        """
        UIの終了処理を行う。cursesの設定を元に戻す。
         - cbreakモードを解除する。
         - nodelayモードを解除する。
         - キーパッドモードを解除する。
         - echoモードを有効にする。
         - cursesを終了する。
        """
        curses.nocbreak()
        self.stdscr.nodelay(False)
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def quit_requested(self) -> bool:
        """
        終了要求があるかどうかを判定する。`q`が押されている場合は終了要求があると判断する。
         - `q`が押されている場合はTrueを返す。
         - それ以外の場合はFalseを返す。

        :return: 終了要求があるかどうか
        :rtype: bool
        """
        return self.pressed_key == 113  # press `q`

    def is_stable(self) -> bool:
        """
        進化が停滞しているかどうかを判定する。prev_stateとcurr_stateが同じであれば、進化が停滞していると判断する。
         - prev_stateとcurr_stateが同じであればTrueを返す。
         - それ以外の場合はFalseを返す。

        :return: 進化が停滞しているかどうか
        :rtype: bool
        """
        return self.curr_state == self.prev_state

    def handle_speed_key(self) -> None:
        """
        描画するスピードを調整する。カーソル上を押すと早くなり、カーソル下を押すと遅くなる。
         - カーソル上が押されている場合はcurr_speedをspeed_stepだけ減らす。
           ただし、curr_speedがmin_speedより小さくならないようにする。
         - カーソル下が押されている場合はcurr_speedをspeed_stepだけ増やす。
           ただし、curr_speedがmax_speedより大きくならないようにする。
        """
        # カーソル上を押すと早くなる
        if self.pressed_key == curses.KEY_UP and self.curr_speed > self.max_speed:
            self.curr_speed -= self.speed_step
        # カーソル下を押すと遅くなる
        elif self.pressed_key == curses.KEY_DOWN and self.curr_speed < self.min_speed:
            self.curr_speed += self.speed_step

    def wait_for_next_frame(self) -> None:
        """次のフレームまで待機する。curr_speed秒だけ待機する。"""
        time.sleep(self.curr_speed)

    def toggle_random_cell_if_requested(self) -> None:
        """
        ランダムにセルの状態を変える。
        `r`が押されている場合は、ランダムにセルを取得し、そのセルの状態を反転させる。
        """
        if self.pressed_key == 114:  # press `r`
            cell = self.universe.get_cell_randomly()
            cell.is_alive = not cell.is_alive


def main(count: int) -> None:
    """ゲームを実行する。"""

    pattern = build_random_pattern(count)
    universe = Universe()
    universe.build_grid(pattern)

    curses_ui = None
    try:
        curses_ui = CursesUI(universe, show_generation_counter=True)
        while True:

            curses_ui.render()
            curses_ui.poll_key()

            # 描画するスピードを調整する
            curses_ui.handle_speed_key()

            # ランダムにセルの状態を変える
            curses_ui.toggle_random_cell_if_requested()

            # 停止要求があれば終了
            if curses_ui.quit_requested():
                break

            # 進化が停滞している場合は終了
            if curses_ui.is_stable():
                break

            curses_ui.wait_for_next_frame()
            universe.step()

    finally:
        if curses_ui is not None:
            curses_ui.finalize()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    help_text: str = "Specify the number of cells in one row/column"
    parser.add_argument("cell_count", help=help_text, type=int)
    args = parser.parse_args()
    main(args.cell_count)
