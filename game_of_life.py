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

    def __str__(self):
        if self.is_alive:
            return "0"
        return "."


class Universe:

    def __init__(self):
        self.rows = []

    def build_grid(self, count):
        """
        グリッドを構築する。

        :param count: グリッドの行数と列数
        :type count: int
        """
        for i in range(count):
            self.add_row()
            for _j in range(count):
                cell = LifeCell()
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

    def get_cells_string(self):
        v = []
        for row in self.rows:
            for cell in row:
                v.append(str(cell))
                v.append(" ")
            v.append("\n")
        return "".join(v)

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


def main(count):

    universe = Universe()
    universe.build_grid(count)

    stdscr = None
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.nodelay(True)
        prev_str = ""

        min_speed = 1.0
        max_speed = 0.1
        curr_speed = 0.5
        speed_step = 0.1

        counter = 0

        while True:

            curr_str = universe.get_cells_string()
            stdscr.addstr(0, 0, curr_str)
            stdscr.refresh()
            print(counter)

            c = stdscr.getch()
            # カーソル上を押すと早くなる
            if c == curses.KEY_UP and curr_speed > max_speed:
                curr_speed -= speed_step
            # カーソル下を押すと遅くなる
            elif c == curses.KEY_DOWN and curr_speed < min_speed:
                curr_speed += speed_step
            # press `q`
            elif c == 113:
                break
            # press `r`
            elif c == 114:
                cell = universe.get_cell_randomly()
                cell.is_alive = not cell.is_alive
            time.sleep(curr_speed)

            universe.step()
            counter += 1

            if curr_str == prev_str:
                break
            else:
                prev_str = curr_str

    finally:
        if stdscr is not None:
            curses.nocbreak()
            stdscr.nodelay(False)
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()


if __name__ == "__main__":
    print(main(20))
