"""
A simple implementation of Conway's Game of Life.
"""

import curses
import random
import time


class LifeCell:

    def __init__(self):
        self.is_alive = False
        self.next_alive = False

    def apply_next_state(self):
        self.is_alive = self.next_alive

    def compute_next_state(self, alive_neighbors):
        if (not self.is_alive and alive_neighbors == 3) or \
            (self.is_alive and alive_neighbors in (2, 3)):
            self.next_alive = True
        else:
            self.next_alive = False


class Universe:

    def __init__(self, cell_class=LifeCell):
        self.rows = []
        self.cell_class = cell_class

    def build_grid(self, count):
        """
        グリッドを構築する。

        :param count: グリッドの行数と列数
        :type count: int
        """
        for i in range(count):
            self.add_row()
            for _j in range(count):
                cell = self.cell_class()
                cell.is_alive = bool(int(random.random() + 0.5))
                self.add_cell(i, cell)

    def add_row(self):
        self.rows.append([])

    def add_cell(self, row_no, cell):
        self.rows[row_no].append(cell)

    def get_count_of_around_alive_cell(self, y, x):
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

    def step(self):
        """世代を1ステップ進める。
        """
        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                count_neighbors = self.get_count_of_around_alive_cell(y, x)
                cell.compute_next_state(count_neighbors)

        for row in self.rows:
            for cell in row:
                cell.apply_next_state()

    def get_cell_randomly(self):
        row_index = random.choice(range(len(self.rows)))
        row = self.rows[row_index]
        cell_index = random.choice(range(len(row)))
        return row[cell_index]

    def _get_cell(self, y, x):
        if y < 0 or x < 0:
            return None
        try:
            return self.rows[y][x]
        except IndexError:
            return None


class BaseUI:
    """UIの基底クラス"""

    def __init__(self, universe):
        self.universe = universe

    def render(self):
        """Universeの状態を描画する。"""
        raise NotImplementedError

    def format_board(self):
        """Boardの状態を描画するための状態を生成する。"""
        raise NotImplementedError

    def finalize(self):
        """UIの終了処理を行う。"""
        raise NotImplementedError


class CursesUI(BaseUI):

    def __init__(self, universe, show_generation_counter=False):
        super().__init__(universe)
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)

        # 世代カウンター用
        self.show_generation_counter = show_generation_counter
        self.generation = 0

        # 進化状態の比較用
        self.prev_state = ""
        self.curr_state = ""

        # 描画スピードの調整用
        self.min_speed = 1.0
        self.max_speed = 0.1
        self.curr_speed = 0.5
        self.speed_step = 0.1

        # キー操作記憶用
        self.pressed_key = None

    def render(self):
        self.prev_state = self.curr_state
        self.curr_state = self.format_board()
        y = 0  # 描画開始位置
        if self.show_generation_counter:
            self.stdscr.addstr(0, 0, f"Generation: {self.generation}\n")
            self.generation += 1
            y = 1
        self.stdscr.addstr(y, 0, self.curr_state)
        self.stdscr.refresh()

    def poll_key(self):
        self.pressed_key = self.stdscr.getch()

    def format_board(self):
        v = []
        for row in self.universe.rows:
            for cell in row:
                v.append("0" if cell.is_alive else ".")
                v.append(" ")
            v.append("\n")
        return "".join(v)

    def finalize(self):
        curses.nocbreak()
        self.stdscr.nodelay(False)
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def quit_requested(self):
        return self.pressed_key == 113  # press `q`

    def is_stable(self):
        return self.curr_state == self.prev_state

    def handle_speed_key(self):
        # カーソル上を押すと早くなる
        if self.pressed_key == curses.KEY_UP and self.curr_speed > self.max_speed:
            self.curr_speed -= self.speed_step
        # カーソル下を押すと遅くなる
        elif self.pressed_key == curses.KEY_DOWN and self.curr_speed < self.min_speed:
            self.curr_speed += self.speed_step

    def wait_for_next_frame(self):
        time.sleep(self.curr_speed)

    def toggle_random_cell_if_requested(self):
        # ランダムにセルの状態を変える
        if self.pressed_key == 114:  # press `r`
            cell = self.universe.get_cell_randomly()
            cell.is_alive = not cell.is_alive


def main(count):

    universe = Universe()
    universe.build_grid(count)

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
    print(main(20))
