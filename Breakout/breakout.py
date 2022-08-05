from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame.locals import *
from enum import Enum
from collections import namedtuple

pygame.init()

# Constants
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
BRICK_COLS = 6
BRICK_ROWS = 6

# Colours
WHITE = (255, 255, 255)
BACKGROUND = (234, 218, 184)
RED_BLOCK = (255, 50, 50)
GREEN_BLOCK = (50, 255, 50)
BLUE_BLOCK = (50, 50, 255)
PADDLE_COLOUR = (142, 135, 123)
PADDLE_OUTLINE = (100, 100, 100)

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
                if row < 2: 
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                
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
                print(brick_colour)
                
                pygame.draw.rect(display, BACKGROUND, brick[0], 2)
        
class paddle():
    def __init__(self):
        # Define paddle dimensions and attributes
        self.height = 10
        self.width = int(WINDOW_WIDTH / BRICK_COLS)
        self.x = int((WINDOW_WIDTH/2) - (self.width / 2))
        self.y = WINDOW_HEIGHT - 3 * (self.height / 2)
        self.speed = 10
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


class breakout_game:
    def __init__(self, width = WINDOW_WIDTH, height = WINDOW_HEIGHT):
        # Set display resolution
        brick_wall = wall()
        brick_wall.create_wall()
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        self.display.fill(BACKGROUND)
        brick_wall.draw_wall(self.display)
        

        # Set window title
        pygame.display.set_caption('Breakout')
        
        

 
    def play_step(self):
        self.update_ui()
        return True, 0


    def update_ui(self):
        player_paddle = paddle()
        player_paddle.draw(self.display)
        player_paddle.move()

        

        # Draw wall
        
        pygame.display.flip()

if __name__ == '__main__':
    game = breakout_game()
    while True:
        
        
        gameOver, score = game.play_step()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

pygame.quit()