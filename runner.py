import pygame  # bringing in pygame so we can do game stuff

pygame.init()  # gotta initialize all the pygame modules

# create the window (800 wide x 400 tall)
screen = pygame.display.set_mode((800, 400))

# set the window title at the top
pygame.display.set_caption('Runner')

# controls the FPS (frames per second)
clock = pygame.time.Clock()

# load a custom pixel-style font so we can draw text (size 50)
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# flag to track if the game is active or not (used for game over)
game_active = True

# load background images
sky_surf = pygame.image.load('graphics/Sky.png').convert()  # sky background
ground_surf = pygame.image.load('graphics/ground.png').convert()  # ground image

# render the game title (score display placeholder)
score_surf = test_font.render('My game', False, (64, 64, 64))  # text with dark gray color
score_rect = score_surf.get_rect(center=(400, 50))  # position the text near the top center

# snail enemy setup
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # snail image with transparency
snail_rect = snail_surf.get_rect(bottomright=(600, 300))  # starting position for snail
snail_x_pos = 600  # separate x position for manual control

# player character setup
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()  # player image with transparency
player_rect = player_surf.get_rect(midbottom=(80, 300))  # start player on the ground
player_gravity = 0  # starts with no gravity force applied

# main game loop — runs until you quit
while True:
    # check for input events like key presses, mouse clicks, or quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # mouse click on player to jump (only if on ground)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            # press space to jump (only if on ground)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
         # press space to restart
          if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True


    # this is where all the actual game drawing and updates happen
    if game_active:
        # draw sky and ground
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        # draw score box and text
        pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)  # border
        pygame.draw.rect(screen, '#c0e8ec', score_rect)  # fill
        screen.blit(score_surf, score_rect)  # the text itself

        # move snail left
        snail_x_pos -= 4
        if snail_x_pos < -100:
            snail_x_pos = 800  # reset to right side of screen
        snail_rect.x = snail_x_pos  # update the actual rect
        screen.blit(snail_surf, snail_rect)  # draw snail

        # apply gravity to player and move them down
        player_gravity += 1  # gravity increases over time
        player_rect.y += player_gravity  # apply to y position

        # don't let player fall through the ground
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        # draw player
        screen.blit(player_surf, player_rect)

        # collision check — if snail touches player, game over
        if snail_rect.colliderect(player_rect):
            game_active = False  # triggers yellow screen next frame

        # draw player again (you had this here twice, so leaving it)
        screen.blit(player_surf, player_rect)

        # alternative collision detection code (commented out)
        # if player_rect.colliderect(snail_rect):
        #     print('collision')

    else:
        # if the game is not active (after collision), fill screen yellow
        screen.fill('yellow')

    # update everything we drew to the screen
    pygame.display.update()
    clock.tick(60)  # keep it running at 60 FPS
