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
pacman_connection = None
ghost_connection = None

PELLET_RADIUS = 10.0
GHOST_COLLISION_MARGIN = 10.0

FONT_FAMILY_PATH = './assets/PressStart2P-Regular.ttf'
FONT_SIZE = 20


PACMAN_SPEED = 10.0
PACMAN_COLOR = 'yellow'

GHOST_SPEED = 1.0 # In px/frame
GHOST_COLOR = 'red'

ROBOT_DIAMETER_INCHES = 3.875
ROBOT_RADIUS = ROBOT_DIAMETER_INCHES / 2 * board.INITIAL_PX_PER_INCH
MAX_FRAME_RATE = 60
PACMAN_START_VEL = (PACMAN_SPEED, 0)

# pygame setup
pygame.init()
FONT = pygame.font.Font(FONT_FAMILY_PATH, FONT_SIZE)
clock = pygame.time.Clock()

def start():
    global pacman_grid_loc, ghost_grid_loc, pellets, score, state, pacman_vel, pacman_pos, ghost_pos
    board_w, board_h = board.INITIAL_BOARD_SIZE
    screen = pygame.display.set_mode(board.INITIAL_BOARD_SIZE, pygame.RESIZABLE) # Screen user actually sees
    unit_screen = screen.copy() # Internal fixed-size screen that makes math simpler

    def reset_game():
        global pacman_grid_loc, ghost_grid_loc, pellets, score, state, pacman_vel, pacman_pos, ghost_pos
        pacman_grid_loc = (0, 0)
        ghost_grid_loc = (7, 3)
        
        pellets = board.INITIAL_PELLETS.copy()
        score = 0
        state = State.PAUSED
        
        pacman_vel = PACMAN_START_VEL
        pacman_pos = pygame.math.Vector2(board_w / 2, board_h / 8)
        ghost_pos = pygame.math.Vector2(board_w / 8, board_h / 8)
    reset_game()
    
    def start_game():
        global state
        state = State.RUNNING
        if args.wireless:
            pacman_connection.start_game()
            ghost_connection.start_game()
    
    def quit_game():
        if args.wireless:
            pacman_connection.quit_game()
            ghost_connection.quit_game()

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
                        pacman_vel = (-PACMAN_SPEED, 0)
                    case pygame.K_RIGHT:
                        pacman_vel = (PACMAN_SPEED, 0)
                    case pygame.K_UP:
                        pacman_vel = (0, -PACMAN_SPEED)
                    case pygame.K_DOWN:
                        pacman_vel = (0, PACMAN_SPEED)
                    case pygame.K_r:
                        if state != State.PAUSED:
                            reset_game()
                    case pygame.K_s:
                        if state == State.PAUSED:
                            start_game()
                    case pygame.K_q:
                        if state == State.RUNNING:
                            lose_game()
                if pacman_connection:
                    pacman_connection.transmit_direction(pacman_vel)
            if event.type == pygame.QUIT:
                if args.wireless:
                    pacman_connection.close()
                    ghost_connection.close()
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
                    pacman_grid_loc = (coordinates[0], coordinates[1])
                    pacman_pos.x, pacman_pos.y = board.INITIAL_PELLETS[pacman_grid_loc]                

                if coordinates[2] != -1 and coordinates[3] != -1:
                    ghost_grid_loc = (coordinates[2], coordinates[3])
                    ghost_pos.x, ghost_pos.y = board.INITIAL_PELLETS[ghost_grid_loc]

                if args.wireless:
                    # Conduct BFS for Ghost's next move
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    
                    queue = [(ghost_grid_loc, [])]
                    visited = set()
                    visited.add(ghost_grid_loc)
                    print("CURRENT GHOST: ", ghost_grid_loc)
                    while queue:
                        current_pos, path = queue.pop(0)
                        print(current_pos)
                        print(pacman_grid_loc)
                        if current_pos == pacman_grid_loc:
                            print("Direction Sent: ", path[0])
                            ghost_connection.transmit_direction(path[0])
                            break
                        
                        for i, (dx, dy) in enumerate(directions):
                            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
                            if new_pos not in visited:
                                visited.add(new_pos)
                                queue.append((new_pos, path + [directions[i]]))
                        
            else:
                pacman_pos.x += pacman_vel[0]
                pacman_pos.y += pacman_vel[1]
                ghost_pos.move_towards_ip(pacman_pos, GHOST_SPEED)
        
        pacman_pos.x = pygame.math.clamp(pacman_pos.x, 0, board.INITIAL_BOARD_W)
        pacman_pos.y = pygame.math.clamp(pacman_pos.y, 0, board.INITIAL_BOARD_H)

        for cell in board.flat_grid:
            if cell.is_filled:
                pygame.draw.rect(unit_screen, 'blue', cell.rect) # Actual cell
            if args.debug:
                pygame.draw.rect(unit_screen, 'green', cell.rect, width=1) # Border
            if cell.collidepoint(pacman_pos):
                pygame.draw.rect(unit_screen, PACMAN_COLOR, cell.rect, width=1) # Border
            if cell.collidepoint(ghost_pos):
                pygame.draw.rect(unit_screen, GHOST_COLOR, cell.rect, width=1) # Border

        pygame.draw.circle(unit_screen, PACMAN_COLOR, pacman_pos, ROBOT_RADIUS)
        
        # Need to copy to avoid "set changed size during iteration" error
        for pellet in pellets.copy():
            if pacman_pos.distance_to(pellet) < PELLET_RADIUS + ROBOT_RADIUS:
                pellets.remove(pellet)
                score += 1
            pygame.draw.circle(unit_screen, "yellow", pellet, PELLET_RADIUS)

        pygame.draw.circle(unit_screen, GHOST_COLOR, ghost_pos, ROBOT_RADIUS)

        if len(pellets) == 0:
            win_game()
        if pacman_pos.distance_to(ghost_pos) < ROBOT_RADIUS * 2 + GHOST_COLLISION_MARGIN:
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
