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
PLAYER_SPEED = 10.0
PLAYER_RADIUS = 20.0

# pygame setup
pygame.init()
FONT = pygame.font.Font('./assets/PressStart2P-Regular.ttf', FONT_SIZE)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

movement_callback = lambda key: None
exit_callback = lambda: None

def start():
    pellets = INITIAL_PELLETS.copy()
    score = 0
    state = 'RUNNING'
    pacman_pos = pygame.math.Vector2(WIDTH / 10, HEIGHT / 10)
    # TODO replace with the ghost pos from pose estimation
    ghost_pos = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)

    while True:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_callback()
                exit()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill('black')

        if state == 'RUNNING':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                pacman_pos.x -= PLAYER_SPEED
                movement_callback(pygame.K_LEFT)
            elif keys[pygame.K_RIGHT]:
                pacman_pos.x += PLAYER_SPEED
                movement_callback(pygame.K_RIGHT)
            elif keys[pygame.K_UP]:
                pacman_pos.y -= PLAYER_SPEED
                movement_callback(pygame.K_UP)
            elif keys[pygame.K_DOWN]:
                pacman_pos.y += PLAYER_SPEED
                movement_callback(pygame.K_DOWN)
            pacman_pos.x = pygame.math.clamp(pacman_pos.x, 0, WIDTH)
            pacman_pos.y = pygame.math.clamp(pacman_pos.y, 0, HEIGHT)
            # pacman_pos = pygame.Vector2(pygame.mouse.get_pos())
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
