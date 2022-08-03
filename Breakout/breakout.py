from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame.locals import *
from enum import Enum
from collections import namedtuple

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

class breakout_game:
    def __init__(self, width = WINDOW_WIDTH, height = WINDOW_HEIGHT):
        # Set display resolution
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))

        # Set window title
        pygame.display.set_caption('Breakout')
        
        self.clock = pygame.time.Clock()

if __name__ == '__main__':
    game = breakout_game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

pygame.quit()