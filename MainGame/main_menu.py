import pygame
import sys

WIDTH = 1280
HEIGHT = 720

window = pygame.display.set_mode((WIDTH, HEIGHT))
caption_title = pygame.display.set_caption("Arcade Menu")

pygame.init()

class ScreenItem():
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        window.blit(self.image, self.rect)

    def mouse_over_button(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True

font = pygame.font.SysFont('arial', 25)

# Game buttons
snake_image = pygame.image.load(
    "MainGame/Buttons/snakeimg.png").convert_alpha()
breakout_image = pygame.image.load(
    "MainGame/Buttons/breakoutimg.png").convert_alpha()

# Button texts
snake_title = font.render("Snake", True, 'green')


snake_button = ScreenItem(263.67, 540, snake_image)
snake_text = ScreenItem(263.67, 450, snake_title)
breakout_button = ScreenItem(600, 540, breakout_image)

show_text = False

running = True
while running:

    for event in pygame.event.get():
        # To exit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # User tried to click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Activate Snake
            if snake_button.mouse_over_button(pygame.mouse.get_pos()):
                print("snake clicked")

            # Activate Breakout
            elif breakout_button.mouse_over_button(pygame.mouse.get_pos()):
                print("breakout clicked")

            # No buttons
            else:
                print("no button clicked")

        if event.type == pygame.MOUSEMOTION:
            # Activate Snake
            if snake_button.mouse_over_button(pygame.mouse.get_pos()):
                show_text = True

            # Activate Breakout
            elif breakout_button.mouse_over_button(pygame.mouse.get_pos()):
                # TODO turn on gif here
                pass

            else:
                show_text = False

    window.fill("black")

    snake_button.update()
    breakout_button.update()
    if show_text == True:
        snake_text.update()


    pygame.display.update()
