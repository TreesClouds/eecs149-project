from cli import args
import pygame
import board
from enum import Enum

class State(Enum):
    PAUSED = 'PAUSED'
    RUNNING = 'RUNNING'
    WON = 'YOU WON!'
    LOST = 'GAME OVER'

# Wireless
FONT_FAMILY_PATH = './assets/PressStart2P-Regular.ttf'
FONT_SIZE = 20

# Prefer low speeds but high frame rates for high collision detection precision,
# which minimizes the risk of clipping through walls
PACMAN_SPEED = 2.0
PACMAN_COLOR = 'yellow'

GHOST_SPEED = 1.0 # In px/frame
GHOST_COLOR = 'red'

MAX_FRAME_RATE = 120

ROBOT_DIAMETER_INCHES = 3.875
ROBOT_DIAMETER = ROBOT_DIAMETER_INCHES * board.INITIAL_PX_PER_INCH
ROBOT_RADIUS = ROBOT_DIAMETER / 2

ROBOT_SAFE_DIAMETER = ROBOT_DIAMETER * 1.2
ROBOT_SAFE_RADIUS = ROBOT_SAFE_DIAMETER / 2

PELLET_RADIUS = 10.0

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# pygame setup
pygame.init()
FONT = pygame.font.Font(FONT_FAMILY_PATH, FONT_SIZE)
clock = pygame.time.Clock()
INITIAL_DIR = pygame.Vector2(1, 0)
ROBOT_SAFE_WIDTH_HEIGHT = pygame.Vector2(ROBOT_SAFE_DIAMETER, ROBOT_SAFE_DIAMETER)

screen = pygame.display.set_mode(board.INITIAL_BOARD_SIZE, pygame.RESIZABLE) # Screen user actually sees
unit_screen = screen.copy() # Internal fixed-size screen that makes math simpler

class Robot:
    SAFE_WIDTH_HEIGHT = pygame.Vector2(ROBOT_DIAMETER, ROBOT_DIAMETER)

    def __init__(self, color, speed):
        self.color = color
        self.pos = pygame.Vector2(0, 0)
        self.speed = speed
        self.dir = INITIAL_DIR.copy()
        self.connection = None
    
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
    def vel(self):
        assert self.dir.magnitude() != 0, 'No direction set'
        self.dir.scale_to_length(self.speed)
        return self.dir

    @property
    def can_move(self):
        saved_pos = self.pos.copy()
        self.pos += self.vel
        res = board.check_valid_bounding_box(self.safe_rect)
        self.pos = saved_pos
        return res
    
    def move(self):
        if self.can_move:
            self.pos += self.vel

    def draw(self):
        pygame.draw.circle(unit_screen, self.color, self.pos, ROBOT_SAFE_RADIUS, width=1)
        pygame.draw.circle(unit_screen, self.color, self.pos, ROBOT_RADIUS)

pacman = Robot(PACMAN_COLOR, PACMAN_SPEED)
ghost = Robot(GHOST_COLOR, GHOST_SPEED)

def start():
    global pellets, score, state, pacman, ghost, screen, unit_screen
    board_w, board_h = board.INITIAL_BOARD_SIZE

    def reset_game():
        global pellets, score, state, pacman, ghost
        pellets = board.INITIAL_PELLETS.copy()
        score = 0
        state = State.PAUSED
        pacman.pos.update(board_w / 2, board_h / 8)
        pacman.dir.update(INITIAL_DIR.copy())
        ghost.pos.update(board_w / 8, board_h / 8)
        ghost.dir.update(INITIAL_DIR.copy())
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

    def draw_centered_text(text: str, center: tuple[int, int]):
        text = FONT.render(text, True, 'white')
        text_rect = text.get_rect(center=center)
        unit_screen.blit(text, text_rect)

    if args.camera:
        from camera import Camera
        cam = Camera()

    while True:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        pacman.dir.update(-1, 0)
                    case pygame.K_RIGHT:
                        pacman.dir.update(1, 0)
                    case pygame.K_UP:
                        pacman.dir.update(0, -1)
                    case pygame.K_DOWN:
                        pacman.dir.update(0, 1)
                    case pygame.K_r:
                        if state != State.PAUSED:
                            reset_game()
                    case pygame.K_s:
                        if state == State.PAUSED:
                            start_game()
                    case pygame.K_q:
                        if state == State.RUNNING:
                            lose_game()
                if pacman.connection:
                    pacman.connection.transmit_direction(pacman.dir)
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
            # print("CURRENT GHOST: ", ghost_grid_loc)
            while queue:
                current_indices, path = queue.pop(0)
                # print(current_pos)
                # print(pacman_grid_loc)
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
            r, c = ghost.indices
            for i, dir in enumerate(shortest_path):
                board.grid[r][c].on_path = True
                c += dir[0]
                r += dir[1]
            next_dir = shortest_path[0]
            recenter_dir = ghost.cell.center_vec - ghost.pos
            ghost.dir.update(next_dir if ghost.can_move else recenter_dir)
            if args.wireless:
                ghost.connection.transmit_direction(next_dir)

        for cell in board.flat_grid:
            if cell.is_filled:
                pygame.draw.rect(unit_screen, 'blue', cell.rect) # Actual cell
            if args.debug:
                pygame.draw.rect(unit_screen, 'green', cell.rect, width=1) # Border
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
