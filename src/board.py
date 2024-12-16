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
        self.center_vec = pygame.Vector2(self.rect.center)

    def collidepoint(self, point: pygame.Vector2):
        return self.rect.collidepoint(point)

    def colliderect(self, rect: pygame.Vector2):
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
BOUNDING_BOX = pygame.Rect((0, 0), INITIAL_BOARD_SIZE)
ASPECT_RATIO = INITIAL_BOARD_W / INITIAL_BOARD_H

PACMAN_INITIAL_INDICES = (1, 1) # top-left space cell
PACMAN_INITIAL_POS = grid[1][1].center_vec

GHOST_INITIAL_POS = grid[-2][-2].center_vec
GHOST_INITIAL_INDICES = (len(grid) - 2, len(grid[0]) - 2) # bottom-right space cell

INITIAL_PELLETS = [
    cell.center_vec for cell in flat_grid
    if cell.is_space and cell.center_vec not in (PACMAN_INITIAL_POS, GHOST_INITIAL_POS)
]

def point_to_cell(point: pygame.Vector2) -> Cell:
    '''If `point` is strictly inside any cell, returns that cell.
    Otherwise, returns the cell with center closest to this point.'''
    if not BOUNDING_BOX.collidepoint(point):
        raise IndexError(f'Point ({point}) out of bounds')
    min_dist, nearest_cell = float('inf'), None
    for cell in flat_grid:
        if cell.collidepoint(point):
            return cell
        new_dist = cell.center_vec.distance_to(point)
        if new_dist < min_dist:
            min_dist, nearest_cell = new_dist, cell
    return nearest_cell

def check_visitable(r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and not grid[r][c].is_filled

def check_valid_bounding_box(rect: pygame.Rect) -> bool:
    for cell in flat_grid:
        if cell.colliderect(rect) and cell.is_filled:
            return False
    return rect.clip((0, 0), INITIAL_BOARD_SIZE) == rect

def reset():
    for cell in flat_grid:
        cell.on_path = False
