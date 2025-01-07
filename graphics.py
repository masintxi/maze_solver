from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="brown", height=self.height, width=self.width)
        self.__running = False
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line, color="black"):
        line.draw(self.__canvas, color)

    def close(self):
        self.__running = False

    def get_bg_color(self):
        return self.__canvas.cget("bg")

        
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, *args):
        if len(args) == 2 and isinstance(args[0], Point) and isinstance(args[1], Point):
            self.p1 = args[0]
            self.p2 = args[1]
        elif len(args) == 4:
            self.p1 = Point(args[0], args[1])
            self.p2 = Point(args[2], args[3])
        else:
            raise ValueError("Can't build a line with that parameters")

    def draw(self, canvas, color="black"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y,
                           fill=color, width=2)




    
