import pygame
import sys

from settings import *
from resources.button import Button
from resources.button import Button_Sprite


class Table:
    def __init__(self, game):
        self.screen = pygame.display.set_mode((width, height))
        self.background = pygame.image.load("assets/fon.png")
        self.game = game
        self.initialize()

    def initialize(self):
        self.buttons = [Button_Sprite(self, 250, 200, lambda: 1, "first.png"),
                        Button_Sprite(self, 450, 200, lambda: 2, "second.png"),
                        Button_Sprite(self, 25, 25, lambda: 3, "back.png")]

    def update(self):
        self.screen.fill("black")
        self.screen.blit(self.background, (-100, 0))
        self.mousepos = pygame.mouse.get_pos()
        for x in self.buttons:
            x.show()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if but.rect.collidepoint(self.mousepos):
                        return but.func()
        pygame.display.flip()
        self.game.clock.tick(fps)

    def show(self):
        while True:
            status = self.check_events()
            if status == 1:
                return 1
            elif status == 2:
                return 2
            elif status == 3:
                return 3
            self.update()
