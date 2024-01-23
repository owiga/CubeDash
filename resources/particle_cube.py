import random

from settings import *


class Particle_Cube(pygame.sprite.Sprite):
    def __init__(self, pos, dx, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.cube = [pygame.image.load(f"assets/particle_cube{str(self.game.current_skin)}1.png"),
                     pygame.image.load(f"assets/particle_cube{str(self.game.current_skin)}2.png"),
                     pygame.image.load(f"assets/particle_cube{str(self.game.current_skin)}3.png")]
        self.image = random.choice(self.cube)
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.size = 25

        rand = [-random.randint(0, 2), 1]
        self.random = random.choice(rand)
        self.dx = dx
        self.velocity = [dx, self.random]
        self.gravition = False
        self.gravity = 1

        self.rect.x, self.rect.y = pos
        self.top_player = self.game.player.rect.top

        self.add(self.game.death_particles)

    def update(self):
        self.rect.x += self.velocity[0]

        if not self.gravition:
            self.velocity[1] += self.gravity
            if self.rect.y < self.top_player + 10:
                self.gravition = True
                self.velocity[1] = self.velocity[1]
            self.rect.y -= self.velocity[1]

        else:
            self.velocity[1] -= self.gravity
            self.rect.y -= self.velocity[1]
