import pygame

WALL_THICKNESS_INCHES = 0.125 # 2 to make the borders more obvious
CORRIDOR_DIST_INCHES = 5.78125
INITIAL_PX_PER_INCH = 20

INITIAL_WALL_THICKNESS = WALL_THICKNESS_INCHES * INITIAL_PX_PER_INCH
INITIAL_CORRIDOR_DIST = CORRIDOR_DIST_INCHES * INITIAL_PX_PER_INCH

class Cell:
    def __init__(
            self,
            is_filled: bool, is_space: bool,
            indices: tuple[int, int],
            left: float, top: float, width: float, height: float):
        self.is_filled = is_filled
        self.is_space = is_space
        self.indices = indices
        self.rect = pygame.Rect(left, top, width, height)
        self.on_path = False

    def collidepoint(self, point: pygame.Vector2):
        return self.rect.collidepoint(point)

    def colliderect(self, rect: pygame.Rect):
        return self.rect.colliderect(rect)
        
BOARD_PATH = './assets/board.txt'
grid: list[list[Cell]] = []
flat_grid: list[Cell] = []
board_w, board_h = 0, 0 # Initial dimensions of entire board, in px
with open(BOARD_PATH, 'r') as f:
    rows = f.readlines()
    y = 0
    for r, row in enumerate(rows):
        new_grid_row = []
        x = 0
        is_big_h = r % 2
        h = (INITIAL_WALL_THICKNESS, INITIAL_CORRIDOR_DIST)[is_big_h]
        board_h += h
        for c, char in enumerate(row.strip()):
            is_big_w = c % 2
            w = (INITIAL_WALL_THICKNESS, INITIAL_CORRIDOR_DIST)[is_big_w]
            if r == 0:
                board_w += w
            new_cell = Cell(
                char != ' ', is_big_h and is_big_w,
                (r, c),
                x, y, w, h
            )
            new_grid_row.append(new_cell)
            flat_grid.append(new_cell)
            x += w
        grid.append(new_grid_row)
        y += h
INITIAL_BOARD_W, INITIAL_BOARD_H = board_w, board_h
INITIAL_BOARD_SIZE = (INITIAL_BOARD_W, INITIAL_BOARD_H)
ASPECT_RATIO = INITIAL_BOARD_W / INITIAL_BOARD_H

INITIAL_PELLETS = [cell.rect.center for cell in flat_grid if cell.is_space]

def point_pixels_to_cell(point: pygame.Vector2) -> Cell:
    for cell in flat_grid:
        if cell.collidepoint(point):
            return cell
    raise IndexError(f'Point ({point}) out of bounds')

def bounding_box_to_cell(rect: pygame.Rect) -> Cell:
    for cell in flat_grid:
        if cell.colliderect(rect):
            return cell
    raise IndexError(f'Bounding box ({rect}) out of bounds')

def check_valid_bounding_box(rect: pygame.Rect) -> bool:
    for cell in flat_grid:
        if cell.colliderect(rect) and cell.is_filled:
            return False
    return rect.clip((0, 0), INITIAL_BOARD_SIZE) == rect

def point_fraction_to_cell(x_fraction, y_fraction) -> Cell:
    return point_pixels_to_cell(
        (x_fraction * INITIAL_BOARD_W, y_fraction * INITIAL_BOARD_H))
