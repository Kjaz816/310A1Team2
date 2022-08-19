from os import environ
from tracemalloc import start
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame.locals import Rect
from enum import Enum
from collections import namedtuple
from random import randint

pygame.init()

# Open image files for graphics
game_over_screen = pygame.image.load('Breakout/resources/gameOverScreenBreakout.png')
you_win_screen = pygame.image.load('Breakout/resources/winScreenBreakout.png')
press_to_start_screen = pygame.image.load('Breakout/resources/pressToStartScreenBreakout.png')

extra_ball = pygame.image.load('Breakout/resources/extraBall.png')
strong_ball = pygame.image.load('Breakout/resources/strongBall.png')

# Window resolution (Default 1280 x 720)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Other setup
clock = pygame.time.Clock()
fps = 60

# Number of bricks in the wall (Default 9 x 9)
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
FAKE_BALL_COLOUR = (255, 255, 255)

# Paddle setup (Do not change)
PADDLE_HEIGHT = 15
PADDLE_WIDTH = 140
PADDLE_Y_POS = WINDOW_HEIGHT - 3 * (PADDLE_HEIGHT / 2)

# Game Settings 
level = 1  #(1, 2, or anything else for randomly generated level)
BALL_RADIUS = 10
BALL_SPEED_X = 0
BALL_SPEED_Y = -4
PADDLE_SPEED = 10
BALL_MAX_SPEED = 5

# Global variables for game
start_game = False
game_over = 0
powerups = []
ball_count = 0
balls = []

class wall():
    def __init__(self):

        # Create the wall dimensions based on the window dimensions and number of bricks wanted
        self.width = WINDOW_WIDTH // BRICK_COLS
        self.height = 40

    def create_wall(self):

        # Create an empty list that will contain the blocks
        self.brick_wall = [] 
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
                
                # Assign brick strength based on the level that the player chose
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
            
            # Add brick row to the overall brick wall list
            self.brick_wall.append(brick_row)

    def draw_wall(self, display):
        for row in self.brick_wall:
            for brick in row:

                # Assign colour based on block strength
                if brick[1] == 3:
                    brick_colour = RED_BLOCK
                elif brick[1] == 2:
                    brick_colour = BLUE_BLOCK
                elif brick[1] == 1:
                    brick_colour = GREEN_BLOCK

                # Draw brick
                pygame.draw.rect(display, brick_colour, brick[0])
                pygame.draw.rect(display, BACKGROUND, brick[0], 2)
        

class paddle():
    def __init__(self):

        # Define paddle dimensions and attributes
        self.height = PADDLE_HEIGHT
        self.width = PADDLE_WIDTH
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

        # Draw paddle
        pygame.draw.rect(display, PADDLE_COLOUR, self.rect)
        pygame.draw.rect(display, PADDLE_OUTLINE, self.rect, 3)


