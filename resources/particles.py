import pygame
import random

from settings import *


class Particle(pygame.sprite.Sprite):
    
    def __init__(self, pos, dx, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load("assets/particle.png").convert_alpha(), (15, 15))
        self.size = 15
        self.rect = self.image.get_rect()
        self.add(self.game.particles)
        rand = [-random.randint(0, 2), 1]
        self.velocity = [dx, random.choice(rand)]

        self.rect.x, self.rect.y = pos
        self.image.set_alpha(100)

        # гравитация будет одинаковой (значение константы)
        self.gravity = 1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[0] -= self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.size *= 0.9
        self.image = pygame.transform.scale(pygame.image.load("assets/particle.png").convert_alpha(), (self.size, self.size))
        self.image.set_alpha(195 - (self.game.player.rect.left - self.rect.x))
        if self.rect.x < self.game.player.rect.left - 300:
            self.kill()
