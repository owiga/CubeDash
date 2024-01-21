import pygame
import random

from settings import *


class Particle_Cube(pygame.sprite.Sprite):
    cube = [pygame.image.load("assets/particle_cube11.png"), pygame.image.load("assets/particle_cube12.png"),
            pygame.image.load("assets/particle_cube13.png")]

    def __init__(self, pos, dx, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = random.choice(self.cube)
        self.rect = self.image.get_rect()
        self.add(self.game.death_particles)
        rand = [-random.randint(0, 2), 1]
        self.dx = dx
        self.random = random.choice(rand)
        self.velocity = [dx, self.random]
        self.size = 25
        self.rect.x, self.rect.y = pos
        self.image.set_alpha(100)
        self.gravition = False
        # гравитация будет одинаковой (значение константы)
        self.gravity = 1
        self.top_player = self.game.player.rect.top

    def update(self):
        self.rect.x += self.velocity[0]
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        if not self.gravition:
            self.velocity[1] += self.gravity
            if self.rect.y < self.top_player + 10:
                self.gravition = True
                self.velocity[1] = self.velocity[1]
            self.rect.y -= self.velocity[1]
        else:
            self.velocity[1] -= self.gravity
            self.rect.y -= self.velocity[1]