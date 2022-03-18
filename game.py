import pygame
import sys
import config
from player import Player, ControllerLayout
from wall import Wall

from time import sleep

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

        self.walls = pygame.sprite.Group()
        self.generate_walls()

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

        for wall in self.walls.sprites():
            wall.draw()

        pygame.display.flip()

    def generate_walls(self):
        for x in range(1 + int(config.WIDTH / config.WALL_HEIGHT)):
            for y in range(1 + int(config.HEIGHT / config.WALL_HEIGHT)):
                vertical_wall = Wall(self)
                vertical_wall.rect.x = x * config.WALL_HEIGHT
                vertical_wall.rect.y = y * config.WALL_HEIGHT
                vertical_wall.rect.width = config.WALL_WIDTH
                vertical_wall.rect.height = config.WALL_HEIGHT
                
                horizontal_wall = Wall(self)
                horizontal_wall.rect.x = x * config.WALL_HEIGHT
                horizontal_wall.rect.y = y * config.WALL_HEIGHT
                horizontal_wall.rect.width = config.WALL_HEIGHT
                horizontal_wall.rect.height = config.WALL_WIDTH

                self.walls.add(vertical_wall)
                self.walls.add(horizontal_wall)


if __name__ == "__main__":
    ct = ChadTrouble()
    ct.run()
