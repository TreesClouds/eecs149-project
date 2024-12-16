from cli import args
import pygame
import board
from enum import Enum

pygame.init()

class State(Enum):
    PAUSED = 'PAUSED'
    RUNNING = 'RUNNING'
    WON = 'YOU WON!'
    LOST = 'GAME OVER'

FONT_FAMILY_PATH = './assets/PressStart2P-Regular.ttf'
FONT_SIZE = 20
FONT = pygame.font.Font(FONT_FAMILY_PATH, FONT_SIZE)

# Prefer low speeds but high frame rates for high collision detection precision,
# which minimizes the risk of clipping through walls
PACMAN_INITIAL_POS = board.grid[1][1].center_vec # top-left empty cell
PACMAN_SPEED = 1
PACMAN_COLOR = 'yellow'

GHOST_INITIAL_POS = board.grid[-2][-2].center_vec # bottom-right empty cell
GHOST_SPEED = 0.9 # In px/frame
GHOST_COLOR = 'pink'

WALL_COLOR = 'cyan'

INITIAL_DIR = pygame.Vector2(1, 0)

clock = pygame.time.Clock()
MAX_FRAME_RATE = 120

ROBOT_DIAMETER_INCHES = 3.875
ROBOT_DIAMETER = ROBOT_DIAMETER_INCHES * board.INITIAL_PX_PER_INCH
ROBOT_RADIUS = ROBOT_DIAMETER / 2

ROBOT_SAFE_DIAMETER = ROBOT_DIAMETER * 1.2
ROBOT_SAFE_RADIUS = ROBOT_SAFE_DIAMETER / 2
ROBOT_SAFE_WIDTH_HEIGHT = pygame.Vector2(ROBOT_SAFE_DIAMETER, ROBOT_SAFE_DIAMETER)

PELLET_RADIUS = 10.0

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

DIR_TO_LETTER = {
    (-1,  0): 'l',
    ( 1,  0): 'r',
    ( 0, -1): 'u',
    ( 0,  1): 'd',
    ( 0,  0): 'i'
}

screen = pygame.display.set_mode(board.INITIAL_BOARD_SIZE, pygame.RESIZABLE) # Screen user actually sees
unit_screen = screen.copy() # Internal fixed-size screen that makes math simpler

def draw_centered_text(msg: str, center: tuple[int, int], color='white'):
    text = FONT.render(msg, True, color)
    text_rect = text.get_rect(center=center)
    unit_screen.blit(text, text_rect)

class Robot:
    SAFE_WIDTH_HEIGHT = pygame.Vector2(ROBOT_DIAMETER, ROBOT_DIAMETER)

    def __init__(self, initial_pos, speed, color):
        self.initial_pos = initial_pos
        self.speed = speed
        self.color = color
        self.reset()
        self.connection = None
    
    def reset(self):
        self.pos = self.initial_pos
        self.dir = INITIAL_DIR.copy()
        self.target_dir = INITIAL_DIR.copy()
        self.target_indices = None
    
    @property
    def safe_rect(self):
        top_left = self.pos - ROBOT_SAFE_WIDTH_HEIGHT / 2
        return pygame.Rect(top_left, ROBOT_SAFE_WIDTH_HEIGHT)
    
    @property
    def cell(self):
        return board.point_to_cell(pygame.Vector2(self.safe_rect.center))

    @property
    def indices(self):
        return self.cell.indices
    
    @property
    def letter(self):
        return DIR_TO_LETTER[tuple(self.dir)]
    
    @property
    def target_letter(self):
        return DIR_TO_LETTER[tuple(self.target_dir)]

    @property
    def vel(self):
        return self.dir * self.speed

    @property
    def can_move(self):
        saved_pos = self.pos.copy()
        self.pos += self.vel
        res = board.check_valid_bounding_box(self.safe_rect)
        self.pos = saved_pos
        return res
    
    def move(self):
        # Smart turning: If you can't move in your target direction, you're stuck on a corner.
        # So first move orthogonal to the desired direction (leaving 2 possible directions)
        # Which direction? The one that points closer to the center of the current cell.
        if self.target_indices:
            self.dir.update(self.target_dir)
            if not self.can_move:
                recenter_dir = self.cell.center_vec - self.pos
                if self.dir.x != 0:
                    self.dir.update(0, (-1 if recenter_dir.y < 0 else 1))
                else:
                    self.dir.update((-1 if recenter_dir.x < 0 else 1), 0)
        if self.can_move:
            self.pos += self.vel
        if self.indices == self.target_indices:
            self.target_indices = None
        if self.connection:
            self.connection.transmit_letter(self.letter)

    def smart_turn(self, target_dir: pygame.Vector2):
        self.dir.update(target_dir)
        target_r = self.indices[0] + round(target_dir.y)
        target_c = self.indices[1] + round(target_dir.x)
        if board.check_visitable(target_r, target_c):
            self.target_dir = target_dir
            self.target_indices = (target_r, target_c)
        else:
            self.target_indices = None

    def draw(self):
        pygame.draw.circle(unit_screen, self.color, self.pos, ROBOT_SAFE_RADIUS, width=1)
        pygame.draw.circle(unit_screen, self.color, self.pos, ROBOT_RADIUS)
        draw_centered_text(self.letter + '/' + self.target_letter, self.pos, 'black')

