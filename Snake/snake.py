from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import random
import math
from enum import Enum
from collections import namedtuple


pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# Open image files for graphics, and font for text
snake_head_up = pygame.image.load('Snake/resources/snakeHeadUp.png')
snake_head_down = pygame.image.load('Snake/resources/snakeHeadDown.png')
snake_head_left = pygame.image.load('Snake/resources/snakeHeadLeft.png')
snake_head_right = pygame.image.load('Snake/resources/snakeHeadRight.png')

snake_head = snake_head_right

snake_segment_vertical = pygame.image.load('Snake/resources/snakeSegment.png')
snake_segment_horizontal = pygame.image.load('Snake/resources/snakeSegmentHorizontal.png')

snake_segment = snake_segment_horizontal

snake_tail_up = pygame.image.load('Snake/resources/snakeTailUp.png')
snake_tail_down = pygame.image.load('Snake/resources/snakeTailDown.png')
snake_tail_left = pygame.image.load('Snake/resources/snakeTailLeft.png')
snake_tail_right = pygame.image.load('Snake/resources/snakeTailRight.png')

snake_tail = snake_head_right

snakeFood = pygame.image.load('Snake/resources/food.png')
font = pygame.font.Font('Snake/resources/BPdotsSquareBold.otf', 25)

game_over_screen = pygame.image.load('Snake/resources/gameOverScreenSnake.png')

game_over = False

# Constants (Do not change)
GRIDSQUARE = 20
HIGHSCORE_FILE_PATH = 'Snake/snakeScore.txt'

# Game settings
SNAKE_SPEED = 10
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
STARTING_SIZE = 3
SNAKE_LOOPING = True # Change to false if you want the snake to die upon hitting a wall

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRASS = (167, 209, 61)
LIGHTGRASS = (175,215,70)

