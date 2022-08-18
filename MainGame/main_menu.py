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
    "MainGame/Buttons/SnakeButton.png").convert_alpha()
breakout_image = pygame.image.load(
    "MainGame/Buttons/BreakoutButton.png").convert_alpha()

# Button texts
play_title = font.render("Click to Play!", True, 'white')

play_text = ScreenItem(0, 0, play_title)

snake_button = ScreenItem(263.67, 540, snake_image)
breakout_button = ScreenItem(657.54, 540, breakout_image)

play_text_show = False

def set_play_text(button):
    play_text.x = button.x
    play_text.y = button.y + 120
    play_text.rect = play_text.image.get_rect(center=(play_text.x, play_text.y))

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
                set_play_text(snake_button)
                play_text_show = True

            # Activate Breakout
            elif breakout_button.mouse_over_button(pygame.mouse.get_pos()):
                set_play_text(breakout_button)
                play_text_show = True

            else:
                play_text_show = False

    window.fill("black")

    snake_button.update()
    breakout_button.update()
    if play_text_show == True:
        play_text.update()


    pygame.display.update()
