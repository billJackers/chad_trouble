import pygame
from pygame import mixer
from pygame.sprite import Sprite
import pygame.font
import sys
import config
from player import Player, ControllerLayout
from weapons import Sword
from weapons import Bow
from weapons import Arrow
from wall import Grid
import time
from displays import Displays
from start_menu import StartMenu
from button import Button
import time
import random

class ArrowItem(Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load("resources/images/quiver.bmp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.spawn_time = time.time()

    def draw(self):
        image_copy = pygame.transform.scale(self.image, (25, 25))
        self.screen.blit(image_copy, self.rect)

class ChadTrouble:

    def __init__(self):
        """Initialize game"""
        # SCREEN INIT
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Chad Trouble")

        # ITEMS
        self.prev_arrow_spawn_time = time.time()
        self.arrow_spawn_interval = random.uniform(30, 50)
        self.arrow_items = pygame.sprite.Group()

        # START MENU
        self.sm = StartMenu(self)

        # AUDIO INIT
        mixer.init()
        self.song = pygame.mixer.Sound("resources/sounds/temp_song.mp3")
        self.music_volume = 100
        self.song.set_volume(self.music_volume/100)
        self.song.play(-1)

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

        # Spawn arrow after time interval
        if time.time() - self.prev_arrow_spawn_time >= self.arrow_spawn_interval:
            self.spawn_arrows()
            self.prev_arrow_spawn_time = time.time()
            self.arrow_spawn_interval = random.uniform(10, 15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                    sys.exit()
                elif event.key == pygame.K_g:
                    if self.player_one.weapon.weapon_type == "Bow":
                        self.player_one.weapon = Sword()
                    else:
                        self.player_one.weapon = Bow(self)
                elif event.key == pygame.K_o:
                    if self.player_two.weapon.weapon_type == "Bow":
                        self.player_two.weapon = Sword()
                    else:
                        self.player_two.weapon = Bow(self)

            [player.handle_action(event) for player in self.players]  # updates player movement keys

    def update_screen(self):
        """Update the screen"""
        if self.sm.game_active and self.player_one.health > 0 and self.player_two.health > 0:
            self.screen.fill(config.BG_COLOR)
            self.grid.draw(self.screen)
            [arrow.draw(self.screen) for arrow in self.arrows]  # draws arrows
            [player.update(self.screen) for player in self.players]  # draws players on screen
            self.display_items()
            self.displays.update_displays()
        elif self.player_one.health <= 0:
            self.display_win_screen(2)
        elif self.player_two.health <= 0:
            self.display_win_screen(1)

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
                                self.arrows.remove(arrow)

    def display_win_screen(self, winner):
        s = "PLAYER ONE WINS!!!"
        if winner == 2:
            s = "PLAYER TWO WINS!!!"

        font = pygame.font.SysFont(None, 100)
        s_image = font.render(s, True, (0, 0, 0), config.BG_COLOR)
        s_image_rect = s_image.get_rect()
        s_image_rect.center = self.screen_rect.center

    def spawn_arrows(self):
        """Spawn a bow randomly on the map"""
        row = int(random.uniform(1, self.grid.rows-1))
        col = int(random.uniform(1, self.grid.cols-1))
        arrow_item = ArrowItem(self, 35+row*config.HEIGHT/self.grid.rows, 35+col*config.WIDTH/self.grid.cols)

        self.arrow_items.add(arrow_item)

    def display_items(self):
        [arrow.draw() for arrow in self.arrow_items]

        self.check_player_pickup_arrow()

    def check_player_pickup_arrow(self):
        """Detect when player picks up arrows"""

        collisions = pygame.sprite.groupcollide(self.arrow_items, self.players, False, False)
        ret_arrow = pygame.sprite.groupcollide(self.players, self.arrow_items, False, True)

        # Spaghetti
        if collisions:
            for players in collisions.values():
                for player in players:
                    for arrows in ret_arrow.values():
                        for arrow in arrows:
                            player.num_arrows += int(random.uniform(2, 5)) 
                            if player.num_arrows > player.max_arrows:
                                player.num_arrows = player.max_arrows

        # Delete arrow item if it has been around for too long
        for arrow_item in self.arrow_items.copy():
            if time.time() - arrow_item.spawn_time > 15:
                self.arrow_items.remove(arrow_item)

if __name__ == "__main__":
    ct = ChadTrouble()
    ct.run()
