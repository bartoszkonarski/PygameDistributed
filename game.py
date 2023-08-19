import sys
import pygame

from config import COLORS, FRAMERATE, RESOLUTION
from sprites import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()

        # self.font = pygame.font.Font('Arial', 32)
        self.running = True

    def create(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.tiles = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 1, 2)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def show(self):
        self.screen.fill(COLORS['BLACK'])
        self.all_sprites.draw(self.screen)
        self.clock.tick(FRAMERATE)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.show()
        self.running = False


if __name__ == "__main__":
    g = Game()
    g.create()
    while g.running:
        g.main()
    pygame.quit()
    sys.exit()