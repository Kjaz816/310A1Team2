from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame.locals import *
from enum import Enum
from collections import namedtuple

pygame.init()

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
BRICK_COLS = 6
BRICK_ROWS = 6

# Colours
WHITE = (255, 255, 255)
RED_BLOCK = (255, 0, 0)
BLUE_BLOCK = (0, 255, 0)
GREEN_BLOCK = (0, 0, 255)

class wall():
    def __init__(self):
        # Create the wall dimensions based on the window dimensions and number of bricks wanted
        self.width = WINDOW_WIDTH // BRICK_COLS
        self.height = 50

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
                    print('red')
                elif brick[1] == 2:
                    brick_colour == BLUE_BLOCK
                    print('blue')
                elif brick[1] == 1:
                    brick_colour == GREEN_BLOCK
                    print('green')
                pygame.draw.rect(display, brick_colour, brick[0])


class breakout_game:
    def __init__(self, width = WINDOW_WIDTH, height = WINDOW_HEIGHT):
        # Set display resolution
        brick_wall = wall()
        brick_wall.create_wall()
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        brick_wall.draw_wall(self.display)
        # Set window title
        pygame.display.set_caption('Breakout')
        
        

 
    def play_step(self):
        self.update_ui()
        return True, 0


    def update_ui(self):

        # Set background to white
        self.display.fill(WHITE)

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