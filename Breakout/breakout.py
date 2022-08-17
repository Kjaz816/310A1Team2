from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame.locals import *
from enum import Enum
from collections import namedtuple
from random import randint

pygame.init()
game_over_screen = pygame.image.load('resources/gameOverScreenBreakout.png')

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BRICK_COLS = 9
BRICK_ROWS = 9

# Colours
WHITE = (255, 255, 255)
BACKGROUND = (234, 218, 184)
RED_BLOCK = (227, 75, 115)
GREEN_BLOCK = (118, 222, 67)
BLUE_BLOCK = (52, 207, 224)
PADDLE_COLOUR = (142, 135, 123)
PADDLE_OUTLINE = (100, 100, 100)

# Global variables for game settings
PADDLE_HEIGHT = 15
PADDLE_Y_POS = WINDOW_HEIGHT - 3 * (PADDLE_HEIGHT / 2)
BALL_RADIUS = 10
BALL_SPEED_X = 4
BALL_SPEED_Y = -4
PADDLE_SPEED = 10
BALL_MAX_SPEED = 5

clock = pygame.time.Clock()
fps = 60

live_ball = False
game_over = 0

level = 2

class wall():
    def __init__(self):
        # Create the wall dimensions based on the window dimensions and number of bricks wanted
        self.width = WINDOW_WIDTH // BRICK_COLS
        self.height = 40

    def create_wall(self):
        # Create an empty list that will contain the blocks
        self.wall = [] 
        bricks = []
        # Create the required number of block rows
        for row in range(BRICK_ROWS):
            brick_row = []

            # Create the required number of block cols
            for col in range(BRICK_COLS):

                # Generate X and Y positions for each block and create a rectangle
                brick_x = col * self.width
                brick_y = row * self.height
                rectangle = pygame.Rect(brick_x, brick_y, self.width, self.height)
                
                # Assign brick strength based on high up they are
                if level == 1: 
                    if row < round(BRICK_ROWS * 0.33): 
                        strength = 3
                    elif row < round(BRICK_ROWS * 0.66): 
                        strength = 2
                    else:
                        strength = 1

                elif level == 2:
                    if col == 0 or col == BRICK_COLS - 1 or row < 2: 
                        strength = 1
                    elif row < round(BRICK_ROWS * 0.66): 
                        strength = 2
                    else:
                        strength = 3

                else:
                    strength = randint(1, 3)
                
                # Add brick and its strength to the brick row list
                bricks = [rectangle, strength]
                brick_row.append(bricks)
            
            self.wall.append(brick_row)

    def draw_wall(self, display):
        for row in self.wall:
            for brick in row:

                # Assign colour based on block strength
                if brick[1] == 3:
                    brick_colour = RED_BLOCK
                elif brick[1] == 2:
                    brick_colour = BLUE_BLOCK
                elif brick[1] == 1:
                    brick_colour = GREEN_BLOCK
                pygame.draw.rect(display, brick_colour, brick[0])
                pygame.draw.rect(display, BACKGROUND, brick[0], 2)
        

class paddle():
    def __init__(self):
        # Define paddle dimensions and attributes
        self.height = PADDLE_HEIGHT
        self.width = int(WINDOW_WIDTH / BRICK_COLS)
        self.x = int((WINDOW_WIDTH/2) - (self.width / 2))
        self.y = PADDLE_Y_POS
        self.speed = PADDLE_SPEED
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

    def move(self):
        # Reset movement
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self, display):
        pygame.draw.rect(display, PADDLE_COLOUR, self.rect)
        pygame.draw.rect(display, PADDLE_OUTLINE, self.rect, 3)


class ball():
    def __init__(self, x, y) :
        self.ball_rad = BALL_RADIUS
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.game_over = 0

    def draw(self, display):
        pygame.draw.circle(display, PADDLE_COLOUR, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(display, PADDLE_OUTLINE, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

    def move(self):

        collision_threshold = 5

        game_won = True

        row_count = 0
        for row in brick_wall.wall:
            brick_count = 0
            for brick in row:
                if self.rect.colliderect(brick[0]):
                    # Check where collision came from
                    # Above:
                    if abs(self.rect.bottom - brick[0].top) < collision_threshold and self.speed_y > 0:
                        self.speed_y *= -1
                    # Below:
                    if abs(self.rect.top - brick[0].bottom) < collision_threshold and self.speed_y < 0:
                        self.speed_y *= -1
                    # Left:
                    if abs(self.rect.right - brick[0].left) < collision_threshold and self.speed_y > 0:
                        self.speed_x *= -1
                    # Right:
                    if abs(self.rect.left - brick[0].right) < collision_threshold and self.speed_y < 0:
                        self.speed_x *= -1
                    
                    # Damage block by 1, and delete it if the blocks health = 0
                    if brick_wall.wall[row_count][brick_count][1] > 1:
                        brick_wall.wall[row_count][brick_count][1] -= 1
                    else:
                        brick_wall.wall[row_count][brick_count][0] = (0, 0, 0, 0)

                # Check if current block exists, and if it does then game over must be false
                if brick_wall.wall[row_count][brick_count][0] != (0, 0, 0, 0):
                    game_won = False
                
                brick_count += 1
            row_count += 1
        
        # Check if all blocks are gone, and if they are then set game_over to 1
        if game_won == True:
            self.game_over = 1

        # Check for wall collisions
        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
        
        # Check if player missed the ball
        if self.rect.bottom > WINDOW_HEIGHT + BALL_RADIUS * 2:
            self.game_over = -1

        # Check for collision with paddle
        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_threshold and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction * 5
                if self.speed_x > BALL_MAX_SPEED:
                    self.speed_x = BALL_MAX_SPEED
                elif self.speed_x < 0 and self.speed_x < -BALL_MAX_SPEED:
                    self.speed_x = -BALL_MAX_SPEED

            else: 
                self.speed_x * -1
            
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        return self.game_over


class breakout_game:
    def __init__(self, width = WINDOW_WIDTH, height = WINDOW_HEIGHT):
        # Set display resolution
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        self.display.fill(BACKGROUND)
        
        # Set window title
        pygame.display.set_caption('Breakout')
 
    def play_step(self, live_ball, game_over):
        self.update_ui(game_over)

        if live_ball == True:
            game_over = ball.move()
            player_paddle.move()
            if game_over != 0:
                live_ball = False
        
        return live_ball, game_over
        
    def update_ui(self, game_over):
        
        player_paddle.draw(self.display)
        brick_wall.draw_wall(self.display)
        ball.draw(self.display)
        if game_over == -1:
            self.display.blit(game_over_screen, (0, 0))
        pygame.display.flip()



if __name__ == '__main__':
    
    # Start Game
    game = breakout_game()

    # Setup 
    brick_wall = wall()
    brick_wall.create_wall()
    player_paddle = paddle()
    ball = ball(player_paddle.x + player_paddle.width // 2, player_paddle.y - player_paddle.height - 5)

    while True:

        game.display.fill(BACKGROUND)
        clock.tick(fps)
        live_ball, game_over = game.play_step(live_ball, game_over)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False and game_over == 0:
                live_ball = True

            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False and game_over == -1:
                pygame.quit()
                quit()
                
pygame.quit()