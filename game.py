import sys

import pygame

from client.client import Network
from config import COLORS, FRAMERATE, RESOLUTION, TILEMAPS
from sprites import Block, Floor, Player, Teleport, Enemy
import json

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Przetwarzanie rozproszone - projekt zaliczeniowy, Bartosz Konarski 200830')
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.enemies_ids = []
        # self.font = pygame.font.Font('Arial', 32)
        self.running = True

        self.network = Network()

    def drawTilemap(self, zone: str, x_offset: int = 0):
        for i, row in enumerate(TILEMAPS[zone]):
            for j, column in enumerate(row):
                Floor(self, j + x_offset, i, zone)
                if column == 'W':
                    Block(self, j + x_offset, i, zone)
                if column == 'T':
                    Teleport(self, j + x_offset, i, zone)

    def get_enemies_positions(self):
        players = self.player.send_event("get_positions",position=[self.player.rect.x, self.player.rect.y])

        for player in players:
            if player == self.network.id:
                continue
            if player not in self.enemies_ids:
                Enemy(self, player, *players[player].get('position'))
                self.enemies_ids.append(player)
            else:
                for enemy in self.enemies:
                    if enemy.id == player:
                        enemy.rect.x, enemy.rect.y = players[player].get('position')

        for enemy in self.enemies:
            if enemy.id not in players:
                if enemy.id in self.enemies_ids:
                    self.enemies_ids.remove(enemy.id)
                enemy.kill()          

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
        self.get_enemies_positions()
        self.enemies.update()

    def show(self):
        self.screen.fill(COLORS['BLACK'])
        self.all_sprites.draw(self.screen)
        self.enemies.draw(self.screen)
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