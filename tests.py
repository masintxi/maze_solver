import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        ncols = 12
        nrows = 10
        m1 = Maze(0, 0, nrows, ncols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            nrows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            ncols,
        )
    
    def test_maze_create_cells_large(self):
        num_cols = 16
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )

    def test_cell_entrance(self):
        ncols = 12
        nrows = 10
        m1 = Maze(0, 0, nrows, ncols, 10, 10)
        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._cells[-1][-1].has_bot_wall,
            False,
        )

    def test_reset_visited(self):
        ncols = 20
        nrows = 15
        m1 = Maze(10, 10, nrows, ncols, 15, 15)
        for col in m1._cells:
            for cell in col:
                self.assertEqual(
                    cell.visited,
                    False,
                )
        self.assertEqual(
            m1._cells[0][0].visited,
            False
        )


if __name__ == "__main__":
    unittest.main()