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
        pygame.init()
        self.checker = False
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.offset_x = 0
        self.bx = -100
        self.speeds = [10, 0]
        # pygame.mixer.music.load("sounds/main2.wav")
        # pygame.mixer.music.play(1)
        # pygame.mixer.music.set_volume(0.1)
        self.blocks = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.player = Player(self)
        self.camera = Camera(self)

    def game(self, num_level):
        self.startpos = [0, 670]
        if num_level == 1:
            self.map_level = level.level(num_level)
            self.load_level(self.map_level)
            self.background2 = pygame.image.load("assets/fon.png")
            self.background = pygame.image.load("assets/fon.png")
        elif num_level == 2:
            self.map_level = level.level(num_level)
            self.load_level(self.map_level)
            self.background2 = pygame.image.load("assets/fon2.png")
            self.background = pygame.image.load("assets/fon2.png")

    def coords(self):
        fpsy = str(int(self.player.rect.x))
        fps_t = font.render(fpsy, 1, pygame.Color("GREEN"))
        self.screen.blit(fps_t, (50, 0))

    def update(self):
        self.screen.fill("black")
        self.screen.blit(self.background, (self.bx, 0))
        self.screen.blit(self.background2, (self.bx + 1800, 0))
        self.blocks.update(self.offset_x)
        self.blocks.draw(self.screen)
        self.players.draw(self.screen)
        self.particles.draw(self.screen)
        if not self.checker:
            self.player.update_(self.offset_x)
            self.particles.update()
        fps_counter(self.clock, self.screen)
        self.coords()
        self.camera.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.checker = not self.checker
        pygame.display.flip()
        self.clock.tick(fps)

    def load_level(self, level):
        self.x, y = 0 - self.camera.offset, 0
        for row in level:
            for element in row:
                if element == "b":
                    Block(self, (self.x, y), 21)
                elif element == "s":
                    Block(self, (self.x, y), 1)
                elif element == "sl":
                    Block(self, (self.x, y), 2)
                elif element == "ms":
                    Block(self, (self.x, y), 3)
                elif element == "p":
                    Block(self, (self.x, y), 20)
                elif element == "p2":
                    Block(self, (self.x, y), 22)
                elif element == "pb":
                    Block(self, (self.x, y), 19)
                self.x += 70
            y += 70
            self.x = 0

    def run(self):
        while True:
            status = menu.MainMenu(self).show()
            if status == 1:
                code_feedback = levels.Table(self).show()
                if code_feedback == 1:
                    self.game(1)
                    break
                elif code_feedback == 2:
                    self.game(2)
                    break
            elif status == 2:
                skins.Menu(self).show()
        while True:
            self.check_events()
            self.update()


if __name__ == '__main__':
    game = Game()
    game.run()
