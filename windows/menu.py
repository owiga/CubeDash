import pygame
import sys

from settings import *
from resources.button import Button
from resources.button import Button_Sprite


class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.initialize()

    def initialize(self):
        self.buttons = [Button_Sprite(self, width // 2 + 150, height // 2 - 95, lambda: 1, "play_button.png"),
                        Button_Sprite(self, width // 2 - 245, height // 2 - 95, lambda: 2, "skin_button.png"),]

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
            status = self.check_events()
            if not status is None:
                break
            self.update()
        return status