pacman = Robot(board.grid[1][1].center_vec, PACMAN_SPEED, PACMAN_COLOR)
ghost = Robot(board.grid[-2][-2].center_vec, GHOST_SPEED, GHOST_COLOR)

def start():
    global pellets, score, state, pacman, ghost, screen, unit_screen
    board_w, board_h = board.INITIAL_BOARD_SIZE

    def reset_game():
        global pellets, score, state, pacman, ghost
        pellets = board.INITIAL_PELLETS.copy()
        score = 0
        state = State.PAUSED
        pacman.reset()
        ghost.reset()
        board.reset()
    reset_game()
    
    def start_game():
        global state
        state = State.RUNNING
        if args.wireless:
            pacman.connection.start_game()
            ghost.connection.start_game()
    
    def quit_game():
        if args.wireless:
            pacman.connection.quit_game()
            ghost.connection.quit_game()

    def win_game():
        global state
        state = State.WON
        quit_game()

    def lose_game():
        global state
        state = State.LOST
        quit_game()

    if args.camera:
        from camera import Camera
        cam = Camera()

    while True:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if state == State.PAUSED:
                    if event.key == pygame.K_s:
                        start_game()
                else:
                    if state == State.RUNNING:
                        match event.key:
                            case pygame.K_LEFT:
                                pacman.smart_turn(pygame.Vector2(-1, 0))
                            case pygame.K_RIGHT:
                                pacman.smart_turn(pygame.Vector2(1, 0))
                            case pygame.K_UP:
                                pacman.smart_turn(pygame.Vector2(0, -1))
                            case pygame.K_DOWN:
                                pacman.smart_turn(pygame.Vector2(0, 1))
                            case pygame.K_q:
                                lose_game()
                    if event.key == pygame.K_r:
                        reset_game()
            if event.type == pygame.QUIT:
                quit_game()
                exit()
            if event.type == pygame.VIDEORESIZE:
                board_w, board_h = event.w, event.h
                # Adjusts width and height to maximum "usable" values
                aspect_ratio = board_w / board_h
                if aspect_ratio > board.ASPECT_RATIO:
                    board_w = board_h * board.ASPECT_RATIO
                else:
                    board_h = board_w / board.ASPECT_RATIO

        unit_screen.fill('black') # Background color

        if args.debug:
            pygame.draw.rect(unit_screen, 'red', (0, 0, board_w, board_h), width=1) # Usable bounding box

        # Updates pacman/ghost coordinates
        if state == State.RUNNING:
            if args.camera:
                coordinates = cam.get_coordinates()

                if coordinates[0] != -1 and coordinates[1] != -1: # If valid position detected update coordinates
                    pacman.pos.update(coordinates[0], coordinates[1])

                if coordinates[2] != -1 and coordinates[3] != -1:
                    ghost.pos.update(coordinates[2], coordinates[3])
            else:
                pacman.move()
                ghost.move()

            # Conduct BFS for Ghost's next move
            shortest_path = [] # from ghost to pacman
            queue = [(ghost.indices, [])] # (indices, path)
            visited = set()
            visited.add(ghost.indices)
            while queue:
                current_indices, path = queue.pop(0)
                if current_indices == pacman.indices:
                    shortest_path = path
                    break
                
                for i, (dc, dr) in enumerate(DIRECTIONS):
                    new_r, new_c = current_indices[0] + dr, current_indices[1] + dc
                    new_indices = (new_r, new_c)
                    if new_indices not in visited and board.check_visitable(new_r, new_c):
                        visited.add(new_indices)
                        queue.append((new_indices, path + [DIRECTIONS[i]]))

            # Mark all cells on path
            board.reset()
            if len(shortest_path):
                r, c = ghost.indices
                for i, dir in enumerate(shortest_path):
                    board.grid[r][c].on_path = True
                    c += dir[0]
                    r += dir[1]
                ghost.smart_turn(pygame.Vector2(shortest_path[0]))
                # ghost.dir.update(shortest_path[0])
                # # If the ghost can't move, it's stuck on a corner.
                # # So move orthogonal to the desired BFS direction (still 2 directions)
                # # Which direction? The one that points closer to the center of the current cell.
                # if not ghost.can_move:
                #     recenter_dir = ghost.cell.center_vec - ghost.pos
                #     if ghost.dir.x != 0:
                #         ghost.dir.update(0, (-1 if recenter_dir.y < 0 else 1))
                #     else:
                #         ghost.dir.update((-1 if recenter_dir.x < 0 else 1), 0)
                # ghost.transmit()
        if args.debug:
            for cell in board.flat_grid:
                if cell.is_filled:
                    pygame.draw.rect(unit_screen, WALL_COLOR, cell.rect) # Actual cell
                if cell.indices == pacman.indices:
                    pygame.draw.rect(unit_screen, PACMAN_COLOR, cell.rect, width=1)
                if cell.on_path:
                    pygame.draw.rect(unit_screen, GHOST_COLOR, cell.rect, width=1)
        
        # Need to copy to avoid "set changed size during iteration" error
        for pellet in pellets.copy():
            if pacman.pos.distance_to(pellet) < PELLET_RADIUS + ROBOT_RADIUS:
                pellets.remove(pellet)
                score += 1
            pygame.draw.circle(unit_screen, "yellow", pellet, PELLET_RADIUS)

        for robot in (pacman, ghost):
            robot.draw()

        if len(pellets) == 0:
            win_game()
        if pacman.pos.distance_to(ghost.pos) < 2 * ROBOT_SAFE_RADIUS:
            lose_game()

        draw_centered_text(f'SCORE: {score}', (board.INITIAL_BOARD_W / 2, FONT_SIZE))
        match state:
            case State.PAUSED:
                draw_centered_text('PRESS S TO START', (board.INITIAL_BOARD_W / 2, board.INITIAL_BOARD_H * 0.45))
                draw_centered_text('(PRESS Q TO QUIT DURING GAME)', (board.INITIAL_BOARD_W / 2, board.INITIAL_BOARD_H * 0.55))
            case State.WON | State.LOST:
                draw_centered_text(state.value, (board.INITIAL_BOARD_W / 2, board.INITIAL_BOARD_H * 0.45))
                draw_centered_text('PRESS R TO RESET', (board.INITIAL_BOARD_W / 2, board.INITIAL_BOARD_H * 0.55))

        # flip() the display to put your work on screen
        screen.blit(pygame.transform.scale(unit_screen, (board_w, board_h)), (0, 0))
        pygame.display.flip()

        clock.tick(MAX_FRAME_RATE)
