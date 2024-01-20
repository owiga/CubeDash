import pygame
import random

from resources.particles import Particle
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.len = 0
        self.game = game
        self.orig_image = pygame.transform.scale(pygame.image.load("assets/skin1.png").convert_alpha(), (70, 70))
        self.speedx = 10
        self.is_jumping = False
        self.falling = False
        self.counter = GRAVITY
        self.angle = 0
        self.add(self.game.players)
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 670
        self.hitbox = pygame.mask.from_surface(self.image)
        self.hitbox_surface = self.hitbox.to_surface()
        self.last = 0

    @staticmethod
    def ch_angle(angle):
        if angle <= 0:
            if -70 >= angle >= -90 or angle <= -90:
                if -169 >= angle >= -180 or angle <= -180:
                    if angle <= -270:
                        if -360 <= angle <= -270:
                            return -270
                        elif angle <= -360:
                            return 0
                        return -270
                    return -180
                return -90
            return 0

    def gravity(self):
        if self.is_jumping:
            self.angle -= 6
            if self.counter >= -GRAVITY:
                self.rect.y -= self.counter
                self.counter -= 1

                # print("В прыжке", self.angle)
            else:
                self.angle = self.ch_angle(self.angle)
                self.is_jumping = False
                self.counter = GRAVITY

                # print("В прыжке2", self.angle)
            self.pos = self.rect.center
            if self.angle == -360:
                self.angle += 354
            self.image = pygame.transform.rotate(self.orig_image, self.angle)
            self.rect = self.image.get_rect(center=self.pos)
        elif self.falling:
            if self.last > 1:
                # print("падаю", self.angle)
                self.angle -= 6
                self.pos = self.rect.center
                if self.angle <= -360:
                    self.angle += 354
                self.image = pygame.transform.rotate(self.orig_image, self.angle)
                self.rect = self.image.get_rect(center=self.pos)
                # print("Градус в конце цикла падения -", self.angle)
            else:
                # print("коснулся", self.angle, self.counter)

                self.pos = self.rect.center
                self.reangle = self.ch_angle(self.angle)
                if self.reangle is None:
                    self.reangle = 0
                self.angle = self.reangle
                self.image = pygame.transform.rotate(self.orig_image, self.angle)
                self.rect = self.image.get_rect(center=self.pos)
            self.rect.y += 13

        else:
            self.create_particles(self.rect.bottomleft)
            self.pos = self.rect.center
            self.reangle = self.ch_angle(self.angle)
            self.angle = self.reangle
            if self.angle <= -360:
                self.angle += 354
            self.image = pygame.transform.rotate(self.orig_image, self.angle)
            self.rect = self.image.get_rect(center=self.pos)
            self.create_particles(self.rect.bottomleft)

    def collide(self):
        blocks_hit_list = pygame.sprite.spritecollide(self, self.game.blocks, False)
        self.len = len(blocks_hit_list)
        if self.len == 0:
            self.last += 1
        if len(blocks_hit_list) > 0:
            for block in blocks_hit_list:
                overlapmask = self.hitbox.overlap_mask(block.hitbox, (
                    block.rect.topleft[0] - self.rect.topleft[0],
                    block.rect.topleft[1] - self.rect.topleft[1]))
                if block.rect.bottom > self.rect.top > block.rect.top:
                    self.falling = False
                    self.is_jumping = False
                    self.counter = GRAVITY
                    self.die()
                elif block.rect.top - 1 <= self.rect.bottom <= block.rect.bottom and self.falling and block.type not in range(1, 4):  # na bloke stoyat'
                    self.rect.bottom = block.rect.top + 1
                    self.is_jumping = False
                    self.falling = False
                    self.last = 0
                    self.counter = GRAVITY
                elif overlapmask.count() > 70:
                    self.game.screen.blit(overlapmask.to_surface(), self.rect.topleft)
                    self.die()
                if block.rect.top <= self.rect.top <= block.rect.bottom:
                    self.die()
        else:
            self.falling = True
        if self.rect.y > 900:
            self.die()

    def create_particles(self, position):
        particle_count = 1
        pos2 = (position[0] - 12, position[1] - 15)
        numbers = range(-2, 2)
        for _ in range(particle_count):
            Particle(pos2, random.choice(numbers), self.game)

    def die(self):
        self.game.blocks.empty()
        self.game.load_level(self.game.map_level)
        self.game.bx = -100
        self.game.particles.empty()
        self.rect.topleft = self.game.startpos


    def update_(self, offset):
        self.gravity()
        self.collide()
        self.hitbox = pygame.mask.from_surface(self.image)
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if (keys[pygame.K_SPACE] or mouse[0]) and not self.falling:
            self.is_jumping = True
        self.rect.x += self.speedx
        self.rect.x += offset
