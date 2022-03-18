import pygame
import sys
import config
from player import Player, ControllerLayout
from wall import Wall
from arrow import Arrow

import random

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

        self.player_group = pygame.sprite.Group()
        self.player_group.add(player_one)
        self.player_group.add(player_two)

        self.players = [player_one, player_two]

        self.walls = pygame.sprite.Group()
        self.generate_side_walls()

        self.generate_maze(0, int(config.WIDTH/config.WALL_HEIGHT), 0, int(config.HEIGHT/config.WALL_HEIGHT))

        self.arrows = pygame.sprite.Group()

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.fire_arrow(self.players[0])
                if event.key == pygame.K_p:
                    self.fire_arrow(self.players[1])

        self.check_arrow_wall_collisions()

    def update_screen(self):
        self.screen.fill((255, 255, 255))

        [player.update(self.screen) for player in self.players]  # draws players on screen

        for wall in self.walls.sprites():
            wall.draw()

        self.arrows.update(self.screen)

        for arrow in self.arrows.sprites():
            arrow.draw(self.screen)

        pygame.display.flip()

    def generate_side_walls(self):
        # Top and bottom
        for x in range(int(config.WIDTH/config.WALL_HEIGHT)):
            top_wall = Wall(self)
            top_wall.rect = pygame.Rect(x * config.WALL_HEIGHT, 0, config.WALL_HEIGHT, config.WALL_WIDTH)

            bottom_wall = Wall(self)
            bottom_wall.rect = pygame.Rect(x * config.WALL_HEIGHT, config.HEIGHT - config.WALL_WIDTH, config.WALL_HEIGHT, config.WALL_WIDTH)

            self.walls.add(top_wall)
            self.walls.add(bottom_wall)

        # Left and right
        for y in range(int(config.HEIGHT/config.WALL_HEIGHT)):
            left_wall = Wall(self)
            left_wall.rect = pygame.Rect(0, y * config.WALL_HEIGHT, config.WALL_WIDTH, config.WALL_HEIGHT)

            right_wall = Wall(self)
            right_wall.rect = pygame.Rect(config.WIDTH - config.WALL_WIDTH, y * config.WALL_HEIGHT, config.WALL_WIDTH, config.WALL_HEIGHT)

            self.walls.add(left_wall)
            self.walls.add(right_wall)

    def generate_maze(self, start_x, end_x, start_y, end_y):
        if end_x - start_x <= 1 or end_y - start_y <= 2:
            return
        # Horizontal
        hole = int(random.uniform(start_x, end_x-1))
        y_level = int(random.uniform(start_y, end_y-1))

        for x in range(start_x, end_x):
            if x != hole:
                new_wall = Wall(self)
                new_wall.rect = pygame.Rect(x * config.WALL_HEIGHT, y_level * config.WALL_HEIGHT, config.WALL_HEIGHT, config.WALL_WIDTH)
                self.walls.add(new_wall)

        # Vertical
        hole = int(random.uniform(start_y, end_y-1))
        x_level = int(random.uniform(start_x, end_x-1))

        for y in range(start_y, end_y):
            if y != hole:
                new_wall = Wall(self)
                new_wall.rect = pygame.Rect(x_level * config.WALL_HEIGHT, y * config.WALL_HEIGHT, config.WALL_WIDTH, config.WALL_HEIGHT)
                self.walls.add(new_wall)

        self.generate_maze(start_x, x_level, start_y, y_level)
        self.generate_maze(x_level, end_x, start_y, y_level)
        self.generate_maze(start_x, x_level, y_level, end_y)
        self.generate_maze(x_level, end_x, y_level, end_y)

    def fire_arrow(self, sprite):
        new_arrow = Arrow(sprite)
        self.arrows.add(new_arrow)

    def check_arrow_wall_collisions(self):
        collisions = pygame.sprite.groupcollide(self.walls, self.arrows, False, False)

        if collisions:
            for arrows in collisions.values():
                for arrow in arrows:
                    arrow.set_inactive()

    def check_player_wall_collisions(self):
        collisions = pygame.sprite.groupcollide(self.walls, self.player_group, False, False)

        if collisions:
            for players in collisions.values():
                for player in players:
                    # TODO
                    continue

if __name__ == "__main__":
    ct = ChadTrouble()
    ct.run()
