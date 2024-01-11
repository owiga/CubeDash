import pygame
import sys

from settings import *
from resources.button import Button


class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.initialize()

    def initialize(self):
        self.buttons = [Button(self, 150, 50, 5, 5, lambda: True)]

    def update(self):
        self.screen.fill("magenta")
        self.mousepos = pygame.mouse.get_pos()
        for x in self.buttons:
            x.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if but.collidepoint(self.mousepos):
                        return but.func()
        pygame.display.flip()

    def show(self):
        while True:
            status = self.check_events()
            if status:
                return
            self.update()
