WALL_THICKNESS_INCHES = 0.125
CORRIDOR_DIST_INCHES = 5.78125
INITIAL_PX_PER_INCH = 20

INITIAL_WALL_THICKNESS = WALL_THICKNESS_INCHES * INITIAL_PX_PER_INCH
INITIAL_CORRIDOR_DIST = CORRIDOR_DIST_INCHES * INITIAL_PX_PER_INCH

class Cell:
    def __init__(self, is_filled: bool, rect: tuple[float, float, float, float]):
        self.is_filled = is_filled
        self.rect = rect
        
BOARD_PATH = './assets/board.txt'
grid: list[list[Cell]] = []
board_w, board_h = 0, 0 # Initial dimensions of entire board, in px
with open(BOARD_PATH, 'r') as f:
    rows = f.readlines()
    y = 0
    for r, row in enumerate(rows):
        new_grid_row = []
        x = 0
        h = (INITIAL_WALL_THICKNESS, INITIAL_CORRIDOR_DIST)[r % 2]
        board_h += h
        for c, char in enumerate(row.strip()):
            w = (INITIAL_WALL_THICKNESS, INITIAL_CORRIDOR_DIST)[c % 2]
            if r == 0:
                board_w += w
            new_grid_row.append(Cell(char != ' ', (x, y, w, h)))
            x += w
        grid.append(new_grid_row)
        y += h
INITIAL_BOARD_W, INITIAL_BOARD_H = board_w, board_h
INITIAL_BOARD_SIZE = (INITIAL_BOARD_W, INITIAL_BOARD_H)
ASPECT_RATIO = INITIAL_BOARD_W / INITIAL_BOARD_H
