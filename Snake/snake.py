from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import random
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
snake_head = pygame.image.load('Snake/resources/snakeHead.png')
snake_segment_vertical = pygame.image.load('Snake/resources/snakeSegment.png')
snake_segment_horizontal = pygame.image.load('Snake/resources/snakeSegmentHorizontal.png')
snake_tail_up = pygame.image.load('Snake/resources/snakeTailUp.png')
snake_tail_down = pygame.image.load('Snake/resources/snakeTailDown.png')
snake_tail_left = pygame.image.load('Snake/resources/snakeTailLeft.png')
snake_tail_right = pygame.image.load('Snake/resources/snakeTailRight.png')
snakeFood = pygame.image.load('Snake/resources/food.png')
font = pygame.font.Font('Snake/resources/BPdotsSquareBold.otf', 25)


# Constants
GRIDSQUARE = 20
SNAKE_SPEED = 10
HIGHSCORE_FILE_PATH = 'Snake/snakeScore.txt'
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

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

        # Create starting snake (3 Segments)
        self.snake = [self.head,
                      Point(self.head.x-GRIDSQUARE, self.head.y),
                      Point(self.head.x-(2*GRIDSQUARE), self.head.y)]

        # Set score and food defaults
        self.score = 0
        self.food = None

        # Place food on level
        self.place_food()


    def place_food(self):

        # Find a random x and y coordinate on the display
        x = random.randint(3, (self.width-GRIDSQUARE)//GRIDSQUARE-3)*GRIDSQUARE
        y = random.randint(3, (self.height-GRIDSQUARE)//GRIDSQUARE-3)*GRIDSQUARE

        # Place food omn the level
        self.food = Point(x, y)

        # If food is inside snake, try again
        if self.food in self.snake:
            self.place_food()
        

    def play_step(self, last_direction):

        # Get user input
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Set direction to whichever arrow key is pressed
            if event.type == pygame.KEYDOWN:

                # Left
                if event.key == pygame.K_LEFT and last_direction is not Direction.RIGHT:
                    self.rotate_snake(last_direction, Direction.LEFT)
                    self.direction = last_direction = Direction.LEFT

                # Right
                elif event.key == pygame.K_RIGHT and last_direction is not Direction.LEFT:
                    self.rotate_snake(last_direction, Direction.RIGHT)
                    self.direction = last_direction = Direction.RIGHT

                # Up
                elif event.key == pygame.K_UP and last_direction is not Direction.DOWN:
                    self.rotate_snake(last_direction, Direction.UP)
                    self.direction = last_direction = Direction.UP

                # Down
                elif event.key == pygame.K_DOWN and last_direction is not Direction.UP:
                    self.rotate_snake(last_direction, Direction.DOWN)
                    self.direction = last_direction = Direction.DOWN
                    
        # Move snake in the direction of key pressed
        self.move(self.direction)
        self.snake.insert(0, self.head)
         
        # Check if the player hit themself or a wall, and end the game if they do
        if self.is_hurt():
            game_over = True
            return game_over, self.score, last_direction
        
        # Add 1 to the player score when the snake eats food
        if self.head == self.food:
            self.score += 1
            self.place_food()
            
        # Remove the last snake segment to move the snake by 1 
        else:
            self.snake.pop()
        
        # Update UI and Clock
        self.update_ui()
        self.clock.tick(SNAKE_SPEED)
        
        # Game over and score
        return game_over, self.score, last_direction

        
    def update_ui(self):
        
        # Set background to grass colour
        self.display.blit(self.field, self.field.get_rect())
                        
        for index, point in enumerate(self.snake[1:]):
            current_segment = self.snake[index] 
            next_segment = self.snake[index+1]

            # Check if the segment is the last segment, and if it is then draws a tail depending on the direction
            if index == len(self.snake) - 2:
                if next_segment.y == current_segment.y:
                    if next_segment.x < current_segment.x:
                        self.display.blit(snake_tail_right, (point.x, point.y))        
                    else:
                        self.display.blit(snake_tail_left, (point.x, point.y))   

                elif next_segment.x == current_segment.x: 
                    if next_segment.y < current_segment.y:
                        self.display.blit(snake_tail_down, (point.x, point.y))  
                    else:
                        self.display.blit(snake_tail_up, (point.x, point.y))  

            # Draws a horizontal snake segment if the next segment in the snake is on the same y level
            elif current_segment.y == next_segment.y:
                self.display.blit(snake_segment_horizontal, (point.x, point.y))

            # Draws a horizontal snake segment if the next segment in the snake is on the same x level
            elif current_segment.x == next_segment.x:
                self.display.blit(snake_segment_vertical, (point.x, point.y))
            
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


    def is_hurt(self):

        # Check if snake head hit a wall
        if self.head.x > self.width - GRIDSQUARE or self.head.x < 0 or self.head.y > self.height - GRIDSQUARE or self.head.y < 0:
            return True

        # Check if snake head hit snake body
        if self.head in self.snake[1:]:
            return True

        return False


    def rotate_snake(self, last_direction, new_direction):

        # Get global image files that make up the snake
        global snake_head
        global snake_segment

        #Rotate the snake head and segments based on which direction the snake changed to, and what the last direction was
        match last_direction:

            # Was moving right
            case Direction.RIGHT:
                match new_direction:
                    
                    # Changed direction to up
                    case Direction.UP:
                        snake_head = pygame.transform.rotate(snake_head, 90)
                        #snake_segment = pygame.transform.rotate(snake_segment, 90)

                    # Changed direction to down
                    case Direction.DOWN:
                        snake_head = pygame.transform.rotate(snake_head, 270)
                        #snake_segment = pygame.transform.rotate(snake_segment, 270)
            
            # Was moving up
            case Direction.UP:
                match new_direction:

                    # Changed direction to left
                    case Direction.LEFT:
                        snake_head = pygame.transform.rotate(snake_head, 90)
                        #snake_segment = pygame.transform.rotate(snake_segment, 90)

                    # Changed direction to right
                    case Direction.RIGHT:
                        snake_head = pygame.transform.rotate(snake_head, -90)
                        #snake_segment = pygame.transform.rotate(snake_segment, -90)

            # Was moving down
            case Direction.DOWN:
                match new_direction:

                    # Changed direction to left
                    case Direction.LEFT:
                        snake_head = pygame.transform.rotate(snake_head, 270)
                        #snake_segment = pygame.transform.rotate(snake_segment, 270)

                    # Changed direction to right
                    case Direction.RIGHT:
                        snake_head = pygame.transform.rotate(snake_head, -270)
                        #snake_segment = pygame.transform.rotate(snake_segment, -270)

            # Was moving left                     
            case Direction.LEFT:
                match new_direction:

                    # Changed direction to up
                    case Direction.UP:
                        snake_head = pygame.transform.rotate(snake_head, -90)
                        #snake_segment = pygame.transform.rotate(snake_segment, -90)

                    # Changed direction to down
                    case Direction.DOWN:
                        snake_head = pygame.transform.rotate(snake_head, -270)
                        #snake_segment = pygame.transform.rotate(snake_segment, -270)
# Start the game    
if __name__ == '__main__':
    game = snake_game()
    last_direction = Direction.RIGHT
    while True:
        gameOver, score, last_direction = game.play_step(last_direction)
        if gameOver == True:
            break
    
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
pygame.quit()