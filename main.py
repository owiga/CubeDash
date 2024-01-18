import sys
import pygame

from settings import *
from resources.player import Player
from resources.block import Block
from resources.camera import Camera
from levels import level
from windows import menu
from windows import skins
from windows import levels


class Game:
    def __init__(self):
        self.toggle = False
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.offset_x = 0
        # pygame.mixer.music.load("sounds/main.mp3")
        # pygame.mixer.music.play(-1)
        # pygame.mixer.music.set_volume(0.1)
        self.blocks = pygame.sprite.Group()
        self.players = pygame.sprite.Group()

    def game(self, num_level):
        self.player = Player(self)
        self.startpos = [100, 670]
        self.camera = Camera(self)
        if num_level == 1:
            self.map_level = level.level(num_level)
            self.load_level(self.map_level)
        elif num_level == 2:
            self.map_level = level.level(num_level)
            self.load_level(self.map_level)

    def update(self):
        self.screen.fill("grey")
        self.player.update_(self.offset_x)
        fps_counter(self.clock, self.screen)
        # self.all_sprites.draw(self.screen)
        self.players.draw(self.screen)
        self.blocks.draw(self.screen)
        self.camera.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        self.clock.tick(fps)

    def load_level(self, level):
        self.x, y = 0 - self.camera.offset, 0
        for row in level:
            for element in row:
                if element == "b":
                    Block(self, (self.x, y), 2)
                elif element == "s":
                    Block(self, (self.x, y), 1)
                elif element == "sl":
                    Block(self, (self.x, y), 3)
                self.x += 70
            y += 70
            self.x = 0

    def run(self):
        while True:
            status = menu.MainMenu().show()
            if status == 1:
                code_feedback = levels.Table().show()
                if code_feedback == 1:
                    self.game(1)
                    break
                elif code_feedback == 2:
                    self.game(2)
                    break
            elif status == 2:
                code_feedback = skins.Menu().show()
        while True:
            self.check_events()
            self.update()


if __name__ == '__main__':
    game = Game()
    game.run()
