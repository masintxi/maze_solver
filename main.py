from graphics import Window, Point, Line
from cell import Cell
from maze import Maze


def main():
    win = Window(800, 600)

    maze1 = Maze(10, 40, 20, 30, win = win)

    if maze1.solve():
        print(f"Solved in {maze1.tries} tries")
    else:
        print(f"Critical miss! {maze1.tries} tries weren't enough to solve the maze")
    
    win.wait_for_close()

main()