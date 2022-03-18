import pygame
import sys
import config
from player import Player, ControllerLayout


class ChadTrouble:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Chad Trouble")

        self.clock = pygame.time.Clock()
        self.running = False

        player_one = Player(ControllerLayout.WASD)
        player_two = Player(ControllerLayout.ARROW)
        self.players = [player_one, player_two]

    def run(self):
        self.running = True

        while self.running:
            self.clock.tick(config.FPS)
            self.check_events()
            self.update_screen()

    def check_events(self):

        [player.handle_movement() for player in self.players]  # updates player movement keys

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()

    def update_screen(self):
        self.screen.fill((255, 255, 255))

        [player.update(self.screen) for player in self.players]  # draws players on screen

        pygame.display.flip()


if __name__ == "__main__":
    ct = ChadTrouble()
    ct.run()