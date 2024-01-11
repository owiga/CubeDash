import sys
import pygame

from settings import *
from resources.player import Player
from resources.block import Block
from resources.camera import Camera
from windows import menu


class Game:
    def __init__(self):
        self.toggle = False
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.offset_x = 0
        self.blocks = pygame.sprite.Group()
        self.masks = pygame.sprite.Group()
        self.game()

    def game(self):
        self.player = Player(self)
        self.startpos = [self.player.rect.x, self.player.rect.y]
        self.camera = Camera(self)
        for i in range(2):
            Block(self, (i * 70 + 50, 730), "spike", pometla=True)
        for i in range(120):
            Block(self, (i * 70 - 2750, 800), "block")
        for i in range(5):
            Block(self, (500, i * 70 + 150), "block")

    def update(self):
        self.screen.fill("white")
        self.player.update_(self.offset_x)
        fps_counter(self.clock, self.screen)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        self.camera.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        self.clock.tick(fps)

    def run(self):
        menu.MainMenu().show()
        while True:
            self.check_events()
            self.update()


if __name__ == '__main__':
    game = Game()
    game.run()
