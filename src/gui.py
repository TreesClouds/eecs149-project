import pygame
import board

# Settings set by main.py from CLI arguments
# Camera
use_camera = False

# Wireless
movement_callback = lambda key: None
exit_callback = lambda: None

# Debug
enable_debug = False

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
clock = pygame.time.Clock()

def start():
    pellets = list(board.INITIAL_PELLETS.values()).copy()
    score = 0
    state = 'RUNNING'
    board_w, board_h = board.INITIAL_BOARD_SIZE

    screen = pygame.display.set_mode(board.INITIAL_BOARD_SIZE, pygame.RESIZABLE) # Screen user actually sees
    unit_screen = screen.copy() # Internal fixed-size screen that makes math simpler

    def draw_centered_text(text: str, center: tuple[int, int]):
        text = FONT.render(text, True, 'white')
        text_rect = text.get_rect(center=center)
        unit_screen.blit(text, text_rect)
    
    pacman_vel = PACMAN_START_VEL
    if use_camera:
        from camera import Camera
        cam = Camera()

    pacman_pos = pygame.math.Vector2(board_w / 2, board_h / 2)
    ghost_pos = pygame.math.Vector2(board_w / 10, board_h / 10)

    while True:
        flat_grid = (cell for row in board.grid for cell in row)

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
                board_w, board_h = event.w, event.h
                # Adjusts width and height to maximum "usable" values
                aspect_ratio = board_w / board_h
                if aspect_ratio > board.ASPECT_RATIO:
                    board_w = board_h * board.ASPECT_RATIO
                else:
                    board_h = board_w / board.ASPECT_RATIO

        unit_screen.fill('black') # Background color

        if enable_debug:
            pygame.draw.rect(unit_screen, 'red', (0, 0, board_w, board_h), width=1) # Usable bounding box

        # Updates pacman/ghost coordinates
        if state == 'RUNNING':
            if use_camera:
                coordinates = cam.get_coordinates()

                if coordinates[0] != -1 and coordinates[1] != -1: # If valid position detected update coordinates
                    pacman_pos.x, pacman_pos.y = board.INITIAL_PELLETS[(coordinates[0], coordinates[1])]                

                if coordinates[2] != -1 and coordinates[3] != -1:
                    ghost_pos.x, ghost_pos.y = board.INITIAL_PELLETS[(coordinates[2], coordinates[3])]
                    
            else:
                pacman_pos.x = pygame.math.clamp(pacman_pos.x + pacman_vel[0], 0, board.INITIAL_BOARD_W)
                pacman_pos.y = pygame.math.clamp(pacman_pos.y + pacman_vel[1], 0, board.INITIAL_BOARD_H)
                # pacman_pos = pygame.Vector2(pygame.mouse.get_pos())
                ghost_pos.move_towards_ip(pacman_pos, GHOST_SPEED)
        
        for cell in flat_grid:
            if cell.is_filled:
                pygame.draw.rect(unit_screen, 'blue', cell.rect) # Actual cell
            if enable_debug:
                pygame.draw.rect(unit_screen, 'green', cell.rect, width=1) # Border

        pygame.draw.circle(unit_screen, "yellow", pacman_pos, PLAYER_RADIUS)
        
        # Need to copy to avoid "set changed size during iteration" error
        for pellet in pellets.copy():
            if pacman_pos.distance_to(pellet) < PELLET_RADIUS + PLAYER_RADIUS:
                pellets.remove(pellet)
                score += 1
            pygame.draw.circle(unit_screen, "yellow", pellet, PELLET_RADIUS)

        pygame.draw.circle(unit_screen, "red", ghost_pos, PLAYER_RADIUS)

        if len(pellets) == 0:
            state = 'YOU WON!'
        elif pacman_pos.distance_to(ghost_pos) < PLAYER_RADIUS * 2 + GHOST_COLLISION_MARGIN:
            state = 'YOU LOST'

        draw_centered_text(f'SCORE: {score}', (board.INITIAL_BOARD_W / 2, FONT_SIZE))
        if state != 'RUNNING':
            draw_centered_text(state, (board.INITIAL_BOARD_W / 2, board.INITIAL_BOARD_H / 2))

        # flip() the display to put your work on screen
        screen.blit(pygame.transform.scale(unit_screen, (board_w, board_h)), (0, 0))
        pygame.display.flip()

        clock.tick(MAX_FRAME_RATE)
