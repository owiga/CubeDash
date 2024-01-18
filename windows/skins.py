import pygame
import sys

from settings import *
from resources.button import Button
from resources.button import Button_Sprite


class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.initialize()

    def initialize(self):
        self.buttons = [Button_Sprite(self, 25, 25, lambda: 3, "back.png"),
                        Button_Sprite(self, width // 2 - 75, 150, lambda: None, "skin1.png"),
                        Button_Sprite(self, width // 3 + 140, 400, lambda: None, "ICON.png", resizemode=2),
                        Button_Sprite(self, width // 3 + 210, 400, lambda: None, "skin1.png", resizemode=2),
                        Button_Sprite(self, width // 3 + 280, 400, lambda: None, "ICON.png", resizemode=2),
                        Button_Sprite(self, width // 3 + 350, 400, lambda: None, "skin1.png", resizemode=2)]

    def update(self):
        self.screen.fill("pink")
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

    def show(self):
        while True:
            self.update()
            status = self.check_events()
            if status == 3:
                return 3
