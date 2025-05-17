import pygame
from sys import exit
from random import randint, choice

# -------------------- PLAYER SPRITE CLASS --------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Initialize the parent class (Sprite)
        # Load walking frames and store them in a list
        walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.walk_frames = [walk_1, walk_2]
        self.index = 0  # Keeps track of which frame is currently shown

        # Load jump image
        self.jump_image = pygame.image.load('graphics/player/jump.png').convert_alpha()

        # Set initial image and rectangle
        self.image = self.walk_frames[self.index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0  # Used to simulate gravity

        # Load jump sound
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        # Detect key press and jump if on the ground
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        # Apply gravity each frame and update position
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300  # Prevent falling below ground

    def animation_state(self):
        # Switch between jump image and walk animation
        if self.rect.bottom < 300:
            self.image = self.jump_image
        else:
            self.index += 0.1
            if self.index >= len(self.walk_frames): self.index = 0
            self.image = self.walk_frames[int(self.index)]

    def update(self):
        # Called every frame
        self.player_input()
        self.apply_gravity()
        self.animation_state()

# -------------------- OBSTACLE SPRITE CLASS --------------------
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        # Load correct images based on obstacle type
        if type == "fly":
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        # Animate the obstacle by switching frames
        self.index += 0.1
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        # Move obstacle and animate it
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        # Remove if off-screen
        if self.rect.x <= -100:
            self.kill()

# -------------------- HELPER FUNCTIONS --------------------
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def collision_sprite():
    # Check for collision between player and any obstacle
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()  # Remove all obstacles after death
        return False
    else:
        return True

# -------------------- PYGAME INITIALIZATION --------------------
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# -------------------- GAME STATE --------------------
game_active = False
start_time = 0
score = 0

# -------------------- SOUND SETUP --------------------
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.play(loops=-1)

# -------------------- SPRITE GROUPS --------------------
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# -------------------- GRAPHICS --------------------
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# Intro / Game Over Screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
game_message = test_font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# -------------------- TIMERS --------------------
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# -------------------- GAME LOOP --------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    # -------------------- ACTIVE GAME --------------------
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    # -------------------- INACTIVE GAME (INTRO / GAME OVER) --------------------
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)

# -------------------- ERROR LOG (MY MISTAKES) --------------------

# ❌ I used `def _init_` instead of `__init__` in the Player class. Fixed by using double underscores.
# ❌ I forgot to call `.convert_alpha()` with parentheses on surface loading (e.g., `convert_alpha` vs `convert_alpha()`).
# ❌ I had `self.image.image.get(...)` instead of `self.image.get_rect(...)` in the Player class.
# ❌ My player animation wasn’t working because I had a typo in player_walk = [walk_2, walk_2] instead of walk_1 and walk_2.
# ❌ I was manually drawing the player surface even after switching to sprites. Sprites should be drawn only using `.draw()` from the group.
# ❌ I used `player_surf` instead of updating `self.image` inside the Player class.
# ❌ I accidentally drew the player twice (once with `screen.blit()` and again with `player.draw()`).
# ❌ I had the timers firing outside of the game state, causing animations and obstacles to still spawn while the game was inactive.
# ❌ I was updating fly/snail surfaces globally instead of using Sprite animations.

# ✅ All issues above have been resolved and are now part of the final working version with Sprite classes, animation, and sound.
