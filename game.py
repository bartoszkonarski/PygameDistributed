import sys
import pygame

from config import COLORS, FRAMERATE, RESOLUTION, TILEMAPS
from sprites import Player, Block, Floor, Teleport


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Przetwarzanie rozproszone - projekt zaliczeniowy, Bartosz Konarski 200830')
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()

        # self.font = pygame.font.Font('Arial', 32)
        self.running = True

    def drawTilemap(self, zone: str, x_offset: int = 0):
        for i, row in enumerate(TILEMAPS[zone]):
            for j, column in enumerate(row):
                Floor(self, j + x_offset, i, zone)
                if column == 'W':
                    Block(self, j + x_offset, i, zone)
                if column == 'T':
                    Teleport(self, j + x_offset, i, zone)

    def create(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.teleports = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 1, 2)

        self.drawTilemap('FOREST')
        self.drawTilemap('CASTLE', 100)

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