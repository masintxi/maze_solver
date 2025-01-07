from graphics import Line, Point, Window
from cell import Cell
import time
import random

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, *args, win: Window = None, seed = None):
        self._win = win
        self._cells = []
        self.x1 = x1
        self.y1 = y1
        self.tries = 0
        self.num_rows = num_rows
        self.num_cols = num_cols
        if self._win is not None:
            self.cell_size_x = (self._win.width - 2 * self.x1) / self.num_cols
            self.cell_size_y = (self._win.height - self.y1 - self.x1) / self.num_rows
        elif len(args) == 2:
            self.cell_size_x = args[0]
            self.cell_size_y = args[1]
        else:
            raise ValueError("If no window, cell size (x and y) must be defined")
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [[Cell(self._win) for j in range(self.num_cols)] for i in range(self.num_rows)]
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        p1 = Point(self.x1 + j * self.cell_size_x, self.y1 + i * self.cell_size_y)
        p2 = Point(p1.x + self.cell_size_x, p1.y + self.cell_size_y)        
        self._cells[i][j].draw(p1, p2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bot_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            if j > 0 and self._cells[i][j - 1].visited == False: #left
                to_visit.append((i, j - 1))
            if j < self.num_cols - 1 and self._cells[i][j + 1].visited == False: #right
                to_visit.append((i, j + 1))
            if i > 0 and self._cells[i - 1][j].visited == False: #top
                to_visit.append((i - 1, j))
            if i < self.num_rows - 1 and self._cells[i + 1][j].visited == False: #bot
                to_visit.append((i + 1, j))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            rng = random.randrange(len(to_visit))
            next_cell = to_visit[rng]

            if next_cell[1] - j < 0: #next is at left
                self._cells[i][j].has_left_wall = False
                self._cells[i][j - 1].has_right_wall = False
            elif next_cell[1] - j > 0: #next is at right
                self._cells[i][j].has_right_wall = False
                self._cells[i][j + 1].has_left_wall = False
            if next_cell[0] - i < 0: #next is at top
                self._cells[i][j].has_top_wall = False
                self._cells[i - 1][j].has_bot_wall = False
            elif next_cell[0] - i > 0: #next is at bot
                self._cells[i][j].has_bot_wall = False
                self._cells[i + 1][j].has_top_wall = False

            self._break_walls_r(next_cell[0], next_cell[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_rows - 1 and j == self.num_cols -1:
            return True
        
        #right (i, j + 1)
        if j < self.num_cols - 1 and self._cells[i][j].has_right_wall == False and self._cells[i][j + 1].visited == False:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            self._cells[i][j + 1].draw_move(self._cells[i][j], undo = True)
            
        #top (i - 1, j)
        if i > 0 and self._cells[i][j].has_top_wall == False and self._cells[i - 1][j].visited == False:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            self._cells[i - 1][j].draw_move(self._cells[i][j], undo = True)
            
        #left (i, j - 1)
        if j > 0 and self._cells[i][j].has_left_wall == False and self._cells[i][j - 1].visited == False:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            self._cells[i][j - 1].draw_move(self._cells[i][j], undo = True)

        #bot (i + 1, j)
        if i < self.num_rows - 1 and self._cells[i][j].has_bot_wall == False and self._cells[i + 1][j].visited == False:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            self._cells[i + 1][j].draw_move(self._cells[i][j], undo = True)

        self.tries += 1
        return False