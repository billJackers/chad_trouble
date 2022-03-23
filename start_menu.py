import pygame
import pygame.font
import sys

import config
from button import Button

class StartMenu:

    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.start_button = Button(300, 100, "START", 0, 0, (116, 1, 113), game)
        self.settings_button = Button(300, 100, "SETTINGS", 0, 100, (137, 41, 133), game)
        self.help_button = Button(300, 100, "HELP", 0, 200, (148, 62, 143), game)
        self.credits_button = Button(300, 100, "CREDITS", 0, 300, (167, 88, 162), game)
        self.quit_button = Button(300, 100, "QUIT", 0, 400, (178, 111, 174), game)

        self.game_active = False
    
    def check_button_pressed(self, mouse_pos):
        """Check when button has been pressed"""
        # Start button
        start_button_clicked = self.start_button.rect.collidepoint(mouse_pos)
        if not self.game_active and start_button_clicked:
            self.game_active = True

        # Quit button
        quit_button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if not self.game_active and quit_button_clicked:
            pygame.quit()
            sys.exit()

    def display(self):
        if not self.game_active:
            self.display_image()

            self.start_button.draw_button()
            self.settings_button.draw_button()
            self.help_button.draw_button()
            self.credits_button.draw_button()
            self.quit_button.draw_button()

            self.display_title()

    def display_title(self):
        # font = pygame.font.SysFont(None, 150)
        
        # chad_label = font.render("CHAD", True, (255, 255, 255), (15, 15, 15))
        # chad_label_rect = chad_label.get_rect()
        # chad_label_rect.left = 20
        # chad_label_rect.bottom = self.screen_rect.bottom - 150

        # trouble_label = font.render("TROUBLE", True, (255, 255, 255), (15, 15, 15))
        # trouble_label_rect = trouble_label.get_rect()
        # trouble_label_rect.left = 20
        # trouble_label_rect.bottom = self.screen_rect.bottom - 50

        # self.screen.blit(chad_label, chad_label_rect)
        # self.screen.blit(trouble_label, trouble_label_rect)

        image = pygame.image.load("resources/images/title_label.png")

        height_to_width_ratio = image.get_rect().height/image.get_rect().width
        image = pygame.transform.scale(image, (300/height_to_width_ratio, 300))

        image_rect = image.get_rect()

        image_rect.left = self.screen_rect.left
        image_rect.top = 525

        self.screen.blit(image, image_rect)

    def display_image(self):
        image = pygame.image.load('resources/images/start_menu_image.png')

        height_to_width_ratio = image.get_rect().height/image.get_rect().width

        image = pygame.transform.scale(image, (config.HEIGHT / height_to_width_ratio, config.HEIGHT))

        image_rect = image.get_rect()

        image_rect.right = self.screen_rect.right+30
        image_rect.top = self.screen_rect.top

        self.screen.blit(image, image_rect)