import pygame
import math

from settings import *


class Block(pygame.sprite.Sprite):
    def __init__(self, game, position, type, pometla=False):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.type = type
        if type == "spike":
            self.image = pygame.transform.scale(pygame.image.load("assets/spike.png"), (70, 70))
        else:
            self.image = pygame.transform.scale(pygame.image.load("assets/block.png"), (70, 70))
        self.rect = self.image.get_rect()
        self.add(self.game.blocks)
        self.add(self.game.all_sprites)
        self.pos = position
        self.rect.topleft = self.pos
        self.hitbox = pygame.mask.from_surface(self.image)
        self.hitbox_surface = self.hitbox.to_surface()
        self.pomet = pometla

    def update_(self, offset):
        self.rect.x += offset


class Block2(pygame.sprite.Sprite):
    def __init__(self, game, position, type, pometla=False):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        if type == "spike":
            self.image = pygame.transform.scale(pygame.image.load("assets/spike.png"), (70, 70))
        else:
            self.image = pygame.transform.scale(pygame.image.load("assets/block.png"), (70, 70))
        self.rect = self.image.get_rect()
        self.pos = position
        self.rect.topleft = self.pos
        self.hitbox = pygame.mask.from_surface(self.image)
        self.hitbox_surface = self.hitbox.to_surface()
        self.pomet = pometla

    def update_(self, offset):
        self.rect.x += offset


