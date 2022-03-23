import pygame
import pygame.font
import sys
import pygame.mixer

import config
from button import Button

class StartMenu:

    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.game = game

        self.start_button = Button(300, 100, "START", 0, 0, (116, 1, 113), game)
        self.settings_button = Button(300, 100, "SETTINGS", 0, 100, (137, 41, 133), game)
        self.help_button = Button(300, 100, "HELP", 0, 200, (148, 62, 143), game)
        self.credits_button = Button(300, 100, "CREDITS", 0, 300, (167, 88, 162), game)
        self.quit_button = Button(300, 100, "QUIT", 0, 400, (178, 111, 174), game)

        self.back_button = Button(150, 50, "BACK", 15, 15, (116, 1, 113), game)

        self.buttons = [self.start_button, self.settings_button, self.help_button, self.credits_button, self.quit_button]

        self.game_active = False
        self.start_menu_active = True
        self.settings_page_active = False
        self.help_page_active = False
        self.credits_page_active = False
        
    def check_button_pressed(self, mouse_pos):
        """Check when button has been pressed"""
        
        # Start button
        start_button_clicked = self.start_button.rect.collidepoint(mouse_pos)
        if not self.game_active and self.start_menu_active and start_button_clicked:
            self.game_active = True

        # Settings button
        settings_button_clicked = self.settings_button.rect.collidepoint(mouse_pos)
        if not self.game_active and self.start_menu_active and settings_button_clicked:
            self.start_menu_active = False
            self.settings_page_active = True

        # Help button
        help_button_clicked = self.help_button.rect.collidepoint(mouse_pos)
        if not self.game_active and self.start_menu_active and help_button_clicked:
            self.start_menu_active = False
            self.help_page_active = True

        # Credits button
        credits_button_clicked = self.credits_button.rect.collidepoint(mouse_pos)
        if self.start_menu_active and credits_button_clicked:
            self.start_menu_active = False
            self.credits_page_active = True

        # Quit button
        quit_button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if not self.game_active and quit_button_clicked and self.start_menu_active:
            pygame.quit()
            sys.exit()

        # Back button
        back_button_clicked = self.back_button.rect.collidepoint(mouse_pos)
        if not self.start_menu_active and back_button_clicked:
            self.start_menu_active = True
            self.settings_page_active = False
            self.help_page_active = False
            self.credits_page_active = False

    def display(self):
        if not self.game_active:

            if not self.start_menu_active:
                self.back_button.draw_button()

            if self.credits_page_active:
                self.display_page('resources/images/credits_label.png')
            elif self.help_page_active:
                self.display_page('resources/images/help_label.png')
            elif self.settings_page_active:
                self.display_settings()
            elif self.start_menu_active:
                self.display_image()

                for button in self.buttons:
                    button.draw_button()

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

    def display_page(self, label):
        image = pygame.image.load(label)

        height_to_width_ratio = image.get_rect().height/image.get_rect().width

        image = pygame.transform.scale(image, (0.75 * config.HEIGHT / height_to_width_ratio, config.HEIGHT * 0.75))

        image_rect = image.get_rect()

        image_rect.center = self.screen_rect.center

        self.screen.blit(image, image_rect)

    def display_settings(self):
        self.display_page('resources/images/settings_label.png')
        music_minus_button = Button(50, 50, "-", self.screen_rect.centerx - 100, self.screen_rect.centery-15, (137, 41, 133), self.game)
        music_plus_button = Button(50, 50, "+", self.screen_rect.centerx + 50, self.screen_rect.centery-15, (137, 41, 133), self.game)

        font = pygame.font.SysFont(None, 50)

        music_volume_image = font.render(str(self.game.music_volume), True, (255, 255, 255), (34, 42, 53))
        music_volume_rect = music_volume_image.get_rect()
        music_volume_rect.centerx = self.screen_rect.centerx
        music_volume_rect.centery = self.screen_rect.centery+5

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if music_minus_button.rect.collidepoint(mouse_pos) and self.game.music_volume > 0:
                    self.game.music_volume -= 10
                elif music_plus_button.rect.collidepoint(mouse_pos) and self.game.music_volume < 100:
                    self.game.music_volume += 10
                else:
                    self.check_button_pressed(mouse_pos)

        music_minus_button.draw_button()
        music_plus_button.draw_button()
        self.screen.blit(music_volume_image, music_volume_rect)

        self.game.song.set_volume(self.game.music_volume/100)