class ball():
    def __init__(self, x, y):

        # Define ball dimensions and attributes
        self.ball_rad = BALL_RADIUS
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.game_over = 0
        self.invincible = False

    def draw(self, display, true_ball):
        if true_ball == True:

            # Draw ball in grey if it is the original ball, and white if it is a powerup ball
            pygame.draw.circle(display, PADDLE_COLOUR, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
            pygame.draw.circle(display, PADDLE_OUTLINE, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)
        
        else:
            pygame.draw.circle(display, FAKE_BALL_COLOUR, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

    def move(self):

        powerup = []
        powerup.append(0)
        collision_threshold = 5
        
        game_won = True

        row_count = 0
        for row in brick_wall.brick_wall:
            brick_count = 0
            for brick in row:
                if self.rect.colliderect(brick[0]):
                    # Check where collision came from
                    # Above:
                    if abs(self.rect.bottom - brick[0].top) < collision_threshold and self.speed_y > 0:
                        if self.invincible == False:
                            self.speed_y *= -1
                    # Below:
                    if abs(self.rect.top - brick[0].bottom) < collision_threshold and self.speed_y < 0:
                        if self.invincible == False:
                            self.speed_y *= -1
                    # Left:
                    if abs(self.rect.right - brick[0].left) < collision_threshold and self.speed_y > 0:
                        if self.invincible == False:
                            self.speed_x *= -1
                    # Right:
                    if abs(self.rect.left - brick[0].right) < collision_threshold and self.speed_y < 0:
                        if self.invincible == False:
                            self.speed_x *= -1
                    
                    # Damage block by 1 if it has at least 2 health
                    if brick_wall.brick_wall[row_count][brick_count][1] > 1:
                        brick_wall.brick_wall[row_count][brick_count][1] -= 1
                    else:
                        
                        # Spawn a powerup with a 33% chance if the block is broken
                        if randint(1, 3) == 3:
                            powerup[0] = randint(1, 2)
                            powerup_pos = [brick_wall.brick_wall[row_count][brick_count][0].x, brick_wall.brick_wall[row_count][brick_count][0].y]
                            powerup.append(powerup_pos)
                        
                        # Set the block rectangle to be invisible if the block is broken
                        brick_wall.brick_wall[row_count][brick_count][0] = (0, 0, 0, 0)

                # Check if current block exists, and if it does then game over must be false
                if brick_wall.brick_wall[row_count][brick_count][0] != (0, 0, 0, 0):
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
            self.invincible = False
        
        # Check if player missed the ball
        if self.rect.bottom > WINDOW_HEIGHT + BALL_RADIUS * 2:
            global ball_count
            ball_count -= 1
            if self in balls:
                balls.remove(self)

        # Check for collision with paddle
        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_threshold and self.speed_y > 0:

                # Reverse Y direction of the ball if player hits the ball with paddle
                self.speed_y *= -1
                collision_pos = player_paddle.rect.left - PADDLE_WIDTH / 2 - self.rect.left
                # Alter the X direction of the ball based on the direction the paddle is moving
                self.speed_x += -((collision_pos / 20) + 6.5) * 2

                # Set the balls speed to the max speed parameter if it is above the max speed
                if self.speed_x > BALL_MAX_SPEED:
                    self.speed_x = BALL_MAX_SPEED
                elif self.speed_x < 0 and self.speed_x < -BALL_MAX_SPEED:
                    self.speed_x = -BALL_MAX_SPEED
        
        # Move the ball based on its speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        return self.game_over, powerup

class power_up:
    def __init__(self, type, x, y):
        self.power_up_type = ""
        # Define powerup location and rectangle to be used for collision
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 30, 30)
        if type == 1:
            self.power_up_type = "extra_ball"
        elif type == 2:
            self.power_up_type = "strong_ball"

    def draw(self, display):

        # Draw correct powerup image on the powerup rectangle location
        if self.power_up_type == "extra_ball":
            display.blit(extra_ball, (self.rect.x, self.rect.y)) 
        elif self.power_up_type == "strong_ball":
            display.blit(strong_ball, (self.rect.x, self.rect.y)) 
        pygame.display.flip()
  

    def move(self):

        # Drop the powerup after it is spawned
        self.rect.y += 2

        # Remove the powerup if it hits the bottom of the screen
        if self.rect.y > WINDOW_HEIGHT:
            powerups.remove(self)

        # Remove the powerup and add a ball if the player collects the powerup
        elif self.rect.colliderect(player_paddle):
            if self.power_up_type == "extra_ball":
                global ball_count
                powerups.remove(self)
                ball_count += 1

            elif self.power_up_type == "strong_ball":
                firstBall.invincible = True
                powerups.remove(self)


class breakout_game:
    def __init__(self, width = WINDOW_WIDTH, height = WINDOW_HEIGHT):

        # Set display resolution
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        self.display.fill(BACKGROUND)
        
        # Set window title
        pygame.display.set_caption('Breakout')
 
    def play_step(self, game_over):
        self.update_ui()
        if game_over == 0:
            if start_game == True:
                game_over, powerup = firstBall.move()
                for current_ball in balls:
                    game_over, powerup = current_ball.move()
                
                # Add a powerup to the powerup list if the 33% chance occurs
                if powerup[0] != 0 and firstBall.invincible == False:
                    new_powerup = power_up(powerup[0], powerup[1][0], powerup[1][1])

                    # Only create a new strong ball powerup if none currently exist
                    if new_powerup.power_up_type == "strong_ball":
                        strong_ball_exists = False
                        for item in powerups:
                            if item.power_up_type == "strong_ball":
                                strong_ball_exists = True
                            
                        if strong_ball_exists == False:
                            powerups.append(new_powerup)
                    
                    else: 
                        powerups.append(new_powerup)
                    
                
                # Draw all powerups in the powerup list
                for item in powerups:
                    item.draw(self.display)
                    item.move()
                    pygame.display.flip()

                player_paddle.move()

            # Check if the player has missed the main ball, and if so then return -1
            if ball_count == -1:
                game_over = -1

        return game_over
        
    def update_ui(self):

        # Draw the paddle and wall
        player_paddle.draw(self.display)
        brick_wall.draw_wall(self.display)

        if start_game == False:
                game.display.blit(press_to_start_screen, (0, 0))
                pygame.display.flip()
                

        # Create a new ball if a powerup was collected
        if len(balls) < ball_count:
            new_ball = ball(player_paddle.rect.x + player_paddle.width // 2, player_paddle.rect.y - player_paddle.height - 5)
            balls.append(new_ball)

        # Draw all balls
        firstBall.draw(self.display, True)
        for current_ball in balls:
            current_ball.draw(self.display, False)

        # Show the game over screen if the player misses the main ball
        if game_over == -1:
            self.display.blit(game_over_screen, (0, 0))

        # Show the you win screen if the player destroys all blocks
        if game_over == 1:
            game.display.blit(you_win_screen, (0, 0))
        pygame.display.flip()

        



if __name__ == '__main__':
    
    # Start Game
    game = breakout_game()

    # Setup 
    brick_wall = wall()
    brick_wall.create_wall()
    player_paddle = paddle()
    firstBall = ball(player_paddle.x + player_paddle.width // 2, player_paddle.y - player_paddle.height - 5)
    

    while True:
        clock.tick(fps)
        game_over = game.play_step(game_over)
        game.display.fill(BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and game_over == 0:
                start_game = True

            if event.type == pygame.MOUSEBUTTONDOWN and game_over != 0:
                pygame.quit()
                quit()
    
pygame.quit()