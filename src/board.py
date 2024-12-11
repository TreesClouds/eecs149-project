WALL_THICKNESS_INCHES = 0.125
CORRIDOR_DIST_INCHES = 5.78125
INITIAL_PX_PER_INCH = 20

INITIAL_WALL_THICKNESS = WALL_THICKNESS_INCHES * INITIAL_PX_PER_INCH
INITIAL_CORRIDOR_DIST = CORRIDOR_DIST_INCHES * INITIAL_PX_PER_INCH

class Cell:
    def __init__(self, is_filled: bool, rect: tuple[float, float, float, float]):
        self.is_filled = is_filled
        self.rect = rect
    
    def resize(self, scale_factor: float):
        self.rect = (
            self.rect[0] * scale_factor, self.rect[1] * scale_factor,
            self.rect[2] * scale_factor, self.rect[3] * scale_factor
        )
        
BOARD_PATH = './assets/board.txt'
grid: list[list[Cell]] = []
initial_board_w, initial_board_h = 0, 0 # Initial dimensions of entire board, in px
with open(BOARD_PATH, 'r') as f:
    rows = f.readlines()
    y = 0
    for r, row in enumerate(rows):
        new_grid_row = []
        x = 0
        h = (INITIAL_WALL_THICKNESS, INITIAL_CORRIDOR_DIST)[r % 2]
        initial_board_h += h
        for c, char in enumerate(row.strip()):
            w = (INITIAL_WALL_THICKNESS, INITIAL_CORRIDOR_DIST)[c % 2]
            if r == 0:
                initial_board_w += w
            new_grid_row.append(Cell(char != ' ', (x, y, w, h)))
            x += w
        grid.append(new_grid_row)
        y += h
INITIAL_BOARD_SIZE = (initial_board_w, initial_board_h)