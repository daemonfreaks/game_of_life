# coding: utf-8

from __future__ import print_function
import curses
import random
import sys
import time


class Cell(object):

    def __init__(self, y, x, manager):
        self.y = y
        self.x = x
        self.is_alive = False
        self.next_alive = False
        self.manager = manager

    def live(self):
        self.is_alive = self.next_alive

    def next(self):
        count = self.manager.get_count_of_around_alive_cell(self.y, self.x)
        if not self.is_alive and count == 3:
            self.next_alive = True
        elif self.is_alive and 2 <= count <= 3:
            self.next_alive = True
        elif self.is_alive and count <= 1 or count >= 4:
            self.next_alive = False

    def __str__(self):
        if self.is_alive:
            return "0"
        return "."


class CellManager(object):

    def __init__(self):
        self.rows = []

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
                cell = self._get_cell(y+i, x+j)
                if cell is None:
                    continue
                if cell.is_alive:
                    alive_cell_count += 1
        return alive_cell_count

    def next(self):
        for row in self.rows:
            for cell in row:
                cell.next()

    def live(self):
        for row in self.rows:
            for cell in row:
                cell.live()

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
        except:
            return None


def main(cell_count):

    manager = CellManager()
    for i in range(cell_count):
        manager.add_row()
        for j in range(cell_count):
            cell = Cell(i, j, manager)
            cell.is_alive = bool(int(random.random() + 0.5))
            manager.add_cell(i, cell)

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.nodelay(1)
    prev_str = ""

    min_speed = 1.0
    max_speed = 0.1
    curr_speed = 0.5
    speed_step = 0.1

    counter = 0

    while True:

        curr_str = manager.get_cells_string()
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
            cell = manager.get_cell_randomly()
            cell.is_alive = not cell.is_alive
        time.sleep(curr_speed)

        manager.next()
        manager.live()

        counter += 1

        if curr_str == prev_str:
            break
        else:
            prev_str = curr_str

    curses.nocbreak()
    stdscr.nodelay(0)
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    print(main(20))
