import pygame  # Bringing in pygame for everything game-related
from sys import exit  # To close the game window cleanly

# -------- DISPLAY SCORE FUNCTION --------
def display_score():
    # Get time passed since game started (in seconds)
    current_time = int(pygame.time.get_ticks() / 1000) - start_time

    # Render the score text surface using the font
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))

    # Center the score on the screen at the top
    score_rect = score_surf.get_rect(center=(400, 50))

    # Draw the score on the screen
    screen.blit(score_surf, score_rect)

    # Return the number so we can reuse it for game over screen
    return current_time

# -------- INIT EVERYTHING --------
pygame.init()  # Always needed to start pygame properly

# Create the game window (800 pixels wide, 400 pixels tall)
screen = pygame.display.set_mode((800, 400))

# Set the window title at the top
pygame.display.set_caption('Runner')

# Clock controls how fast the game runs (FPS)
clock = pygame.time.Clock()

# Load the pixel font from file and set size to 50
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# -------- GAME STATE VARIABLES --------
game_active = False   # Is the game running or are we on the intro/game over screen?
start_time = 0        # Time when the game started (used to track score)
score = 0             # Stores the current score (used for game over display)

# -------- LOAD BACKGROUND IMAGES --------
sky_surface = pygame.image.load('graphics/Sky.png').convert()        # Sky background
ground_surface = pygame.image.load('graphics/ground.png').convert()  # Ground texture

# -------- INTRO SCREEN GRAPHICS --------
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # Make player_stand image bigger
player_stand_rect = player_stand.get_rect(center=(400, 200))  # Center it on the screen

# Game title and instructions for intro screen
game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# -------- PLAYER SETUP --------
player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))  # Bottom left-ish of screen
player_gravity = 0  # Gravity controls falling speed each frame

# -------- SNAIL SETUP (Manual enemy) --------
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright=(600, 300))  # Starts near the right side
snail_x_pos = 600  # This value manually controls snail's horizontal position

# -------- MAIN GAME LOOP --------
while True:
    # -------- EVENT LOOP --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # Clean shutdown

        if game_active:
            # Handle jump input — only if on ground
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20  # Big upward force to simulate jump

        else:
            # Restart game when pressing space on intro/game over screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True                              # Resume game state
                start_time = int(pygame.time.get_ticks() / 1000)  # Restart the score timer
                player_rect.bottom = 300                        # Reset player position
                player_gravity = 0                              # Reset fall speed
                score = 0                                       # Start score at 0

                # -------- FIXED SNAIL COLLISION BUG --------
                # We need to move the snail completely off-screen,
                # and update BOTH the x position variable AND the actual rectangle
                snail_x_pos = 800           # Reset the snail far right
                snail_rect.x = snail_x_pos  # Actually apply the new position
                # If we forget to update snail_x_pos, it moves back into player instantly

    # -------- GAME ACTIVE --------
    if game_active:
        # Draw background sky and ground
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # Show and track the score
        score = display_score()

        # Move snail left across screen each frame
        snail_x_pos -= 4  # Lower = slower, higher = faster
        if snail_x_pos < -100:
            snail_x_pos = 800  # Wrap around to right side again
        snail_rect.x = snail_x_pos  # Apply manual movement
        screen.blit(snail_surface, snail_rect)  # Draw the snail

        # Apply gravity to player each frame
        player_gravity += 1
        player_rect.y += player_gravity  # Move player downward

        # Stop player from falling through ground
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        # Draw the player character
        screen.blit(player_surface, player_rect)

        # -------- COLLISION DETECTION --------
        if player_rect.colliderect(snail_rect):
            game_active = False  # Switch to game over mode

    # -------- GAME NOT ACTIVE (INTRO OR GAME OVER SCREEN) --------
    else:
        screen.fill((94, 129, 162))  # Background color (soft blue)
        screen.blit(player_stand, player_stand_rect)  # Show large standing player art
        screen.blit(game_name, game_name_rect)        # Show game title

        if score == 0:
            # First time playing: show instructions
            screen.blit(game_message, game_message_rect)
        else:
            # After game ends: show final score
            score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 330))
            screen.blit(score_message, score_message_rect)

    # -------- UPDATE DISPLAY AND FPS --------
    pygame.display.update()  # Draw everything we just set up this frame
    clock.tick(60)  # Cap frame rate at 60 FPS
