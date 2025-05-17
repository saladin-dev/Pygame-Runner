import pygame                    # Handles graphics, game logic, and input
from sys import exit             # Used to close the game window properly
import random                    # Needed to spawn obstacles at random X positions

class Player(pygame.sprite.Sprite):
    def _init_(self):
      super()._init_()
      self.image = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha
      self.rect = self.image.image.get(midbottom = (200, 300))







# -------- Function: player_animation --------
# Handles switching between jump frame and walk animation based on player position
def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        # If the player is in the air, use the jump image
        player_surf = player_jump
    else:
        # If on the ground, cycle between walking frames
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

# -------- Function: display_score --------
# Draws score at the top of the screen based on how long you survived
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

# -------- Function: obstacle_movement --------
# Moves all obstacles left and draws them; removes any that go off-screen
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

# -------- Function: collisions --------
# Checks if player has collided with any obstacle
def collisions(player, obstacles):
    for obstacle_rect in obstacles:
        if player.colliderect(obstacle_rect):
            return False
    return True

# -------- INIT Pygame + Setup --------
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# -------- Game State --------
game_active = False
start_time = 0
score = 0
obstacle_rect_list = []

player = pygame.sprite.GroupSingle()
player.add(Player())

# -------- Background Art --------
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# -------- Intro Screen Assets --------
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# -------- Player Setup --------
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]  # ✅ FIXED: Previously you had [player_walk_2, player_walk_2]
player_index = 0
player_surf = player_walk[player_index]
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

# -------- Snail Setup --------
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1 , snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
# -------- Fly Setup --------
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1 , fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# -------- Obstacle Timer --------
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)
# -------- Main Game Loop --------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                player_rect.bottom = 300
                player_gravity = 0
                score = 0
                obstacle_rect_list.clear()
        if game_active:
         if event.type == obstacle_timer:
            if random.randint(0, 2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright=(random.randint(900, 1100), 300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright=(random.randint(900, 1100), 210)))

        if event.type == snail_animation_timer:
              if snail_frame_index == 0: snail_frame_index = 1
              else: snail_frame_index = 0
              snail_surf = snail_frames[snail_frame_index]
        if event.type == fly_animation_timer:
          if fly_frame_index == 0: fly_frame_index = 1
          else: fly_frame_index = 0
          fly_surf = fly_frames[fly_frame_index]



    # -------- Game Active --------
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        score = display_score()

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        player_animation()  
        screen.blit(player_surf, player_rect)
        player.draw(screen)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active = collisions(player_rect, obstacle_rect_list)
 
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 330))
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
