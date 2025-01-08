from tkinter import Tk, BOTH, Canvas, Button, Label, Frame, Entry, Checkbutton, IntVar

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")

        top_frame = Frame(self.__root)
        top_frame.pack(side="top", fill=BOTH)

        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(10, weight=1)
        
        genbtn = Button(top_frame, text="Generate", command=self.generate_maze)
        nrows_lbl = Label(top_frame, text="Rows")
        self.nrows_ent = Entry(top_frame, width=5)
        self.nrows_ent.insert(0, 20)
        ncols_lbl = Label(top_frame, text="Columns")
        self.ncols_ent = Entry(top_frame, width=5)
        self.ncols_ent.insert(0, 30)
        seed_lbl = Label(top_frame, text="Seed")
        self.seed_ent = Entry(top_frame, width=10)
        self.wronglbl = Label(top_frame, text="wrong steps")
        self.chk_var = IntVar()
        self.chkbtn = Checkbutton(top_frame, text="RNG", variable=self.chk_var)
        solvebtn = Button(top_frame, text="Solve", command=self.solve_maze)        
        
        genbtn.grid(row=0, column=1)
        nrows_lbl.grid(row=0, column=2)
        self.nrows_ent.grid(row=0, column=3)
        ncols_lbl.grid(row=0, column=5)
        self.ncols_ent.grid(row=0, column=6)
        seed_lbl.grid(row=0, column=7)
        self.seed_ent.grid(row=0, column=8)
        self.wronglbl.grid(row=0, column=12, columnspan=3, sticky="e")
        self.chkbtn.grid(row=0, column=19, sticky="e")
        solvebtn.grid(row=0, column=20, sticky="e")
        
        self.wronglbl.grid_remove()

        self.__canvas = Canvas(self.__root, bg="black", height=self.height, width=self.width)
        self.__running = False
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.maze = None

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line, color="black", width=2):
        line.draw(self.__canvas, color, width)

    def close(self):
        self.__running = False

    def get_bg_color(self):
        return self.__canvas.cget("bg")
    
    def generate_maze(self):
        from maze import Maze
        
        self.__canvas.delete("all")
        self.wronglbl.grid_remove()
        self.wronglbl.config(text="wrong steps")
        self.maze = Maze(10, 10, int(self.nrows_ent.get()), 
                         int(self.ncols_ent.get()), win = self, seed = self.seed_ent.get())

    def solve_maze(self):
        if self.maze is not None:
            self.wronglbl.grid()
            self.maze.solve(self.chk_var.get())

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

    def draw(self, canvas, color="black", width=2):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y,
                           fill=color, width=width)