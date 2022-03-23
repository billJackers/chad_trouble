import pygame
from pygame import mixer
import sys
import config
from player import Player, ControllerLayout
from wall import Grid
from time import sleep
import time
from displays import Displays
from start_menu import StartMenu

class ChadTrouble:

    def __init__(self):
        """Initialize game"""
        # SCREEN INIT
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Chad Trouble")

        # START MENU
        self.sm = StartMenu(self)

        # AUDIO INIT
        mixer.init()
        mixer.music.load("resources/sounds/temp_song.mp3")
        mixer.music.set_volume(1)
        mixer.music.play(-1)

        # CLOCK
        self.clock = pygame.time.Clock()
        self.running = False

        # PLAYERS
        from weapons import Bow, Sword  # need the import here or else python will throw error
        self.player_one = Player(ControllerLayout.WASD, Sword())
        self.player_two = Player(ControllerLayout.ARROW, Sword())
        self.players = pygame.sprite.Group()
        self.players.add(self.player_one)
        self.players.add(self.player_two)

        # ARROWS
        self.arrows = pygame.sprite.Group()

        # MAP
        self.walls = pygame.sprite.Group()
        self.grid = Grid(10, 10)
        self.grid.create()

        # DISPLAYS
        self.displays = Displays(self)

    def run(self):
        """Game loop"""
        while not self.sm.game_active:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.sm.check_button_pressed(mouse_pos)

            self.screen.fill((76, 31, 31))
            self.sm.display()
            pygame.display.flip()

        self.running = True
        while self.running:
            self.clock.tick(config.FPS)
            self.check_events()
            self.update_screen()

    def check_events(self):
        """Check keyboard events and collisions"""

        # CHECK COLLISIONS
        self.check_arrow_wall_collisions()
        self.check_arrow_player_collisions()

        [player.handle_movement(self.grid) for player in self.players]  # updates player movement keys
        [arrow.update() for arrow in self.arrows]  # handle arrows

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_q:
                self.running = False
                sys.exit()

            [player.handle_action(event) for player in self.players]  # updates player movement keys

    def update_screen(self):
        """Update the screen"""
        self.screen.fill(config.BG_COLOR)
        self.grid.draw(self.screen)
        [arrow.draw(self.screen) for arrow in self.arrows]  # draws arrows
        [player.update(self.screen) for player in self.players]  # draws players on screen
        self.displays.update_displays()
        pygame.display.flip()

    def check_arrow_wall_collisions(self):
        """Check for when an arrow hits a wall"""
        collisions = pygame.sprite.groupcollide(self.grid.walls, self.arrows, False, False, collided=pygame.sprite.collide_mask)

        if collisions:
            for arrows in collisions.values():
                for arrow in arrows:
                    arrow.alive = False
                    if arrow.inactive_start_time == 0:
                        arrow.inactive_start_time = time.time()

                    # Delete arrow 3 seconds it has hit a wall
                    if time.time() - arrow.inactive_start_time >= 5:
                        self.arrows.remove(arrow)
                        del arrow

    def check_arrow_player_collisions(self):
        """Check for when an arrow hits a player"""
        collisions = pygame.sprite.groupcollide(self.arrows, self.players, False, False, collided=pygame.sprite.collide_mask)
        ret_arrow = pygame.sprite.groupcollide(self.players, self.arrows, False, False)

        if collisions:
            for players in collisions.values():
                for player in players:
                    for arrows in ret_arrow.values():
                        for arrow in arrows:
                            if arrow.alive and arrow.input_type != player.input_keys:
                                player.health -= arrow.damage
                                print(player.health)
                                self.arrows.remove(arrow)

if __name__ == "__main__":
    ct = ChadTrouble()
    ct.run()
