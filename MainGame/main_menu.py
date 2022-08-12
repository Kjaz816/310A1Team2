import pygame
import sys

WIDTH = 1280
HEIGHT = 720

window = pygame.display.set_mode((WIDTH, HEIGHT))
caption_title = pygame.display.set_caption("Arcade Menu")

class Button():
    def __init__(self, x, y, image, gif_image):
        self.image = image
        self.gif_image = gif_image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        window.blit(self.image, self.rect)

    def button_clicked(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True

# Game buttons
snake_image = pygame.image.load("MainGame/Buttons/snakeimg.png").convert_alpha()
breakout_image = pygame.image.load("MainGame/Buttons/breakoutimg.png").convert_alpha()

snake_button = Button(263.67, 540, snake_image, "no gif yet")
breakout_button = Button(527.32, 540, breakout_image, "no gif yet")

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
            if snake_button.button_clicked(pygame.mouse.get_pos()):
                print("snake clicked")

            # Activate Breakout
            elif breakout_button.button_clicked(pygame.mouse.get_pos()):
                print("breakout clicked")
                
            # No buttons
            else:
                print("no button clicked")
            
    window.fill("black")

    snake_button.update()

    pygame.display.update()