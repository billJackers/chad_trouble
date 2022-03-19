import pygame
import sys
import config
from player import Player, ControllerLayout
from wall import Grid
from time import sleep
import time


class ChadTrouble:

    def __init__(self):
        # SCREEN INIT
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Chad Trouble")

        # CLOCK
        self.clock = pygame.time.Clock()
        self.running = False

        # PLAYERS
        from weapons import Bow, Sword  # need the import here or else python will throw error
        player_one = Player(ControllerLayout.WASD, Sword())
        player_two = Player(ControllerLayout.ARROW, Bow(self))
        self.players = [player_one, player_two]

        # ARROWS
        self.arrows = pygame.sprite.Group()

        # MAP
        self.walls = pygame.sprite.Group()
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
        [arrow.update() for arrow in self.arrows]  # handle arrows

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()

            [player.handle_action(event) for player in self.players]  # updates player movement keys

        self.check_arrow_wall_collisions()

    def update_screen(self):
        self.screen.fill((240, 240, 255))

        self.grid.draw(self.screen)

        [arrow.draw(self.screen) for arrow in self.arrows]  # draws arrows

        [player.update(self.screen) for player in self.players]  # draws players on screen

        pygame.display.flip()

    def check_arrow_wall_collisions(self):
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

if __name__ == "__main__":
    ct = ChadTrouble()
    ct.run()
