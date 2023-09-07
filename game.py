import sys

import pygame
import json

from client.client import Network
from client.consumer import RabbitConsumer
from config import COLORS, FRAMERATE, RESOLUTION, TILEMAPS
from sprites import Attack, Block, Enemy, Floor, Player, Teleport, Button


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Przetwarzanie rozproszone - projekt zaliczeniowy, Bartosz Konarski 200830')
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.enemies_ids = []
        self.font = pygame.font.Font('BreatheFireIii-PKLOB.ttf', 36)
        self.running = True

        self.network = Network('FOREST')

    def drawTilemap(self, zone: str, x_offset: int = 0):
        for i, row in enumerate(TILEMAPS[zone]):
            for j, column in enumerate(row):
                Floor(self, j + x_offset, i, zone)
                if column == 'W':
                    Block(self, j + x_offset, i, zone)
                if column == 'T':
                    Teleport(self, j + x_offset, i, zone)

    def get_enemies_positions(self):
        try:
            players = self.player.send_event("get_positions", position=[self.player.rect.x, self.player.rect.y])

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
        except TypeError:
            self.playing = False          

    def change_server(self, zone_name):
        self.network = Network(zone_name)
        for enemy in self.enemies:
            enemy.kill()
            self.enemies_ids = []


    def create(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.teleports = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 1, 2)
        self.drawTilemap('FOREST')
        self.drawTilemap('CASTLE', 100)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    Attack(self, self.player.rect.x + self.player.width, self.player.rect.y, 'right')
                if event.key == pygame.K_LEFT:
                    Attack(self, self.player.rect.x - self.player.width, self.player.rect.y, 'left')
                if event.key == pygame.K_UP:
                    Attack(self, self.player.rect.x, self.player.rect.y - self.player.width, 'up')
                if event.key == pygame.K_DOWN:
                    Attack(self, self.player.rect.x, self.player.rect.y + self.player.width, 'down')

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

    def game_over(self):
        game_over = True

        current_zone = self.player.current_zone
        forest_q = RabbitConsumer(current_zone)
        forest_scoreboard = json.loads(forest_q.response)

        scoreboard_toggle_button = Button(320-125, 540, 250, 80, COLORS['WHITE'], COLORS['BLACK'], 'EXIT', 24)
        title = self.font.render(current_zone, True, COLORS['BLACK'])
        title_rect = title.get_rect(x=320-title.get_width()/2, y=25)

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if scoreboard_toggle_button.is_pressed(mouse_pos, mouse_pressed):
                game_over = False
                self.running = False

            self.screen.blit(pygame.image.load(f'./assets/bg_{current_zone}.png'), (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(scoreboard_toggle_button.image, scoreboard_toggle_button.rect)
            self.clock.tick(FRAMERATE)
            pygame.display.update()
                

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.show()
        self.game_over()
        self.running = False


if __name__ == "__main__":
    g = Game()
    g.create()
    while g.running:
        g.main()
    pygame.quit()
    sys.exit()