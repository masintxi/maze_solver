from graphics import Line, Point, Window

class Cell():

    def __init__(self, win: Window = None, **kwargs: bool):
        """Args:
            win: The window object to draw on
            **kwargs: Wall configurations where keys can be:
                - wleft (bool): Whether left wall exists
                - wright (bool): Whether right wall exists
                - wtop (bool): Whether top wall exists
                - wbot (bool): Whether bottom wall exists
        """
        self._win = win
        self.cell_color = "grey"
        self.has_left_wall = kwargs.get("wleft", True)
        self.has_right_wall = kwargs.get("wright", True)
        self.has_top_wall = kwargs.get("wtop", True)
        self.has_bot_wall = kwargs.get("wbot", True)
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.visited = False
    
    def draw(self, *args):
        if len(args) == 2 and isinstance(args[0], Point) and isinstance(args[1], Point):
            self.x1 = args[0].x
            self.y1 = args[0].y
            self.x2 = args[1].x
            self.y2 = args[1].y
        elif len(args) == 4:
            self.x1 = args[0]
            self.y1 = args[1]
            self.x2 = args[2]
            self.y2 = args[3]
        else:
            raise ValueError("Cell requires either 2 Points or 4 coordinates")
        
        self._win.draw_line(Line(self.x1, self.y1, self.x1, self.y2), self._wall_color(self.has_left_wall))        
        self._win.draw_line(Line(self.x2, self.y1, self.x2, self.y2), self._wall_color(self.has_right_wall))
        self._win.draw_line(Line(self.x1, self.y1, self.x2, self.y1), self._wall_color(self.has_top_wall))
        self._win.draw_line(Line(self.x1, self.y2, self.x2, self.y2), self._wall_color(self.has_bot_wall))

    def _wall_color(self, wall):
        if wall:
            return self.cell_color
        return self._win.get_bg_color()

    def draw_move(self, to_cell, undo=False):
        start = Point(self.x1 + abs(self.x2 - self.x1)//2, self.y1 + abs(self.y2 - self.y1)//2)
        end = Point(to_cell.x1 + abs(to_cell.x2 - to_cell.x1)//2, to_cell.y1 + abs(to_cell.y2 - to_cell.y1)//2)
        
        fil_col = "yellow"
        if undo:
            fil_col = "blue"            
        
        self._win.draw_line(Line(start, end), fil_col)