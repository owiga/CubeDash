import pygame

from settings import font


class Button(pygame.Rect):
    def __init__(self, game, width, height, x, y, func, font=font):
        self.font = font
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.game = game
        self.func = func
        super().__init__((self.x, self.y, self.width, self.height))

    def draw(self):
        pygame.draw.rect(self.game.screen, "green", (self.x, self.y, self.width, self.height))
