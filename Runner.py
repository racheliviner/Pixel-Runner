from random import randint, choice
from sys import exit
import pygame

# Player class representing the player character
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load player images for animation
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walks = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.gravity = 0

        # Set initial image and position of the player
        self.image = self.player_walks[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 300))
        # Load jump image and jump sound effect
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/jump_sound.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        # Check for key press events (spacebar for jumping)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            # Apply upward force and play jump sound
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        # Apply gravity to simulate falling
        self.gravity += 1
        self.rect.y += self.gravity
        # Keep the player above the ground
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        # Update player animation based on the current state
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            # Animate walking when on the ground
            self.player_index += 0.1
            if self.player_index >= len(self.player_walks):
                self.player_index = 0
            self.image = self.player_walks[int(self.player_index)]

    def update(self):
        # Update player state each frame
        self.player_input()
        self.apply_gravity()
        self.animation_state()


# Obstacle class representing obstacles in the game
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type_obstacle):
        super().__init__()
        # Load obstacle images based on the type
        if type_obstacle == 'fly':
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomleft=(randint(800, 1100), y_pos))

    def animation_state(self):
        # Update obstacle animation
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        # Update obstacle state each frame
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        # Remove obstacle when off-screen
        if self.rect.x <= -100:
            self.kill()


# Function to set the font size
def set_size_font(size):
    return pygame.font.Font('font/pixeltype.ttf', size)

# Function to display the opening or closing screen
def display_open_close_screen(final_score):
    player_stand = pygame.transform.scale2x(pygame.image.load('graphics/Player/player_stand.png').convert_alpha())
    player_stand_rect = player_stand.get_rect(center=(400, 180))
    game_restart_surface = set_size_font(30).render('Press  Enter To Run', False, (111, 196, 169))
    game_restart_rect = game_restart_surface.get_rect(center=(400, 350))
    screen.fill((94, 129, 162))
    screen.blit(game_restart_surface, game_restart_rect)
    screen.blit(player_stand, player_stand_rect)
    if final_score == 0:
        pixel_surface = set_size_font(80).render('Pixel runner', False, (111, 196, 169))
        pixel_rect = pixel_surface.get_rect(center=(400, 50))
        screen.blit(pixel_surface, pixel_rect)
    else:
        game_over_surface = set_size_font(80).render('GAME OVER', False, (111, 196, 169))
        game_over_rect = game_over_surface.get_rect(center=(400, 50))
        final_score_sur = set_size_font(50).render(f'Your Score:{final_score}', False, (111, 196, 169))
        final_score_rect = final_score_sur.get_rect(center=(400, 310))
        screen.blit(game_over_surface, game_over_rect)
        screen.blit(final_score_sur, final_score_rect)


# Function to display the current score
def display_score():
    cur_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = set_size_font(50).render(f'Score: {cur_time} ', False, 'Black')
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return cur_time

# Function to check for collisions between player and obstacles
def collisions():
    if pygame.sprite.spritecollide(player.sprite, obstacles_group, False):
        obstacles_group.empty()
        return False
    return True


# Main game setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
player_gravity = 0
game_active = False
start_time = 0
score = 0

# Load background images and music
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
bg_music = pygame.mixer.Sound('audio/background_music.wav')
bg_music.play()

# Set up a timer for obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

# Create the player and obstacles groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacles_group = pygame.sprite.Group()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacles_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # Draw background and ground
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Draw and update player and obstacles
        player.draw(screen)
        player.update()
        obstacles_group.draw(screen)
        obstacles_group.update()

        # Check for collisions
        game_active = collisions()
    else:
        # Display opening or closing screen
        display_open_close_screen(score)

    pygame.display.update()
    clock.tick(60)