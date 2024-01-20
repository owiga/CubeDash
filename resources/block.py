import pygame
import math

from settings import *


class Block(pygame.sprite.Sprite):
    def __init__(self, game, position, type, pometla=False):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.type = type
        self.image = pygame.transform.scale(pygame.image.load(blocks.get(type)).convert_alpha(), (70, 70))
        self.rect = self.image.get_rect()
        self.add(self.game.blocks)
        self.pos = position
        self.rect.topleft = self.pos
        self.hitbox = pygame.mask.from_surface(self.image)
        self.hitbox_surface = self.hitbox.to_surface()
        self.pomet = pometla

    def update(self, offset):
        self.rect.x += offset
        if self.rect.right < 0:
            self.kill()



