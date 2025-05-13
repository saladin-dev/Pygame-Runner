import pygame  # bringing in pygame so we can do game stuff

pygame.init()  # gotta initialize all the pygame modules

# create the window (800 wide x 400 tall)
screen = pygame.display.set_mode((800, 400))

# set the window title at the top
pygame.display.set_caption('Runner')

# use this to control the FPS (frames per second)
clock = pygame.time.Clock()

# loading a font file so we can draw text — 50 is the size
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# background images
sky_surf = pygame.image.load('graphics/Sky.png').convert()  # just loads the sky and optimizes it
ground_surf = pygame.image.load('graphics/ground.png').convert()  # same thing for the ground

# setting up the score text
score_surf = test_font.render('My game', False, (64, 64, 64))  # text, antialias off, dark gray
score_rect = score_surf.get_rect(center=(400, 50))  # centering the text near top of screen

# snail enemy setup
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # loads snail with transparency
snail_rect = snail_surf.get_rect(bottomright=(600, 300))  # start position of the snail
snail_x_pos = 600  # we'll use this to move him manually

# player character setup
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()  # load player with transparency
player_rect = player_surf.get_rect(midbottom=(80, 300))  # starting position of the player

# game loop — runs every frame until you quit
while True:
    # event loop — checks for inputs like mouse, keyboard, window close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # closes pygame window properly
            exit()  # fully exits the program

        # you can detect if the mouse is hovering over the player like this
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print('collision')

    # draw the background images first (sky and ground)
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))

    # draw the score box — kinda like a border (light blueish)
    pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)  # border
    pygame.draw.rect(screen, '#c0e8ec', score_rect)  # fill
    screen.blit(score_surf, score_rect)  # draw the actual score text

    # move the snail to the left every frame
    snail_x_pos -= 4
    if snail_x_pos < -100:  # once it goes off screen to the left, reset to the right
        snail_x_pos = 800
    snail_rect.x = snail_x_pos  # update snail's actual position
    screen.blit(snail_surf, snail_rect)  # draw the snail

    # draw the player character
    screen.blit(player_surf, player_rect)

    # collision detection (disabled right now)
    # if player_rect.colliderect(snail_rect):
    #     print('collision')

    pygame.display.update()  # update everything on the screen
    clock.tick(60)  # run at 60 frames per second