class snake_game:

    def __init__(self, width = WINDOW_WIDTH, height = WINDOW_HEIGHT):

        # Set display resolution
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))

        # Initialize the field surface to be called in the loop
        self.field = pygame.Surface((self.width, self.height))
        self.field.fill(GRASS)
        for row in range(self.height):
           if row % 2 == 0:
                for col in range(self.width):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * GRIDSQUARE, row * GRIDSQUARE, GRIDSQUARE, GRIDSQUARE)
                        pygame.draw.rect(self.field, LIGHTGRASS, grass_rect)

        # Set window title
        pygame.display.set_caption('Snake')
        
        self.clock = pygame.time.Clock()

        # Set Starting direction
        self.direction = Direction.RIGHT

        # Set starting position of snake
        self.head = Point(self.width/2, self.height/2)
        self.headRect = pygame.Rect(self.head.x-GRIDSQUARE/2, self.head.y-GRIDSQUARE/2, GRIDSQUARE, GRIDSQUARE)

        # Create starting snake (3 Segments)
        self.snake = [self.head]
        for x in range(STARTING_SIZE):
            self.snake.append(Point((self.head.x-x*GRIDSQUARE), self.head.y))

        # Set score and food defaults
        self.score = 0
        self.food = None

        # Place food on level
        self.place_food()


    def place_food(self):

        # Find a random x and y coordinate on the display
        x = random.randint(3, (self.width-GRIDSQUARE)//GRIDSQUARE-3)*GRIDSQUARE
        y = random.randint(3, (self.height-GRIDSQUARE)//GRIDSQUARE-3)*GRIDSQUARE

        # Place food on the level
        self.food = Point(x, y)
        self.foodRect = pygame.Rect(self.food.x-GRIDSQUARE/2, self.food.y-GRIDSQUARE/2, GRIDSQUARE, GRIDSQUARE)

        # If food is inside snake, try again
        if self.foodRect.colliderect(self.headRect):
            self.place_food()
        

    def play_step(self, game_over):
        
        # Get user input
        key = pygame.key.get_pressed()

        # Left
        if key[pygame.K_LEFT] and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT

        # Right    
        elif key[pygame.K_RIGHT] and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

        # Up
        elif key[pygame.K_UP] and self.direction != Direction.DOWN:
            self.direction = Direction.UP

        # Down
        elif key[pygame.K_DOWN] and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        
        self.rotate_snake(self.direction)
  
        # Move snake in the direction of key pressed
        self.move(self.direction)
        self.snake.insert(0, self.head)
         
        # Check if the player hit anything
        collided_with_wall = self.collided()
        if collided_with_wall == True:
            game_over = True
            return game_over, self.score
        
        # Add 1 to the player score when the snake eats food
        if self.foodRect.colliderect(self.headRect) or self.head == self.food:
            self.score += 1
            self.place_food()
            
        # Remove the last snake segment to move the snake by 1 
        else:
            self.snake.pop()
        
        # Update UI and Clock
        self.update_ui()
        self.clock.tick(SNAKE_SPEED)
        
        # Game over and score
        return game_over, self.score


    def update_ui(self):
        
        # Set background to grass colour
        self.display.blit(self.field, self.field.get_rect())
                        
        for index, point in enumerate(self.snake[1:]):
            current_segment = self.snake[index] 
            next_segment = self.snake[index+1]

            snake_segment = snake_segment_horizontal
            # Check if the segment is the last segment, and if it is then sets the current segment to the correct tail
            if index == len(self.snake) - 2:
                if next_segment.y == current_segment.y:
                    if next_segment.x < current_segment.x:
                        snake_segment = snake_tail_right
                    else:
                        snake_segment = snake_tail_left

                elif next_segment.x == current_segment.x: 
                    if next_segment.y < current_segment.y:
                        snake_segment = snake_tail_down
                    else:
                        snake_segment = snake_tail_up
       
            # If the next segment in the snake is on the same y level and is not the tail, sets the segment to the horizontal segment
            elif current_segment.y == next_segment.y:
                snake_segment = snake_segment_horizontal

            # If the next segment in the snake is on the same x level and is not the tail, sets the segment to the vertical segment
            elif current_segment.x == next_segment.x:
                snake_segment = snake_segment_vertical
            
            # Draws the segment chosen based on the previous logic
            self.display.blit(snake_segment, (point.x, point.y))

        # Draw snake head
        self.display.blit(snake_head, (self.head.x, self.head.y))

        # Draw a cherry on the fruit position
        self.display.blit(snakeFood, (self.food.x, self.food.y))

        # Open high score file to display on screen
        with open(HIGHSCORE_FILE_PATH, "r") as high_score_read:
            high_score = high_score_read.readline()
        high_score_read.close()

        # Display current score and high score on screen
        text = font.render("Score: " + str(self.score) + " High Score: " + high_score, True, BLACK)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def move(self, direction):

        # Get current snake head position
        snake_x_pos = self.head.x
        snake_y_pos = self.head.y

        self.headRect = pygame.Rect(self.head.x-GRIDSQUARE/2, self.head.y-GRIDSQUARE/2, GRIDSQUARE, GRIDSQUARE)

        # Move snake head in direction of arrow key pressed
        if direction == Direction.RIGHT:
            snake_x_pos += GRIDSQUARE
        elif direction == Direction.LEFT:
            snake_x_pos -= GRIDSQUARE
        elif direction == Direction.UP:
            snake_y_pos -= GRIDSQUARE 
        elif direction == Direction.DOWN:
            snake_y_pos += GRIDSQUARE

        self.head = Point(snake_x_pos, snake_y_pos)


    def collided(self):
        game_over = False

        # If snake looping is true, loop the snake to the other side of the screen when the snake hits a side
        if SNAKE_LOOPING == True:
            if self.head.x > self.width:
                self.head = Point(-20, self.head.y)
            elif self.head.x < 0:
                self.head = Point(self.width, self.head.y)
            elif self.head.y > self.height:
                self.head = Point(self.head.x, -20)
            elif self.head.y < 0:
                self.head = Point(self.head.x, self.height)

        # Otherwise, check if snake head hit a wall and end the game if so
        else:
            if self.head.x > self.width - GRIDSQUARE or self.head.x < 0 or self.head.y > self.height - GRIDSQUARE or self.head.y < 0:
                game_over = True

        # Check if snake head hit snake body
        if self.head in self.snake[1:]:
            game_over = True

        return game_over


    def rotate_snake(self, new_direction):

        global snake_head
        # Set the current snake head graphic based on the direction the snake is moving
        match new_direction:

            # moving right
            case Direction.RIGHT:
                snake_head = snake_head_right
            
            # Was moving up
            case Direction.UP:
                snake_head = snake_head_up

            # Was moving down
            case Direction.DOWN:
                snake_head = snake_head_down

            # Was moving left                     
            case Direction.LEFT:
                snake_head = snake_head_left


    def start_game(self):
        global game_over
        game = snake_game()
        while game_over == False:
            game_over, score = game.play_step(game_over)
                
            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN and game_over == True:
                    pygame.quit()
                    quit()

        
        while True:
            self.display.blit(game_over_screen, (0, 0))
            pygame.display.flip()
            
            # Wait 1 second after the game is over before accepting inputs in order to combat accidental keypresses
            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.set_high_score(score)
                        game_over = False 
                        self.start_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.set_high_score(score)
                    pygame.quit()
                    quit()
                    

            clock = pygame.time.Clock()
            clock.tick(60)

    def set_high_score(self, score):
        # Open high score file and change high score if current game beat it
        with open(HIGHSCORE_FILE_PATH, "r") as high_score_read:
            high_score = high_score_read.readline()
            if int(high_score) < score:
                high_score = score
                with open(HIGHSCORE_FILE_PATH, "w") as high_score_write: 
                    high_score_write.write(str(high_score))
                high_score_write.close()
        high_score_read.close()

        print('Final Score', score, 'High Score', high_score)
        

# Start the game    
snake_game_instance = snake_game()
snake_game_instance.start_game()
    
pygame.quit()