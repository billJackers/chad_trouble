import pygame

class ChadTrouble():

    def __init__(self):
        pygame.init()

        self.screen_width = 800
        self.screen_height = 800

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Chad Trouble")

        self.running = False

    def run(self):
        self.running = True

        while self.running:
            self.check_events()
            self.update_screen()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

    def update_screen(self):
        self.screen.fill((255, 255, 255))

        pygame.display.flip()

if __name__ == "__main__":
    ct = ChadTrouble()
    ct.run()