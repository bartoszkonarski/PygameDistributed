from typing import Any
import pygame
from itertools import cycle
import math

from config import (
    BLOCKS_LAYER, 
    CHARACTERS_LAYER, 
    FLOOR_LAYER,
    SQUARE_SIZE, 
    COLORS, 
    PLAYER_SPEED,
    ZONES
)


class Spritesheet:
    def __init__(self, name='Sheet') -> None:
        self.sheet = pygame.image.load(f"assets/{name}.png").convert()

    def get_sprite(self, x, y):
        sprite = pygame.Surface([SQUARE_SIZE, SQUARE_SIZE])
        sprite.set_colorkey(COLORS['BLACK'])
        sprite.blit(self.sheet, (0,0), (x, y, SQUARE_SIZE, SQUARE_SIZE))

        return sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name='Player') -> None:
        
        self.game = game
        self._layer = CHARACTERS_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        self.x = x * SQUARE_SIZE
        self.y = y * SQUARE_SIZE
        self.width = SQUARE_SIZE
        self.height = SQUARE_SIZE

        self.x_move = 0
        self.y_move = 0

        self.name=name

        self.image = Spritesheet().get_sprite(1280,1888)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.current_zone = 'FOREST'
        

    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_move -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.x_move += PLAYER_SPEED
        self.rect.x += self.x_move
        if pygame.sprite.spritecollide(self, self.game.blocks, False):
            self.rect.x -= self.x_move

        if keys[pygame.K_w]:
            self.y_move -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.y_move += PLAYER_SPEED
        self.rect.y += self.y_move
        if pygame.sprite.spritecollide(self, self.game.blocks, False):
            self.rect.y -= self.y_move

        self.x_move = 0
        self.y_move = 0

        if any(list(keys)):
            self.send_event("movement", position=[self.rect.x, self.rect.y])
        

    def change_zone(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and pygame.sprite.spritecollide(self, self.game.teleports, False):
            mult = 100
            zones = cycle(ZONES)
            for zone in zones:
                if zone == self.current_zone:
                    next_zone = next(zones)
                    mult = (ZONES.index(zone) - ZONES.index(next_zone)) * 100
                    self.current_zone = next_zone
                    self.game.change_server(next_zone)
                    break

            for sprite in self.game.all_sprites:
                sprite.rect.x += mult * SQUARE_SIZE

            self.rect.x -= mult * SQUARE_SIZE

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.move()
        self.change_zone()

    def send_event(self, event_type, **kwargs):
        data = {
                "id": self.game.network.id,
                "event_type": event_type,
                "name": self.name,
                **kwargs
            }
        return self.game.network.send(data)
        

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x ,y, zone) -> None:
        
        self.game = game
        self._layer = BLOCKS_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        super().__init__(self.groups)

        self.x = x * SQUARE_SIZE
        self.y = y * SQUARE_SIZE

        self.size = [SQUARE_SIZE, SQUARE_SIZE]

        self.image = Spritesheet(f'{zone}_wall').get_sprite(0,0)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Floor(pygame.sprite.Sprite):
    def __init__(self, game, x, y, zone) -> None:
        self.game = game
        self._layer = FLOOR_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        self.x = x * SQUARE_SIZE
        self.y = y * SQUARE_SIZE
        self.width = SQUARE_SIZE
        self.height = SQUARE_SIZE

        self.image = Spritesheet(f'{zone}_floor').get_sprite(0,0)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Teleport(pygame.sprite.Sprite):
    def __init__(self, game, x, y, zone) -> None:
        self.game = game
        self._layer = FLOOR_LAYER
        self.groups = self.game.all_sprites, self.game.teleports
        super().__init__(self.groups)

        self.x = x * SQUARE_SIZE
        self.y = y * SQUARE_SIZE
        self.width = SQUARE_SIZE
        self.height = SQUARE_SIZE

        self.image = Spritesheet(f'{zone}_teleport').get_sprite(0,0)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, id, x, y) -> None:
        self.game = game
        self.id = id
        self._layer = CHARACTERS_LAYER
        self.groups = self.game.enemies
        super().__init__(self.groups)

        self.x = x * SQUARE_SIZE
        self.y = y * SQUARE_SIZE

        self.size = [SQUARE_SIZE, SQUARE_SIZE]

        self.image = Spritesheet(f'characters/enemy').get_sprite(0,0)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction) -> None:
        self.game = game
        self.x = x 
        self.y = y
        self.size = [SQUARE_SIZE, SQUARE_SIZE]

        self.direction = direction
        self._layer = CHARACTERS_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        super().__init__(self.groups)

        self.animation_loop = 0
        self.image = Spritesheet(f'attacks/right_1').get_sprite(0,0)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

        if hits:
            self.send_event("kill_enemy", id=hits[0].id)

    def send_event(self, event_type, **kwargs):
        data = {
                "id": self.game.network.id,
                "event_type": event_type,
                **kwargs
            }

        return self.game.network.send(data)

    def animate(self):
        animations = [
                    Spritesheet(f'attacks/{self.direction}_1').get_sprite(0,0),
                    Spritesheet(f'attacks/{self.direction}_2').get_sprite(0,0),
                    Spritesheet(f'attacks/{self.direction}_3').get_sprite(0,0),
                    Spritesheet(f'attacks/{self.direction}_4').get_sprite(0,0),
                ]
        
        self.image = animations[math.floor(self.animation_loop)]
        self.image.set_colorkey(COLORS['WHITE'])
        self.animation_loop += 0.5
        if self.animation_loop >=4:
            self.kill()

class Button:
    def __init__(self, x, y, width, height, bg, fg, content, fontsize) -> None:
        self.font = pygame.font.Font('BreatheFireIii-PKLOB.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

# pygame.init()
# screen = pygame.display.set_mode((640, 640))
# clock = pygame.time.Clock()
# image = Spritesheet().get_sprite(449,1920)
# image.set_colorkey(COLORS['WHITE'])
# pygame.image.save(image, 'assets/characters/enemy.png')