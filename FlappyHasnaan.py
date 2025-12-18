# Zain Shahzada
# 2025-12-10 to 2025-12-13
# Flappy Bird Clone (Python)

import pygame
from pygame.locals import *
from sys import exit # Terminate the program
import random

# Window Variables
window_width = 600
window_height = 720 # 80 pixels are for the scrolling ground

# Game Variables
floor_scroll = 0
floor_speed = 4
background_scroll = 0
background_speed = 0.5
game_start = False # This variable is to check if the game has started
game_over = False # This variable is to check if the game has ended
pipe_gap = 225
pipe_frequency = 1500 # Milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency # Takes messure of time as soon as game is started
score = 0
pass_pipe = False

pygame.init() # Initialize pygame
window = pygame.display.set_mode((window_width, window_height)) # Passing a touple for width and height
pygame.display.set_caption("Flappy Hasnaan")
clock = pygame.time.Clock() # Used for fps
fps = 60 # Number of frames per second

# Define font & color (Must be kept below pygame.init())
font = pygame.font.SysFont('Times New Roman', 60) # Size 60 font
yellow_font = (139, 128, 0)

# Load images
background_image = pygame.image.load('Background.png').convert_alpha()
second_background_image = pygame.image.load('Background.png').convert_alpha()
floor_image = pygame.image.load('Floor.png').convert_alpha()
restart_button_image = pygame.image.load('Restart.png').convert_alpha()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(window_height/ 2)
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'Man{num}.png').convert_alpha()
            self.images.append(img)
        self.dead_image = pygame.image.load("Man4.png").convert_alpha()
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 0
        self.clicked = False

    def update(self):

        if game_start == True:
            # Gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 640:
                self.rect.y += int(self.vel)

        if game_over == False:
            # Jumping
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == False:
                self.clicked = False

            # Animation Handling
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            center = self.rect.center
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center=center)

            # Rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], -self.vel)
        else:
            center = self.rect.center
            self.image = pygame.transform.rotate(self.dead_image, 90)
            self.rect = self.image.get_rect(center=center)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Pipe.png').convert_alpha()
        self.rect = self.image.get_rect()
        # Position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.topleft = [x, y - int(pipe_gap / 2)]
        else:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= floor_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        mouse_clicked = False

        # Get Mouse Position
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over button
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == True:
                mouse_clicked = True

        # Draw Button
        window.blit(self.image, (self.rect.x, self.rect.y))

        return mouse_clicked

# Sprite Groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# Instances of classes
flappy = Bird(100, int(window_height / 2))
bird_group.add(flappy)
restart_button = Button(window_width / 2 - 100, window_height / 2 - 100, restart_button_image)


while True: # Game loop

    # Game Background
    window.blit(background_image, (background_scroll, 0))
    window.blit(second_background_image, (background_scroll + 800, 0))

    # Sprite Animation
    bird_group.draw(window)
    bird_group.update()
    pipe_group.draw(window)

    # Draw ground
    window.blit(floor_image, (floor_scroll, window_height - 80))

    # Look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: # The two False's are delete operations
        game_over = True

    # Check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.centerx > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.centerx < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    #print(score)
    draw_text(str(score), font, yellow_font, int(window_width / 2), 50)

    # Check if the bird has hit the ground
    if flappy.rect.bottom  >= 640:
        game_over = True

    if game_over == False and game_start == True:
        # Generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-150, 150)
            btm_pipe = Pipe(window_width, int(window_height / 2 + pipe_height), -1) # Adjust the 50 for height of pipe
            top_pipe = Pipe(window_width, int(pipe_height), 1) # Adjust the 50 for height of pipe
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # Background & Floor Animation
        floor_scroll -= floor_speed
        background_scroll -= background_speed
        
        if abs(floor_scroll) > 34:
            floor_scroll = 0

        if abs(background_scroll) >= 800:
            background_scroll = 0

        pipe_group.update()

    # Check for game over and reset
    if game_over == True:
        if restart_button.draw() == True:
            game_over = False
            score = reset_game()

    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_start == False and game_over == False:
            game_start = True
    
    pygame.display.update()
    clock.tick(fps) # fps