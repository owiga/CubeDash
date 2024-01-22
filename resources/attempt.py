import pygame

from settings import *


class Attempt:
    def __init__(self, game, x, y):
        self.font = pygame.font.Font("fonts/font2.ttf", 50)
        self.game = game
        self.text = self.font.render(f"Attempt {self.game.attempts}", 1, pygame.Color("White"))
        self.x, self.y = x, y

    def update(self):
        self.game.screen.blit(self.text, (self.x, self.y))
