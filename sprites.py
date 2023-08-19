from typing import Any
import pygame

from config import CHARACTERS_LAYER, SQUARE_SIZE, COLORS, PLAYER_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y) -> None:
        
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

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(COLORS['RED'])

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_move -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.x_move += PLAYER_SPEED
        if keys[pygame.K_w]:
            self.y_move -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.y_move += PLAYER_SPEED

        self.x += self.x_move
        self.y += self.y_move

        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.move()
        
        self.x_move = 0
        self.y_move = 0
        