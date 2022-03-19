import pygame
import sys
import config
from player import Player, ControllerLayout
from wall import Grid
from time import sleep


class ChadTrouble:

    PROJECTILES = []

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Chad Trouble")

        self.clock = pygame.time.Clock()
        self.running = False

        from weapons import Bow, Sword  # need the import here or else python will throw error
        player_one = Player(ControllerLayout.WASD, Sword())
        player_two = Player(ControllerLayout.ARROW, Bow())

        self.players = [player_one, player_two]

        self.grid = Grid(10, 10)
        self.grid.create()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(config.FPS)
            self.check_events()
            self.update_screen()

    def check_events(self):

        [player.handle_movement(self.grid) for player in self.players]  # updates player movement keys
        [arrow.update() for arrow in ChadTrouble.PROJECTILES]  # handle arrows

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()

            [player.handle_action(event) for player in self.players]  # updates player movement keys

    def update_screen(self):
        self.screen.fill((240, 240, 255))

        self.grid.draw(self.screen)

        [arrow.draw(self.screen) for arrow in ChadTrouble.PROJECTILES]  # draws arrows

        [player.update(self.screen) for player in self.players]  # draws players on screen

        pygame.display.flip()


if __name__ == "__main__":
    ct = ChadTrouble()
    ct.run()
