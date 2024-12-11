import pygame

WIDTH, HEIGHT = 600, 300

# Board constants
WALL_THICKNESS_INCHES = 0.125
CORRIDOR_DIST_INCHES = 5.78125
INITIAL_PX_PER_INCH = 24

INITIAL_WALL_THICKNESS = WALL_THICKNESS_INCHES * INITIAL_PX_PER_INCH
INITIAL_CORRIDOR_DIST = CORRIDOR_DIST_INCHES * INITIAL_PX_PER_INCH

class Cell:
    def __init__(self, is_filled: bool, rect: tuple[float, float, float, float]):
        self.is_filled = is_filled
        self.rect = rect

BOARD_PATH = './assets/board.txt'
grid: list[list[Cell]] = []
initial_w, initial_h = 0, 0
with open(BOARD_PATH, 'r') as f:
    rows = f.readlines()
    y = 0
    for r, row in enumerate(rows):
        new_grid_row = []
        x = 0
        h = (INITIAL_WALL_THICKNESS, INITIAL_CORRIDOR_DIST)[r % 2]
        initial_h += h
        for c, char in enumerate(row.strip()):
            w = (INITIAL_WALL_THICKNESS, INITIAL_CORRIDOR_DIST)[c % 2]
            if r == 0:
                initial_w += w
            new_grid_row.append(Cell(char != ' ', (x, y, w, h)))
            x += w
        grid.append(new_grid_row)
        y += h

INITIAL_PELLETS = set([
    (30, 60),
    (120, 50),
    (80, 170),
    (350, 240),
    (530, 270)
])
PELLET_RADIUS = 10.0
GHOST_COLLISION_MARGIN = 10.0

FONT_FAMILY_PATH = './assets/PressStart2P-Regular.ttf'
FONT_SIZE = 20

GHOST_SPEED = 1.0 # In px/frame
PLAYER_SPEED = 10.0
PLAYER_RADIUS = 20.0
MAX_FRAME_RATE = 60
PACMAN_START_VEL = (PLAYER_SPEED, 0)

# pygame setup
pygame.init()
FONT = pygame.font.Font(FONT_FAMILY_PATH, FONT_SIZE)
screen = pygame.display.set_mode((initial_w, initial_h), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Settings that can be set in main.py
use_camera = False
movement_callback = lambda key: None
exit_callback = lambda: None

def start():
    pellets = INITIAL_PELLETS.copy()
    score = 0
    state = 'RUNNING'
    usable_w, usable_h = initial_w, initial_h

    def draw_centered_text(text: str, center: tuple[int, int]):
        text = FONT.render(text, True, 'white')
        text_rect = text.get_rect(center=center)
        screen.blit(text, text_rect)
    
    pacman_vel = PACMAN_START_VEL
    if use_camera:
        from camera import Camera
        cam = Camera()
        # coordinates = cam.get_coordinates()
        # pacman_pos = pygame.math.Vector2(coordinates[0], coordinates[1])
        # ghost_pos = pygame.math.Vector2(coordinates[2], coordinates[3])
        pacman_pos = pygame.math.Vector2(usable_w / 2, usable_h / 2)
        ghost_pos = pygame.math.Vector2(usable_w / 10, usable_h / 10)
    else:
        pacman_pos = pygame.math.Vector2(usable_w / 2, usable_h / 2)
        ghost_pos = pygame.math.Vector2(usable_w / 10, usable_h / 10)

    while True:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        pacman_vel = (-PLAYER_SPEED, 0)
                    case pygame.K_RIGHT:
                        pacman_vel = (PLAYER_SPEED, 0)
                    case pygame.K_UP:
                        pacman_vel = (0, -PLAYER_SPEED)
                    case pygame.K_DOWN:
                        pacman_vel = (0, PLAYER_SPEED)
                movement_callback(event.key)
            if event.type == pygame.QUIT:
                exit_callback()
                exit()
            if event.type == pygame.VIDEORESIZE:
                usable_w, usable_h = event.w, event.h
                # Adjusts width and height to maximum "usable" values
                initial_aspect_ratio = initial_w / initial_h
                new_aspect_ratio = event.w / event.h
                if new_aspect_ratio > initial_aspect_ratio:
                    usable_w = event.h * initial_aspect_ratio
                else:
                    usable_h = event.w / initial_aspect_ratio

        screen.fill('black') # Background color

        pygame.draw.rect(screen, 'red', (0, 0, usable_w, usable_h), width=1) # Usable bounding box

        # Updates pacman/ghost coordinates
        if state == 'RUNNING':
            if use_camera:
                coordinates = cam.get_coordinates()

                if coordinates[0] != -1 and coordinates[1] != -1: # If valid position detected update coordinates
                    pacman_pos.x, pacman_pos.y = GRID[(coordinates[0], coordinates[1])]                

                if coordinates[2] != -1 and coordinates[3] != -1:
                    ghost_pos.x, ghost_pos.y = GRID[(coordinates[2], coordinates[3])]
                    
            else:
                pacman_pos.x = pygame.math.clamp(pacman_pos.x + pacman_vel[0], 0, usable_w)
                pacman_pos.y = pygame.math.clamp(pacman_pos.y + pacman_vel[1], 0, usable_h)
                # pacman_pos = pygame.Vector2(pygame.mouse.get_pos())
                ghost_pos.move_towards_ip(pacman_pos, GHOST_SPEED)
        
        for row in grid:
            for cell in row:
                if cell.is_filled:
                    pygame.draw.rect(screen, 'blue', cell.rect) # Actual cell
                pygame.draw.rect(screen, 'green', cell.rect, width=1) # Border

        pygame.draw.circle(screen, "yellow", pacman_pos, PLAYER_RADIUS)
        
        # Need to copy to avoid "set changed size during iteration" error
        for pellet in pellets.copy():
            if pacman_pos.distance_to(pellet) < PELLET_RADIUS + PLAYER_RADIUS:
                pellets.remove(pellet)
                score += 1
            pygame.draw.circle(screen, "yellow", pellet, PELLET_RADIUS)

        pygame.draw.circle(screen, "red", ghost_pos, PLAYER_RADIUS)

        if len(pellets) == 0:
            state = 'YOU WON!'
        elif pacman_pos.distance_to(ghost_pos) < PLAYER_RADIUS * 2 + GHOST_COLLISION_MARGIN:
            state = 'YOU LOST'

        draw_centered_text(f'SCORE: {score}', (usable_w / 2, FONT_SIZE))
        if state != 'RUNNING':
            draw_centered_text(state, (usable_w / 2, usable_h / 2))

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(MAX_FRAME_RATE)
