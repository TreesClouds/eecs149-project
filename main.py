import pygame

WIDTH, HEIGHT = 600, 600
INITIAL_PELLETS = set([
    (30, 60),
    (120, 50),
    (80, 170),
    (240, 350),
    (270, 530)
])
PELLET_RADIUS = 10.0
GHOST_COLLISION_MARGIN = 10.0
FONT_FAMILY = './assets/PressStart2P-Regular.ttf'
FONT_SIZE = 20
GHOST_SPEED = 3.0 # In px/frame
PLAYER_RADIUS = 20.0

# pygame setup
pygame.init()
FONT = pygame.font.Font('./assets/PressStart2P-Regular.ttf', FONT_SIZE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
dt = 0

pellets = INITIAL_PELLETS.copy()
score = 0
state = 'RUNNING'

# TODO replace with the ghost pos from pose estimation
pacman_pos = pygame.math.Vector2(0, 0)
ghost_pos = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill('black')

    if state == 'RUNNING':
        pacman_pos = pygame.Vector2(pygame.mouse.get_pos())
        ghost_pos.move_towards_ip(pacman_pos, GHOST_SPEED)

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

    screen.blit(FONT.render(f'SCORE: {score}', True, 'white'), (100, 20))
    if state != 'RUNNING':
        screen.blit(FONT.render(state, True, 'white'), (WIDTH / 2, HEIGHT / 2))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
