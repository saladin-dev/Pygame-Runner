import pygame  # bringing in pygame so we can do game stuff
from sys import exit  # allows us to use exit() to close the game

# Function to display and return the current score (time survived)
def display_score():
    # get the number of seconds since the game started
    current_time = int(pygame.time.get_ticks() / 1000) - start_time

    # render the score text onto a surface
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))

    # center the score text at the top of the screen
    score_rect = score_surf.get_rect(center=(400, 50))

    # draw the score text onto the screen
    screen.blit(score_surf, score_rect)

    # return the score so we can store and show it later
    return current_time

pygame.init()  # initialize all the pygame modules

# create a display window with width=800 and height=400
screen = pygame.display.set_mode((800, 400))

# set the title of the window
pygame.display.set_caption('Runner')

# create a clock to control the frame rate
clock = pygame.time.Clock()

# load a pixel-style font at size 50
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# flag to check if game is active or showing intro
game_active = True

# store the time the game started (used for score)
start_time = 0

# store the last score for display on the intro screen
score = 0

# load background images and optimize them
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# load the snail enemy image and make background transparent
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()

# get the rectangle for snail and position it near bottom right
snail_rect = snail_surf.get_rect(bottomright=(600, 300))
snail_x_pos = 600  # manually update x position for movement

# load the player sprite and get its rectangle
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0  # this controls falling and jumping

# load and scale the standing player image for intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# render game name and its position
game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

# render the "Press space" message
game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 340))

# ---------------- MAIN GAME LOOP ----------------
while True:
    # check for events like key presses or window closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # --------- input handling while game is running ---------
        if game_active:
            # jump if mouse clicks on player while grounded
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            # jump if spacebar is pressed while grounded
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

        # --------- input on game over / intro screen ---------
        else:
            # press space once to restart the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True                      # turn game back on
                snail_rect.left = 800                   # move snail off screen
                start_time = int(pygame.time.get_ticks() / 1000)  # reset timer
                player_rect.bottom = 300                # reset player position
                player_gravity = 0                      # clear jump
                score = 0                               # reset score display

    # ---------------- GAME LOGIC + DRAWING ----------------
    if game_active:
        # draw sky and ground
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        # draw score and update the score variable
        score = display_score()

        # move snail left each frame
        snail_x_pos -= 4
        if snail_x_pos < -100:
            snail_x_pos = 800  # loop snail back to right edge
        snail_rect.x = snail_x_pos  # apply new x position
        screen.blit(snail_surf, snail_rect)  # draw snail

        # apply gravity to player and move downward
        player_gravity += 1
        player_rect.y += player_gravity

        # stop player from falling below ground
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        # draw player character
        screen.blit(player_surf, player_rect)

        # if player hits the snail — game over
        if snail_rect.colliderect(player_rect):
            game_active = False  # turn off game mode

        # draw player again (optional layering)
        screen.blit(player_surf, player_rect)

    else:
        # draw the intro or game over screen background
        screen.fill((94, 129, 162))

        # draw the standing player image
        screen.blit(player_stand, player_stand_rect)

        # draw game title text
        screen.blit(game_name, game_name_rect)

        # if score is 0 (first launch), show press-space message
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            # if game ended, show final score
            score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 330))
            screen.blit(score_message, score_message_rect)

    # update everything drawn this frame
    pygame.display.update()
    clock.tick(60)  # run the game at 60 FPS
